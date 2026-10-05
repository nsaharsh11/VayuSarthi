"""Seeded fictional fleet construction; evaluation data stays outside planning."""
from pathlib import Path
from collections import OrderedDict
from contextlib import redirect_stdout
from dataclasses import asdict, dataclass, replace
import hashlib
import io
import json
import math
from typing import Any, Mapping, Sequence

import numpy as np
import pandas as pd

from vayu.schemas import DATA_LABEL, Plan, PlanningState, Resource, Spare, Tail, canonical_json

WHATIF_LABEL = 'Fictional what-if story; RUL ranges and man-hour costs are assumed scenario inputs.'
VALIDATION_NOTE = 'simulated; scenario-based'
POLICY_NAMES = {'B0': 'Run-to-failure', 'B1': 'Fixed-interval', 'B2-K0': 'Earliest deadline, no interventions', 'B2': 'Earliest deadline',
                'B3': 'Slack shortfall', 'B4': 'Float + slack shortfall', 'B4b': 'Direct float shortfall'}
DESIGN_REVISION = 'v2_post_hoc'
OUTCOME_METRICS = ('aog_days','unplanned_failures','wasted_life_cycles','plan_churn')
VALIDATION_METRICS = {'aog_days': ('Aircraft-days unserviceable (AOG)', 'aircraft-days'),
    'unplanned_failures': ('Unplanned failures', 'failures'),
    'wasted_life_cycles': ('Wasted life at removal', 'flight cycles'),
    'plan_churn': ('Plan churn', 'changed placements'),
    'intervention_man_hours': ('Intervention cost', 'man-hours'),
    'unused_weeks': ('Unused intervention weeks', 'weeks'),
    'waiting_spare_days': ('Grounded waiting for spare', 'aircraft-days'),
    'waiting_bay_days': ('Grounded waiting for bay', 'aircraft-days'),
    'waiting_crew_days': ('Grounded waiting for crew', 'aircraft-days'),
    'waiting_slot_days': ('Grounded waiting for permitted slot', 'aircraft-days'),
    'maintenance_days': ('Induction or repair duration', 'aircraft-days')}
PAIRED_POLICIES = (('B4','B3'),('B3','B2'),('B4b','B4'),('B4b','B3'),('B2','B2-K0'))
INTERVENTION_POLICIES = ('B2','B3','B4','B4b')
PREVENTIVE_POLICIES = ('B2-K0',*INTERVENTION_POLICIES)
CHOICE_PAIRS = (('B2','B3'),('B2','B4'),('B3','B4'),('B2','B4b'),('B3','B4b'),('B4','B4b'))
ACTION_TYPES = ('expedite_spare','add_crew_shift','add_bay')
DIAGNOSTIC_COLUMNS = ['review_weeks','multi_candidate_weeks','multi_candidate_share',
    'b2_b3_b4_different_tail_weeks','b2_b3_b4_different_tail_share',
    'b2_b3_b4_b4b_different_tail_weeks','b2_b3_b4_b4b_different_tail_share',
    *[f'{kind}_count' for kind in ACTION_TYPES], 'power_note',
    *[f'{a.lower()}_{b.lower()}_share{suffix}' for a,b in CHOICE_PAIRS
      for suffix in ('','_ci_low','_ci_high')]]
VALIDATION_COLUMNS = ['design_revision','stress_level','repair_multiplier','horizon_days','policy','policy_name','row_type',
    'n_scenarios','fixed_interval_cycles','weekly_budget','initial_age_rule',
    'tie_scenarios','ties_over_n','tie_metric_scope','note',
    *[f'{metric}_{suffix}' for metric in VALIDATION_METRICS
      for suffix in ('mean','ci_low','ci_high','ties','ties_over_n')], *DIAGNOSTIC_COLUMNS]



@dataclass(frozen=True)
class SimulationConfig:
    """Explicit scenario assumptions; these inputs are not measured performance."""
    n_scenarios: int = 200
    seed: int = 26249
    bootstrap_seed: int = 26250
    bootstrap_samples: int = 2000
    weekly_budget: int = 1
    max_spare_delay: int = 7
    fixed_interval_cycles: int = 1000
    float_radius: int = 40
    residual_scale: float = 1.
    repair_multiplier: float = 2.

    def __post_init__(self) -> None:
        for name in ('n_scenarios', 'seed', 'bootstrap_seed', 'bootstrap_samples', 'weekly_budget',
                     'max_spare_delay', 'fixed_interval_cycles', 'float_radius'):
            value = getattr(self, name)
            minimum = 1 if name in ('n_scenarios', 'bootstrap_samples', 'fixed_interval_cycles') else 0
            if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
                raise ValueError(f'{name} must be an integer >= {minimum}')
        for name,minimum in (('residual_scale',0.),('repair_multiplier',1.)):
            value = getattr(self,name)
            if isinstance(value,bool) or not math.isfinite(value) or value < minimum:
                raise ValueError(f'{name} must be finite and >= {minimum}')


@dataclass(frozen=True)
class StressLevel:
    """Predeclared fictional capacity, lead-time and signed-error assumptions."""
    name: str
    bay_count: int
    crew_count: int
    eta_multiplier: int
    max_spare_delay: int
    residual_scale: float


STRESS_LEVELS = (StressLevel('benign',3,2,1,2,.5),
                StressLevel('moderate',2,1,2,7,1.),
                StressLevel('stressed',1,1,5,21,2.))
REPAIR_MULTIPLIERS = (1.5,2.,3.)
HORIZON_DAYS = (40,80)


def stress_inputs(state: PlanningState, level: StressLevel,
                  config: SimulationConfig) -> tuple[PlanningState, SimulationConfig]:
    """Transform believed inputs once before drawing or comparing any policy."""
    stressed = replace(state,
        spares=tuple(replace(s,available_day=state.today+max(0,s.available_day-state.today)*level.eta_multiplier)
                     for s in state.spares),
        bays=tuple(Resource(f'BAY-{i:02d}',state.today) for i in range(1,level.bay_count+1)),
        crews=tuple(Resource(f'CREW-{i:02d}',state.today) for i in range(1,level.crew_count+1)))
    return stressed,replace(config,max_spare_delay=level.max_spare_delay,residual_scale=level.residual_scale)


def training_fixed_interval(data_dir: Path, model_path: Path) -> int:
    """Freeze B1's assumed interval as median fit-engine terminal TRAIN cycle.

    This empirical lifetime proxy is not an approved overhaul interval. No
    calibration engine or official TEST target contributes to the setting.
    """
    from pdm.data.cmapss import load_fd001
    from vayu.rul import load_cached_model
    model = load_cached_model(model_path)
    train,_,_ = load_fd001(data_dir)
    lifetimes = train[train.unit.isin(model.train_units)].groupby('unit').cycle.max()
    if set(lifetimes.index) != set(model.train_units):
        raise ValueError('Complete fit-training engines needed to freeze B1 interval')
    return math.ceil(float(lifetimes.median()))


@dataclass(frozen=True)
class MonteCarloScenario:
    """Evaluation-only signed RUL draws and delays; never passed to policy functions."""
    scenario_id: int
    true_rul: tuple[tuple[str, float], ...]
    spare_delays: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class PolicyOutcome:
    """One paired simulation outcome with weekly costs and execution events."""
    metrics: dict[str, float]
    weeks: tuple[dict[str, Any], ...]
    events: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class ValidationResult:
    """Generated summary and source rows from the same scenario draws."""
    summary: pd.DataFrame
    runs: pd.DataFrame
    weeks: pd.DataFrame
    manifest: dict[str, Any]


