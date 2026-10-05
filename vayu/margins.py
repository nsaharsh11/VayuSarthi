"""Directional decision float, frozen deadline slack and planning attention."""
from collections import OrderedDict
from dataclasses import asdict, dataclass, replace
import math
import re
from time import perf_counter
from typing import Any, Callable, Mapping, Sequence

from vayu.planner import deadline_day, decision_signature, pinned_reservations, plan, planning_state
from vayu.schemas import (Plan, Placement, PlannerConfig, PinnedPlacement, PlanningState,
                          Resource, Spare, Tail, canonical_json)

TailInputs = Sequence[Tail | Mapping[str, Any]]
Pins = Sequence[PinnedPlacement | Mapping[str, Any]] | None


@dataclass(frozen=True)
class DecisionChange:
    """A witness restricted to the four Master Brief decision fields."""
    tail_id: str
    fields: tuple[str, ...]
    before: tuple[Any, ...]
    after: tuple[Any, ...]

    def to_dict(self) -> dict[str, Any]:
        """Expose auditable before/after values as JSON-compatible data."""
        names = ('start_day', 'bay', 'spare', 'status')
        return {'tail': self.tail_id, 'fields': list(self.fields),
                'before': dict(zip(names, self.before)), 'after': dict(zip(names, self.after))}


@dataclass(frozen=True)
class DecisionFloat:
    """Closest witness and independently searched downward/upward thresholds."""
    value: int | None
    radius: int
    delta: int | None
    changed_tails: tuple[str, ...]
    float_down: int | None = None
    float_up: int | None = None
    down_changes: tuple[DecisionChange, ...] = ()
    up_changes: tuple[DecisionChange, ...] = ()

    @property
    def display(self) -> str:
        """Use a finite search bound, never an unbounded substitute."""
        return str(self.value) if self.value is not None else f'> {self.radius}'

    @property
    def direction(self) -> str | None:
        """Report both when equal nearest thresholds are witnessed."""
        if self.value is None:
            return None
        if self.float_down == self.float_up:
            return 'both'
        return 'down' if self.float_down == self.value else 'up'

    def to_dict(self) -> dict[str, Any]:
        """Return exactly the requested directional summary and witness fields."""
        def bounded(value: int | None) -> int | str:
            return value if value is not None else f'> {self.radius}'
        return {'float_down': bounded(self.float_down), 'float_up': bounded(self.float_up),
                'float_min': bounded(self.value), 'direction': self.direction,
                'what_changed': {'down': [c.to_dict() for c in self.down_changes],
                                 'up': [c.to_dict() for c in self.up_changes]}}


@dataclass(frozen=True)
class Attention:
    """Planning attention only; no risk or airworthiness interpretation."""
    tail_id: str
    float_result: DecisionFloat
    slack: float | None
    half_width: float
    label: str
    reason: str


class PlannerCache:
    """Bounded in-memory LRU of immutable plans, keyed by all believed inputs."""

    def __init__(self, max_size: int = 4096) -> None:
        if isinstance(max_size, bool) or not isinstance(max_size, int) or max_size < 1:
            raise ValueError('Cache size must be a positive integer')
        self.max_size = max_size
        self.hits = self.misses = 0
        self._plans: OrderedDict[tuple[Callable[..., Plan], str], Plan] = OrderedDict()

    def clear(self) -> None:
        """Discard entries and reset hit/miss counters for independent sweeps."""
        self._plans.clear()
        self.hits = self.misses = 0

    def get(self, state: PlanningState, overrides: Mapping[str, float] | None = None,
            pins: tuple[PinnedPlacement, ...] = ()) -> Plan:
        """Reuse canonical input order, preserving numeric types and pin choices."""
        data = asdict(state)
        for source, identifier in (('tails', 'tail_id'), ('spares', 'spare_id'),
                                    ('bays', 'resource_id'), ('crews', 'resource_id')):
            data[source] = sorted(data[source], key=lambda row: row[identifier])
        key = (plan, canonical_json({'state': data, 'overrides': dict(overrides or {}),
                                       'pins': [asdict(pin) for pin in sorted(pins, key=lambda p: p.tail_id)]}))
        if key in self._plans:
            self.hits += 1
            self._plans.move_to_end(key)
            return self._plans[key]
        result = plan(state, overrides, pinned_placements=pins)
        self.misses += 1
        self._plans[key] = result
        if len(self._plans) > self.max_size:
            self._plans.popitem(last=False)
        return result


