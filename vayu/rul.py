"""Offline FD001 point/quantile models with engine-held-out split CQR."""
from dataclasses import dataclass
from pathlib import Path
import json
import math
import re
import sys
import hashlib

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GroupKFold

from vayu.schemas import canonical_json


@dataclass
class RULModel:
    """Three boosters and engine-level conformal scores; legacy JSON readable."""
    booster: lgb.Booster
    sensors: tuple[str, ...]
    windows: tuple[int, ...]
    bins: tuple[float, ...]
    quantiles: tuple[tuple[float, float, float], ...]
    train_units: tuple[int, ...]
    calibration_units: tuple[int, ...]
    lower_booster: lgb.Booster | None = None
    upper_booster: lgb.Booster | None = None
    conformal_delta: float = 0.
    calibration_scores: tuple[float, ...] = ()
    cap: float = 125.


def features(frame: pd.DataFrame, sensors: tuple[str, ...],
             windows: tuple[int, ...] = (5, 15, 30)) -> pd.DataFrame:
    """Last/rolling mean/std/slope using only cycles <= the current row."""
    if frame.empty or frame.duplicated(['unit', 'cycle']).any():
        raise ValueError('Require nonempty unique unit/cycle observations')
    if not windows or any(w < 1 for w in windows) or not sensors:
        raise ValueError('Require sensors and positive windows')
    if not np.isfinite(frame[['unit', 'cycle', *sensors]].to_numpy(dtype=float)).all():
        raise ValueError('Features must be finite')
    result: dict[str, pd.Series] = {}
    result['cycle'] = frame['cycle'].astype(float)
    ordered = frame.sort_values(['unit', 'cycle'], kind='stable')
    for sensor in sensors:
        result[sensor+'_last'] = frame[sensor].astype(float)
        for window in windows:
            mean, std, slope = (pd.Series(index=frame.index, dtype=float) for _ in range(3))
            for _, engine in ordered.groupby('unit', sort=True):
                y = engine[sensor].astype(float)
                x = engine['cycle'].astype(float)
                mean.loc[engine.index] = y.rolling(window, min_periods=1).mean()
                std.loc[engine.index] = y.rolling(window, min_periods=1).std(ddof=0)
                xy = (x*y).rolling(window, min_periods=1).mean()
                xm = x.rolling(window, min_periods=1).mean()
                ym = y.rolling(window, min_periods=1).mean()
                variance = (x*x).rolling(window, min_periods=1).mean()-xm*xm
                slope.loc[engine.index] = ((xy-xm*ym)/variance.replace(0, np.nan)).fillna(0)
            result[f'{sensor}_mean_{window}'] = mean
            result[f'{sensor}_std_{window}'] = std
            result[f'{sensor}_slope_{window}'] = slope
    return pd.DataFrame(result, index=frame.index)


def _bin(points: np.ndarray, bins: tuple[float, ...]) -> np.ndarray:
    return np.clip(np.searchsorted(bins, points, side='right')-1, 0, len(bins)-2)


def conformal_adjustment(scores: np.ndarray, miscoverage: float = .2) -> float:
    """Finite-sample CQR rank ceil((n+1)*(1-alpha)), one score per engine.

    Negative adjustments are clamped to zero, conservatively avoiding interval
    shrinkage. Reject too-small calibration sets rather than using infinity.
    """
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 1 or not len(scores) or not np.isfinite(scores).all() or not 0 < miscoverage < 1:
        raise ValueError('Require finite engine scores and valid miscoverage')
    rank = math.ceil((len(scores) + 1) * (1 - miscoverage))
    if rank > len(scores):
        raise ValueError('Too few calibration engines for a finite conformal range')
    return max(0., float(np.sort(scores)[rank - 1]))


def _engine_split(frame: pd.DataFrame, seed: int,
                  calibration_fraction: float) -> tuple[tuple[int, ...], tuple[int, ...], np.random.Generator]:
    """Split complete engines before selecting features or fitting models."""
    if not 0 < calibration_fraction < 1:
        raise ValueError('Invalid calibration fraction')
    units = np.sort(frame.unit.unique())
    rng = np.random.default_rng(seed)
    shuffled = rng.permutation(units)
    n_cal = math.ceil(len(units) * calibration_fraction)
    calibration = tuple(sorted(int(u) for u in shuffled[:n_cal]))
    training = tuple(sorted(int(u) for u in shuffled[n_cal:]))
    if len(training) < 2 or len(calibration) < 4:
        raise ValueError('Need at least two fit engines and four calibration engines')
    return training, calibration, rng


