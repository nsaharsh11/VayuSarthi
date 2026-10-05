"""Pure, deterministic earliest-start scheduling using believed inputs only."""
from dataclasses import asdict
import hashlib
from itertools import product
import math
from typing import Any, Mapping, Sequence

from vayu.schemas import (Plan, Placement, PlannerConfig, PinnedPlacement, PlanningState,
                          Resource, Spare, Tail, canonical_json)


def deadline_day(rul_point: float, safety_buffer: float, rate: float) -> int:
    """Apply the authoritative flight-cycle deadline formula, without offsets."""
    if not all(math.isfinite(v) for v in (rul_point,safety_buffer,rate)) or rate <= 0 or safety_buffer < 0:
        raise ValueError('Finite point/buffer and positive rate required')
    return math.floor((rul_point-safety_buffer)/rate)


def decision_signature(result: Plan) -> tuple:
    """Compare exactly all tails' (start,bay,spare,status), keyed by tail ID."""
    return tuple((p.tail_id,p.start_day,p.bay,p.spare,p.status)
                 for p in sorted(result.placements,key=lambda p:p.tail_id))


def plan(state: PlanningState, point_overrides: Mapping[str,float] | None = None,
         pinned_placements: Sequence[PinnedPlacement] | None = None) -> Plan:
    """Sort by deadline/ID, reserve crew/bay intervals and consume each spare.

    Overrides are mathematical planning-point perturbations for the float
    analysis, including negative values. They never replace health intervals.
    Pins form a reserved prefix: consume their spares and release each bay/
    crew after its last pinned induction ends. Do not insert jobs before pins.
    """
    overrides = dict(point_overrides or {})
    if not set(overrides) <= {t.tail_id for t in state.tails} or any(not math.isfinite(v) for v in overrides.values()):
        raise ValueError('Unknown tail ID or nonfinite point override')
    bays = {b.resource_id:b.free_day for b in state.bays}
    crews = {c.resource_id:c.free_day for c in state.crews}
    spares = {s.spare_id:s for s in state.spares if s.available_day <= state.horizon}
    deadlines = {t.tail_id:deadline_day(overrides.get(t.tail_id,t.rul_point),state.safety_buffer,t.rate) for t in state.tails}
    pins = tuple(pinned_placements or ())
    placements = _reserve_pins(state, pins, deadlines, bays, crews, spares)
    pinned_ids = {p.tail_id for p in pins}
    for tail in sorted((t for t in state.tails if t.tail_id not in pinned_ids),
                       key=lambda t:(deadlines[t.tail_id],t.tail_id)):
        deadline = deadlines[tail.tail_id]
        compatible = [s for s in spares.values() if s.part_number == tail.part_number]
        if not compatible:
            placements.append(Placement(tail.tail_id,deadline,None,None,None,None,None,'Unplanned','spare',
                                        f'No unused compatible spare available within horizon day {state.horizon}'))
            continue
        candidates = [(max(state.today+1,s.available_day,bays[b],crews[c]),s.available_day,s.spare_id,b,c)
                      for s,b,c in product(compatible,sorted(bays),sorted(crews))]
        start,_,spare_id,bay,crew = min(candidates)
        constraints = (('spare',spares[spare_id].available_day),('bay',bays[bay]),('crew',crews[crew]))
        binding = next((name for name,day in constraints if day == start),None)
        reason = ({'spare': f'Spare {spare_id} available only on day {start}',
                   'bay': f'Bay {bay} free only on day {start}',
                   'crew': f'Technician crew {crew} free only on day {start}'}[binding]
                  if binding is not None else f'Earliest permitted induction day is {start}')
        end = start+tail.duration
        placements.append(Placement(tail.tail_id,deadline,start,end,bay,crew,spare_id,
                                    'On time' if start <= deadline else 'Late',binding,reason))
        bays[bay],crews[crew] = end,end
        del spares[spare_id]
    data = asdict(state)
    for key,identifier in (('tails','tail_id'),('spares','spare_id'),('bays','resource_id'),('crews','resource_id')):
        data[key] = sorted(data[key],key=lambda row:row[identifier])
    hash_data = {'state':data,'point_overrides':overrides}
    if pins:
        hash_data['pinned_placements'] = [asdict(p) for p in sorted(pins, key=lambda p:p.tail_id)]
    inputs_hash = hashlib.sha256(canonical_json(hash_data).encode()).hexdigest()
    return Plan(tuple(sorted(placements, key=lambda p:(p.deadline_day,p.tail_id))),inputs_hash)