DEFAULT_CACHE = PlannerCache()


def _changes(before: Plan, after: Plan) -> tuple[DecisionChange, ...]:
    """Ignore crew, deadline, binding and explanations exactly as specified."""
    a = {row[0]: row[1:] for row in decision_signature(before)}
    b = {row[0]: row[1:] for row in decision_signature(after)}
    names = ('start_day', 'bay', 'spare', 'status')
    return tuple(DecisionChange(tail, tuple(name for name, old, new in zip(names, a[tail], b[tail])
                                          if old != new), a[tail], b[tail])
                 for tail in sorted(a) if a[tail] != b[tail])


def changed_tails(before: Plan, after: Plan) -> tuple[str, ...]:
    """Observe all fleet tails' four-field changes, not just the perturbed tail."""
    a = {row[0]: row[1:] for row in decision_signature(before)}
    b = {row[0]: row[1:] for row in decision_signature(after)}
    return tuple(tail for tail in sorted(set(a) | set(b)) if a.get(tail) != b.get(tail))


def _radius(value: int) -> int:
    """Validate a finite integer search bound, including the no-probe bound zero."""
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError('Search radius must be a nonnegative integer')
    return value


def _validate(state: PlanningState, tail_id: str, radius: int) -> Tail:
    _radius(radius)
    tail = next((tail for tail in state.tails if tail.tail_id == tail_id), None)
    if tail is None:
        raise ValueError('Unknown tail')
    return tail


def _state(tails: PlanningState | TailInputs,
           spares: Sequence[Spare | Mapping[str, Any]] | None,
           bays: Sequence[Resource | str | Mapping[str, Any]] | None,
           crews: Sequence[Resource | str | Mapping[str, Any]] | None,
           config: PlannerConfig | Mapping[str, Any] | None) -> PlanningState:
    """Use shared input normalisation without making a planner call."""
    if isinstance(tails, PlanningState):
        if any(value is not None for value in (spares, bays, crews, config)):
            raise ValueError('Use a PlanningState or separate inputs, not both')
        return tails
    if spares is None or bays is None or crews is None:
        raise ValueError('Separate tails require explicit spares, bays and crews')
    return planning_state(tails, spares, bays, crews, config if config is not None else {})