def _fit(frame: pd.DataFrame, x: pd.DataFrame, sensors: tuple[str, ...], windows: tuple[int, ...],
         seed: int, n_estimators: int, bins: tuple[float, ...], cap: float,
         calibration_fraction: float) -> RULModel:
    training, calibration, rng = _engine_split(frame, seed, calibration_fraction)
    if not math.isfinite(cap) or cap <= 0 or n_estimators < 1:
        raise ValueError('Require a finite positive cap and positive estimator count')
    if not np.isfinite(frame.true_rul.to_numpy(dtype=float)).all() or (frame.true_rul < 0).any():
        raise ValueError('Training RUL labels must be finite and nonnegative')
    x = x[[column for column in x if any(marker in column for marker in ('_mean_', '_std_', '_slope_'))]]
    train_mask = frame.unit.isin(training)
    cal_mask = frame.unit.isin(calibration)
    # All model seeds come from the explicitly seeded numpy Generator.
    model_seed = int(rng.integers(0, 2**31-1))
    parameters = dict(n_estimators=n_estimators, learning_rate=.05, num_leaves=31,
                      n_jobs=1, verbosity=-1, deterministic=True, force_col_wise=True,
                      random_state=model_seed)
    boosters = []
    for objective, alpha in (('regression', None), ('quantile', .1), ('quantile', .9)):
        model = lgb.LGBMRegressor(**parameters, objective=objective,
                                **({'alpha': alpha} if alpha is not None else {}))
        model.fit(x.loc[train_mask], np.minimum(frame.loc[train_mask, 'true_rul'], cap))
        boosters.append(model.booster_)
    low, high = _quantile_bounds(boosters[1], boosters[2], x.loc[cal_mask])
    y = np.minimum(frame.loc[cal_mask, 'true_rul'].to_numpy(), cap)
    row_scores = pd.Series(np.maximum(low - y, y - high), index=x.loc[cal_mask].index)
    # Within-engine cycles are correlated: use a maximum per calibration
    # engine, not a pooled row quantile with an inflated sample count.
    engine_scores = row_scores.groupby(frame.loc[cal_mask, 'unit']).max().sort_index()
    delta = conformal_adjustment(engine_scores.to_numpy())
    return RULModel(boosters[0], sensors, windows, bins, (), training, calibration,
                    boosters[1], boosters[2], delta, tuple(float(s) for s in engine_scores), cap)


def fit_model(frame: pd.DataFrame, sensors: tuple[str, ...], windows: tuple[int, ...] = (30,),
              seed: int = 7, n_estimators: int = 400, bins: tuple[float, ...] = (0, 20, 40, 70, 1000),
              cap: float = 125, calibration_fraction: float = .2) -> RULModel:
    """Fit point/0.1/0.9 models on fit engines; calibrate whole held-out engines."""
    if not 0 < calibration_fraction < 1 or len(bins) < 2 or any(a >= b for a,b in zip(bins, bins[1:])):
        raise ValueError('Invalid calibration fraction or bins')
    return _fit(frame, features(frame, sensors, windows), sensors, windows, seed,
                n_estimators, bins, cap, calibration_fraction)


