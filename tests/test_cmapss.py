from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from pdm.data.cmapss import COLUMNS, SENSOR_COLUMNS, drop_constant_sensors, load_fd001

RAW = Path(__file__).resolve().parents[1] / 'data/raw'


@pytest.fixture(scope='module')
def dataset():
    return load_fd001(RAW)


def test_real_loader_shapes_and_columns(dataset):
    train, test, rul = dataset
    expected = ['unit', 'cycle', 'op1', 'op2', 'op3'] + [f's{i}' for i in range(1, 22)]
    assert list(COLUMNS) == expected
    assert list(train.columns) == expected + ['true_rul']
    assert list(test.columns) == expected
    assert list(rul.columns) == ['unit', 'rul']
    assert train['unit'].nunique() == test['unit'].nunique() == 100
    assert len(rul) == 100
    assert train.shape[1] == 27 and test.shape[1] == 26
    assert list(rul['unit']) == sorted(test['unit'].unique())
    assert all(pd.api.types.is_integer_dtype(train[name]) for name in ('unit', 'cycle', 'true_rul'))


def test_train_rul_ends_at_zero_and_decrements(dataset):
    train, _, _ = dataset
    for _, engine in train.groupby('unit'):
        assert engine.iloc[-1]['true_rul'] == 0
        assert (engine['cycle'].diff().dropna() == 1).all()
        assert (engine['true_rul'].diff().dropna() == -1).all()
        np.testing.assert_array_equal(engine['true_rul'], engine['cycle'].max() - engine['cycle'])


def test_constant_sensors_computed_and_deterministic(dataset):
    train, _, _ = dataset
    original = train.copy(deep=True)
    dropped = drop_constant_sensors(train)
    assert isinstance(dropped, list) and dropped
    assert set(dropped) <= set(SENSOR_COLUMNS)
    assert dropped == drop_constant_sensors(train.copy())
    # Deliberately vary a detected column and flatten a retained column using real rows.
    changed = train.copy()
    changed[dropped[0]] = np.arange(len(changed), dtype=float)
    retained = next(sensor for sensor in SENSOR_COLUMNS if sensor not in dropped)
    changed[retained] = changed[retained].iloc[0]
    recomputed = drop_constant_sensors(changed)
    assert dropped[0] not in recomputed
    assert retained in recomputed
    pd.testing.assert_frame_equal(train, original)


def test_repeat_load_is_identical(dataset):
    for initial, repeated in zip(dataset, load_fd001(RAW)):
        pd.testing.assert_frame_equal(initial, repeated)


def test_missing_data_never_substituted(tmp_path):
    with pytest.raises(FileNotFoundError, match='FD001'):
        load_fd001(tmp_path)


def test_sensor_selection_requires_valid_threshold(dataset):
    with pytest.raises(ValueError):
        drop_constant_sensors(dataset[0], threshold=-1)
    with pytest.raises(ValueError):
        drop_constant_sensors(dataset[0], threshold=float('nan'))


def test_loader_does_not_connect_to_network(monkeypatch):
    import socket

    def forbid(*args, **kwargs):
        raise AssertionError('Network use is prohibited')

    monkeypatch.setattr(socket, 'create_connection', forbid)
    load_fd001(RAW)
