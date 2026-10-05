"""Costed offline interventions and deterministic planner/margin comparisons."""
from dataclasses import dataclass, replace
from itertools import combinations
import math
from typing import Any, Literal, Sequence

from vayu.margins import Attention, PlannerCache, analyze, changed_tails
from vayu.planner import pinned_reservations, plan
from vayu.schemas import PinnedPlacement, Plan, PlanningState, Resource

BENEFIT_DEFINITION = 'Increase in Covered tails plus reduction in Late tails per man-hour'


@dataclass(frozen=True)
class Intervention:
    """One hypothetical action with an explicit positive man-hour cost.

    factor scales each interval endpoint's distance from the unchanged point.
    Added crew shifts are whole crews in this day-based planning abstraction.
    """
    intervention_id: str
    kind: Literal['expedite_spare', 'add_crew_shift', 'add_bay', 'inspect_tail']
    cost_man_hours: float
    target: str
    days: int = 0
    factor: float = .5

    def __post_init__(self) -> None:
        """Reject ambiguous IDs, nonfinite costs and invalid action parameters."""
        if not isinstance(self.intervention_id, str) or not self.intervention_id.strip():
            raise ValueError('Intervention ID must be nonempty')
        if self.kind not in ('expedite_spare', 'add_crew_shift', 'add_bay', 'inspect_tail'):
            raise ValueError('Unsupported intervention kind')
        if not isinstance(self.target, str) or not self.target.strip():
            raise ValueError('Intervention target must be nonempty')
        if isinstance(self.cost_man_hours, bool) or not math.isfinite(self.cost_man_hours) or self.cost_man_hours <= 0:
            raise ValueError('Man-hour cost must be finite and positive')
        if isinstance(self.days, bool) or not isinstance(self.days, int) or self.days < 0:
            raise ValueError('Expedite days must be a nonnegative integer')
        if isinstance(self.factor, bool) or not math.isfinite(self.factor) or not 0 < self.factor <= 1:
            raise ValueError('Assumed inspection factor must be in (0,1]')


@dataclass(frozen=True)
class ScenarioSnapshot:
    """Immutable computed schedule and attention for a single hypothetical state."""
    plan: Plan
    attention: tuple[Attention, ...]


def apply_intervention(state: PlanningState, action: Intervention) -> PlanningState:
    """Copy believed inputs; never mutate or execute a maintenance action."""
    if action.kind == 'expedite_spare':
        spare = next((s for s in state.spares if s.spare_id == action.target), None)
        if spare is None:
            raise ValueError('Unknown spare target')
        return apply_change(state, 'spare', action.target, max(0, spare.available_day-action.days))
    if action.kind in ('add_bay', 'add_crew_shift'):
        collection = 'bays' if action.kind == 'add_bay' else 'crews'
        resources = getattr(state, collection)
        if action.target in {r.resource_id for r in resources}:
            raise ValueError('Added resource ID already exists')
        return replace(state, **{collection: (*resources, Resource(action.target, state.today+1))})
    if action.target not in {t.tail_id for t in state.tails}:
        raise ValueError('Unknown inspection tail')
    tails = tuple(replace(t, lower=t.rul_point-(t.rul_point-t.lower)*action.factor,
                          upper=t.rul_point+(t.upper-t.rul_point)*action.factor)
                  if t.tail_id == action.target else t for t in state.tails)
    return replace(state, tails=tails)


def _summary(snapshot: ScenarioSnapshot) -> dict[str, Any]:
    """Calculate count/slack results rather than embedding demo outcomes."""
    slacks = [a.slack for a in snapshot.attention if a.slack is not None]
    return {'label_counts': {name: sum(a.label == name for a in snapshot.attention)
                             for name in ('Covered', 'Fragile')},
            'late_count': sum(p.status == 'Late' for p in snapshot.plan.placements),
            'unplanned_count': sum(p.status == 'Unplanned' for p in snapshot.plan.placements),
            'min_slack': min(slacks) if slacks else None}