def _decision_float(state: PlanningState, tail_id: str, radius: int, cache: PlannerCache,
                    pins: tuple[PinnedPlacement, ...], baseline: Plan | None = None) -> DecisionFloat:
    tail = _validate(state, tail_id, radius)
    baseline = baseline if baseline is not None else cache.get(state, pins=pins)
    pinned_ids = {pin.tail_id for pin in pins}
    used_spares = {pin.spare for pin in pins}
    remaining = sum(spare.part_number == tail.part_number and spare.available_day <= state.horizon
                    and spare.spare_id not in used_spares for spare in state.spares)
    earliest = (deadline_day(tail.rul_point-radius, state.safety_buffer, tail.rate), tail_id)
    preceding = sum(other.tail_id != tail_id and other.tail_id not in pinned_ids and
                    other.part_number == tail.part_number and
                    (deadline_day(other.rul_point, state.safety_buffer, other.rate), other.tail_id) < earliest
                    for other in state.tails)
    if tail_id not in pinned_ids and preceding >= remaining:
        # Even at the earliest reachable deadline, preceding same-part jobs
        # consume every compatible spare. This tail can never reserve resources
        # within the bound; all other tails' relative order stays unchanged.
        return DecisionFloat(None, radius, None, ())
    deadlines = {other.tail_id: deadline_day(other.rul_point, state.safety_buffer, other.rate)
                 for other in state.tails}
    movable = [other.tail_id for other in state.tails if other.tail_id not in pinned_ids]
    ordering = sorted(movable, key=lambda identifier: (deadlines[identifier], identifier))
    placement = next(item for item in baseline.placements if item.tail_id == tail_id)
    found: dict[str, tuple[int | None, tuple[DecisionChange, ...]]] = {}
    for direction, sign in (('down', -1), ('up', 1)):
        endpoint = deadline_day(tail.rul_point+sign*radius, state.safety_buffer, tail.rate)
        endpoint_order = sorted(movable, key=lambda identifier: (
            endpoint if identifier == tail_id else deadlines[identifier], identifier))
        status = ('Unplanned' if placement.start_day is None else
                  'On time' if placement.start_day <= endpoint else 'Late')
        if endpoint_order == ordering and status == placement.status:
            # A single monotonic deadline cannot cross a neighbour and return;
            # a fixed start cannot cross its status boundary and return either.
            found[direction] = (None, ())
    regions: dict[tuple[str, ...], tuple[Plan, tuple[DecisionChange, ...]]] = {
        tuple(ordering): (baseline, ())}
    for magnitude in range(1, radius + 1):
        for direction, sign in (('down', -1), ('up', 1)):
            if direction in found:
                continue
            point = tail.rul_point + sign * magnitude
            current_deadline = deadline_day(point, state.safety_buffer, tail.rate)
            region = tuple(sorted(movable, key=lambda identifier: (
                current_deadline if identifier == tail_id else deadlines[identifier], identifier)))
            entry = regions.get(region)
            result = entry[0] if entry is not None else None
            changes = entry[1] if entry is not None else ()
            cached = next((item for item in result.placements if item.tail_id == tail_id), None) if result else None
            status = ('Unplanned' if cached is not None and cached.start_day is None else
                      'On time' if cached is not None and cached.start_day <= current_deadline else 'Late')
            if cached is None or status != cached.status:
                result = cache.get(state, {tail_id: point}, pins)
                changes = _changes(baseline, result)
                regions[region] = (result, changes)
            if changes:
                found[direction] = (magnitude, changes)
        if len(found) == 2:
            break
    down, down_changes = found.get('down', (None, ()))
    up, up_changes = found.get('up', (None, ()))
    finite = [value for value in (down, up) if value is not None]
    value = min(finite) if finite else None
    delta = (-down if down == value else up) if value is not None else None
    nearest = down_changes if delta is not None and delta < 0 else up_changes
    return DecisionFloat(value, radius, delta, tuple(change.tail_id for change in nearest),
                         down, up, down_changes, up_changes)


def decision_float(tail_id: str | PlanningState, tails: PlanningState | TailInputs | str,
                   radius: int = 40, *, R: int | None = None,
                   spares: Sequence[Spare | Mapping[str, Any]] | None = None,
                   bays: Sequence[Resource | str | Mapping[str, Any]] | None = None,
                   crews: Sequence[Resource | str | Mapping[str, Any]] | None = None,
                   config: PlannerConfig | Mapping[str, Any] | None = None,
                   pinned_placements: Pins = None, cache: PlannerCache | None = None
                   ) -> dict[str, Any] | DecisionFloat:
    """Search both signs independently and return first fleet-change witnesses.

    decision_float(tail_id, state_or_tails, ...) returns the requested dict.
    Existing decision_float(state, tail_id, radius) returns the typed result
    for the demo. Only one point is overridden per probe; negative mathematical
    perturbations are allowed. No range, pin or other tail input is changed.
    """
    bound = _radius(radius if R is None else R)
    legacy = isinstance(tail_id, PlanningState)
    if legacy:
        if not isinstance(tails, str):
            raise ValueError('Typed legacy call requires a tail ID')
        state, identifier = _state(tail_id, spares, bays, crews, config), tails
    else:
        if isinstance(tails, str):
            raise ValueError('Require a PlanningState or tail input collection')
        state, identifier = _state(tails, spares, bays, crews, config), tail_id
    result = _decision_float(state, identifier, bound, cache if cache is not None else DEFAULT_CACHE,
                             pinned_reservations(pinned_placements))
    return result if legacy else result.to_dict()


