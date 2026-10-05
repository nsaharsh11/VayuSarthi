"""Paired offline Monte Carlo, observable-only policies and shared action budgets."""
from dataclasses import replace
import inspect
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from vayu.schemas import PlanningState, Resource, Spare, Tail, canonical_json
from vayu.sim import (SimulationConfig, MonteCarloScenario, draw_scenarios,
                      run_policy, monte_carlo, bootstrap_summary, select_tail,
                      calibration_residuals, write_validation, POLICY_NAMES)


def fleet(horizon=6):
    return PlanningState((Tail('A',8,6,10,1,2),),(Spare('S',0),),
                         (Resource('B'),),(Resource('C'),),horizon=horizon,safety_buffer=0)


def scenario(remaining=5, delay=0):
    return MonteCarloScenario(0, (('A', float(remaining)),), (('S', delay),))


def test_exact_drawing_and_common_scenarios():
    config = SimulationConfig(n_scenarios=200, seed=12, bootstrap_samples=50)
    state = fleet()
    draws = draw_scenarios(state, [-10., 3.], config)
    assert len(draws) == 200 and draws == draw_scenarios(state, [-10., 3.], config)
    assert {dict(s.true_rul)['A'] for s in draws} == {-2., 11.}
    assert all(0 <= dict(s.spare_delays)['S'] <= config.max_spare_delay for s in draws)
    assert draws != draw_scenarios(state, [-10., 3.], replace(config, seed=13))
    with pytest.raises(ValueError):
        draw_scenarios(state, [np.nan], config)


def test_hand_computed_aog_and_wasted_life():
    config = SimulationConfig(weekly_budget=0, bootstrap_samples=50)
    healthy = run_policy(fleet(), scenario(), 'B2', {'A':0}, config)
    assert healthy.metrics['aog_days'] == 2  # Planned maintenance also unserviceable.
    assert healthy.metrics['unplanned_failures'] == 0
    assert healthy.metrics['wasted_life_cycles'] == 4
    reactive = run_policy(fleet(), scenario(1), 'B0', {'A':0}, config)
    assert reactive.metrics['aog_days'] == 5  # One day waiting plus four-day failure repair.
    assert reactive.metrics['unplanned_failures'] == 1
    assert reactive.metrics['wasted_life_cycles'] == 0
    assert all(event['cause'] for event in reactive.events if event['event'] == 'REPLAN')
    absent = run_policy(replace(fleet(), spares=()), MonteCarloScenario(0, (('A',1.),), ()),
                        'B0', {'A':0}, config)
    assert absent.metrics['aog_days'] == 5
    initial = run_policy(fleet(), scenario(-2), 'B0', {'A':0}, config)
    assert initial.metrics['unplanned_failures'] == 1 and initial.metrics['aog_days'] == 5


@pytest.mark.parametrize('policy',['B2','B3','B4'])
def test_helpful_action_is_used_and_week_trace_explains_selection(policy):
    state = PlanningState((Tail('A',20,18,22,2,2),),(Spare('S',12),),
                         (Resource('B'),),(Resource('C'),),horizon=21,safety_buffer=0)
    outcome = run_policy(state,scenario(100),policy,{'A':0},SimulationConfig())
    week = outcome.weeks[0]
    assert week['fragile_tails'] == ['A'] and week['tail'] == 'A'
    assert week['top_action'] == 'EXPEDITE:S' and week['top_benefit'] > 0
    assert week['interventions'] == 1 and week['man_hours'] > 0 and not week['unused']


def test_failure_waits_for_spare_resources_and_longer_repair_then_replans():
    state = replace(fleet(horizon=14),spares=(Spare('S',5),),
                    bays=(Resource('B',7),),crews=(Resource('C',8),))
    config = SimulationConfig(weekly_budget=0,bootstrap_samples=50)
    for policy in ('B0','B1','B2','B3','B4'):
        outcome = run_policy(state,scenario(1),policy,{'A':0},config)
        assert outcome.metrics['aog_days'] == 11  # Grounded [1,8), repair [8,12).
        assert outcome.metrics['waiting_spare_days'] == 4
        assert outcome.metrics['waiting_bay_days'] == 2
        assert outcome.metrics['waiting_crew_days'] == 1
        assert outcome.metrics['maintenance_days'] == 4
        start = next(e for e in outcome.events if e['event'] == 'STARTED')
        assert (start['day'],start['end_day']) == (8,12)
        assert any(e['event'] == 'REPLAN' and e['day'] == 1 and 'failure' in e['cause'].lower()
                   for e in outcome.events)