def draw_initial_ages(state: PlanningState, config: SimulationConfig) -> tuple[dict[str,float], ...]:
    """Neutral paired technical ages, independent of RUL, stresses and horizon."""
    ids = sorted(t.tail_id for t in state.tails)
    rng = np.random.default_rng(config.seed+1000)
    values = rng.uniform(0,config.fixed_interval_cycles,size=(config.n_scenarios,len(ids)))
    return tuple(dict(zip(ids,map(float,row))) for row in values)


def calibration_residuals(data_dir: Path | None = None, model_path: Path | None = None) -> pd.DataFrame:
    """Signed capped-target minus point residuals on held-out calibration engines.

    Use causal windows with at least thirty observations. These residuals are
    not the nonnegative CQR scores and do not use official TEST labels.
    Missing NASA data/model fails through the existing offline loader.
    """
    from pdm.data.cmapss import load_fd001
    from vayu.rul import DEFAULT_CACHE, ROOT, load_cached_model, predict
    model = load_cached_model(model_path or DEFAULT_CACHE)
    train, _, _ = load_fd001(data_dir or ROOT/'data/CMAPSS')
    frame = train[train.unit.isin(model.calibration_units)].copy()
    if set(frame.unit) != set(model.calibration_units) or set(model.train_units) & set(frame.unit):
        raise ValueError('Calibration residual engines must be complete and disjoint from fit engines')
    predicted = predict(model, frame)
    pool = frame[['unit', 'cycle']].rename(columns={'unit': 'engine_id'})
    pool['target'] = frame.true_rul.clip(upper=model.cap)
    pool['point'] = predicted.point
    pool['residual'] = pool.target - pool.point
    return pool[pool.cycle >= 30].sort_values(['engine_id','cycle']).reset_index(drop=True)


def draw_scenarios(state: PlanningState, residuals: pd.DataFrame | Sequence[float],
                   config: SimulationConfig) -> tuple[MonteCarloScenario, ...]:
    """Pre-draw common shocks, sampling engines uniformly then their residual rows.

    A plain residual sequence uses uniform row sampling. Signed draws preserve
    point + error exactly; nonpositive life is an initially observed failure.
    Spare delays are uniformly distributed integral days in [0,max_delay].
    """
    if isinstance(residuals, pd.DataFrame):
        if not {'engine_id','residual'} <= set(residuals):
            raise ValueError('Calibration pool requires engine_id and residual')
        groups = [group.residual.to_numpy(dtype=float) for _, group in residuals.groupby('engine_id', sort=True)]
    else:
        groups = [np.asarray(residuals, dtype=float)]
    if not groups or any(values.ndim != 1 or not len(values) or not np.isfinite(values).all() for values in groups):
        raise ValueError('A nonempty finite signed calibration residual pool is required')
    rng = np.random.default_rng(config.seed)
    draws = []
    for index in range(config.n_scenarios):
        remaining = []
        for tail in sorted(state.tails, key=lambda t: t.tail_id):
            group = groups[int(rng.integers(len(groups)))]
            remaining.append((tail.tail_id, tail.rul_point + config.residual_scale*float(group[int(rng.integers(len(group)))])))
        delays = tuple((s.spare_id, int(rng.integers(config.max_spare_delay+1)))
                       for s in sorted(state.spares, key=lambda s: s.spare_id))
        draws.append(MonteCarloScenario(index, tuple(remaining), delays))
    return tuple(draws)


class ValidationCache:
    """Bounded caches of believed inputs shared across policies and paired scenarios."""
    def __init__(self) -> None:
        from vayu.margins import PlannerCache
        self.planner = PlannerCache(max_size=8192)
        self.attention: OrderedDict[str, Any] = OrderedDict()
        self.actions: OrderedDict[str, Any] = OrderedDict()
        self.rankings: OrderedDict[str, Any] = OrderedDict()

    @staticmethod
    def remember(cache: OrderedDict, key: str, value: Any) -> Any:
        """Bound large what-if results without including truth in cache keys."""
        cache[key] = value
        cache.move_to_end(key)
        if len(cache) > 1024:
            cache.popitem(last=False)
        return value


ATTENTION_WINDOW_DAYS = 14


def candidate_tails(state: PlanningState) -> dict[str, int]:
    """Waiting tails whose believed deadline is within the frozen 14-day window."""
    from vayu.planner import deadline_day
    deadlines = {t.tail_id: deadline_day(t.rul_point,state.safety_buffer,t.rate) - state.today for t in state.tails}
    return {tail: day for tail,day in deadlines.items() if day <= ATTENTION_WINDOW_DAYS}


def select_tail(state: PlanningState, policy: str, config: SimulationConfig,
                cache: ValidationCache | None = None) -> str | None:
    """Choose an intervention tail from believed values only (frozen in DECISIONS.md).

    Candidates are tails with deadline within 14 days. B2 picks the earliest
    deadline. B3 picks the largest shortfall half-width - slack. B4 picks the
    largest shortfall half-width - min(float,slack). Unplanned slack is an
    infinite shortfall; > R floats use R. Ties use deadline, then tail ID.
    """
    from vayu.margins import analyze, deadline_slack
    if policy == 'B2-K0':
        policy = 'B2'
    if policy not in INTERVENTION_POLICIES or not state.tails:
        return None
    candidates = candidate_tails(state)
    if not candidates:
        return None
    if policy == 'B2':
        return min(candidates, key=lambda tail: (candidates[tail],tail))
    shared = cache or ValidationCache()
    scheduled = shared.planner.get(state)
    slack = deadline_slack(scheduled,state.tails,today=state.today,safety_buffer=state.safety_buffer)
    half = {t.tail_id: (t.upper-t.lower)/2 for t in state.tails}
    floats = {}
    if policy in ('B4','B4b'):
        key = canonical_json(state) + f':R={config.float_radius}'
        if key not in shared.attention:
            with redirect_stdout(io.StringIO()):
                shared.remember(shared.attention, key, analyze(state,config.float_radius,cache=shared.planner))
        floats = {a.tail_id: a.float_result.value if a.float_result.value is not None else config.float_radius
                  for a in shared.attention[key]}
    def order(tail: str) -> tuple:
        if policy == 'B4b':
            placement = next(p for p in scheduled.placements if p.tail_id == tail)
            value = 0. if placement.status == 'Unplanned' else floats[tail]
            return -(half[tail]-value), candidates[tail], tail
        margin = slack[tail] if slack[tail] is not None else -math.inf
        if policy == 'B4':
            margin = min(floats[tail],margin)
        return -(half[tail]-margin), candidates[tail], tail
    return min(candidates, key=order)


def intervention_ranking(state: PlanningState, tail_id: str, config: SimulationConfig,
                         cache: ValidationCache | None = None) -> tuple[tuple[Any, ...], list[dict[str, Any]]]:
    """Return the complete common action ranking, including zero-benefit rows.

    The menu is the selected tail's assigned spare expedite and shared
    bay/crew additions. For an Unplanned tail, include compatible unused
    spares. Inspection is assumed, not scored. Costs and ranking come from
    vayu.whatif.
    """
    from vayu.whatif import WhatIfExplorer, default_interventions
    shared = cache or ValidationCache()
    key = canonical_json(state) + f':{tail_id}:R={config.float_radius}'
    if key in shared.rankings:
        return shared.rankings[key]
    tail = next(t for t in state.tails if t.tail_id == tail_id)
    placement = next(p for p in shared.planner.get(state).placements if p.tail_id == tail_id)
    compatible = {s.spare_id for s in state.spares if s.part_number == tail.part_number}
    spare_ids = {placement.spare} if placement.spare is not None else compatible
    actions = tuple(a for a in default_interventions(state)
                    if a.kind in ('add_bay','add_crew_shift') or
                    (a.kind == 'expedite_spare' and a.target in spare_ids))
    with redirect_stdout(io.StringIO()):
        explorer = WhatIfExplorer(state,actions,config.float_radius,cache=shared.planner)
        ranked = explorer.rank(benefit_tail=tail_id)
    return shared.remember(shared.rankings,key,(actions,ranked))