def _slack(point: float, rate: float, start: int | None, today: int, buffer: float) -> float | None:
    """Only arithmetic on a frozen placement; no planner or cache access."""
    if not all(math.isfinite(value) for value in (point, rate, buffer)) or rate <= 0 or buffer < 0:
        raise ValueError('Finite point/buffer and positive rate required')
    if isinstance(today, bool) or not isinstance(today, int) or today < 0:
        raise ValueError('today must be a nonnegative integer')
    if start is None:
        return None
    if isinstance(start, bool) or not isinstance(start, int) or start < today:
        raise ValueError('Frozen start must be an integer on or after today')
    return point - buffer - rate * (start - today)


def deadline_slack(frozen_plan: Plan | Sequence[Mapping[str, Any]] | PlanningState,
                   tails: TailInputs | Tail, placement: Placement | None = None, *,
                   today: int = 0, safety_buffer: float = 0
                   ) -> dict[str, float | None] | float | None:
    """Frozen per-tail slack in cycles; pass original today and safety buffer.

    deadline_slack(plan, tails, today=..., safety_buffer=...) returns a map.
    Existing (state, tail, placement) returns that tail's scalar.
    Neither form calls the planner, retrieves a plan or modifies placement.
    """
    if isinstance(frozen_plan, PlanningState):
        if not isinstance(tails, Tail) or placement is None or placement.tail_id != tails.tail_id:
            raise ValueError('Tail and frozen placement must match')
        return _slack(tails.rul_point, tails.rate, placement.start_day,
                      frozen_plan.today, frozen_plan.safety_buffer)
    if isinstance(tails, Tail) or placement is not None:
        raise ValueError('Per-tail map requires a tail collection and frozen plan')
    rows = [asdict(p) for p in frozen_plan.placements] if isinstance(frozen_plan, Plan) else list(frozen_plan)
    starts: dict[str, int | None] = {}
    for row in rows:
        identifier = row.get('tail_id', row.get('tail'))
        if not isinstance(identifier, str) or identifier in starts or 'start_day' not in row:
            raise ValueError('Frozen plan requires unique tail IDs and explicit start_day')
        starts[identifier] = row['start_day']
    result: dict[str, float | None] = {}
    for tail in tails:
        row = asdict(tail) if isinstance(tail, Tail) else tail
        identifier = row.get('tail_id', row.get('tail'))
        if identifier not in starts or identifier in result:
            raise ValueError('Every unique tail must have a frozen placement')
        result[identifier] = _slack(row['rul_point'], row['rate'], starts[identifier], today, safety_buffer)
    if set(result) != set(starts):
        raise ValueError('Frozen plan and tails must have matching IDs')
    return dict(sorted(result.items()))


def label(tail: Tail | Mapping[str, Any], float_result: DecisionFloat | int | str | None = None,
          slack: float | None = None, *, radius: int | None = None) -> str:
    """Covered iff float and frozen slack both cover interval half-width.

    Mappings accept lower/upper or half_width/h, float_min and
    deadline_slack/slack. Typed Tail accepts float_result and slack arguments.
    A > R bound establishes coverage only when R >= h; otherwise attention
    is conservatively Fragile. Unplanned slack stays undefined.
    """
    if isinstance(tail, Tail):
        width = (tail.upper - tail.lower) / 2
    else:
        width = ((tail['upper'] - tail['lower']) / 2 if 'lower' in tail and 'upper' in tail
                 else tail.get('half_width', tail.get('h')))
        float_result = tail.get('float_min', float_result)
        slack = tail.get('deadline_slack', tail.get('slack', slack))
    if width is None or isinstance(width, bool) or not math.isfinite(width) or width < 0:
        raise ValueError('Require a finite nonnegative half-width')
    if slack is not None and (isinstance(slack, bool) or not math.isfinite(slack)):
        raise ValueError('Deadline slack must be finite or undefined')
    if isinstance(float_result, DecisionFloat):
        radius, float_result = float_result.radius, float_result.value
    if isinstance(float_result, str):
        match = re.fullmatch(r'>\s*(\d+)', float_result)
        if match is None:
            raise ValueError('Expected a finite > R decision-float bound')
        radius, float_result = int(match.group(1)), None
    if float_result is not None and (isinstance(float_result, bool) or
                                    not math.isfinite(float_result) or float_result < 0):
        raise ValueError('Decision float must be finite, nonnegative or bounded')
    if radius is not None:
        _radius(radius)
    covers = float_result >= width if float_result is not None else radius is not None and radius >= width
    return 'Covered' if slack is not None and slack >= width and covers else 'Fragile'