@pytest.mark.parametrize('policy', list(POLICY_NAMES))
@pytest.mark.parametrize('missing', ['spare', 'bay', 'crew'])
def test_failed_repair_cannot_start_without_all_three_resources(policy, missing):
    """Withhold each resource independently: a failure must wait, not start."""
    state = fleet(horizon=14)
    unavailable = state.horizon + 1
    if missing == 'spare':
        state = replace(state, spares=(Spare('S', unavailable),))
    elif missing == 'bay':
        state = replace(state, bays=(Resource('B', unavailable),))
    else:
        state = replace(state, crews=(Resource('C', unavailable),))
    outcome = run_policy(state, scenario(1), policy, {'A': 0},
                         SimulationConfig(weekly_budget=0))
    assert outcome.metrics['unplanned_failures'] == 1
    assert not any(event['event'] == 'STARTED' for event in outcome.events)
    assert outcome.metrics['maintenance_days'] == 0
    assert outcome.metrics['aog_days'] == state.horizon - 1


def test_stress_levels_frozen_common_inputs_and_use_budget():
    from vayu.sim import STRESS_LEVELS, stress_inputs
    from vayu.quality import read_fleet_pack, planning_state_from_fleet
    from vayu.rul import predict_tail
    root = Path(__file__).resolve().parents[1]
    pack = read_fleet_pack(root/'data/fleet')
    base = planning_state_from_fleet(pack,{e:predict_tail(e) for e in pack.accepted['tails.csv'].engine_id},safety_buffer=0)
    assert [(s.name,s.bay_count,s.crew_count,s.eta_multiplier,s.max_spare_delay,s.residual_scale)
            for s in STRESS_LEVELS] == [('benign',3,2,1,2,.5),('moderate',2,1,2,7,1.),('stressed',1,1,5,21,2.)]
    state,config = stress_inputs(base,STRESS_LEVELS[-1],SimulationConfig(n_scenarios=3,bootstrap_samples=50))
    result = monte_carlo(state,[-1.,0.,1.],{t.tail_id:0 for t in state.tails},config)
    for policy in ('B2','B3','B4'):
        subset = result.runs[result.runs.policy == policy]
        assert subset.intervention_man_hours.gt(0).all()
        assert subset.unused_weeks.lt(6).all()
    assert len(state.bays) == len(state.crews) == 1


def test_fixed_interval_uses_technical_age_and_no_interventions():
    config = SimulationConfig(fixed_interval_cycles=100, bootstrap_samples=50)
    young = run_policy(fleet(), scenario(100), 'B1', {'A':0}, config)
    due = run_policy(fleet(), scenario(100), 'B1', {'A':100}, config)
    assert young.metrics['aog_days'] == 0 and due.metrics['aog_days'] == 3
    assert due.metrics['intervention_man_hours'] == 0
    assert all(row['man_hours'] == 0 and row['budget'] == 0 for row in due.weeks)


def test_grounding_stops_cycles_and_new_failures_at_exact_deadline():
    state = PlanningState((Tail('A',3,2,4,2,2),),(Spare('S',8),),
                         (Resource('B'),),(Resource('C'),),horizon=12,safety_buffer=0)
    outcome = run_policy(state,scenario(2.1),'B2',{'A':0},SimulationConfig(weekly_budget=0))
    assert outcome.metrics['unplanned_failures'] == 0
    assert outcome.metrics['aog_days'] == 9  # Ground [1,8), maintenance [8,10).
    assert outcome.metrics['wasted_life_cycles'] == pytest.approx(.1)
    assert next(e['day'] for e in outcome.events if e['event'] == 'GROUNDED') == 1
    assert outcome.metrics['aog_days'] == sum(outcome.metrics[k] for k in
        ('waiting_spare_days','waiting_bay_days','waiting_crew_days','waiting_slot_days','maintenance_days'))


