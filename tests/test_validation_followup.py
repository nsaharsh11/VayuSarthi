"""Forward interval scheduling, intervention control and wide paired exports."""
from dataclasses import replace

import numpy as np
import pandas as pd

from vayu.schemas import PlanningState, Resource, Spare, Tail
from vayu.sim import (MonteCarloScenario, SimulationConfig, monte_carlo,
                      run_policy, validation_cell_rows)


def helpful_state() -> PlanningState:
    return PlanningState((Tail('A',20,18,22,2,2),),(Spare('S',12),),
                         (Resource('B'),),(Resource('C'),),horizon=21,safety_buffer=0)


def test_b1_preplans_future_due_date_without_grounding_healthy_wait():
    state = PlanningState((Tail('A',80,75,85,1,2),),(Spare('S',8),),
                         (Resource('B'),),(Resource('C'),),horizon=15,safety_buffer=3)
    draw = MonteCarloScenario(0,(('A',100.),),(('S',0),))
    outcome = run_policy(state,draw,'B1',{'A':90},SimulationConfig(fixed_interval_cycles=100))
    proposal = next(e for e in outcome.events if e['event'] == 'PROPOSED')
    start = next(e for e in outcome.events if e['event'] == 'STARTED')
    assert proposal['day'] == 0 and proposal['deadline_day'] == 10
    assert start['day'] == 8 and start['end_day'] == 10
    assert outcome.metrics['aog_days'] == 2 and outcome.metrics['waiting_spare_days'] == 0
    assert outcome.metrics['inductions_before_due'] == 1
    assert not any(e['event'] == 'GROUNDED' for e in outcome.events)
    # Health estimates do not set B1's interval deadline.
    alternate = replace(state,tails=(replace(state.tails[0],rul_point=30,lower=25,upper=35),))
    other = run_policy(alternate,draw,'B1',{'A':90},SimulationConfig(fixed_interval_cycles=100))
    assert other.metrics == outcome.metrics


def test_k0_control_uses_the_same_planner_and_no_intervention():
    state = helpful_state()
    draw = MonteCarloScenario(0,(('A',100.),),(('S',0),))
    config = SimulationConfig()
    control = run_policy(state,draw,'B2-K0',{'A':0},config)
    disabled = run_policy(state,draw,'B2',{'A':0},replace(config,weekly_budget=0))
    treated = run_policy(state,draw,'B2',{'A':0},config)
    assert control.metrics == disabled.metrics
    assert control.metrics['intervention_man_hours'] == control.metrics['unused_weeks'] == 0
    assert all(w['budget'] == 0 and not w['action_ids'] for w in control.weeks)
    assert treated.metrics['intervention_man_hours'] > 0
    assert treated.metrics['aog_days'] < control.metrics['aog_days']


def test_b1_leaves_intervals_outside_the_horizon_flying():
    state = PlanningState((Tail('A',80,75,85,1,2),),(Spare('S',0),),
                         (Resource('B'),),(Resource('C'),),horizon=5,safety_buffer=0)
    draw = MonteCarloScenario(0,(('A',100.),),(('S',0),))
    outcome = run_policy(state,draw,'B1',{'A':90},SimulationConfig(fixed_interval_cycles=100))
    assert outcome.metrics['aog_days'] == outcome.metrics['maintenance_days'] == 0
    assert not any(e['event'] in ('PROPOSED','GROUNDED','STARTED') for e in outcome.events)


def test_wide_export_pairs_use_scenario_differences_and_exact_ties():
    config = SimulationConfig(n_scenarios=5,bootstrap_samples=50)
    result = monte_carlo(helpful_state(),[-5.,0.,5.],{'A':0},config)
    report = validation_cell_rows(result,config,'benign',2.)
    assert not report.duplicated(['stress_level','repair_multiplier','policy']).any()
    assert 'metric' not in report and len(report) == 12
    for left,right in [('B4','B3'),('B3','B2'),('B4b','B3'),('B2','B2-K0')]:
        row = report.set_index('policy').loc[f'{left}-{right}']
        wide = result.runs.pivot(index='scenario_id',columns='policy',values='aog_days')
        differences = wide[left]-wide[right]
        assert row.aog_days_mean == differences.mean()
        assert row.aog_days_ties == (differences == 0).sum()
        assert row.aog_days_ties_over_n == f'{(differences == 0).sum()}/{config.n_scenarios}'
        rng = np.random.default_rng(config.bootstrap_seed)
        indices = rng.integers(config.n_scenarios,size=(config.bootstrap_samples,config.n_scenarios))
        low,high = np.quantile(differences.to_numpy()[indices].mean(axis=1),[.025,.975])
        assert (row.aog_days_ci_low,row.aog_days_ci_high) == (low,high)
    controls = report.query("policy == 'B2-K0'").iloc[0]
    assert controls.expedite_spare_count == controls.add_bay_count == controls.add_crew_shift_count == 0
    assert report.query("policy == 'B2'").iloc[0].expedite_spare_count > 0


def test_opportunity_diagnostics_measure_multicandidates_and_any_choice_difference():
    from vayu.sim import opportunity_diagnostics
    weeks = pd.DataFrame([{'scenario_id':0,'week':week,'policy':policy,'candidates':candidates,
                          'tail':tail,'action_types':actions}
        for week,candidates,choices in [(0,['A','B'],('A','B','B')),(1,[],(None,None,None))]
        for policy,tail,actions in zip(('B2','B3','B4'),choices,
                                     (['expedite_spare'],[],['add_crew_shift']) if week == 0 else ([],[],[]))])
    diagnostics = opportunity_diagnostics(weeks).set_index('policy')
    assert diagnostics.multi_candidate_share.eq(.5).all()
    assert diagnostics.b2_b3_b4_different_tail_share.eq(.5).all()
    assert diagnostics.loc['B2','expedite_spare_count'] == 1
    assert diagnostics.loc['B4','add_crew_shift_count'] == 1
    assert diagnostics.loc['B3','add_bay_count'] == 0


def test_resume_reuses_only_unchanged_policies_with_matching_inputs(monkeypatch):
    import vayu.sim as sim
    import pytest
    config = SimulationConfig(n_scenarios=3,bootstrap_samples=20)
    state = helpful_state()
    first = monte_carlo(state,[-2.,0.,2.],{'A':0},config)
    evaluated = []
    original = sim.run_policy
    def counted(*args, **kwargs):
        evaluated.append(args[2])
        return original(*args, **kwargs)
    monkeypatch.setattr(sim,'run_policy',counted)
    resumed = monte_carlo(state,[-2.,0.,2.],{'A':0},config,unchanged=first)
    assert evaluated == ['B1','B2-K0'] * config.n_scenarios
    pd.testing.assert_frame_equal(first.runs,resumed.runs)
    pd.testing.assert_frame_equal(first.weeks,resumed.weeks)
    pd.testing.assert_frame_equal(first.summary,resumed.summary)
    with pytest.raises(ValueError,match='archive'):
        monte_carlo(state,[-2.,0.,2.],{'A':0},replace(config,seed=1),unchanged=first)