def _fleet(state: PlanningState, radius: int, pins: tuple[PinnedPlacement, ...],
           cache: PlannerCache) -> tuple[Plan, dict[str, DecisionFloat]]:
    """Time a full fleet sharing one baseline; never embed time in results."""
    _radius(radius)
    started = perf_counter()
    calls, hits = cache.misses, cache.hits
    baseline = cache.get(state, pins=pins)
    results = {tail.tail_id: _decision_float(state, tail.tail_id, radius, cache, pins, baseline)
               for tail in sorted(state.tails, key=lambda t: t.tail_id)}
    elapsed = perf_counter() - started
    print(f'Full-fleet decision-float sweep: {elapsed:.6f} s '
          f'({len(state.tails)} tails, R={radius}; planner calls={cache.misses-calls}, '
          f'cache hits={cache.hits-hits})')
    return baseline, results


def full_fleet_sweep(tails: PlanningState | TailInputs, R: int = 40, *,
                     spares: Sequence[Spare | Mapping[str, Any]] | None = None,
                     bays: Sequence[Resource | str | Mapping[str, Any]] | None = None,
                     crews: Sequence[Resource | str | Mapping[str, Any]] | None = None,
                     config: PlannerConfig | Mapping[str, Any] | None = None,
                     pinned_placements: Pins = None, cache: PlannerCache | None = None
                     ) -> dict[str, dict[str, Any]]:
    """Return directional floats for every tail and print measured sweep seconds."""
    state = _state(tails, spares, bays, crews, config)
    _, values = _fleet(state, R, pinned_reservations(pinned_placements),
                        cache if cache is not None else DEFAULT_CACHE)
    return {identifier: value.to_dict() for identifier, value in values.items()}


def analyze(state: PlanningState, radius: int = 40, *, pinned_placements: Pins = None,
            cache: PlannerCache | None = None) -> tuple[Attention, ...]:
    """Measure full-fleet float, then frozen slack and attention labels for the UI."""
    baseline, values = _fleet(state, radius, pinned_reservations(pinned_placements),
                              cache if cache is not None else DEFAULT_CACHE)
    slacks = deadline_slack(baseline, state.tails, today=state.today, safety_buffer=state.safety_buffer)
    results = []
    for tail in sorted(state.tails, key=lambda t: t.tail_id):
        value, slack = values[tail.tail_id], slacks[tail.tail_id]
        half_width = (tail.upper - tail.lower) / 2
        attention = label(tail, value, slack)
        if slack is None:
            reason = 'Unplanned: no placement to measure deadline slack.'
        elif value.value is None and radius < half_width:
            reason = 'Search bound is smaller than interval half-width; Covered cannot be established.'
        elif attention == 'Covered':
            reason = 'Decision float and frozen deadline slack both cover the interval half-width.'
        else:
            reason = 'Decision float or frozen deadline slack is smaller than interval half-width.'
        results.append(Attention(tail.tail_id, value, slack, half_width, attention, reason))
    return tuple(results)


