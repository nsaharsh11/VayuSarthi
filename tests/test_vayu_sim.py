"""Synthetic-only simulation accounting and deterministic logs."""
from vayu.schemas import Tail, Spare, Resource, PlanningState, canonical_json
from vayu.planner import plan
from vayu.sim import simulate


def test_hand_computed_operating_maintenance_and_failure():
    s = PlanningState((Tail('A',8,6,10,1,2),),(Spare('S',2),),
                      (Resource('B'),),(Resource('C'),),horizon=6,safety_buffer=0)
    scheduled = plan(s)
    healthy = simulate(s,scheduled,{'A':5})
    assert healthy['metrics']['operating_tail_days'] == 4
    assert healthy['metrics']['planned_maint_days'] == 2
    assert healthy['metrics']['aog_days'] == 0
    failed = simulate(s,scheduled,{'A':1})
    assert failed['metrics']['operating_tail_days'] == 3
    assert failed['metrics']['aog_days'] == 3
    assert failed['metrics']['planned_maint_days'] == 0
    assert failed['metrics']['unplanned_failures'] == 1


def test_accounting_and_determinism_for_seeded_cases():
    import numpy as np
    for seed in range(25):
        rng = np.random.default_rng(seed)
        s = PlanningState(tuple(Tail(f'T{i}',10,5,15,float(rng.choice([.5,1.,2.])),3) for i in range(5)),
                          tuple(Spare(f'S{i}',int(rng.integers(0,20))) for i in range(3)),
                          (Resource('B'),),(Resource('C'),),horizon=20)
        remaining = {t.tail_id:float(rng.integers(1,15)) for t in s.tails}
        a,b = simulate(s,plan(s),remaining),simulate(s,plan(s),remaining)
        assert canonical_json(a) == canonical_json(b)
        m = a['metrics']
        assert m['operating_tail_days']+m['planned_maint_days']+m['aog_days'] == 100
        assert 0 <= m['availability'] <= 1


def test_simulation_requires_complete_evaluation_values():
    import pytest
    s = PlanningState((Tail('A',8,6,10,1,2),),(),(Resource('B'),),(Resource('C'),))
    with pytest.raises(ValueError):
        simulate(s,plan(s),{})