def test_failure_on_previously_planned_start_extends_occupied_resources():
    state = PlanningState((Tail('A',10,9,11,1,2),Tail('B',20,19,21,1,2)),
        (Spare('SA',0),Spare('SB',0)),(Resource('BAY'),),(Resource('CREW'),),horizon=10,safety_buffer=0)
    draw = MonteCarloScenario(0,(('A',1.),('B',100.)),(('SA',0),('SB',0)))
    outcome = run_policy(state,draw,'B2',{'A':0,'B':0},SimulationConfig(weekly_budget=0))
    starts = [e for e in outcome.events if e['event'] == 'STARTED']
    assert [(e['tail'],e['day'],e['end_day']) for e in starts] == [('A',1,5),('B',5,7)]
    assert outcome.metrics['aog_days'] == 6 and outcome.metrics['unplanned_failures'] == 1


def test_b0_every_observed_failure_is_in_its_day_replan():
    state = PlanningState((Tail('A',20,18,22,1,2),Tail('B',20,18,22,1,2)),
        (Spare('SA',0),Spare('SB',0)),(Resource('BAY'),),(Resource('CREW'),),horizon=12,safety_buffer=0)
    for lives in ((1.,3.),(1.,1.)):
        draw = MonteCarloScenario(0,(('A',lives[0]),('B',lives[1])),(('SA',0),('SB',0)))
        outcome = run_policy(state,draw,'B0',{'A':0,'B':0},SimulationConfig())
        failures = [e for e in outcome.events if e['event'] == 'FAILURE']
        assert len(failures) == 2
        for failure in failures:
            assert any(e['event'] == 'REPLAN' and e['day'] == failure['day'] and failure['tail'] in e['cause']
                       for e in outcome.events)


@pytest.mark.parametrize('multiplier,end',[(1.5,6),(2.,7),(3.,10)])
def test_assumed_repair_duration_sensitivity(multiplier,end):
    state = replace(fleet(horizon=14),tails=(Tail('A',8,6,10,1,3),))
    outcome = run_policy(state,scenario(1),'B0',{'A':0},SimulationConfig(repair_multiplier=multiplier))
    assert next(e['end_day'] for e in outcome.events if e['event'] == 'STARTED') == end+1


def test_training_interval_uses_fit_engines_only_and_paired_sensitivity_draws():
    from vayu.sim import training_fixed_interval
    from vayu.rul import load_cached_model
    from pdm.data.cmapss import load_fd001
    root = Path(__file__).resolve().parents[1]
    model = load_cached_model()
    train,_,_ = load_fd001(root/'data/CMAPSS')
    expected = int(np.ceil(train[train.unit.isin(model.train_units)].groupby('unit').cycle.max().median()))
    assert training_fixed_interval(root/'data/CMAPSS',root/'artifacts/rul_model.joblib') == expected
    config = SimulationConfig(n_scenarios=3)
    assert draw_scenarios(fleet(),[-1.,1.],config) == draw_scenarios(fleet(),[-1.,1.],replace(config,repair_multiplier=3.))


def test_same_planner_no_budget_ties_and_resource_feasibility():
    state = PlanningState((Tail('A',20,18,22,1,3),Tail('B',25,23,27,1,3)),
        (Spare('S1',0),Spare('S2',0)),(Resource('B'),),(Resource('C'),),horizon=9,safety_buffer=0)
    draw = MonteCarloScenario(0, (('A',50.),('B',50.)), (('S1',0),('S2',0)))
    config = SimulationConfig(weekly_budget=0, bootstrap_samples=50)
    outcomes = [run_policy(state, draw, policy, {'A':0,'B':0}, config) for policy in ('B2','B3','B4')]
    assert outcomes[0].metrics == outcomes[1].metrics == outcomes[2].metrics
    starts = [event for event in outcomes[0].events if event['event'] == 'STARTED']
    assert [(e['day'], e['end_day']) for e in starts] == [(1,4),(4,7)]
    assert len({e['spare'] for e in starts}) == len(starts)
    assert outcomes[0].metrics['plan_churn'] == 0  # Completion is not schedule churn.