def choose_intervention(state: PlanningState, tail_id: str, config: SimulationConfig,
                        cache: ValidationCache | None = None) -> tuple[Any, dict[str, Any]] | None:
    """Use the same positive-benefit what-if rule for every intervention policy."""
    shared = cache or ValidationCache()
    key = canonical_json(state) + f':{tail_id}:R={config.float_radius}'
    if key in shared.actions:
        return shared.actions[key]
    actions,ranked = intervention_ranking(state,tail_id,config,shared)
    helpful = [row for row in ranked if row['effect'] != 'No effect' and row['benefit'] > 0]
    selected = None
    if helpful:
        row = helpful[0]
        action = next(a for a in actions if a.intervention_id == row['intervention_ids'][0])
        selected = action, row
    return shared.remember(shared.actions,key,selected)


def run_policy(state: PlanningState, scenario: MonteCarloScenario, policy: str,
               cycles_since_overhaul: Mapping[str, float], config: SimulationConfig,
               cache: ValidationCache | None = None) -> PolicyOutcome:
    """Execute one policy on common evaluation shocks, separated from its view.

    Day order: observe failures/completions and due-date grounding, start
    feasible previously proposed jobs, review interventions weekly, replan,
    then fly serviceable tails. AOG includes grounded resource waiting and
    preventive induction or assumed longer failure repair. Replacements
    are assumed serviceable to horizon. Only one removal per original engine.
    """
    from vayu.whatif import apply_intervention
    if policy not in POLICY_NAMES:
        raise ValueError('Unknown simulation policy')
    ids = {t.tail_id for t in state.tails}
    remaining, delays = dict(scenario.true_rul), dict(scenario.spare_delays)
    if set(remaining) != ids or set(delays) != {s.spare_id for s in state.spares}:
        raise ValueError('Scenario must contain exactly the fleet tails and spares')
    if any(not math.isfinite(v) for v in remaining.values()) or any(
            isinstance(v,bool) or not isinstance(v,int) or v < 0 for v in delays.values()):
        raise ValueError('Finite signed RUL and nonnegative integral delays required')
    if set(cycles_since_overhaul) != ids or any(not math.isfinite(v) or v < 0 for v in cycles_since_overhaul.values()):
        raise ValueError('Complete finite nonnegative observed technical ages required')
    shared = cache or ValidationCache()
    tails = {t.tail_id: t for t in state.tails}
    forecasts = {s.spare_id:s.available_day for s in state.spares}
    actual_eta = {s.spare_id:s.available_day+delays[s.spare_id] for s in state.spares}
    spares = {s.spare_id:s for s in state.spares}
    bays = {r.resource_id:r.free_day for r in state.bays}
    crews = {r.resource_id:r.free_day for r in state.crews}
    flown = {tail:0. for tail in ids}
    failed, completed, grounded = set(), set(), set()
    active: dict[str, int] = {}
    pending: dict[str, Any] = {}
    metrics = {metric:0. for metric in VALIDATION_METRICS}
    metrics.update({key:0. for key in ('waiting_spare_days','waiting_bay_days','waiting_crew_days',
                                     'waiting_slot_days','maintenance_days')})
    metrics.update(initial_overdue_tails=sum(age >= config.fixed_interval_cycles for age in cycles_since_overhaul.values())
                   if policy == 'B1' else 0, inductions_before_due=0)
    weeks, events = [], []
    for day in range(state.today,state.horizon):
        new_failures = []
        for tail in sorted(ids):
            if tail in active and active[tail] == day:
                del active[tail]
                completed.add(tail)
                failed.discard(tail)
                grounded.discard(tail)
                events.append({'day':day,'tail':tail,'event':'COMPLETED'})
            if tail not in completed and tail not in active and tail not in grounded and remaining[tail] <= 0:
                failed.add(tail)
                grounded.add(tail)
                new_failures.append(tail)
                metrics['unplanned_failures'] += 1
                events.append({'day':day,'tail':tail,'event':'FAILURE'})
            elif tail not in completed and tail not in active and tail not in grounded:
                due = (policy in PREVENTIVE_POLICIES and
                       math.floor((tails[tail].rul_point-flown[tail]-state.safety_buffer)/tails[tail].rate) <= 0)
                due = due or (policy == 'B1' and cycles_since_overhaul[tail]+flown[tail] >= config.fixed_interval_cycles)
                if due:
                    grounded.add(tail)
                    events.append({'day':day,'tail':tail,'event':'GROUNDED','cause':'Preventive due date'})
        for tail,p in sorted(pending.items()):
            if p.start_day != day or tail in completed or tail in active:
                continue
            if p.spare not in spares or actual_eta[p.spare] > day or bays[p.bay] > day or crews[p.crew] > day:
                events.append({'day':day,'tail':tail,'event':'START_BLOCKED'})
                continue
            duration = math.ceil(tails[tail].duration*config.repair_multiplier) if tail in failed else tails[tail].duration
            end_day = day+duration
            active[tail] = end_day
            grounded.add(tail)
            bays[p.bay] = crews[p.crew] = end_day
            del spares[p.spare]
            metrics['wasted_life_cycles'] += max(0.,remaining[tail])
            if policy == 'B1' and tail not in failed and cycles_since_overhaul[tail]+flown[tail] < config.fixed_interval_cycles:
                metrics['inductions_before_due'] += 1
            events.append({'day':day,'tail':tail,'event':'STARTED','end_day':end_day,
                           'bay':p.bay,'crew':p.crew,'spare':p.spare,'deadline_day':p.deadline_day})
        waiting = sorted(ids - completed - set(active))
        visible = []
        for tail in waiting:
            t = tails[tail]
            point = max(0.,t.rul_point-flown[tail])
            visible.append(replace(t,rul_point=0. if tail in failed else point,
                                   lower=0. if tail in failed else max(0.,t.lower-flown[tail]),
                                   upper=0. if tail in failed else max(point,t.upper-flown[tail]),
                                   duration=math.ceil(t.duration*config.repair_multiplier) if tail in failed else t.duration))
        if policy == 'B0':
            visible = [t for t in visible if t.tail_id in failed]
        elif policy == 'B1':
            visible = [t for t in visible if t.tail_id in failed or
                       math.floor((config.fixed_interval_cycles-cycles_since_overhaul[t.tail_id]-flown[t.tail_id])/t.rate)
                       <= state.horizon-day]
        # Use a relative-day view so the exact Master Brief deadline formula
        # still applies at each replan; execution dates are translated below.
        view = PlanningState(tuple(visible),tuple(replace(s, available_day=(
            0 if actual_eta[s.spare_id] <= day else max(1,forecasts[s.spare_id]-day))) for s in spares.values()),
            tuple(Resource(key,max(0,value-day)) for key,value in sorted(bays.items())),
            tuple(Resource(key,max(0,value-day)) for key,value in sorted(crews.items())),
            today=0,horizon=state.horizon-day,safety_buffer=0 if policy == 'B1' else state.safety_buffer)
        if (day-state.today) % 7 == 0:
            fragile = []
            if policy in INTERVENTION_POLICIES:
                from vayu.margins import analyze
                key = canonical_json(view)+f':R={config.float_radius}'
                if key not in shared.attention:
                    with redirect_stdout(io.StringIO()):
                        shared.remember(shared.attention,key,analyze(view,config.float_radius,cache=shared.planner))
                fragile = sorted(a.tail_id for a in shared.attention[key] if a.label == 'Fragile')
            budget = config.weekly_budget if policy in INTERVENTION_POLICIES else 0
            week = {'week':(day-state.today)//7,'day':day,'policy':policy,'budget':budget,
                    'interventions':0,'man_hours':0.,'unused':False,'tail':None,
                    'action_ids':[],'action_types':[],'effect':'No effect','benefit':0.,'chosen_rank':None,
                    'fragile_tails':fragile,'candidates':sorted(candidate_tails(view)) if policy in PREVENTIVE_POLICIES else [],'top_action':None,'top_benefit':None,'top_benefit_per_cost':None,
                    'unused_reason':'No intervention allowance' if not budget else ''}
            if policy == 'B2-K0':
                week['tail'] = select_tail(view,policy,config,shared)
            for _ in range(budget):
                target = select_tail(view,policy,config,shared)
                week['tail'] = target
                if target is not None:
                    _,ranking = intervention_ranking(view,target,config,shared)
                    if ranking:
                        top = ranking[0]
                        week.update(top_action=top['intervention_ids'][0],top_benefit=top['benefit'],
                                    top_benefit_per_cost=top['benefit_per_cost'])
                chosen = choose_intervention(view,target,config,shared) if target is not None else None
                if chosen is None:
                    week['unused_reason'] = ('No positive target-benefit action for selected tail' if target else
                                              'No tail with deadline within 14 days')
                    break
                action,row = chosen
                view = apply_intervention(view,action)
                week.update(tail=target,effect=row['effect'],chosen_rank=1)
                week['interventions'] += 1
                week['man_hours'] += action.cost_man_hours
                week['benefit'] += row['benefit']
                week['action_ids'].append(action.intervention_id)
                week['action_types'].append(action.kind)
                if action.kind == 'expedite_spare':
                    forecasts[action.target] = max(day,forecasts[action.target]-action.days)
                    actual_eta[action.target] = max(day,actual_eta[action.target]-action.days)
                elif action.kind in ('add_bay','add_crew_shift'):
                    (bays if action.kind == 'add_bay' else crews)[action.target] = day+1
                else:
                    # Assumed narrowing changes only the believed range, not sampled life.
                    t = tails[action.target]
                    tails[action.target] = replace(t,lower=t.rul_point-(t.rul_point-t.lower)*action.factor,
                                                   upper=t.rul_point+(t.upper-t.rul_point)*action.factor)
            week['unused'] = budget > 0 and week['interventions'] < budget
            metrics['intervention_man_hours'] += week['man_hours']
            metrics['unused_weeks'] += int(week['unused'])
            weeks.append(week)
        overrides = ({t.tail_id: 0. if t.tail_id in failed else
                      config.fixed_interval_cycles-cycles_since_overhaul[t.tail_id]-flown[t.tail_id]
                      for t in view.tails} if policy == 'B1' else None)
        scheduled = shared.planner.get(view,overrides)
        new_pending = {p.tail_id:replace(p,start_day=None if p.start_day is None else p.start_day+day,
                        end_day=None if p.end_day is None else p.end_day+day,
                        deadline_day=p.deadline_day+day) for p in scheduled.placements}
        for tail in sorted(set(pending) & set(new_pending)):
            if tail in active or tail in completed:
                continue
            old,new = pending[tail],new_pending[tail]
            if (old.start_day,old.bay,old.crew,old.spare) != (new.start_day,new.bay,new.crew,new.spare):
                metrics['plan_churn'] += 1
        for tail in sorted(set(new_pending) - set(pending)):
            events.append({'day':day,'tail':tail,'event':'PROPOSED','planned_start':new_pending[tail].start_day,
                           'deadline_day':new_pending[tail].deadline_day})
        events.append({'day':day,'event':'REPLAN','inputs_hash':scheduled.inputs_hash,
                       'cause': 'Observed failure: '+', '.join(new_failures) if new_failures else
                                'Initial simulated policy proposal' if day == state.today else
                                'Daily simulated review of utilisation and observed failures/arrivals'})
        pending = new_pending
        for tail in sorted(ids):
            if tail in grounded:
                metrics['aog_days'] += 1
                if tail in active:
                    metrics['maintenance_days'] += 1
                else:
                    p = pending.get(tail)
                    reason = ('spare' if p is None or p.spare is None or actual_eta[p.spare] > day else
                              'bay' if bays[p.bay] > day else 'crew' if crews[p.crew] > day else 'slot')
                    metrics[f'waiting_{reason}_days'] += 1
                    events.append({'day':day,'tail':tail,'event':'WAITING','resource':reason})
            elif tail not in completed:
                remaining[tail] -= tails[tail].rate
                flown[tail] += tails[tail].rate
    return PolicyOutcome(metrics,tuple(weeks),tuple(events))


