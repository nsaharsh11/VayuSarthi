"""Hand-calculated deterministic records and immutable pinned reservations."""
from dataclasses import replace

import pytest

from vayu.planner import plan, plan_fleet
from vayu.schemas import PinnedPlacement, PlannerConfig, PlanningState, Resource, Spare, Tail


def three_tail_state() -> PlanningState:
    """Two bays, one crew and staggered spares: starts 1, 4, 12."""
    return PlanningState((Tail('T3', 30, 28, 32, 2, 3), Tail('T2', 5, 3, 7, 1, 3),
                          Tail('T1', 10, 8, 12, 2, 3)),
                         (Spare('S3', 12), Spare('S2', 0), Spare('S1', 0)),
                         (Resource('B2'), Resource('B1')), (Resource('C1'),))


def test_three_tail_records_and_reversed_inputs() -> None:
    state = three_tail_state()
    records = plan_fleet(state.tails, state.spares, state.bays, state.crews, PlannerConfig())
    assert list(records[0]) == ['tail', 'deadline_day', 'start_day', 'bay', 'crew',
                                'spare', 'status', 'binding_resource', 'reason_code']
    assert [(r['tail'], r['deadline_day'], r['start_day'], r['status']) for r in records] == [
        ('T2', 3, 1, 'On time'), ('T1', 4, 4, 'On time'), ('T3', 14, 12, 'On time')]
    assert records[0]['binding_resource'] is None
    assert records[1]['binding_resource'] == 'bay'
    assert records[2]['reason_code'] == 'Spare S3 available only on day 12'
    assert records == plan_fleet(state.tails[::-1], state.spares[::-1], state.bays[::-1],
                                 state.crews, {})
    assert records == plan_fleet(state.tails, state.spares, state.bays, state.crews, {})


def test_pins_consumed_first_and_resources_reusable_after_end() -> None:
    state = three_tail_state()
    pin = PinnedPlacement('T3', 12, 'B2', 'C1', 'S3')
    result = plan(state, pinned_placements=(pin,))
    by_id = {p.tail_id: p for p in result.placements}
    assert (by_id['T3'].start_day, by_id['T3'].bay, by_id['T3'].spare) == (12, 'B2', 'S3')
    assert by_id['T3'].reason_code.startswith('Pinned placement honoured')
    assert by_id['T2'].start_day == 15 and by_id['T1'].start_day == 18
    assert by_id['T2'].binding == 'crew' and by_id['T2'].status == 'Late'
    assert result.inputs_hash != plan(state).inputs_hash
    assert result == plan(replace(state, tails=state.tails[::-1]), pinned_placements=(pin,))


def test_nonoverlapping_pins_on_shared_resources_are_order_invariant() -> None:
    state = three_tail_state()
    pins = (PinnedPlacement('T2', 1, 'B1', 'C1', 'S1'),
            PinnedPlacement('T1', 4, 'B1', 'C1', 'S2'))
    assert plan(state, pinned_placements=pins) == plan(state, pinned_placements=pins[::-1])
    assert plan(state, pinned_placements=pins).placements[-1].start_day == 12


@pytest.mark.parametrize('pins', [
    (PinnedPlacement('UNKNOWN', 12, 'B1', 'C1', 'S3'),),
    (PinnedPlacement('T3', 11, 'B1', 'C1', 'S3'),),
    (PinnedPlacement('T3', 12, 'UNKNOWN', 'C1', 'S3'),),
    (PinnedPlacement('T3', 12, 'B1', 'UNKNOWN', 'S3'),),
    (PinnedPlacement('T3', 12, 'B1', 'C1', 'UNKNOWN'),),
    (PinnedPlacement('T2', 1, 'B1', 'C1', 'S1'), PinnedPlacement('T1', 2, 'B2', 'C1', 'S2')),
    (PinnedPlacement('T2', 1, 'B1', 'C1', 'S1'), PinnedPlacement('T1', 4, 'B2', 'C1', 'S1')),
    (PinnedPlacement('T2', 1, 'B1', 'C1', 'S1'), PinnedPlacement('T2', 4, 'B2', 'C1', 'S2')),
])
def test_invalid_pins_fail_without_partial_schedule(pins: tuple[PinnedPlacement, ...]) -> None:
    with pytest.raises(ValueError, match='[Pp]in'):
        plan(three_tail_state(), pinned_placements=pins)


def test_dictionary_adapter_and_unplanned_explanation() -> None:
    records = plan_fleet([{'tail_id': 'T1', 'rul_point': 20, 'rate': 2}],
                         [{'spare_id': 'S2', 'available_day': 12}], ['B'], ['C'],
                         {'duration': 3, 'horizon': 20})
    assert records[0]['deadline_day'] == 9 and records[0]['status'] == 'Late'
    assert records[0]['reason_code'] == 'Spare S2 available only on day 12'
    records = plan_fleet([{'tail': 'T1', 'rul_point': 20, 'rate': 2}], [], ['B'], ['C'], {})
    assert records[0]['status'] == 'Unplanned'
    assert 'No unused compatible spare' in records[0]['reason_code']
    with pytest.raises(ValueError, match='Unknown'):
        plan_fleet([{'tail': 'T1', 'rul_point': 20, 'rate': 2, 'secret': 7}], [], ['B'], ['C'], {})


def test_dictionary_pins_and_pinned_status_recalculated() -> None:
    state = three_tail_state()
    records = plan_fleet(state.tails, state.spares, state.bays, state.crews, {},
                        pinned_placements=[{'tail': 'T3', 'start_day': 12,
                                            'bay': 'B2', 'crew': 'C1', 'spare': 'S3'}])
    assert records[-1]['start_day'] == 12
    altered = plan(state, {'T3': 0}, pinned_placements=(PinnedPlacement('T3', 12, 'B2', 'C1', 'S3'),))
    assert altered.placements[0].tail_id == 'T3' and altered.placements[0].status == 'Late'