def test_weekly_budget_top_action_and_unused_weeks():
    from vayu.sim import whatif_demo_state
    state = replace(whatif_demo_state(), horizon=21)
    draw = MonteCarloScenario(0, tuple((t.tail_id, t.rul_point+50) for t in state.tails),
                              tuple((s.spare_id, 0) for s in state.spares))
    config = SimulationConfig(bootstrap_samples=50)
    for policy in POLICY_NAMES:
        outcome = run_policy(state, draw, policy, {t.tail_id:0 for t in state.tails}, config)
        assert len(outcome.weeks) == 3
        assert all(row['interventions'] <= row['budget'] for row in outcome.weeks)
        assert outcome.metrics['intervention_man_hours'] == sum(row['man_hours'] for row in outcome.weeks)
        if policy in ('B0','B1','B2-K0'):
            assert not outcome.metrics['intervention_man_hours']
        else:
            assert outcome.metrics['unused_weeks'] == sum(row['unused'] for row in outcome.weeks)
            assert outcome.metrics['intervention_man_hours'] > 0  # The story spends its budget.
            for row in outcome.weeks:
                if row['interventions']:
                    assert row['effect'] != 'No effect' and row['benefit'] > 0
                    assert row['chosen_rank'] == 1
    # Ample healthy placement has no positive-benefit action: do not burn the budget.
    unused = run_policy(fleet(horizon=15), scenario(100), 'B2', {'A':0}, config)
    assert unused.metrics['unused_weeks'] == 3 and not unused.metrics['intervention_man_hours']


def test_policy_and_action_functions_do_not_receive_evaluation_values():
    from vayu.sim import choose_intervention
    for function in (select_tail, choose_intervention):
        source = inspect.getsource(function)
        assert 'true_rul' not in source and 'spare_delays' not in source and 'scenario' not in inspect.signature(function).parameters


def attention_state():
    return PlanningState((Tail('A',10,7,13,1,1),Tail('B',9,1,17,1,1),Tail('C',10,4,16,1,1)),
        (Spare('S1',1),Spare('S2',3),Spare('S3',5)),(Resource('B1'),),(Resource('C1'),),safety_buffer=0)


def test_attention_rules_choose_tails_then_share_exact_whatif_ranking():
    from vayu.planner import plan
    from vayu.sim import choose_intervention
    from vayu.whatif import WhatIfExplorer, default_interventions
    # Hand values (days, cycles): deadlines A10 B9 C10; float 1 for all; planned starts B1 A3 C5,
    # so slack A7 B8 C5 and half-widths A3 B8 C6.
    state = attention_state()
    config = SimulationConfig(float_radius=10)
    assert select_tail(state,'B2',config) == 'B'  # Earliest deadline.
    assert select_tail(state,'B3',config) == 'C'  # Shortfalls A-4, B0, C1.
    assert select_tail(state,'B4',config) == 'B'  # Shortfalls with min(float,slack)=1: A2, B7, C5.
    spare = next(p.spare for p in plan(state).placements if p.tail_id == 'C')
    actions = tuple(a for a in default_interventions(state) if a.kind in ('add_bay','add_crew_shift')
                    or (a.kind == 'expedite_spare' and a.target == spare))
    expected = next((row for row in WhatIfExplorer(state,actions,10).rank(benefit_tail='C')
                     if row['effect'] != 'No effect' and row['benefit'] > 0),None)
    chosen = choose_intervention(state,'C',config)
    if expected is None:
        assert chosen is None
    else:
        assert chosen[0].intervention_id == expected['intervention_ids'][0] and chosen[1] == expected


def test_attention_candidates_use_fourteen_day_window_and_unplanned_is_unbounded_shortfall():
    from vayu.sim import candidate_tails
    state = PlanningState((Tail('N',14,10,18,1,1),Tail('F',15,11,19,1,1)),(Spare('S',1),),
                          (Resource('B'),),(Resource('C'),),safety_buffer=0)
    assert candidate_tails(state) == {'N':14}  # Deadline 14 is inside; 15 is outside.
    for policy in ('B2','B3','B4'):
        assert select_tail(state,policy,SimulationConfig()) == 'N'
    outside = replace(state,tails=(state.tails[1],))
    assert all(select_tail(outside,policy,SimulationConfig()) is None for policy in ('B2','B3','B4'))
    first = run_policy(outside,MonteCarloScenario(0,(('F',100.),),(('S',0),)),'B3',{'F':0},SimulationConfig()).weeks[0]
    assert first['tail'] is None and first['unused'] and first['candidates'] == []
    assert first['unused_reason'] == 'No tail with deadline within 14 days'
    # Two tails, one spare: the unplanned tail has an infinite shortfall and is chosen by B3 and B4.
    pair = PlanningState((Tail('P',6,4,8,1,1),Tail('U',6,5,7,1,1)),(Spare('S',1),),
                         (Resource('B'),),(Resource('C'),),safety_buffer=0)
    from vayu.planner import plan
    unplanned = next(p.tail_id for p in plan(pair).placements if p.status == 'Unplanned')
    assert select_tail(pair,'B3',SimulationConfig()) == unplanned == select_tail(pair,'B4',SimulationConfig())