def bootstrap_summary(runs: pd.DataFrame, config: SimulationConfig) -> pd.DataFrame:
    """Percentile bootstrap of scenario means, sharing resample indices across policies."""
    scenario_ids = sorted(runs.scenario_id.unique())
    if len(scenario_ids) != config.n_scenarios or runs.duplicated(['scenario_id','policy']).any():
        raise ValueError('Require exactly one paired result per policy and scenario')
    rng = np.random.default_rng(config.bootstrap_seed)
    indices = rng.integers(len(scenario_ids),size=(config.bootstrap_samples,len(scenario_ids)))
    rows = []
    for policy in POLICY_NAMES:
        subset = runs[runs.policy == policy].set_index('scenario_id').reindex(scenario_ids)
        if subset[list(VALIDATION_METRICS)].isna().any().any():
            raise ValueError('Incomplete paired policy metrics')
        for metric,(title,unit) in VALIDATION_METRICS.items():
            values = subset[metric].to_numpy(dtype=float)
            means = values[indices].mean(axis=1)
            low,high = np.quantile(means,[.025,.975])
            rows.append({'policy':policy,'policy_name':POLICY_NAMES[policy],'metric':metric,'metric_name':title,
                         'unit':unit,'mean':float(values.mean()),'ci_low':float(low),'ci_high':float(high),
                         'n_scenarios':len(values),'note':VALIDATION_NOTE})
    return pd.DataFrame(rows)