def _reserve_pins(state: PlanningState, pins: tuple[PinnedPlacement, ...],
                  deadlines: Mapping[str, int], bays: dict[str, int], crews: dict[str, int],
                  spares: dict[str, Spare]) -> list[Placement]:
    """Validate every fixed reservation before using residual resource capacity."""
    tails = {t.tail_id:t for t in state.tails}
    used_tails: set[str] = set()
    used_spares: set[str] = set()
    reservations: list[Placement] = []
    for pin in sorted(pins, key=lambda p:(p.start_day,p.tail_id)):
        if pin.tail_id not in tails or pin.tail_id in used_tails:
            raise ValueError('Pinned tail is unknown or duplicated')
        if pin.spare not in spares or pin.spare in used_spares or pin.bay not in bays or pin.crew not in crews:
            raise ValueError('Pinned resource is unknown, consumed or outside the spare horizon')
        tail, spare = tails[pin.tail_id], spares[pin.spare]
        if spare.part_number != tail.part_number:
            raise ValueError('Pinned spare is incompatible with tail')
        if pin.start_day < max(state.today+1,spare.available_day,bays[pin.bay],crews[pin.crew]):
            raise ValueError('Pinned induction starts before availability or overlaps another pin')
        end = pin.start_day + tail.duration
        reservations.append(Placement(pin.tail_id,deadlines[pin.tail_id],pin.start_day,end,
                                      pin.bay,pin.crew,pin.spare,
                                      'On time' if pin.start_day <= deadlines[pin.tail_id] else 'Late',None,
                                      f'Pinned placement honoured on day {pin.start_day}; '
                                      f'spare {pin.spare} reserved for {pin.tail_id}'))
        used_tails.add(pin.tail_id)
        used_spares.add(pin.spare)
        bays[pin.bay], crews[pin.crew] = end, end
    for spare in used_spares:
        del spares[spare]
    return reservations


def _checked_mapping(value: Mapping[str, Any], allowed: set[str]) -> dict[str, Any]:
    """Reject unrecognised input fields instead of consuming hidden metadata."""
    unknown = set(value) - allowed
    if unknown:
        raise ValueError(f'Unknown input fields: {", ".join(sorted(unknown))}')
    return dict(value)


def _tail_id(row: dict[str, Any]) -> dict[str, Any]:
    """Accept the requested tail output alias or the schema's tail_id key."""
    if 'tail' in row:
        if 'tail_id' in row and row['tail_id'] != row['tail']:
            raise ValueError('Conflicting tail and tail_id')
        row['tail_id'] = row.pop('tail')
    return row


def planning_state(tails: Sequence[Tail | Mapping[str, Any]],
               spares: Sequence[Spare | Mapping[str, Any]],
               bays: Sequence[Resource | str | Mapping[str, Any]],
               crews: Sequence[Resource | str | Mapping[str, Any]],
               config: PlannerConfig | Mapping[str, Any]) -> PlanningState:
    """Normalise explicit planner inputs once, without scheduling or side effects."""
    settings = config if isinstance(config, PlannerConfig) else PlannerConfig(**_checked_mapping(
        config, {'today','horizon','safety_buffer','duration'}))
    parsed_tails = []
    for tail in tails:
        if isinstance(tail, Tail):
            parsed_tails.append(tail)
            continue
        row = _tail_id(_checked_mapping(tail, {'tail','tail_id','rul_point','rate','duration',
                                              'lower','upper','part_number'}))
        row.setdefault('lower',row['rul_point'])
        row.setdefault('upper',row['rul_point'])
        row.setdefault('duration',settings.duration)
        parsed_tails.append(Tail(**row))
    parsed_spares = tuple(spare if isinstance(spare, Spare) else Spare(**_checked_mapping(
        spare, {'spare_id','available_day','part_number'})) for spare in spares)

    def resources(values: Sequence[Resource | str | Mapping[str, Any]]) -> tuple[Resource, ...]:
        """Normalise resource IDs, typed resources or resource_id/free_day rows."""
        return tuple(value if isinstance(value, Resource) else Resource(value) if isinstance(value, str)
                     else Resource(**_checked_mapping(value, {'resource_id','free_day'})) for value in values)

    return PlanningState(tuple(parsed_tails),parsed_spares,resources(bays),resources(crews),
                         settings.today,settings.horizon,settings.safety_buffer)


def pinned_reservations(values: Sequence[PinnedPlacement | Mapping[str, Any]] | None
                        ) -> tuple[PinnedPlacement, ...]:
    """Normalise optional fixed placements for planning and margin cache keys."""
    return tuple(pin if isinstance(pin, PinnedPlacement) else PinnedPlacement(**_tail_id(
        _checked_mapping(pin, {'tail','tail_id','start_day','bay','crew','spare'})))
                 for pin in values or ())


def plan_fleet(tails: Sequence[Tail | Mapping[str, Any]],
               spares: Sequence[Spare | Mapping[str, Any]],
               bays: Sequence[Resource | str | Mapping[str, Any]],
               crews: Sequence[Resource | str | Mapping[str, Any]],
               config: PlannerConfig | Mapping[str, Any],
               pinned_placements: Sequence[PinnedPlacement | Mapping[str, Any]] | None = None
               ) -> list[dict[str, Any]]:
    """Return Master Brief dictionaries; mappings use configured default duration."""
    state = planning_state(tails,spares,bays,crews,config)
    pins = pinned_reservations(pinned_placements)
    result = plan(state, pinned_placements=pins)
    return [{'tail':p.tail_id,'deadline_day':p.deadline_day,'start_day':p.start_day,
             'bay':p.bay,'crew':p.crew,'spare':p.spare,'status':p.status,
             'binding_resource':p.binding,'reason_code':p.reason_code} for p in result.placements]
