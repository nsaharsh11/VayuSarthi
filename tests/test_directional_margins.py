"""Directional float witnesses, frozen slack, cache correctness and timing."""
from dataclasses import replace
from unittest.mock import Mock

import pytest

import vayu.margins as margins
from vayu.planner import plan
from vayu.schemas import PinnedPlacement, PlanningState, Resource, Spare, Tail, canonical_json


def ample() -> PlanningState:
    """A fictional tail with slack comfortably beyond the tested search bound."""
    return PlanningState((Tail('A', 100, 95, 105, 1, 3),), (Spare('S', 0),),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)


def six() -> PlanningState:
    """Start is day 15 at rate 2: point 35 crosses Late first at delta -6."""
    return PlanningState((Tail('A', 35, 30, 40, 2, 3),), (Spare('S', 15),),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)


def test_frozen_slack_worked_example_makes_zero_planner_calls(monkeypatch) -> None:
    state = replace(ample(), tails=(Tail('A', 40, 35, 45, 2, 3),), today=5,
                    spares=(Spare('S', 17),))
    frozen = plan(state)
    forbidden = Mock(side_effect=AssertionError('Slack must never replan'))
    monkeypatch.setattr(margins, 'plan', forbidden)
    assert margins.deadline_slack(frozen, state.tails, today=5, safety_buffer=0) == {'A': 16}
    assert margins.deadline_slack(state, state.tails[0], frozen.placements[0]) == 16
    assert forbidden.call_count == 0


def test_directional_none_and_six_cycle_witness() -> None:
    bound = margins.decision_float('A', ample(), R=20)
    assert bound == {'float_down': '> 20', 'float_up': '> 20', 'float_min': '> 20',
                     'direction': None, 'what_changed': {'down': [], 'up': []}}
    value = margins.decision_float('A', six(), R=10)
    assert (value['float_down'], value['float_up'], value['float_min'], value['direction']) == (
        6, '> 10', 6, 'down')
    change = value['what_changed']['down'][0]
    assert change['tail'] == 'A' and change['fields'] == ['status']
    assert change['before']['status'] == 'On time' and change['after']['status'] == 'Late'
    assert canonical_json(value) == canonical_json(margins.decision_float('A', six(), R=10))


def test_no_compatible_spare_shortcut_matches_exhaustive_fleet_replanning(monkeypatch):
    """An unschedulable tail cannot reorder or consume another tail's resources."""
    state = PlanningState((Tail('A', 5, 3, 7, 1, 3, 'UNAVAILABLE'),
                           Tail('B', 5, 3, 7, 1, 3)),
                          (Spare('SB', 0), Spare('SA', 50, 'UNAVAILABLE')),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)
    baseline = plan(state)
    for delta in range(-10, 11):
        assert margins.changed_tails(baseline, plan(state, {'A': 5 + delta})) == ()
    spy = Mock(wraps=margins.plan)
    monkeypatch.setattr(margins, 'plan', spy)
    result = margins.decision_float('A', state, R=10, cache=margins.PlannerCache())
    assert result['float_min'] == result['float_down'] == result['float_up'] == '> 10'
    assert spy.call_count == 1


def test_bounded_spare_exhaustion_proof_and_its_priority_boundary(monkeypatch):
    state = PlanningState((Tail('A', 100, 90, 110, 1, 2), Tail('B', 1, 0, 2, 1, 2),
                           Tail('C', 2, 1, 3, 1, 2)), (Spare('S', 0),),
                          (Resource('BAY'),), (Resource('CREW'),), safety_buffer=0)
    baseline = plan(state)
    for delta in range(-10, 11):
        assert margins.changed_tails(baseline, plan(state, {'A': 100 + delta})) == ()
    spy = Mock(wraps=margins.plan)
    monkeypatch.setattr(margins, 'plan', spy)
    result = margins.decision_float('A', state, R=10, cache=margins.PlannerCache())
    assert result['float_min'] == '> 10' and spy.call_count == 1
    # A ties B at point 1, wins by tail ID, and takes the spare: do not shortcut.
    boundary = margins.decision_float('A', state, R=100, cache=margins.PlannerCache())
    assert boundary['float_down'] == boundary['float_min'] == 99
    assert [row['tail'] for row in boundary['what_changed']['down']] == ['A', 'B']


def test_optimized_float_matches_exhaustive_integer_probes_on_seeded_fleets():
    """Independent whole-plan probes cover ordering, status, parts and pins."""
    import numpy as np
    rng = np.random.default_rng(426)
    for case in range(24):
        tails = tuple(Tail(str(i), float(point), max(0., float(point)-2), float(point)+2,
                           float(rng.choice([1.5, 2., 3.])), int(rng.integers(1, 4)),
                           'OTHER' if i == 2 else 'PN-ENG-A')
                      for i, point in enumerate(rng.integers(0, 40, size=3)))
        state = PlanningState(tails, (Spare('S1', 0), Spare('S2', int(rng.integers(0, 10))),
                                      Spare('S3', 0, 'OTHER')),
                              (Resource('B'),), (Resource('C'),), safety_buffer=0)
        pins = (PinnedPlacement('2', 1, 'B', 'C', 'S3'),) if case % 2 else ()
        baseline = plan(state, pinned_placements=pins)
        for tail in tails:
            expected = {}
            for sign, direction in ((-1, 'down'), (1, 'up')):
                for magnitude in range(1, 10):
                    probe = plan(state, {tail.tail_id: tail.rul_point+sign*magnitude}, pins)
                    if margins.changed_tails(baseline, probe):
                        expected[direction] = magnitude
                        break
            result = margins.decision_float(tail.tail_id, state, R=9,
                                           pinned_placements=pins, cache=margins.PlannerCache())
            assert result['float_down'] == expected.get('down', '> 9')
            assert result['float_up'] == expected.get('up', '> 9')
            expected_min = min(expected.values()) if expected else '> 9'
            assert result['float_min'] == expected_min


