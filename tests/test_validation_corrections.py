"""Post-hoc v2 definitions, fixed before the corrected results are generated."""
from dataclasses import replace

import numpy as np
import pandas as pd

from vayu.schemas import PlanningState, Resource, Spare, Tail
from vayu.sim import MonteCarloScenario, SimulationConfig, run_policy


def small_state() -> PlanningState:
    """A fictional one-tail fixture with a known helpful expedite."""
    return PlanningState((Tail('A',20,18,22,2,2),),(Spare('S',12),),
                         (Resource('B'),),(Resource('C'),),horizon=40,safety_buffer=0)


def test_neutral_ages_are_uniform_seeded_and_paired_across_sensitivities():
    from vayu.sim import draw_initial_ages
    state = small_state()
    config = SimulationConfig(n_scenarios=20,fixed_interval_cycles=100)
    ages = draw_initial_ages(state,config)
    expected = np.random.default_rng(config.seed+1000).uniform(0,100,size=(20,1))
    np.testing.assert_array_equal([row['A'] for row in ages],expected[:,0])
    assert all(0 <= row['A'] < config.fixed_interval_cycles for row in ages)
    assert ages == draw_initial_ages(replace(state,horizon=80),replace(config,repair_multiplier=3.,residual_scale=2.))
    for i,row in enumerate(ages):
        outcome = run_policy(state,MonteCarloScenario(i,(('A',100.),),(('S',0),)),'B1',row,config)
        assert outcome.metrics['initial_overdue_tails'] == 0
        assert not any(e['event'] == 'GROUNDED' and e['day'] == 0 for e in outcome.events)


def test_target_score_does_not_reward_other_tails_or_hide_target_gains():
    from vayu.whatif import score_for_tail
    row = {'benefit':2,'benefit_per_cost':.25,'cost_man_hours':8,
           'benefit_components':{'covered_increase':1,'late_reduction':1},
           'benefit_definition':'fleet count change','per_tail_changes':[
               {'tail':'A','before':{'label':'Covered','status':'On time'},
                            'after':{'label':'Covered','status':'On time'}},
               {'tail':'B','before':{'label':'Fragile','status':'Late'},
                            'after':{'label':'Covered','status':'On time'}}]}
    a,b = score_for_tail(row,'A'),score_for_tail(row,'B')
    assert a['benefit'] == a['benefit_per_cost'] == 0
    assert b['benefit'] == 2 and b['benefit_per_cost'] == .25
    assert a['fleet_benefit'] == b['fleet_benefit'] == 2
    assert row['benefit'] == 2 and 'benefit_tail' not in row  # No cache mutation.


def test_policy_action_ranking_uses_target_changes_and_excludes_no_effect():
    from vayu.sim import choose_intervention, intervention_ranking, whatif_demo_state
    state,config = whatif_demo_state(),SimulationConfig()
    assert choose_intervention(state,'T-01',config) is None
    actions,ranked = intervention_ranking(state,'T-04',config)
    chosen = choose_intervention(state,'T-04',config)
    assert chosen is not None and chosen[0].intervention_id == 'EXPEDITE:S2'
    assert all(row['benefit_tail'] == 'T-04' for row in ranked)
    for row in ranked:
        change = next(t for t in row['per_tail_changes'] if t['tail'] == 'T-04')
        before,after = change['before'],change['after']
        gain = int(after['label']=='Covered')-int(before['label']=='Covered')
        reduction = int(before['status']=='Late')-int(after['status']=='Late')
        assert row['benefit'] == gain+reduction
        assert row['benefit_per_cost'] == row['benefit']/row['cost_man_hours']
    assert all(a.kind in ('expedite_spare','add_crew_shift','add_bay') for a in actions)


def test_b4b_uses_direct_float_shortfall_with_a_finite_unplanned_rule():
    from vayu.sim import select_tail
    state = PlanningState((Tail('P',6,0,12,1,1),Tail('U',6,5,7,1,1)),(Spare('S',1),),
                         (Resource('B'),),(Resource('C'),),safety_buffer=0)
    config = SimulationConfig()
    assert select_tail(state,'B4',config) == 'U'  # Existing combined rule retained.
    assert select_tail(state,'B4b',config) == 'P'  # P: 6-1; U: 1-0.
    outcome = run_policy(small_state(),MonteCarloScenario(0,(('A',100.),),(('S',0),)),
                         'B4b',{'A':0},config)
    assert outcome.metrics['intervention_man_hours'] > 0
    assert outcome.weeks[0]['budget'] == 1