def _tail_results(snapshot: ScenarioSnapshot) -> dict[str, dict[str, Any]]:
    """Expose physical placements and planning margins for every tail."""
    placements = {p.tail_id: p for p in snapshot.plan.placements}
    rows = {}
    for attention in sorted(snapshot.attention, key=lambda a: a.tail_id):
        p = placements[attention.tail_id]
        directional = attention.float_result.to_dict()
        rows[attention.tail_id] = {
            'deadline_day': p.deadline_day, 'start_day': p.start_day, 'end_day': p.end_day,
            'bay': p.bay, 'crew': p.crew, 'spare': p.spare, 'status': p.status,
            'binding_resource': p.binding, 'reason_code': p.reason_code, 'label': attention.label,
            'deadline_slack': attention.slack, 'half_width': attention.half_width,
            'float_down': directional['float_down'], 'float_up': directional['float_up'],
            'float_min': directional['float_min'], 'direction': directional['direction'],
        }
    return rows


def _assumptions(action: Intervention) -> list[str]:
    """Keep assumed diagnostic efficacy and crew capacity interpretation visible."""
    if action.kind == 'inspect_tail':
        return [f'Assumed diagnostic check: {action.target} half-width multiplied by '
                f'{action.factor:g}; point estimate unchanged. No diagnostic measurement supplied.']
    if action.kind == 'add_crew_shift':
        return [f'Crew shift represented as one additional whole crew {action.target} '
                'from tomorrow for the planning horizon in this day-based prototype.']
    return []


def _rank_key(result: dict[str, Any]) -> tuple[float, tuple[str, ...]]:
    """Descending benefit per cost, then sorted action IDs for all score ties."""
    return -result['benefit_per_cost'], tuple(result['intervention_ids'])


def score_for_tail(result: dict[str, Any], tail_id: str) -> dict[str, Any]:
    """Score only the named tail's Covered gain and Late reduction per man-hour.

    Keep fleet-wide results descriptive and copy the score fields so shared
    evaluation caches are never mutated by another policy's selected target.
    """
    change = next((row for row in result['per_tail_changes'] if row['tail'] == tail_id),None)
    if change is None:
        raise ValueError('Unknown benefit target tail')
    before,after = change['before'],change['after']
    covered = int(after['label'] == 'Covered')-int(before['label'] == 'Covered')
    late = int(before['status'] == 'Late')-int(after['status'] == 'Late')
    benefit = covered+late
    return {**result,'fleet_benefit':result.get('fleet_benefit',result['benefit']),
            'fleet_benefit_per_cost':result.get('fleet_benefit_per_cost',result['benefit_per_cost']),
            'benefit':benefit,'benefit_per_cost':benefit/result['cost_man_hours'],
            'benefit_components':{'covered_increase':covered,'late_reduction':late},
            'benefit_definition':'Selected tail Covered increase plus Late reduction per man-hour',
            'benefit_scope':'target_tail','benefit_tail':tail_id}