def monte_carlo(state: PlanningState, residuals: pd.DataFrame | Sequence[float],
                cycles_since_overhaul: Mapping[str,float] | Sequence[Mapping[str,float]], config: SimulationConfig | None = None,
                *, progress: bool = False, unchanged: ValidationResult | None = None) -> ValidationResult:
    """Evaluate all policies on exactly the same pre-drawn scenario pack."""
    settings = config or SimulationConfig()
    scenarios = draw_scenarios(state,residuals,settings)
    ages = ([dict(cycles_since_overhaul) for _ in scenarios] if isinstance(cycles_since_overhaul,Mapping)
            else [dict(row) for row in cycles_since_overhaul])
    ids = {t.tail_id for t in state.tails}
    if len(ages) != len(scenarios) or any(set(row) != ids or any(
            not math.isfinite(value) or value < 0 for value in row.values()) for row in ages):
        raise ValueError('Complete finite nonnegative initial ages needed for each paired scenario')
    ages_hash = hashlib.sha256(canonical_json(ages).encode()).hexdigest()
    state_hash = hashlib.sha256(canonical_json(state).encode()).hexdigest()
    scenarios_hash = hashlib.sha256(canonical_json([asdict(s) for s in scenarios]).encode()).hexdigest()
    reused = ('B0','B2','B3','B4','B4b') if unchanged is not None else ()
    if unchanged is not None:
        if (unchanged.manifest.get('design_revision') != DESIGN_REVISION or
            unchanged.manifest.get('initial_ages_sha256') != ages_hash or
            unchanged.manifest.get('state_sha256') != state_hash or
            unchanged.manifest.get('scenarios_sha256') != scenarios_hash or
            unchanged.manifest.get('config') != asdict(settings)):
            raise ValueError('Unchanged-policy archive does not match inputs, config or paired shocks')
        ids = {draw.scenario_id for draw in scenarios}
        source = unchanged.runs[unchanged.runs.policy.isin(reused)]
        if source.duplicated(['scenario_id','policy']).any() or any(
            set(source[source.policy == policy].scenario_id) != ids for policy in reused):
            raise ValueError('Incomplete or duplicate unchanged-policy archive')
        week_count = math.ceil((state.horizon-state.today)/7)
        for policy in reused:
            subset = unchanged.weeks[unchanged.weeks.policy == policy]
            if subset.duplicated(['scenario_id','week']).any() or set(zip(subset.scenario_id,subset.week)) != {
                (scenario,week) for scenario in ids for week in range(week_count)}:
                raise ValueError('Incomplete weekly unchanged-policy archive')
        if not np.isfinite(source[list(VALIDATION_METRICS)].to_numpy(dtype=float)).all():
            raise ValueError('Nonfinite unchanged-policy archive outcomes')
        source = source.set_index(['scenario_id','policy'])
    shared = ValidationCache()
    runs,weeks = [],[]
    for index,draw in enumerate(scenarios):
        for policy in POLICY_NAMES:
            if policy in reused:
                stored = source.loc[(draw.scenario_id,policy)].to_dict()
                stored.setdefault('initial_overdue_tails',0)
                stored.setdefault('inductions_before_due',0)
                runs.append({'scenario_id':draw.scenario_id,'policy':policy,**stored})
                weeks.extend(unchanged.weeks[(unchanged.weeks.scenario_id == draw.scenario_id) &
                                             (unchanged.weeks.policy == policy)].to_dict('records'))
                continue
            outcome = run_policy(state,draw,policy,ages[index],settings,shared)
            runs.append({'scenario_id':draw.scenario_id,'policy':policy,**outcome.metrics})
            weeks.extend({'scenario_id':draw.scenario_id,**row} for row in outcome.weeks)
        if progress and (index+1) % 20 == 0:
            print(f'Validation scenarios completed: {index+1}/{settings.n_scenarios}',flush=True)
    frame = pd.DataFrame(runs).astype({'initial_overdue_tails':'int64','inductions_before_due':'int64'}).assign(
        horizon_days=state.horizon-state.today)
    manifest = {'note':VALIDATION_NOTE,'config':asdict(settings),'design_revision':DESIGN_REVISION,
        'horizon_days':state.horizon-state.today,'initial_ages_sha256':ages_hash,
        'bootstrap_confidence':.95,
        'state_sha256':state_hash,'scenarios_sha256':scenarios_hash,
        'reused_policies':list(reused),
        'policies':POLICY_NAMES,'metrics':VALIDATION_METRICS,
        'initial_nonpositive_rul_draws':sum(v <= 0 for s in scenarios for _,v in s.true_rul),
        'assumptions':[
            'Signed capped-target minus point calibration residuals; sample engines then causal residual rows uniformly.',
            'True RUL equals point plus sampled residual times the predeclared stress scale; nonpositive draws are initially failed.',
            'Independent uniform integral spare delays; forecasts reveal missed ETAs, never future arrival dates.',
            'AOG is time from grounding to completion, including resource waiting and induction/repair; healthy future-slot waiting is excluded.',
            'Grounding occurs at observed failure, preventive RUL deadline, or fixed-interval due date. Grounded aircraft stop flying and cannot newly fail.',
            'Unplanned duration is ceil(normal duration times assumed repair multiplier); all policies need spare, bay and crew.',
            'Disjoint waiting-day components use spare, bay, crew priority, then permitted-slot delay; maintenance is counted separately.',
            'Fixed-interval preplans future interval deadlines within the horizon using observed technical age and the same planner.',
            'B2/B3/B4/B4b share the preventive planner; frozen attention definitions choose only the intervention tail.',
            'Resource action score is selected-tail Covered increase plus Late reduction per man-hour; fleet benefit is descriptive.',
            'B2/B3/B4/B4b share the resource-action menu and costs; exclude No effect and nonpositive target-benefit actions.',
            'B0/B1/B2-K0 have no interventions; unused_weeks is zero for policies without an intervention budget.',
            'Inspection is assumed, not scored: it is not in any simulated action menu.',
            'Attention candidates: tails with deadline within 14 days. B2 earliest deadline; B3 largest half-width minus slack; B4 largest half-width minus min(float,slack). K=1; no fallback tail.',
            'B4b ranks half-width minus float directly; > R uses R; Unplanned float is zero; ties by deadline then tail ID.',
            'B2 versus B2-K0 paired comparisons and combined ties cover AOG, failures, wasted life and churn only.',
            'Added resources persist to horizon; expedite moves both forecast and hidden ETA by the same days.',
            'Plan churn counts changed future start/bay/crew/spare; first assignment and completion are excluded.',
            'One original-engine removal per tail; replacement assumed serviceable to horizon.',
            'Marginal percentile bootstrap intervals use common scenario resamples; no claim of aircraft performance.'],
        'b3_b4':[]}
    a = frame[frame.policy == 'B3'].set_index('scenario_id')
    b = frame[frame.policy == 'B4'].set_index('scenario_id')
    for metric in VALIDATION_METRICS:
        difference = b[metric]-a[metric]
        manifest['b3_b4'].append({'metric':metric,'mean_difference_b4_minus_b3':float(difference.mean()),
                                 'exact_scenario_ties':int((difference == 0).sum()),
                                 'all_scenarios_tied':bool((difference == 0).all())})
    week_frame = pd.DataFrame(weeks).reindex(columns=['scenario_id','week','day','policy','budget','interventions',
        'man_hours','unused','tail','action_ids','action_types','effect','benefit','chosen_rank','fragile_tails',
        'candidates','top_action','top_benefit','top_benefit_per_cost','unused_reason']).assign(
            horizon_days=state.horizon-state.today)
    return ValidationResult(bootstrap_summary(frame,settings),frame,week_frame,manifest)


