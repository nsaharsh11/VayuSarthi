"""Causal features, engine-separated calibration and deterministic fitting."""
import numpy as np
import pandas as pd
import pytest

from vayu.rul import features, fit_model, predict, save_model, load_model


@pytest.fixture
def trajectories():
    rng = np.random.default_rng(23)
    rows = [(unit, cycle, cycle * .1 + rng.normal(0, .01), 20-cycle)
            for unit in range(1, 21) for cycle in range(1, 21)]
    return pd.DataFrame(rows, columns=['unit', 'cycle', 's1', 'true_rul'])


def test_features_causal_and_ignore_targets(trajectories):
    full = features(trajectories, ('s1',), (5, 15))
    truncated = trajectories[trajectories.cycle <= 9].copy()
    truncated['true_rul'] = -999
    short = features(truncated, ('s1',), (5, 15))
    pd.testing.assert_frame_equal(full.loc[short.index], short)
    assert full.loc[0, 's1_std_5'] == 0
    assert full.loc[0, 's1_slope_5'] == 0


def test_model_roundtrip_reproducible_and_prediction_causal(trajectories, tmp_path):
    options = dict(sensors=('s1',), windows=(5,), seed=19, n_estimators=8, bins=(0, 20, 1000))
    model = fit_model(trajectories, **options)
    other = fit_model(trajectories, **options)
    assert set(model.train_units).isdisjoint(model.calibration_units)
    first, second = tmp_path/'a.json', tmp_path/'b.json'
    save_model(model, first)
    save_model(other, second)
    assert first.read_bytes() == second.read_bytes()
    restored = load_model(first)
    result = predict(restored, trajectories)
    assert (result.lower <= result.point).all() and (result.point <= result.upper).all()
    short = trajectories[trajectories.cycle <= 9]
    pd.testing.assert_frame_equal(result.loc[short.index], predict(restored, short))


def test_fit_rejects_too_few_engines(trajectories):
    with pytest.raises(ValueError, match='engines'):
        fit_model(trajectories[trajectories.unit == 1], sensors=('s1',))


def test_generated_fd001_report_and_oof():
    import json
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    report = json.loads((root/'reports/model_metrics.json').read_text())
    oof = pd.read_csv(root/'data/processed/oof_predictions.csv')
    assert oof.unit.nunique() == 100 and not oof.duplicated(['unit', 'cycle']).any()
    assert (oof.lower <= oof.point).all() and (oof.point <= oof.upper).all()
    for fold in report['fold_membership']:
        training, calibration, evaluation = map(set, (fold['train_units'], fold['calibration_units'], fold['evaluation_units']))
        assert training.isdisjoint(calibration | evaluation)
        assert calibration.isdisjoint(evaluation)
    assert set(report['checkpoints']) == {'10','20','30','40','50','60'}
    assert report['benchmark']['count'] == 100
    assert report['benchmark']['nasa_asymmetric_score'] >= 0
    for metrics in report['checkpoints'].values():
        assert 0 <= metrics['two_sided_coverage'] <= metrics['low_bound_coverage'] <= 1
