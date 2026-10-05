"""Split CQR, cached predictions and real-FD001 reproducibility contracts."""
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest

from vayu.rul import (conformal_adjustment, fit_model, load_cached_model,
                      features, predict, predict_tail, train_fd001)

ROOT = Path(__file__).resolve().parents[1]


def test_exact_last_thirty_cycle_statistics() -> None:
    """Mean/std/slope exclude observations older than the 30-cycle window."""
    frame = pd.DataFrame({'unit': [1] * 35, 'cycle': np.arange(1, 36),
                          's1': np.arange(1, 36, dtype=float)})
    result = features(frame, ('s1',), (30,))
    assert result.iloc[-1].s1_mean_30 == 20.5
    assert result.iloc[-1].s1_std_30 == pytest.approx(np.std(np.arange(6, 36)))
    assert result.iloc[-1].s1_slope_30 == pytest.approx(1)
    frame.loc[frame.cycle <= 5, 's1'] = -999
    changed = features(frame, ('s1',), (30,))
    pd.testing.assert_series_equal(result.iloc[-1], changed.iloc[-1])


def test_engine_conformal_rank() -> None:
    """Finite-sample rank counts engines, and never silently returns infinity."""
    assert conformal_adjustment(np.arange(1, 21, dtype=float)) == 17
    with pytest.raises(ValueError, match='calibration engines'):
        conformal_adjustment(np.array([1.]))
    assert conformal_adjustment(-np.ones(20)) == 0


def test_calibration_targets_cannot_train_any_booster() -> None:
    frame = pd.DataFrame([(u, c, float(c), 50-c) for u in range(1, 21)
                          for c in range(1, 41)], columns=['unit', 'cycle', 's1', 'true_rul'])
    options = dict(sensors=('s1',), windows=(30,), seed=11, n_estimators=5,
                   calibration_fraction=.25)
    first = fit_model(frame, **options)
    changed = frame.copy()
    changed.loc[changed.unit.isin(first.calibration_units), 'true_rul'] += 50
    second = fit_model(changed, **options)
    assert set(first.train_units).isdisjoint(first.calibration_units)
    assert first.lower_booster.params['objective'] == 'quantile'
    assert first.lower_booster.params['alpha'] == .1
    assert first.upper_booster.params['alpha'] == .9
    for name in ('booster', 'lower_booster', 'upper_booster'):
        assert getattr(first, name).model_to_string() == getattr(second, name).model_to_string()
    result = predict(first, frame.drop(columns='true_rul'))
    assert (result.lower <= result.point).all() and (result.point <= result.upper).all()
    assert len(first.calibration_scores) == len(first.calibration_units)


def test_missing_data_prints_manual_instructions_and_creates_no_cache(tmp_path: Path,
                                                                    capsys) -> None:
    with pytest.raises(FileNotFoundError, match='train_FD001.txt'):
        train_fd001(tmp_path / 'missing', tmp_path / 'artifacts', n_estimators=2)
    text = capsys.readouterr().err
    assert 'Download' in text and 'NASA' in text and 'RUL_FD001.txt' in text
    assert not (tmp_path / 'artifacts').exists()


def test_real_fd001_metrics_and_cache_reproducible(tmp_path: Path) -> None:
    """Two independent real-data runs must produce identical metric/cache bytes."""
    first, second = tmp_path / 'a', tmp_path / 'b'
    a = train_fd001(ROOT / 'data/CMAPSS', first, seed=29, n_estimators=8)
    b = train_fd001(ROOT / 'data/CMAPSS', second, seed=29, n_estimators=8)
    assert a == b
    assert (first / 'rul_metrics.json').read_bytes() == (second / 'rul_metrics.json').read_bytes()
    assert (first / 'rul_model.joblib').read_bytes() == (second / 'rul_model.joblib').read_bytes()
    assert set(a['fit_engines']).isdisjoint(a['calibration_engines'])
    assert set(a['fit_engines']) | set(a['calibration_engines']) == set(range(1, 101))
    assert a['test']['count'] == 100
    assert a['test']['rmse'] >= 0 and a['test']['nasa_asymmetric_score'] >= 0
    assert 0 <= a['test']['picp'] <= 1 and a['test']['mpiw'] >= 0
    cached = load_cached_model(first / 'rul_model.joblib')
    assert cached.windows == (30,)
    assert 's1' not in cached.sensors
    result = predict_tail(1, first / 'rul_model.joblib')
    assert set(result) == {'rul_point', 'lower', 'upper', 'half_width'}
    assert 0 <= result['lower'] <= result['rul_point'] <= result['upper']
    assert result['half_width'] == (result['upper'] - result['lower']) / 2
    assert predict_tail('E-01', first / 'rul_model.joblib') == result
    # Mapping is explicit: fictional E-01 resolves to FD001 test unit 1.
    with pytest.raises(KeyError, match='engine'):
        predict_tail('E-999', first / 'rul_model.joblib')
    bundle = joblib.load(first / 'rul_model.joblib')
    assert all('true_rul' not in row for row in bundle['tail_predictions'].values())
    from pdm.data.cmapss import load_fd001
    _, test, truth = load_fd001(ROOT / 'data/CMAPSS')
    final = test.groupby('unit', sort=True).tail(1)
    restored = predict(cached, test).loc[final.index]
    assert restored.iloc[0]['point'] == result['rul_point']
    assert restored.iloc[0]['lower'] == result['lower']
    assert restored.iloc[0]['upper'] == result['upper']
    error = restored.point.to_numpy() - truth.rul.to_numpy()
    assert a['test']['rmse'] == pytest.approx(np.sqrt(np.mean(error ** 2)))
    assert a['test']['nasa_asymmetric_score'] == pytest.approx(
        sum(np.expm1(-e / 13) if e < 0 else np.expm1(e / 10) for e in error))