class WhatIfExplorer:
    """Reuse one baseline/cache for single actions and pairs without applying them."""

    def __init__(self, state: PlanningState, candidates: Sequence[Intervention], radius: int = 40,
                 pinned_placements: Sequence[PinnedPlacement] | None = None,
                 cache: PlannerCache | None = None) -> None:
        self.state = state
        self.candidates = tuple(sorted(candidates, key=lambda a: a.intervention_id))
        if len({a.intervention_id for a in self.candidates}) != len(self.candidates):
            raise ValueError('Duplicate intervention IDs')
        for action in self.candidates:
            apply_intervention(state, action)  # Validate each action even if later outside top k.
        self.radius = radius
        self.pins = pinned_reservations(pinned_placements)
        self.cache = cache if cache is not None else PlannerCache()
        self.baseline = self._snapshot(state)

    def _snapshot(self, state: PlanningState) -> ScenarioSnapshot:
        """Re-run the same planner and directional margins through their cache."""
        scheduled = self.cache.get(state, pins=self.pins)
        attention = analyze(state, self.radius, pinned_placements=self.pins, cache=self.cache)
        return ScenarioSnapshot(scheduled, attention)

    def evaluate(self, interventions: Intervention | Sequence[Intervention]) -> dict[str, Any]:
        """Compare a single or combined scenario with the same original baseline."""
        actions = ((interventions,) if isinstance(interventions, Intervention) else tuple(interventions))
        actions = tuple(sorted(actions, key=lambda a: a.intervention_id))
        if not actions or len({a.intervention_id for a in actions}) != len(actions):
            raise ValueError('Require distinct nonempty intervention IDs')
        changed = self.state
        for action in actions:
            changed = apply_intervention(changed, action)
        after = self._snapshot(changed)
        before_summary, after_summary = _summary(self.baseline), _summary(after)
        before_tails, after_tails = _tail_results(self.baseline), _tail_results(after)
        placement_fields = {'start_day', 'end_day', 'bay', 'crew', 'spare', 'status'}
        changes = []
        for tail_id in sorted(before_tails):
            old, new = before_tails[tail_id], after_tails[tail_id]
            fields = [key for key in old if old[key] != new[key]]
            changes.append({'tail': tail_id, 'changed_fields': fields,
                            'placement_changed': bool(placement_fields.intersection(fields)),
                            'before': old, 'after': new})
        covered_gain = after_summary['label_counts']['Covered'] - before_summary['label_counts']['Covered']
        late_reduction = before_summary['late_count'] - after_summary['late_count']
        benefit = covered_gain + late_reduction
        cost = sum(a.cost_man_hours for a in actions)
        return {
            'intervention_ids': [a.intervention_id for a in actions],
            'interventions': [{'id': a.intervention_id, 'kind': a.kind, 'target': a.target,
                               'days': a.days, 'factor': a.factor, 'cost_man_hours': a.cost_man_hours}
                              for a in actions],
            'cost_man_hours': cost, 'benefit': benefit, 'benefit_per_cost': benefit/cost,
            'benefit_components': {'covered_increase': covered_gain, 'late_reduction': late_reduction},
            'benefit_definition': BENEFIT_DEFINITION,
            **after_summary, 'before': before_summary, 'per_tail_changes': changes,
            'changed_tails': [row['tail'] for row in changes if row['changed_fields']],
            'effect': 'Effect' if any(row['changed_fields'] for row in changes) else 'No effect',
            'assumed': any(a.kind == 'inspect_tail' for a in actions),
            'assumptions': [text for a in actions for text in _assumptions(a)],
            'data_label': 'Fictional/simulated planning comparison; no maintenance is executed.',
        }

    def rank(self, *, benefit_tail: str | None = None) -> list[dict[str, Any]]:
        """Rank resource actions, retaining no-effect and negative-benefit cases.

        Inspection only illustrates an assumed change of belief and is excluded
        from scoring/ranking, even when explicitly supplied by a caller.
        """
        if benefit_tail is not None and benefit_tail not in {t.tail_id for t in self.state.tails}:
            raise ValueError('Unknown benefit target tail')
        rows = (self.evaluate(a) for a in self.candidates if a.kind != 'inspect_tail')
        if benefit_tail is not None:
            rows = (score_for_tail(row,benefit_tail) for row in rows)
        return sorted(rows,key=_rank_key)

    def pairs_for_top_k(self, k: int) -> list[dict[str, Any]]:
        """Replan each unordered pair among the top k singles; sum costs, not gains."""
        if isinstance(k, bool) or not isinstance(k, int) or k < 0:
            raise ValueError('k must be a nonnegative integer')
        if k < 2:
            return []
        lookup = {a.intervention_id: a for a in self.candidates}
        top = [lookup[row['intervention_ids'][0]] for row in self.rank()[:k]]
        return sorted((self.evaluate(pair) for pair in combinations(top, 2)), key=_rank_key)


