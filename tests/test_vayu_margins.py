"""Both-sign float search must observe fleet effects and freeze slack."""
from dataclasses import replace
import pytest

from vayu.schemas import Tail, Spare, Resource, PlanningState
from vayu.planner import plan
from vayu.margins import decision_float, deadline_slack, analyze, sweep


def state(tails, **kwargs):
    return PlanningState(tuple(tails),(Spare('S1',0),Spare('S2',0)),
                         (Resource('B'),),(Resource('C'),),safety_buffer=0,**kwargs)


def test_positive_sign_can_be_first_ordering_boundary():
    s = state([Tail('A',5,3,7,1,3),Tail('B',5,3,7,1,3)])
    value = decision_float(s,'A',10)
    assert value.value == 1 and value.delta == 1
    assert value.changed_tails == ('A','B')


def test_negative_sign_and_status_only_change():
    s = state([Tail('A',1,0,2,1,3)])
    value = decision_float(s,'A',10)
    assert value.value == 1 and value.delta == -1 and value.changed_tails == ('A',)


def test_full_fleet_changes_even_when_focal_signature_unchanged():
    # A stays Late at start 10 on its unique spare; swapping order delays B.
    s = replace(state([Tail('A',8,6,10,1,3),Tail('B',7,5,9,1,3,'OTHER')]),
                spares=(Spare('S1',10),Spare('S2',0,'OTHER')))
    value = decision_float(s,'A',5)
    assert value.value == 1 and value.delta == -1
    assert value.changed_tails == ('B',)


def test_no_change_reports_bound_and_conservative_label():
    s = state([Tail('A',100,95,105,1,3)])
    value = decision_float(s,'A',3)
    assert value.value is None and value.display == '> 3'
    assert analyze(s,3)[0].label == 'Fragile'
    assert analyze(s,10)[0].label == 'Covered'


def test_slack_uses_frozen_placement_and_cycles():
    s = state([Tail('A',10,8,12,2,3)],today=2)
    p = plan(s).placements[0]
    assert deadline_slack(s,s.tails[0],p) == 8
    assert p.start_day == 3
    # Half-width equality is Covered, ordinary negative slack is Fragile.
    equality = state([Tail('A',2,1,3,1,3)])
    assert analyze(equality,5)[0].label == 'Covered'
    late = state([Tail('A',0,0,2,1,3)])
    assert analyze(late,5)[0].label == 'Fragile'


def test_unplanned_is_fragile_without_infinite_slack():
    s = replace(state([Tail('A',10,8,12,1,3)]),spares=())
    result = analyze(s,40)[0]
    assert result.slack is None and result.label == 'Fragile'
    assert result.float_result.display == '> 40'


def test_sweep_reruns_and_validation():
    s = state([Tail('A',5,3,7,1,3),Tail('B',5,3,7,1,3)])
    rows = sweep(s,'A',2)
    assert [row['delta'] for row in rows] == [-2,-1,0,1,2]
    assert rows[3]['changed_tails'] == ('A','B')
    with pytest.raises(ValueError):
        decision_float(s,'NO',3)
    with pytest.raises(ValueError):
        decision_float(s,'A',-1)
