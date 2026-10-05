"""Scenario comparisons change one named resource and preserve the original."""
from dataclasses import asdict
import pytest

from vayu.schemas import Tail, Spare, Resource, PlanningState
from vayu.whatif import apply_change, compare


def state():
    return PlanningState((Tail('A',8,6,10,1,3),),(Spare('S',10),),
                         (Resource('B'),),(Resource('C'),),safety_buffer=0)


def test_spare_intervention_and_nonbinding_control():
    s = state()
    changed = apply_change(s,'spare','S',0)
    before,after = asdict(s),asdict(changed)
    assert [k for k in before if before[k] != after[k]] == ['spares']
    result = compare(s,'spare','S',0)
    assert result.changed_tails == ('A',)
    assert result.before.placements[0].status == 'Late'
    assert result.after.placements[0].status == 'On time'
    assert compare(s,'bay','B',0).changed_tails == ()
    assert s.spares[0].available_day == 10


@pytest.mark.parametrize('kind,target,day', [('spare','BAD',0),('anything','S',0),
                                           ('spare','S',-1),('spare','S',1.5)])
def test_invalid_change(kind,target,day):
    with pytest.raises(ValueError):
        apply_change(state(),kind,target,day)