def write_validation(result: ValidationResult, artifact_dir: Path) -> None:
    """Save computed outputs with fixed formatting and print all results, including ties."""
    artifact_dir.mkdir(parents=True,exist_ok=True)
    config = SimulationConfig(**result.manifest['config'])
    level = result.manifest.get('stress_level',{}).get('name','original')
    wide = validation_cell_rows(result,config,level,config.repair_multiplier)
    for name,frame in (('validation.csv',wide),('validation_runs.csv',result.runs),
                       ('validation_weeks.csv',result.weeks)):
        stored = frame.copy()
        for column in ('action_ids','action_types','fragile_tails','candidates'):
            if column in stored:
                stored[column] = stored[column].map(canonical_json)
        stored.to_csv(artifact_dir/name,index=False,lineterminator='\n',float_format='%.12g')
    (artifact_dir/'validation_manifest.json').write_bytes(canonical_json(result.manifest).encode('utf-8'))
    print(VALIDATION_NOTE)
    print('Means with 95% percentile bootstrap confidence intervals')
    print(result.summary[['policy','metric_name','unit','mean','ci_low','ci_high']].to_string(
        index=False,float_format=lambda value:f'{value:.12g}'))
    for row in result.manifest['b3_b4']:
        print(f"B3 / B4 {row['metric']}: {'tie in every scenario' if row['all_scenarios_tied'] else 'observed differences'}; "
              f"mean B4 - B3 = {row['mean_difference_b4_minus_b3']:.12g}; "
              f"exact scenario ties = {row['exact_scenario_ties']}/{result.manifest['config']['n_scenarios']}")


def validation_cell_rows(result: ValidationResult, config: SimulationConfig,
                         stress_level: str, repair_multiplier: float) -> pd.DataFrame:
    """One wide row per policy or paired comparison, with all outcome CIs."""
    long = pd.concat([result.summary,paired_difference_rows(result,config)],ignore_index=True)
    diagnostics = opportunity_diagnostics(result.weeks).set_index('policy')
    choice_shares = tail_difference_rows(result,config)
    rows = []
    for policy,group in long.groupby('policy',sort=False):
        paired = policy not in POLICY_NAMES
        row = dict(design_revision=DESIGN_REVISION,stress_level=stress_level,repair_multiplier=repair_multiplier,
                   horizon_days=result.manifest['horizon_days'],policy=policy,
                   policy_name=group.iloc[0].policy_name,row_type='paired_difference' if paired else 'policy',
                   n_scenarios=config.n_scenarios,fixed_interval_cycles=config.fixed_interval_cycles,note=VALIDATION_NOTE,
                   weekly_budget=config.weekly_budget,initial_age_rule=result.manifest.get('initial_age_rule','caller-supplied ages'),
                   tie_metric_scope='outcomes_only' if policy == 'B2-B2-K0' else
                       'all_reported_metrics' if paired else 'not_applicable')
        for _,values in group.iterrows():
            for suffix,source in (('mean','mean'),('ci_low','ci_low'),('ci_high','ci_high')):
                row[f'{values.metric}_{suffix}'] = values[source]
            if paired:
                ties = int(values.tie_scenarios)
                row[f'{values.metric}_ties'] = ties
                row[f'{values.metric}_ties_over_n'] = f'{ties}/{config.n_scenarios}'
        if paired:
            left,right = next((a,b) for a,b in PAIRED_POLICIES if f'{a}-{b}' == policy)
            metrics = paired_metrics(left,right)
            a = result.runs[result.runs.policy == left].set_index('scenario_id')[list(metrics)]
            b = result.runs[result.runs.policy == right].set_index('scenario_id')[list(metrics)]
            ties = int(a.eq(b).all(axis=1).sum())
            row.update(tie_scenarios=ties,ties_over_n=f'{ties}/{config.n_scenarios}')
        else:
            row.update(diagnostics.loc[policy].to_dict())
            for _,share in choice_shares.iterrows():
                key = share.policy.lower().replace('/','_')+'_share'
                row.update({key:share['mean'],key+'_ci_low':share.ci_low,key+'_ci_high':share.ci_high})
        rows.append(row)
    return pd.DataFrame(rows).reindex(columns=VALIDATION_COLUMNS)


def opportunity_diagnostics(weeks: pd.DataFrame) -> pd.DataFrame:
    """Descriptive competing-choice exposure and applied-action counts by policy."""
    choices = weeks[weeks.policy.isin(('B2','B3','B4'))].copy()
    choices['tail'] = choices['tail'].fillna('none')
    wide = choices.pivot(index=['scenario_id','week'],columns='policy',values='tail')
    if set(wide.columns) != {'B2','B3','B4'} or wide.isna().any().any():
        raise ValueError('Complete paired weekly choices required')
    differing = wide.nunique(axis=1) > 1
    all_choices = weeks[weeks.policy.isin(INTERVENTION_POLICIES)].assign(tail=lambda f:f['tail'].fillna('none'))
    all_wide = all_choices.pivot(index=['scenario_id','week'],columns='policy',values='tail')
    all_differing = all_wide.nunique(axis=1) > 1
    rows = []
    for policy,group in weeks.groupby('policy',sort=False):
        multi = group.candidates.map(len).ge(2)
        share = float(multi.mean())
        kinds = [kind for items in group.action_types for kind in items]
        if set(kinds) - set(ACTION_TYPES):
            raise ValueError('Only scored resource actions belong in validation diagnostics')
        note = ('Few competing-tail weeks: test lacks power to distinguish attention rules; descriptive warning, not a formal power calculation.'
                if policy in PREVENTIVE_POLICIES and share < .25 else
                'Opportunity share is descriptive; ties do not establish policy equivalence.' if policy in PREVENTIVE_POLICIES else
                'No attention-based intervention policy.')
        rows.append(dict(policy=policy,review_weeks=len(group),multi_candidate_weeks=int(multi.sum()),
                         multi_candidate_share=share,b2_b3_b4_different_tail_weeks=int(differing.sum()),
                         b2_b3_b4_different_tail_share=float(differing.mean()),power_note=note,
                         b2_b3_b4_b4b_different_tail_weeks=int(all_differing.sum()),
                         b2_b3_b4_b4b_different_tail_share=float(all_differing.mean()),
                         **{f'{kind}_count':kinds.count(kind) for kind in ACTION_TYPES}))
    return pd.DataFrame(rows)


def print_week_trace(result: ValidationResult, count: int = 3) -> None:
    """Print complete B2-B4 weekly decision traces for the first paired draws."""
    columns = ['scenario_id','policy','week','candidates','fragile_tails','tail','top_action','top_benefit',
                'action_ids','effect','benefit','man_hours','unused_reason']
    rows = result.weeks[(result.weeks.scenario_id < count) & result.weeks.policy.isin(INTERVENTION_POLICIES)]
    print('Weekly traces: candidates (deadline <= 14 days), Fragile tails, policy choice and shared ranking')
    print(rows[columns].to_string(index=False))
    print(chosen_tail_differences(result.weeks,count).to_string(index=False))


def chosen_tail_differences(weeks: pd.DataFrame, count: int | None = None) -> pd.DataFrame:
    """Share of paired weeks where two policies chose different tails (None counts as a value)."""
    frame = weeks if count is None else weeks[weeks.scenario_id < count]
    chosen = frame[frame.policy.isin(INTERVENTION_POLICIES)].assign(tail=lambda f: f['tail'].fillna('none'))
    wide = chosen.pivot_table(index=['scenario_id','week'],columns='policy',values='tail',aggfunc='first')
    return pd.DataFrame([{'pair':f'{a}/{b}','weeks':len(wide),'differ':int((wide[a] != wide[b]).sum()),
                          'share':float((wide[a] != wide[b]).mean())} for a,b in CHOICE_PAIRS if a in wide and b in wide])