def default_interventions(state: PlanningState, *, expedite_days: int = 5,
                          expedite_cost: float = 8, crew_cost: float = 8,
                          bay_cost: float = 16, inspection_cost: float = 4,
                          inspection_factor: float = .5) -> tuple[Intervention, ...]:
    """Enumerate inventory expedites and one bay/crew addition.

    Default man-hour costs are illustrative, configurable inputs, not measured
    effort. Existing IDs determine deterministic collision-free added-resource IDs.
    Legacy inspection parameters are accepted for compatibility, but inspections
    are assumed, not scored, and are never added to the ranked menu.
    """
    def resource_id(prefix: str, resources: tuple[Resource, ...]) -> str:
        """Choose the first unused numbered resource ID."""
        existing = {r.resource_id for r in resources}
        i = 1
        while f'{prefix}-EXTRA-{i:02d}' in existing:
            i += 1
        return f'{prefix}-EXTRA-{i:02d}'
    actions = [Intervention(f'EXPEDITE:{s.spare_id}', 'expedite_spare', expedite_cost,
                            target=s.spare_id, days=expedite_days) for s in sorted(state.spares, key=lambda s: s.spare_id)]
    actions += [Intervention('ADD:CREW', 'add_crew_shift', crew_cost, target=resource_id('CREW', state.crews)),
                Intervention('ADD:BAY', 'add_bay', bay_cost, target=resource_id('BAY', state.bays))]
    return tuple(sorted(actions, key=lambda a: a.intervention_id))


def rank_interventions(state: PlanningState, candidates: Sequence[Intervention] | None = None,
                       radius: int = 40, *, pinned_placements: Sequence[PinnedPlacement] | None = None,
                       cache: PlannerCache | None = None) -> list[dict[str, Any]]:
    """Rank candidates with user-selected count benefit per positive man-hour cost."""
    return WhatIfExplorer(state, candidates if candidates is not None else default_interventions(state),
                          radius, pinned_placements, cache).rank()


def pairs_for_top_k(k: int, *, state: PlanningState | None = None,
                    candidates: Sequence[Intervention] | None = None, radius: int = 40,
                    pinned_placements: Sequence[PinnedPlacement] | None = None,
                    cache: PlannerCache | None = None) -> list[dict[str, Any]]:
    """Test top-k pairs; without inputs use the deterministic assumed story pack."""
    if state is None:
        from vayu.sim import whatif_demo_state
        state = whatif_demo_state()
    return WhatIfExplorer(state, candidates if candidates is not None else default_interventions(state),
                          radius, pinned_placements, cache).pairs_for_top_k(k)


@dataclass(frozen=True)
class Comparison:
    """Concrete before/after schedules; no attribution beyond the comparison."""
    kind: str
    target: str
    old_day: int
    new_day: int
    before: Plan
    after: Plan
    changed_tails: tuple[str,...]


def apply_change(state: PlanningState, kind: str, target: str, new_day: int) -> PlanningState:
    """Copy state, changing exactly one named resource's availability day."""
    if kind not in ('spare','bay','crew') or isinstance(new_day,bool) or not isinstance(new_day,int) or new_day < 0:
        raise ValueError('Require spare/bay/crew and nonnegative integer availability')
    key,identifier,field = ('spares','spare_id','available_day') if kind == 'spare' else (
        'bays' if kind == 'bay' else 'crews','resource_id','free_day')
    items = getattr(state,key)
    if target not in {getattr(item,identifier) for item in items}:
        raise ValueError('Unknown resource')
    replaced = tuple(replace(item,**{field:new_day}) if getattr(item,identifier) == target else item for item in items)
    return replace(state,**{key:replaced})


def compare(state: PlanningState, kind: str, target: str, new_day: int) -> Comparison:
    """Report the actual whole-fleet effect, including no-change controls."""
    changed = apply_change(state,kind,target,new_day)
    collection = state.spares if kind == 'spare' else state.bays if kind == 'bay' else state.crews
    old_day = next((item.available_day if kind == 'spare' else item.free_day) for item in collection
                   if (item.spare_id if kind == 'spare' else item.resource_id) == target)
    before,after = plan(state),plan(changed)
    return Comparison(kind,target,old_day,new_day,before,after,changed_tails(before,after))