def test_stable_order_region_is_reused_until_the_exact_status_boundary(monkeypatch):
    state = PlanningState((Tail('A', 30, 28, 32, 3, 2), Tail('B', 60, 58, 62, 2, 2)),
                          (Spare('S1', 0), Spare('S2', 0)),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)
    spy = Mock(wraps=margins.plan)
    monkeypatch.setattr(margins, 'plan', spy)
    result = margins.decision_float('A', state, R=40, cache=margins.PlannerCache())
    assert result['float_down'] == result['float_min'] == 28
    assert result['float_up'] == '> 40'
    assert result['what_changed']['down'][0]['fields'] == ['status']
    assert spy.call_count == 2  # Original plan plus the witnessed Late boundary.


def test_directional_upper_threshold_and_changes_on_other_tails() -> None:
    state = PlanningState((Tail('A', 5, 3, 7, 1, 3), Tail('B', 5, 3, 7, 1, 3)),
                          (Spare('S1', 0), Spare('S2', 0)),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)
    result = margins.decision_float('A', state, R=8)
    assert result['float_up'] == 1 and result['float_down'] == 5
    assert result['direction'] == 'up'
    assert [row['tail'] for row in result['what_changed']['up']] == ['A', 'B']


def test_cache_reuses_whole_plans_and_separates_changed_inputs(monkeypatch) -> None:
    spy = Mock(wraps=margins.plan)
    monkeypatch.setattr(margins, 'plan', spy)
    cache = margins.PlannerCache(max_size=100)
    first = margins.decision_float('A', ample(), R=4, cache=cache)
    calls = spy.call_count
    assert calls >= 1
    assert first == margins.decision_float('A', ample(), R=4, cache=cache)
    assert spy.call_count == calls
    margins.decision_float('A', replace(ample(), today=1), R=4, cache=cache)
    assert spy.call_count > calls
    assert cache.hits >= 1
    cache.clear()
    assert cache.hits == cache.misses == 0
    calls = spy.call_count
    margins.decision_float('A', ample(), R=4, cache=cache)
    assert spy.call_count > calls


def test_cache_canonicalises_collection_order_and_tracks_pins(monkeypatch) -> None:
    state = replace(ample(), spares=(Spare('S', 0), Spare('S2', 0)))
    spy = Mock(wraps=margins.plan)
    monkeypatch.setattr(margins, 'plan', spy)
    cache = margins.PlannerCache(max_size=100)
    margins.decision_float('A', state, R=2, cache=cache)
    calls = spy.call_count
    margins.decision_float('A', replace(state, spares=state.spares[::-1]), R=2, cache=cache)
    assert spy.call_count == calls
    pins = (PinnedPlacement('A', 12, 'B', 'C', 'S'),)
    pinned = margins.decision_float('A', state, R=2, cache=cache, pinned_placements=pins)
    assert spy.call_count > calls and pinned['float_min'] == '> 2'


def test_label_uses_minimum_slack_half_width_and_finite_bound() -> None:
    assert margins.label({'half_width': 6, 'float_min': 6, 'deadline_slack': 6}) == 'Covered'
    assert margins.label({'half_width': 6, 'float_min': 5, 'deadline_slack': 100}) == 'Fragile'
    assert margins.label({'lower': 0, 'upper': 12, 'float_min': '> 6', 'slack': 6}) == 'Covered'
    assert margins.label({'half_width': 6, 'float_min': '> 5', 'slack': 100}) == 'Fragile'
    assert margins.label({'half_width': 0, 'float_min': '> 5', 'slack': None}) == 'Fragile'
    with pytest.raises(ValueError):
        margins.label({'half_width': 1, 'float_min': float('inf'), 'slack': 5})


def test_full_fleet_timing_is_measured_not_embedded(capsys, monkeypatch) -> None:
    times = iter([10., 10.25])
    monkeypatch.setattr(margins, 'perf_counter', lambda: next(times))
    result = margins.full_fleet_sweep(ample(), R=4, cache=margins.PlannerCache())
    assert result['A']['float_min'] == '> 4'
    assert '0.250000 s' in capsys.readouterr().out
    assert 'runtime' not in result['A']


def test_mapping_interfaces_and_zero_radius() -> None:
    tails = [{'tail': 'A', 'rul_point': 35, 'lower': 30, 'upper': 40, 'rate': 2}]
    result = margins.decision_float('A', tails, spares=[{'spare_id': 'S', 'available_day': 15}],
                                   bays=['B'], crews=['C'], config={'safety_buffer': 0}, R=10)
    assert result['float_min'] == 6
    frozen = [{'tail': 'A', 'start_day': 12}]
    assert margins.deadline_slack(frozen, [{'tail': 'A', 'rul_point': 40, 'rate': 2}]) == {'A': 16}
    assert margins.decision_float('A', ample(), R=0)['float_min'] == '> 0'
    with pytest.raises(ValueError):
        margins.decision_float('MISSING', ample(), R=2)
    with pytest.raises(ValueError):
        margins.deadline_slack([], ample().tails)