def sweep(state: PlanningState, tail_id: str, radius: int = 40, *, pinned_placements: Pins = None,
          cache: PlannerCache | None = None) -> list[dict[str, Any]]:
    """Chart every tested point using cached whole-fleet plans and fixed pins."""
    tail = _validate(state, tail_id, radius)
    cache = cache if cache is not None else DEFAULT_CACHE
    pins = pinned_reservations(pinned_placements)
    baseline = cache.get(state, pins=pins)
    rows, previous = [], None
    for delta in range(-radius, radius+1):
        result = baseline if delta == 0 else cache.get(state, {tail_id: tail.rul_point+delta}, pins)
        p = next(p for p in result.placements if p.tail_id == tail_id)
        rows.append({'delta': delta, 'rul_point': tail.rul_point+delta,
                     'start_day': p.start_day, 'deadline_day': p.deadline_day,
                     'bay': p.bay, 'spare': p.spare, 'status': p.status, 'binding': p.binding,
                     'changed_tails': changed_tails(baseline, result),
                     'boundary_tails': changed_tails(previous, result) if previous is not None else ()})
        previous = result
    return rows


def spare_eta_sweep(spare_id: str, state: PlanningState, max_delay: int = 5, *,
                    pinned_placements: Pins = None, cache: PlannerCache | None = None
                    ) -> list[dict[str, Any]]:
    """Delay one spare in days, reusing cached plans and fleet-wide witnesses.

    Compare the same four decision fields as RUL float. An ETA that invalidates
    a fixed pin is reported as blocked; pins are never moved or released.
    """
    _radius(max_delay)
    spare = next((item for item in state.spares if item.spare_id == spare_id), None)
    if spare is None:
        raise ValueError('Unknown spare')
    cache = cache if cache is not None else DEFAULT_CACHE
    pins = pinned_reservations(pinned_placements)
    baseline = cache.get(state, pins=pins)
    rows = []
    for shift in range(1, max_delay + 1):
        available = spare.available_day + shift
        blocked = next((pin for pin in pins if pin.spare == spare_id and
                        (available > pin.start_day or available > state.horizon)), None)
        if blocked is not None:
            reason = (f'Pinned placement for {blocked.tail_id} on day {blocked.start_day} '
                      f'conflicts with spare {spare_id} availability on day {available}; '
                      'placement review required')
            rows.append({'shift_days': shift, 'available_day': available,
                         'changed_tails': [], 'what_changed': [],
                         'late_tails': [], 'blocked_reason': reason})
            continue
        delayed = replace(state, spares=tuple(replace(item, available_day=available)
                          if item.spare_id == spare_id else item for item in state.spares))
        changes = _changes(baseline, cache.get(delayed, pins=pins))
        witnesses = [change.to_dict() for change in changes]
        late = [row['tail'] for row in witnesses if row['after']['status'] == 'Late'
                and row['before']['status'] != 'Late']
        rows.append({'shift_days': shift, 'available_day': available,
                     'changed_tails': [change.tail_id for change in changes],
                     'what_changed': witnesses, 'late_tails': late, 'blocked_reason': None})
    return rows


def spare_eta_float(spare_id: str, state: PlanningState, max_delay: int = 5, *,
                    pinned_placements: Pins = None, cache: PlannerCache | None = None
                    ) -> dict[str, Any]:
    """Return the first plan-change day and a separate observed Late threshold.

    All probes are retained so a later Late transition can be distinguished
    from an earlier start/resource change. No change uses a finite day bound.
    """
    probes = spare_eta_sweep(spare_id, state, max_delay,
                             pinned_placements=pinned_placements, cache=cache)
    first = next((row for row in probes if row['what_changed']), None)
    late = next((row for row in probes if row['late_tails']), None)
    blocked = next((row for row in probes if row['blocked_reason']), None)
    value = first['shift_days'] if first is not None else (
        'Pin conflict' if blocked is not None else f'> {max_delay} days')
    return {'spare': spare_id, 'max_delay_days': max_delay, 'float_min': value,
            'changed_tails': first['changed_tails'] if first is not None else [],
            'what_changed': first['what_changed'] if first is not None else [],
            'late_shift': late['shift_days'] if late is not None else None,
            'late_tails': late['late_tails'] if late is not None else [],
            'blocked_shift': blocked['shift_days'] if blocked is not None else None,
            'blocked_reason': blocked['blocked_reason'] if blocked is not None else None,
            'probes': probes}