def test_k0_combined_ties_and_paired_columns_use_outcomes_only():
    from vayu.sim import monte_carlo, bootstrap_summary, validation_cell_rows
    config = SimulationConfig(n_scenarios=3,weekly_budget=0,bootstrap_samples=20)
    result = monte_carlo(small_state(),[0.],{'A':0},config)
    changed = result.runs.copy()
    changed.loc[changed.policy=='B2','unused_weeks'] = 6
    changed.loc[changed.policy=='B2','intervention_man_hours'] = 8
    report = validation_cell_rows(replace(result,runs=changed,summary=bootstrap_summary(changed,config)),
                                  config,'benign',2.)
    control = report.set_index('policy').loc['B2-B2-K0']
    assert control.tie_scenarios == 3 and control.ties_over_n == '3/3'
    assert control.tie_metric_scope == 'outcomes_only'
    assert pd.isna(control.intervention_man_hours_mean) and pd.isna(control.unused_weeks_mean)
    assert control.aog_days_mean == 0 and control.aog_days_ties == 3


def test_monte_carlo_uses_each_scenarios_common_initial_ages():
    from vayu.sim import monte_carlo, draw_initial_ages, POLICY_NAMES
    state,config = small_state(),SimulationConfig(n_scenarios=3,weekly_budget=0,bootstrap_samples=20,max_spare_delay=0)
    ages = draw_initial_ages(state,config)
    result = monte_carlo(state,[0.],ages,config)
    assert set(result.runs.policy) == set(POLICY_NAMES) and 'B4b' in POLICY_NAMES
    for scenario,age in enumerate(ages):
        expected = run_policy(state,MonteCarloScenario(scenario,(('A',20.),),(('S',0),)),
                              'B1',age,config)
        observed = result.runs.query("scenario_id == @scenario and policy == 'B1'").iloc[0]
        assert observed.aog_days == expected.metrics['aog_days']
    assert result.manifest['initial_ages_sha256']
    assert result.manifest['design_revision'] == 'v2_post_hoc'


def test_v1_archive_preserves_bytes_and_is_never_overwritten(tmp_path):
    from scripts.validation import preserve_v1_artifacts
    import pytest
    artifacts = tmp_path/'artifacts'
    nested = artifacts/'validation/benign/repair_2'
    nested.mkdir(parents=True)
    (artifacts/'validation.csv').write_bytes(b'v1 report\n')
    (nested/'validation_runs.csv').write_bytes(b'v1 raw evidence\n')
    archive = preserve_v1_artifacts(artifacts)
    assert (archive/'validation.csv').read_bytes() == b'v1 report\n'
    assert (archive/'validation/benign/repair_2/validation_runs.csv').read_bytes() == b'v1 raw evidence\n'
    (artifacts/'validation.csv').write_bytes(b'v2 report\n')
    assert preserve_v1_artifacts(artifacts) == archive
    assert (archive/'validation.csv').read_bytes() == b'v1 report\n'
    (archive/'validation.csv').write_bytes(b'tampered\n')
    with pytest.raises(ValueError,match='archive'):
        preserve_v1_artifacts(artifacts)


def test_v1_archive_bytes_survive_git_checkout_with_windows_line_endings(tmp_path):
    """A fresh checkout must retain the raw bytes covered by the v1 hash ledger."""
    import shutil
    import subprocess
    import pytest
    from pathlib import Path
    git = shutil.which('git')
    if git is None:
        pytest.skip('Git is needed for the archive checkout integration check')
    attributes = Path(__file__).resolve().parents[1]/'.gitattributes'
    shutil.copyfile(attributes,tmp_path/'.gitattributes')
    archive = tmp_path/'artifacts/validation_v1'
    archive.mkdir(parents=True)
    original = {'unix.log':b'v1 evidence\n','windows.log':b'v1 evidence\r\n',
                'validation.csv':b'policy,outcome\r\nB0,1\r\n'}
    for name,content in original.items():
        (archive/name).write_bytes(content)
    def run(*args):
        return subprocess.run([git,'-c','core.autocrlf=true',*args],cwd=tmp_path,
                              check=True,capture_output=True)
    run('init','--quiet')
    run('add','.')
    for name in original:
        (archive/name).write_bytes(b'replace before checkout\n')
    run('checkout-index','--force','--all')
    assert {name:(archive/name).read_bytes() for name in original} == original