def paired_metrics(left: str, right: str) -> tuple[str, ...]:
    """The no-budget control compares physical outcomes, without budget columns."""
    return OUTCOME_METRICS if (left,right) == ('B2','B2-K0') else tuple(VALIDATION_METRICS)


def paired_difference_rows(result: ValidationResult, config: SimulationConfig) -> pd.DataFrame:
    """Named scenario-paired differences with common bootstrap CIs and exact ties."""
    rng = np.random.default_rng(config.bootstrap_seed)
    ids = sorted(result.runs.scenario_id.unique())
    indices = rng.integers(len(ids),size=(config.bootstrap_samples,len(ids)))
    rows = []
    for left,right in PAIRED_POLICIES:
        a = result.runs[result.runs.policy == left].set_index('scenario_id').reindex(ids)
        b = result.runs[result.runs.policy == right].set_index('scenario_id').reindex(ids)
        for metric in paired_metrics(left,right):
            title,unit = VALIDATION_METRICS[metric]
            diff = (a[metric]-b[metric]).to_numpy(dtype=float)
            low,high = np.quantile(diff[indices].mean(axis=1),[.025,.975])
            rows.append({'policy':f'{left}-{right}','policy_name':f'{left} minus {right} (paired)','metric':metric,'metric_name':title,
                         'unit':unit,'mean':float(diff.mean()),'ci_low':float(low),'ci_high':float(high),
                         'n_scenarios':len(diff),'note':VALIDATION_NOTE,'tie_scenarios':int((diff == 0).sum())})
    return pd.DataFrame(rows)


def tail_difference_rows(result: ValidationResult, config: SimulationConfig) -> pd.DataFrame:
    """Per-scenario share of weeks with different chosen tails, with bootstrap CIs."""
    rng = np.random.default_rng(config.bootstrap_seed)
    ids = sorted(result.runs.scenario_id.unique())
    indices = rng.integers(len(ids),size=(config.bootstrap_samples,len(ids)))
    chosen = result.weeks[result.weeks.policy.isin(INTERVENTION_POLICIES)].assign(tail=lambda f: f['tail'].fillna('none'))
    wide = chosen.pivot_table(index=['scenario_id','week'],columns='policy',values='tail',aggfunc='first')
    rows = []
    for a,b in CHOICE_PAIRS:
        if a not in wide or b not in wide:
            continue
        share = (wide[a] != wide[b]).groupby(level=0).mean().reindex(ids).to_numpy(dtype=float)
        low,high = np.quantile(share[indices].mean(axis=1),[.025,.975])
        rows.append({'policy':f'{a}/{b}','policy_name':f'{a} vs {b} chosen tail','metric':'tail_differs',
                     'metric_name':'Weeks with different chosen tail','unit':'share of weeks','mean':float(share.mean()),
                     'ci_low':float(low),'ci_high':float(high),'n_scenarios':len(ids),'note':VALIDATION_NOTE,
                     'tie_scenarios':int((share == 0).sum())})
    return pd.DataFrame(rows)


def whatif_demo_state(seed: int = 49) -> PlanningState:
    """Seeded assumed fixture with a focal spare delay and one-bay bottleneck.

    Inputs specify a hypothetical planning story, never model or aircraft
    performance. Labels/benefits are computed by the planner and margin code.
    """
    rng = np.random.default_rng(seed)
    points = (4, 8, 12, 40, 80, 120)
    tails = []
    for index, point in enumerate(points, start=1):
        width = 16. if index == 4 else float(rng.uniform(.25, 1) if index <= 3 else rng.uniform(2, 5))
        tails.append(Tail(f'T-{index:02d}', float(point), point-width, point+width, 2.,
                          3 if index == 4 else 2, 'PN-FOCAL' if index == 4 else 'PN-DEMO'))
    spares = tuple(Spare(f'S{i}', 15 if i == 2 else 0, 'PN-FOCAL' if i == 2 else 'PN-DEMO')
                   for i in range(1, 7))
    return PlanningState(tuple(tails), spares, (Resource('BAY-01'),), (Resource('CREW-01'),),
                          safety_buffer=0)


def generate_whatif_demo(directory: Path, seed: int = 49) -> None:
    """Write a byte-reproducible assumed fixture compatible with offline ingestion."""
    from dataclasses import asdict
    state = whatif_demo_state(seed)
    fleet = pd.DataFrame([{**asdict(t), 'source': 'assumed_whatif_scenario',
                           'updated_day': state.today, 'data_label': WHATIF_LABEL} for t in state.tails])
    tables = {'fleet.csv': fleet,
              'spares.csv': pd.DataFrame([asdict(s) for s in state.spares]),
              'resources.csv': pd.DataFrame([{'kind': kind, **asdict(r)}
                  for kind, resources in (('bay', state.bays), ('crew', state.crews)) for r in resources]),
              'health_stream.csv': pd.DataFrame([{'tail_id': t.tail_id, 'cycle': 30,
                  'point': t.rul_point, 'lower': t.lower, 'upper': t.upper} for t in state.tails])}
    directory.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(directory/name, index=False, lineterminator='\n', float_format='%.12g')
    manifest = {'data_label': WHATIF_LABEL, 'seed': seed, 'today': state.today,
                'horizon': state.horizon, 'safety_buffer': state.safety_buffer,
                'model_source': 'assumed fictional scenario; not a calibrated model result'}
    (directory/'manifest.json').write_bytes(canonical_json(manifest).encode('utf-8'))


def story_silos(state: PlanningState) -> dict[str, pd.DataFrame]:
    """Describe the assumed story using the four-silo CSV schemas.

    Technical counters and health update days are fictional input annotations,
    not measured engine histories. Resources/rates describe this same scenario.
    """
    tails = sorted(state.tails, key=lambda t: t.tail_id)
    return {
        'tails.csv': pd.DataFrame([{'tail_id': t.tail_id, 'utilisation_cycles_per_day': t.rate,
                                   'engine_id': f'E-{i:02d}'} for i, t in enumerate(tails, 1)]),
        'health.csv': pd.DataFrame([{'engine_id': f'E-{i:02d}', 'last_update_day': state.today}
                                    for i in range(1, len(tails)+1)]),
        'tech_records.csv': pd.DataFrame([{'tail_id': t.tail_id, 'cycles_since_overhaul': i*100,
                                         'open_snags': 0} for i, t in enumerate(tails, 1)]),
        'spares.csv': pd.DataFrame([{'spare_id': s.spare_id, 'available_day': s.available_day}
                                    for s in state.spares], columns=['spare_id', 'available_day']),
        'resources.csv': pd.DataFrame([{'resource': kind, 'count': len(resources), 'shift_hours': 8}
                                       for kind, resources in (('bay', state.bays), ('crew', state.crews))]),
    }


