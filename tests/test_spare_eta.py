"""Spare ETA witnesses, finite bounds, fleet effects and preserved pins."""
from dataclasses import replace
from unittest.mock import Mock

import pytest

from vayu import margins
from vayu.schemas import PinnedPlacement, PlanningState, Resource, Spare, Tail, canonical_json


def coupled() -> PlanningState:
    """Delaying A's spare first moves both jobs, then makes B Late."""
    return PlanningState((Tail('A', 12, 11, 13, 1, 2),
                          Tail('B', 13, 12, 14, 1, 2, 'OTHER')),
                         (Spare('S1', 10), Spare('S2', 0, 'OTHER')),
                         (Resource('BAY'),), (Resource('CREW'),), safety_buffer=0)


def test_first_plan_change_is_distinct_from_first_late_transition():
    result = margins.spare_eta_float('S1', coupled())
    assert result['float_min'] == 1
    assert result['changed_tails'] == ['A', 'B']
    assert result['late_shift'] == 2 and result['late_tails'] == ['B']
    assert result['what_changed'][0]['before']['start_day'] == 10
    assert result['what_changed'][0]['after']['start_day'] == 11
    assert result['what_changed'][0]['after']['status'] == 'On time'
    assert [row['shift_days'] for row in result['probes']] == [1, 2, 3, 4, 5]
    assert coupled().spares[0].available_day == 10


def test_finite_bound_and_inclusive_fifth_day_boundary():
    state = PlanningState((Tail('A', 9, 8, 10, 1, 2),), (Spare('S', 0),),
                          (Resource('B', 9),), (Resource('C'),), safety_buffer=0)
    unchanged = margins.spare_eta_float('S', state)
    assert unchanged['float_min'] == '> 5 days'
    assert unchanged['late_shift'] is None and unchanged['what_changed'] == []
    boundary = margins.spare_eta_float('S', replace(state, spares=(Spare('S', 5),)))
    assert boundary['float_min'] == boundary['late_shift'] == 5
    assert boundary['late_tails'] == ['A']


def test_shared_cache_reuses_every_probe_and_collection_order():
    spy = Mock(wraps=margins.plan)
    cache = margins.PlannerCache()
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr(margins, 'plan', spy)
        result = margins.spare_eta_float('S1', coupled(), cache=cache)
        assert spy.call_count == 6
        again = margins.spare_eta_float('S1', replace(coupled(),
            tails=coupled().tails[::-1], spares=coupled().spares[::-1]), cache=cache)
        assert canonical_json(result) == canonical_json(again)
        assert spy.call_count == 6


def test_delayed_eta_never_silently_moves_a_pin():
    state = PlanningState((Tail('A', 20, 18, 22, 1, 2),), (Spare('S', 10),),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)
    pins = (PinnedPlacement('A', 11, 'B', 'C', 'S'),)
    result = margins.spare_eta_float('S', state, pinned_placements=pins)
    assert result['float_min'] == 'Pin conflict'
    assert result['blocked_shift'] == 2 and result['changed_tails'] == []
    assert result['probes'][0]['what_changed'] == []
    assert all(row['blocked_reason'] for row in result['probes'][1:])
    assert 'A' in result['blocked_reason'] and '11' in result['blocked_reason']


def test_eta_validation_and_unused_spare():
    with pytest.raises(ValueError, match='Unknown spare'):
        margins.spare_eta_float('absent', coupled())
    for invalid in (-1, True, 1.5):
        with pytest.raises(ValueError):
            margins.spare_eta_float('S1', coupled(), max_delay=invalid)
    state = replace(coupled(), spares=(*coupled().spares, Spare('unused', 30)))
    assert margins.spare_eta_float('unused', state)['float_min'] == '> 5 days'


def test_eta_can_remove_a_spare_at_the_horizon_cutoff():
    state = PlanningState((Tail('A', 8, 7, 9, 1, 2),), (Spare('S', 5),),
                          (Resource('B'),), (Resource('C'),), horizon=5, safety_buffer=0)
    result = margins.spare_eta_float('S', state)
    assert result['float_min'] == 1
    assert result['what_changed'][0]['after']['status'] == 'Unplanned'
    assert result['late_shift'] is None  # Unplanned is not a Late transition.


def test_demo_summaries_are_computed_and_byte_reproducible(tmp_path):
    import json
    from scripts.whatif_demo import write_demo_summaries
    from vayu.sim import generate_whatif_demo
    pack = tmp_path/'pack'
    generate_whatif_demo(pack)
    write_demo_summaries(pack, tmp_path/'one')
    write_demo_summaries(pack, tmp_path/'two')
    for name in ('greedy_summary.json', 'float_summary.json'):
        assert (tmp_path/'one'/name).read_bytes() == (tmp_path/'two'/name).read_bytes()
    greedy = json.loads((tmp_path/'one/greedy_summary.json').read_text())
    floats = json.loads((tmp_path/'one/float_summary.json').read_text())
    assert 'fictional' in greedy['data_label'].lower()
    focal = next(row for row in greedy['plan']['placements'] if row['tail_id'] == 'T-04')
    attention = next(row for row in floats['tails'] if row['tail'] == 'T-04')
    assert focal['spare'] == 'S2' and attention['label'] == 'Fragile'
    assert floats['spare_eta'][1]['spare'] == 'S2'
