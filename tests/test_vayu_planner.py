"""Hand-computed scheduler rules and resource reservation invariants."""
from dataclasses import replace
from pathlib import Path
import re

import numpy as np
import pytest

from vayu.schemas import Tail, Spare, Resource, PlanningState, canonical_json
from vayu.planner import plan, deadline_day, decision_signature


def state(tails=None, spares=None, bays=None, crews=None, **kwargs):
    return PlanningState(tuple(tails or [Tail('A',10,8,12,1,3)]),
                         tuple(spares if spares is not None else [Spare('S1',0),Spare('S2',0)]),
                         tuple(bays or [Resource('B')]),tuple(crews or [Resource('C')]),**kwargs)


@pytest.mark.parametrize('point,buffer,rate,expected', [(10,2,1,8),(10,2,2,4),(7.5,2,2,2),
                                                       (0,2,1,-2),(1,0,1,1),(10,1,1.5,6)])
def test_deadline_exact(point,buffer,rate,expected):
    assert deadline_day(point,buffer,rate) == expected


def test_sequential_capacity_and_id_order():
    input_state = state(tails=[Tail('B',10,8,12,1,3),Tail('A',10,8,12,1,3)])
    result = plan(input_state)
    a,b = result.placements
    assert (a.tail_id,a.start_day,a.end_day,a.spare,a.status,a.binding) == ('A',1,4,'S1','On time',None)
    assert (b.tail_id,b.start_day,b.end_day,b.spare,b.binding) == ('B',4,7,'S2','bay')
    assert canonical_json(result) == canonical_json(plan(replace(input_state,tails=input_state.tails[::-1],spares=input_state.spares[::-1])))


@pytest.mark.parametrize('spare,bay,crew,binding', [(10,0,0,'spare'),(0,10,0,'bay'),
                                                 (0,0,10,'crew'),(10,10,10,'spare')])
def test_binding(spare,bay,crew,binding):
    result = plan(state(spares=[Spare('S',spare)],bays=[Resource('B',bay)],crews=[Resource('C',crew)]))
    assert result.placements[0].binding == binding
    assert result.placements[0].start_day == 10
    assert result.placements[0].status == 'Late'


def test_no_spare_compatible_or_within_horizon():
    for spares in ([],[Spare('S',41)],[Spare('S',0,'OTHER')]):
        p = plan(state(spares=spares)).placements[0]
        assert p.status == 'Unplanned' and p.start_day is None and p.bay is None
    assert plan(state(spares=[Spare('S',40)])).placements[0].start_day == 40


def test_nonzero_today_has_no_deadline_offset():
    p = plan(state(today=5)).placements[0]
    assert p.deadline_day == 8 and p.start_day == 6


def test_point_override_can_cross_zero_without_creating_new_estimate():
    input_state = state()
    result = plan(input_state,{'A':-2})
    assert result.placements[0].deadline_day == -4
    assert input_state.tails[0].rul_point == 10
    with pytest.raises(ValueError):
        plan(input_state,{'UNKNOWN':2})
    with pytest.raises(ValueError):
        plan(input_state,{'A':float('nan')})


def test_signature_excludes_crew_deadline_and_binding():
    first = plan(state())
    changed = replace(first,placements=(replace(first.placements[0],crew='C2',deadline_day=99,binding='crew'),))
    assert decision_signature(first) == decision_signature(changed)


def test_resource_invariants_over_seeded_fleets():
    for seed in range(30):
        rng = np.random.default_rng(seed)
        tails = [Tail(f'T{i}',float(p),0,float(p+5),float(rng.choice([.5,1.,2.])),int(rng.integers(1,5)))
                 for i,p in enumerate(rng.integers(0,50,10))]
        spares = [Spare(f'S{i}',int(d)) for i,d in enumerate(rng.integers(0,41,10))]
        result = plan(state(tails,spares,[Resource('B1'),Resource('B2')],[Resource('C1'),Resource('C2')]))
        assert len({p.spare for p in result.placements}) == len(result.placements)
        for i,p in enumerate(result.placements):
            assert p.start_day >= 1 and p.end_day-p.start_day == next(t.duration for t in tails if t.tail_id == p.tail_id)
            assert p.status == ('On time' if p.start_day <= p.deadline_day else 'Late')
            for q in result.placements[i+1:]:
                if p.bay == q.bay or p.crew == q.crew:
                    assert p.end_day <= q.start_day or q.end_day <= p.start_day


def test_active_planner_ground_truth_firewall():
    source = (Path(__file__).resolve().parents[1]/'vayu/planner.py').read_text()
    assert not re.search(r'true_rul|failure_cycle|simulation_truth|scenario\.truth|read_csv|sqlite|open\(',source)