def generate_fleet_pack(directory: Path, seed: int = 49, today: int = 0) -> None:
    """Write the requested four-silo fictional CSV pack with reproducible bytes.

    Health and technical records are separate silos; spares/resources form
    the capacity silo. No benchmark estimates or evaluation truth are read.
    """
    if isinstance(today, bool) or not isinstance(today, int) or today < 0:
        raise ValueError('today must be a nonnegative integer')
    rng = np.random.default_rng(seed)
    tails = [f'T-{i:02d}' for i in range(1, 11)]
    engines = [f'E-{i:02d}' for i in range(1, 11)]
    tables = {
        'tails.csv': pd.DataFrame({'tail_id': tails,
            'utilisation_cycles_per_day': np.round(rng.uniform(1.5, 3.0, 10), 6),
            'engine_id': engines}),
        'health.csv': pd.DataFrame({'engine_id': engines,
            'last_update_day': today - rng.integers(0, min(today, 7) + 1, 10)}),
        'tech_records.csv': pd.DataFrame({'tail_id': tails,
            'cycles_since_overhaul': rng.integers(100, 2001, 10),
            'open_snags': rng.integers(0, 4, 10)}),
        'spares.csv': pd.DataFrame({'spare_id': ['SP-01', 'SP-02', 'SP-03'],
            'available_day': today + np.sort(rng.integers(0, 21, 3))}),
        'resources.csv': pd.DataFrame({'resource': ['bay', 'crew'],
            'count': [2, 1], 'shift_hours': [8, 8]}),
    }
    directory.mkdir(parents=True, exist_ok=True)
    for name, frame in tables.items():
        frame.to_csv(directory / name, index=False, lineterminator='\n', float_format='%.12g')
    manifest = {'data_label': 'Fictional simulated four-silo fleet; no live aircraft data.',
                'seed': seed, 'today': today, 'files': list(tables)}
    (directory / 'manifest.json').write_bytes(canonical_json(manifest).encode('utf-8'))


def generate_pack(oof: pd.DataFrame, directory: Path, seed: int = 7,
                  n_tails: int = 6, n_spares: int = 4, n_bays: int = 1,
                  n_crews: int = 1, horizon: int = 40) -> None:
    """Replay held-out NASA estimates on a seeded, explicitly fictional fleet."""
    required = {'unit','cycle','true_rul','point','lower','upper'}
    if not required <= set(oof) or n_tails < 1 or n_spares < 0 or min(n_bays,n_crews,horizon) < 1:
        raise ValueError('Invalid OOF data or fleet settings')
    candidates = oof[(oof.true_rul.between(8,40)) & (oof.cycle >= 30)]
    units = np.sort(candidates.unit.unique())
    if len(units) < n_tails:
        raise ValueError('Not enough distinct benchmark engines')
    rng = np.random.default_rng(seed)
    selected = rng.choice(units, size=n_tails, replace=False)
    fleet, histories, evaluation = [], [], {}
    for i, unit in enumerate(selected):
        rows = candidates[candidates.unit == unit].sort_values('cycle')
        row = rows.iloc[int(rng.integers(len(rows)))]
        tail_id = f'TAIL-{i+1:02d}'
        rate = float(rng.choice([1.,1.5,2.]))
        fleet.append({'tail_id':tail_id, 'rul_point':float(row.point), 'lower':float(row.lower),
                      'upper':float(row.upper), 'rate':rate, 'duration':int(rng.integers(2,5)),
                      'part_number':'PN-ENG-A', 'engine_unit':int(unit), 'observed_cycle':int(row.cycle),
                      'source':'lightgbm_oof', 'updated_day':0, 'data_label':DATA_LABEL})
        history = oof[(oof.unit == unit)&(oof.cycle <= row.cycle)].tail(30)[['cycle','point','lower','upper']].copy()
        history.insert(0,'tail_id',tail_id)
        histories.append(history)
        evaluation[tail_id] = float(row.true_rul)
    spares = [{'spare_id':f'SP-{i+1:02d}', 'available_day':int(day), 'part_number':'PN-ENG-A'}
              for i,day in enumerate(np.sort(rng.integers(0,horizon+1,n_spares)))]
    resources = [{'kind':kind, 'resource_id':f'{prefix}-{i+1:02d}', 'free_day':0}
                 for kind,prefix,count in (('bay','BAY',n_bays), ('crew','CREW',n_crews)) for i in range(count)]
    directory.mkdir(parents=True, exist_ok=True)
    tables = {'fleet.csv':pd.DataFrame(fleet), 'spares.csv':pd.DataFrame(spares,columns=['spare_id','available_day','part_number']),
              'resources.csv':pd.DataFrame(resources), 'health_stream.csv':pd.concat(histories,ignore_index=True)}
    for name, frame in tables.items():
        frame.to_csv(directory/name, index=False, lineterminator='\n', float_format='%.12g')
    manifest = {'seed':seed,'horizon':horizon,'data_label':DATA_LABEL,
                'model_source':'lightgbm_oof','n_tails':n_tails,'n_spares':n_spares,
                'n_bays':n_bays,'n_crews':n_crews}
    (directory/'manifest.json').write_bytes(canonical_json(manifest).encode('utf-8'))
    (directory/'simulation_truth.json').write_bytes(canonical_json({'data_label':'Synthetic evaluation only',
                                                                  'remaining_cycles':evaluation}).encode('utf-8'))


def simulate(state: PlanningState, scheduled: Plan, remaining_cycles: Mapping[str,float]) -> dict:
    """Account synthetic tail-days against a fixed proposed plan.

    Exhausting a flying day's cycles causes failure on the next day. An
    induction after failure counts as AOG through its repair. A completed
    replacement is assumed serviceable for the rest of this short horizon.
    This is evaluation only and does not approve or execute the plan.
    """
    if set(remaining_cycles) != {t.tail_id for t in state.tails} or any(
            not math.isfinite(v) or v < 0 for v in remaining_cycles.values()):
        raise ValueError('Complete, finite nonnegative synthetic remaining cycles required')
    placements = {p.tail_id:p for p in scheduled.placements}
    if set(placements) != set(remaining_cycles):
        raise ValueError('Plan and fleet tail IDs must match')
    counts = {'OPERATING':0,'PLANNED_MAINT':0,'AOG':0}
    events,states = [],[]
    failures,planned_actions,unused_life = 0,0,0.
    for tail in sorted(state.tails,key=lambda t:t.tail_id):
        p = placements[tail.tail_id]
        remaining = float(remaining_cycles[tail.tail_id])
        failed,replaced = remaining <= 0,False
        for day in range(state.today,state.horizon):
            if p.end_day is not None and day == p.end_day:
                failed,replaced = False,True
                events.append({'day':day,'tail_id':tail.tail_id,'event':'COMPLETED'})
            if p.start_day == day:
                if not failed:
                    planned_actions += 1
                    unused_life += remaining
                events.append({'day':day,'tail_id':tail.tail_id,'event':'STARTED','after_failure':failed})
            in_maintenance = p.start_day is not None and p.start_day <= day < p.end_day
            daily_status = ('AOG' if failed else 'PLANNED_MAINT') if in_maintenance else ('AOG' if failed else 'OPERATING')
            counts[daily_status] += 1
            states.append({'day':day,'tail_id':tail.tail_id,'status':daily_status})
            if daily_status == 'OPERATING' and not replaced:
                remaining -= tail.rate
                if remaining <= 0:
                    failed = True
                    failures += 1
                    events.append({'day':day+1,'tail_id':tail.tail_id,'event':'FAILURE'})
    total = len(state.tails)*(state.horizon-state.today)
    metrics = {'operating_tail_days':counts['OPERATING'],'planned_maint_days':counts['PLANNED_MAINT'],
               'aog_days':counts['AOG'],'availability':counts['OPERATING']/total if total else 0.,
               'unplanned_failures':failures,'planned_actions':planned_actions,'unused_life_cycles':unused_life}
    return {'data_label':'Synthetic scenario accounting; not aircraft performance. Uses evaluation values unavailable to planning.',
            'inputs_hash':scheduled.inputs_hash,'metrics':metrics,
            'events':sorted(events,key=lambda e:(e['day'],e['tail_id'],e['event'])),
            'daily_states':sorted(states,key=lambda e:(e['day'],e['tail_id']))}
