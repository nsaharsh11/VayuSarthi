"""Offline FD001 loader; target construction stays outside planner inputs."""
from pathlib import Path

import numpy as np
import pandas as pd

from pdm.config import ROOT, load_config
from pdm.data.check import FILES, check_data

SENSOR_COLUMNS = tuple(f's{i}' for i in range(1, 22))
COLUMNS = ('unit', 'cycle', 'op1', 'op2', 'op3', *SENSOR_COLUMNS)


def load_fd001(directory: str | Path = ROOT / 'data/raw') -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Return (train, test, rul). RUL rows carry explicit test-engine IDs.

    Train alone includes the uncapped true_rul target. No files are rewritten,
    no synthetic rows are supplied, and no downloads are attempted.
    """
    directory = Path(directory)
    missing = [name for name in FILES if not (directory / name).is_file()]
    if missing:
        raise FileNotFoundError(f'Missing FD001 files in {directory}: {", ".join(missing)}')
    result = check_data(directory)
    if not result.ok:
        raise ValueError(result.message)
    dtypes = {column: 'float64' for column in COLUMNS}
    dtypes.update(unit='int64', cycle='int64')
    train, test = (
        pd.read_csv(directory / name, sep=r'\s+', header=None, names=COLUMNS, dtype=dtypes)
        .sort_values(['unit', 'cycle'], kind='stable').reset_index(drop=True)
        for name in ('train_FD001.txt', 'test_FD001.txt')
    )
    train['true_rul'] = train.groupby('unit')['cycle'].transform('max') - train['cycle']
    rul = pd.read_csv(directory / 'RUL_FD001.txt', sep=r'\s+', header=None, names=['rul'], dtype='int64')
    rul.insert(0, 'unit', sorted(test['unit'].unique()))
    return train, test, rul


def drop_constant_sensors(train_df: pd.DataFrame, threshold: float | None = None) -> list[str]:
    """Return sensor names whose population variance is below the threshold.

    Despite the historical function name, the caller's frame is not modified.
    Only training values determine the selection, in canonical sensor order.
    """
    if threshold is None:
        threshold = load_config().model.constant_sensor_variance_threshold
    if not np.isfinite(threshold) or threshold < 0:
        raise ValueError('Constant sensor variance threshold must be finite and non-negative')
    sensors = train_df.loc[:, SENSOR_COLUMNS]
    if sensors.empty or not np.isfinite(sensors.to_numpy(dtype=float)).all():
        raise ValueError('Sensor values must be nonempty and finite')
    variances = sensors.var(axis=0, ddof=0)
    return [sensor for sensor in SENSOR_COLUMNS if variances[sensor] < threshold]