def _quantile_bounds(lower: lgb.Booster, upper: lgb.Booster,
                     x: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Sort crossing quantiles and intersect with nonnegative RUL support."""
    a, b = lower.predict(x, num_threads=1), upper.predict(x, num_threads=1)
    return np.maximum(0, np.minimum(a, b)), np.maximum(0, np.maximum(a, b))


def _predict(model: RULModel, x: pd.DataFrame) -> pd.DataFrame:
    x = x.loc[:, model.booster.feature_name()]
    point = np.maximum(0, model.booster.predict(x, num_threads=1))
    if model.lower_booster is not None and model.upper_booster is not None:
        point = np.minimum(point, model.cap)
        low, high = _quantile_bounds(model.lower_booster, model.upper_booster, x)
        raw_low, raw_high = np.maximum(0, low - model.conformal_delta), high + model.conformal_delta
    else:
        # Only old demo artifacts use predicted-bin residual ranges.
        q = np.asarray(model.quantiles)[_bin(point, model.bins)]
        raw_low, raw_high = np.maximum(0, point+q[:,0]), np.maximum(0, point+q[:,2])
    return pd.DataFrame({'point':point, 'lower':np.minimum(raw_low, point),
                         'upper':np.maximum(raw_high, point),
                         'clipped':(raw_low > point) | (raw_high < point)}, index=x.index)


def predict(model: RULModel, frame: pd.DataFrame) -> pd.DataFrame:
    """Predict calibrated intervals without consulting labels in the input."""
    return _predict(model, features(frame, model.sensors, model.windows))


def save_model(model: RULModel, path: Path) -> None:
    """Write canonical JSON; no pickle, network or volatile timestamp."""
    data = _model_payload(model)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(data).encode('utf-8'))


def load_model(path: Path) -> RULModel:
    """Restore the local artifact with its retained training feature schema."""
    return _restore_model(json.loads(path.read_text(encoding='utf-8')))


def _model_payload(model: RULModel) -> dict:
    """Serialize booster strings to avoid nondeterministic pickle object state."""
    data = vars(model).copy()
    for key in ('booster', 'lower_booster', 'upper_booster'):
        data[key] = data[key].model_to_string() if data[key] is not None else None
    return data


def _restore_model(payload: dict) -> RULModel:
    """Restore CQR or legacy model data without mutating the payload."""
    data = payload.copy()
    for key in ('booster', 'lower_booster', 'upper_booster'):
        if data.get(key) is not None:
            data[key] = lgb.Booster(model_str=data[key])
    for key in ('sensors', 'windows', 'bins', 'train_units', 'calibration_units'):
        data[key] = tuple(data[key])
    data['quantiles'] = tuple(tuple(row) for row in data['quantiles'])
    if 'calibration_scores' in data:
        data['calibration_scores'] = tuple(data['calibration_scores'])
    return RULModel(**data)


def _metrics(frame: pd.DataFrame) -> dict[str, float | int]:
    """Report empirical checkpoint coverage and widths without target tuning."""
    width = frame.upper-frame.lower
    return {'count':len(frame), 'rmse':float(np.sqrt(mean_squared_error(frame.true_rul, frame.point))),
            'two_sided_coverage':float(((frame.lower <= frame.true_rul)&(frame.true_rul <= frame.upper)).mean()),
            'low_bound_coverage':float((frame.true_rul >= frame.lower).mean()),
            'mean_width':float(width.mean()), 'median_width':float(width.median()),
            'mean_signed_error':float((frame.point-frame.true_rul).mean())}


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CACHE = ROOT / 'artifacts/rul_model.joblib'
FD001_FILES = ('train_FD001.txt', 'test_FD001.txt', 'RUL_FD001.txt')


def train_fd001(data_dir: Path | None = None, artifact_dir: Path | None = None,
                 seed: int = 7, n_estimators: int = 400,
                 calibration_fraction: float = .2) -> dict:
    """Train split CQR and evaluate one final observation per FD001 test engine.

    Informative sensors are selected on fit engines only. Calibration uses
    maximum nonconformity across each held-out engine's capped trajectory.
    Test metrics use official uncapped terminal RUL, never fit/calibration
    labels. Test engine IDs form an independent dataset namespace.
    """
    from pdm.data.cmapss import SENSOR_COLUMNS, drop_constant_sensors, load_fd001
    directory = Path(data_dir) if data_dir is not None else ROOT / 'data/CMAPSS'
    output = Path(artifact_dir) if artifact_dir is not None else ROOT / 'artifacts'
    missing = [name for name in FD001_FILES if not (directory / name).is_file()]
    if missing:
        instructions = (f'Missing NASA FD001 files in {directory}: {", ".join(missing)}.\n'
                        'Download the NASA Turbofan Engine Degradation Simulation Data Set '
                        'from the NASA data portal (https://data.nasa.gov/).\n'
                        'Extract CMAPSSData.zip and copy train_FD001.txt, test_FD001.txt '
                        f'and RUL_FD001.txt into {directory}. Then rerun training. '
                        'No download is attempted by this program.')
        print(instructions, file=sys.stderr)
        raise FileNotFoundError(instructions)
    train, test, truth = load_fd001(directory)
    fit_units, _, _ = _engine_split(train, seed, calibration_fraction)
    dropped = drop_constant_sensors(train[train.unit.isin(fit_units)])
    sensors = tuple(sensor for sensor in SENSOR_COLUMNS if sensor not in dropped)
    model = fit_model(train, sensors, windows=(30,), seed=seed,
                      n_estimators=n_estimators, calibration_fraction=calibration_fraction)
    predictions = predict(model, test)
    last = test.groupby('unit', sort=True).tail(1)
    benchmark = last[['unit', 'cycle']].join(predictions.loc[last.index]).reset_index(drop=True)
    benchmark = benchmark.merge(truth.rename(columns={'rul': 'true_rul'}), on='unit',
                                 validate='one_to_one', sort=True)
    error = benchmark.point.to_numpy() - benchmark.true_rul.to_numpy()
    score = float(np.where(error < 0, np.expm1(-error / 13), np.expm1(error / 10)).sum())
    metrics = _metrics(benchmark)
    report = {
        'data_label': 'NASA C-MAPSS FD001 simulated benchmark; not aircraft performance.',
        'method': 'split-conformal quantile regression', 'seed': seed,
        'n_estimators': n_estimators, 'nominal_coverage': .8, 'target_cap_cycles': model.cap,
        'window_cycles': 30, 'informative_sensors': sensors, 'dropped_sensors': dropped,
        'fit_engines': model.train_units, 'calibration_engines': model.calibration_units,
        'calibration_fraction': calibration_fraction,
        'conformal_adjustment_cycles': model.conformal_delta,
        'calibration_scores': dict(zip(map(str, model.calibration_units), model.calibration_scores)),
        'source_sha256': {name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
                          for name in FD001_FILES},
        'test': {'count': metrics['count'], 'rmse': metrics['rmse'],
                 'nasa_asymmetric_score': score, 'picp': metrics['two_sided_coverage'],
                 'mpiw': metrics['mean_width']},
        'notes': ('Engine-level maximum CQR scores address correlated cycles; the nominal '
                  'range concerns capped trajectories under exchangeability. Test scores '
                  'use official uncapped final RUL. Actual PICP is measured, not assumed. '
                  'Sorted quantiles, nonnegative support and point inclusion only expand '
                  'the conformal range. E-01 maps explicitly to FD001 test unit 1, etc.'),
    }
    tail_predictions = {
        str(int(row.unit)): {'rul_point': float(row.point), 'lower': float(row.lower),
                            'upper': float(row.upper), 'half_width': float((row.upper - row.lower) / 2)}
        for row in benchmark.itertuples(index=False)
    }
    output.mkdir(parents=True, exist_ok=True)
    # Dump strings/scalars, not transient native booster object state; two
    # identical runs produce byte-identical joblib caches and metrics JSON.
    joblib.dump({'format_version': 1, 'model': _model_payload(model),
                 'tail_predictions': tail_predictions}, output / 'rul_model.joblib',
                compress=0, protocol=5)
    (output / 'rul_metrics.json').write_bytes(canonical_json(report).encode('utf-8'))
    return report


def load_cached_model(path: Path = DEFAULT_CACHE) -> RULModel:
    """Restore a locally generated joblib model with its fitted feature schema."""
    bundle = joblib.load(path)
    if bundle.get('format_version') != 1:
        raise ValueError('Unsupported RUL cache format; rerun training')
    return _restore_model(bundle['model'])


def predict_tail(engine_id: int | str, model_path: Path = DEFAULT_CACHE) -> dict[str, float]:
    """Return the cached latest FD001 test-engine prediction in flight cycles.

    Integer/unit-string IDs and fictional E-NN aliases resolve explicitly to
    benchmark test units. This is a fixed offline snapshot, not live telemetry.
    Cache absence fails clearly instead of inventing a prediction.
    """
    if isinstance(engine_id, bool):
        raise KeyError(f'Unknown benchmark engine {engine_id!r}')
    match = re.fullmatch(r'(?:E-)?([0-9]+)', str(engine_id))
    if match is None:
        raise KeyError(f'Unknown benchmark engine {engine_id!r}')
    bundle = joblib.load(model_path)
    if bundle.get('format_version') != 1:
        raise ValueError('Unsupported RUL cache format; rerun training')
    key = str(int(match.group(1)))
    if key not in bundle['tail_predictions']:
        raise KeyError(f'Unknown benchmark engine {engine_id!r}')
    return dict(bundle['tail_predictions'][key])


def train_benchmark(root: Path) -> dict:
    """Generate grouped OOF, official-test scores, model and benchmark report."""
    from pdm.config import load_config
    from pdm.data.cmapss import SENSOR_COLUMNS, drop_constant_sensors, load_fd001
    config = load_config(root/'config/default.yaml')
    settings = config.model
    train, test, truth = load_fd001(root/'data/raw')
    sensors = tuple(s for s in SENSOR_COLUMNS if s not in drop_constant_sensors(train))
    windows, bins = tuple(settings.window_sizes), tuple(settings.predicted_rul_bins)
    x = features(train, sensors, windows)
    rng = np.random.default_rng(settings.lgbm.seed)
    folds, memberships = [], []
    for fold, (fit_indices, held_indices) in enumerate(GroupKFold(settings.cv_folds).split(x, groups=train.unit)):
        fitted = _fit(train.iloc[fit_indices], x.iloc[fit_indices], sensors, windows,
                      int(rng.integers(0, 2**31-1)), settings.lgbm.n_estimators, bins,
                      settings.rul_cap, settings.calibration_engine_fraction)
        predictions = _predict(fitted, x.iloc[held_indices])
        result = train.loc[predictions.index, ['unit', 'cycle', 'true_rul']].join(predictions)
        result['fold'] = fold
        folds.append(result)
        memberships.append({'fold':fold, 'train_units':fitted.train_units,
                            'calibration_units':fitted.calibration_units,
                            'evaluation_units':sorted(int(u) for u in result.unit.unique())})
    oof = pd.concat(folds).sort_values(['unit','cycle'], kind='stable').reset_index(drop=True)
    model = _fit(train, x, sensors, windows, settings.lgbm.seed, settings.lgbm.n_estimators,
                 bins, settings.rul_cap, settings.calibration_engine_fraction)
    all_test = predict(model, test)
    last = test.groupby('unit', sort=True).tail(1)
    benchmark = all_test.loc[last.index].copy()
    benchmark['true_rul'] = truth.rul.to_numpy()
    error = benchmark.point-benchmark.true_rul
    score = np.where(error < 0, np.expm1(-error/13), np.expm1(error/10)).sum()
    report = {'data_label':'NASA C-MAPSS FD001 benchmark; not aircraft performance',
              'config_hash':config.config_hash, 'source':'lightgbm', 'seed':settings.lgbm.seed,
              'oof':_metrics(oof), 'fold_membership':memberships,
              'bands':{}, 'checkpoints':{}, 'clipped_fraction':float(oof.clipped.mean()),
              'benchmark':{**_metrics(benchmark), 'nasa_asymmetric_score':float(score)},
              'notes':'Split conformal quantile regression, calibrated using maximum capped-target nonconformity per held-out engine. Nominal engine-level range; empirical benchmark coverage is reported, not assumed.'}
    for a,b,label in ((0,20,'0-20'),(20,40,'20-40'),(40,70,'40-70'),(70,np.inf,'70+')):
        report['bands'][label] = _metrics(oof[(oof.true_rul >= a)&(oof.true_rul < b)])
    for checkpoint in settings.eval_checkpoints_true_rul:
        subset = oof[oof.true_rul == checkpoint]
        report['checkpoints'][str(checkpoint)] = _metrics(subset) if len(subset) else {'count':0}
    processed, reports = root/'data/processed', root/'reports'
    processed.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    oof.to_csv(processed/'oof_predictions.csv', index=False, lineterminator='\n', float_format='%.12g')
    save_model(model, processed/'rul_model.json')
    (reports/'model_metrics.json').write_bytes(canonical_json(report).encode('utf-8'))
    return report