def test_inspection_is_not_in_the_scored_menu():
    from vayu.sim import intervention_ranking
    _,ranked = intervention_ranking(attention_state(),'C',SimulationConfig(float_radius=10))
    assert ranked and not any('INSPECT' in row['intervention_ids'][0] for row in ranked)


def test_chosen_tail_difference_share_counts_none_as_a_choice():
    from vayu.sim import chosen_tail_differences
    weeks = pd.DataFrame([{'scenario_id':0,'week':w,'policy':p,'tail':t}
        for w,(a,b,c) in enumerate([('X','X','Y'),(None,'X','X')])
        for p,t in zip(('B2','B3','B4'),(a,b,c))])
    shares = chosen_tail_differences(weeks).set_index('pair')
    assert shares.loc['B2/B3','differ'] == 1 and shares.loc['B3/B4','differ'] == 1 and shares.loc['B2/B4','differ'] == 2


def test_future_eta_hidden_and_observed_delay_causes_churn():
    state = replace(fleet(horizon=9), spares=(Spare('S',2),))
    config = SimulationConfig(weekly_budget=0, bootstrap_samples=50)
    prompt = run_policy(state, scenario(100, 0), 'B2', {'A':0}, config)
    delayed = run_policy(state, scenario(100, 3), 'B2', {'A':0}, config)
    assert prompt.events[0]['planned_start'] == delayed.events[0]['planned_start'] == 2
    starts = [e for e in delayed.events if e['event'] == 'STARTED']
    assert starts[0]['day'] == 5 and delayed.metrics['plan_churn'] > 0


def test_real_residual_pool_is_signed_and_held_out():
    from vayu.rul import load_cached_model
    model = load_cached_model()
    pool = calibration_residuals()
    assert set(pool.engine_id) == set(model.calibration_units)
    assert set(pool.engine_id).isdisjoint(model.train_units)
    np.testing.assert_allclose(pool.residual, pool.target - pool.point)
    assert pool.cycle.min() >= 30 and pool.target.max() <= model.cap


def test_bootstrap_pairing_and_byte_reproducible_report(tmp_path, capsys):
    state = fleet()
    config = SimulationConfig(n_scenarios=12, weekly_budget=0, bootstrap_samples=100)
    first = monte_carlo(state, [-2.,0.,2.], {'A':0}, config)
    second = monte_carlo(state, [-2.,0.,2.], {'A':0}, config)
    pd.testing.assert_frame_equal(first.runs, second.runs)
    pd.testing.assert_frame_equal(first.summary, second.summary)
    assert set(first.runs.policy) == set(POLICY_NAMES)
    assert first.runs.groupby('scenario_id').policy.nunique().eq(7).all()
    a, b = tmp_path/'a', tmp_path/'b'
    write_validation(first, a)
    write_validation(second, b)
    for name in ('validation.csv','validation_runs.csv','validation_weeks.csv','validation_manifest.json'):
        assert (a/name).read_bytes() == (b/name).read_bytes()
    output = capsys.readouterr().out
    assert 'simulated; scenario-based' in output and 'B3 / B4' in output and 'tie' in output.lower()
    assert first.summary.n_scenarios.eq(12).all()
    assert first.summary.ci_low.le(first.summary['mean']).all()
    assert first.summary.ci_high.ge(first.summary['mean']).all()
    constant = first.runs.copy()
    constant['aog_days'] = 3
    report = bootstrap_summary(constant, config)
    assert report.query("metric == 'aog_days'")[['mean','ci_low','ci_high']].eq(3).all().all()


@pytest.mark.parametrize('options', [{'weekly_budget':-1}, {'n_scenarios':0}, {'seed':-1},
    {'max_spare_delay':-1}, {'fixed_interval_cycles':0}, {'bootstrap_samples':0}, {'float_radius':-1},
    {'repair_multiplier':.5},{'repair_multiplier':float('nan')},{'residual_scale':-1}])
def test_invalid_config(options):
    with pytest.raises(ValueError):
        SimulationConfig(**options)
