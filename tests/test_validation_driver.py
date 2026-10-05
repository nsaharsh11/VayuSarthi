"""End-to-end export contract on small offline caller-supplied fixtures."""
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

from vayu.schemas import PlanningState, Resource, Spare, Tail
from vayu.sim import SimulationConfig, VALIDATION_COLUMNS


def test_driver_finishes_all_stress_repair_cells_and_paired_export(tmp_path, monkeypatch, capsys):
    import scripts.validation as driver
    state = PlanningState((Tail('A',8,6,10,1,2),),(Spare('S',0),),
                          (Resource('B'),),(Resource('C'),),horizon=6,safety_buffer=0)
    pack = SimpleNamespace(planning_hold=False,accepted={
        'tails.csv':pd.DataFrame({'tail_id':['A'],'engine_id':['E']}),
        'tech_records.csv':pd.DataFrame({'tail_id':['A'],'cycles_since_overhaul':[0]})})
    (tmp_path/'data/fleet').mkdir(parents=True)
    (tmp_path/'data/CMAPSS').mkdir()
    (tmp_path/'data/CMAPSS/train_FD001.txt').write_text('local training fixture',encoding='utf-8')
    (tmp_path/'artifacts').mkdir()
    (tmp_path/'artifacts/rul_model.joblib').write_bytes(b'local model fixture')
    monkeypatch.setattr(driver,'read_fleet_pack',lambda path:pack)
    monkeypatch.setattr(driver,'predict_tail',lambda *args:{})
    monkeypatch.setattr(driver,'planning_state_from_fleet',lambda *args,**kwargs:state)
    monkeypatch.setattr(driver,'training_fixed_interval',lambda *args:100)
    monkeypatch.setattr(driver,'calibration_residuals',lambda *args:pd.DataFrame({'engine_id':[1],'residual':[0.]}))
    config = SimulationConfig(n_scenarios=3,bootstrap_samples=20,weekly_budget=0)
    driver.validate(tmp_path,config)
    report = pd.read_csv(tmp_path/'artifacts/validation.csv')
    assert list(report) == VALIDATION_COLUMNS
    assert set(report.stress_level) == {'benign','moderate','stressed'}
    assert set(report.repair_multiplier) == {1.5,2.,3.}
    assert set(report.horizon_days) == {40,80}
    assert report.groupby(['stress_level','repair_multiplier','horizon_days']).size().eq(12).all()
    paired = report[report.policy == 'B4-B3']
    assert len(paired) == 18 and paired.tie_scenarios.eq(3).all()
    assert report[report.row_type == 'policy'].b2_b3_share.between(0,1).all()
    assert set(report.policy) >= {'B3-B2','B2-K0','B2-B2-K0','B4b','B4b-B4','B4b-B3'}
    comparison = (tmp_path/'artifacts/validation_comparison.md').read_text(encoding='utf-8')
    assert 'B4 minus B3' in comparison and 'Chosen-tail differences' in comparison
    assert (tmp_path/'artifacts/validation_preregistered.json').is_file()
    b1 = pd.read_csv(tmp_path/'artifacts/validation_b1_scenarios.csv')
    assert len(b1) == 54 and b1.fixed_interval_cycles.eq(100).all()
    assert b1.initial_overdue_tails.eq(0).all()
    ages = pd.read_csv(tmp_path/'artifacts/validation_initial_ages.csv')
    assert len(ages) == 3 and ages.initial_age_cycles.between(0,100,inclusive='left').all()
    printed = capsys.readouterr().out
    assert 'action_ids' in printed and 'unused_reason' in printed
    traces = (tmp_path/'artifacts/validation_diagnostics.log').read_text(encoding='utf-8')
    assert all(f'three scenarios, {level}' in traces for level in ('benign','moderate','stressed'))
    source = tmp_path/'artifacts/validation/stressed/horizon_40/repair_2'
    runs = pd.read_csv(source/'validation_runs.csv')
    weeks = pd.read_csv(source/'validation_weeks.csv')
    driver.validate(tmp_path,config)
    pd.testing.assert_frame_equal(runs,pd.read_csv(source/'validation_runs.csv'))
    pd.testing.assert_frame_equal(weeks,pd.read_csv(source/'validation_weeks.csv'))
    pd.testing.assert_frame_equal(report,pd.read_csv(tmp_path/'artifacts/validation.csv'))
    # A report-only refresh adds/reconciles comparisons without rerunning a policy.
    raw_bytes = (source/'validation_runs.csv').read_bytes()
    monkeypatch.setattr(driver, 'monte_carlo', lambda *args, **kwargs: (_ for _ in ()).throw(
        AssertionError('Report refresh must not resimulate unchanged policies')))
    driver.validate(tmp_path, config, resume_frozen=True)
    assert (source/'validation_runs.csv').read_bytes() == raw_bytes
    assert (tmp_path/'artifacts/validation_resume_manifest.json').is_file()
    driver.refresh_exports(tmp_path)
    refreshed = pd.read_csv(tmp_path/'artifacts/validation.csv')
    assert refreshed.groupby(['stress_level','repair_multiplier','horizon_days']).size().eq(12).all()
    assert set(refreshed.policy) == set(report.policy)
    assert (source/'validation_runs.csv').read_bytes() == raw_bytes
    first_bytes = (tmp_path/'artifacts/validation.csv').read_bytes()
    driver.refresh_exports(tmp_path)
    assert (tmp_path/'artifacts/validation.csv').read_bytes() == first_bytes
    assert (tmp_path/'artifacts/validation_refresh_manifest.json').is_file()
    # Rounded raw values cannot establish an exact unrounded tie by themselves.
    import json
    import pytest
    manifest_path = source/'validation_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['b3_b4'][0]['all_scenarios_tied'] = False
    manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(ValueError, match='unrounded evidence'):
        driver.refresh_exports(tmp_path)
    assert (tmp_path/'artifacts/validation.csv').read_bytes() == first_bytes
