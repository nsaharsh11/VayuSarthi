import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
from pydantic import ValidationError

from pdm.config import Config, load_config

ROOT = Path(__file__).resolve().parents[1]


def test_config_round_trip():
    config = load_config(ROOT / 'config/default.yaml')
    restored = Config.model_validate_json(config.model_dump_json())
    assert restored == config
    assert restored.config_hash == config.config_hash
    assert len(config.config_hash) == 64


def test_hash_stable_across_processes():
    command = [sys.executable, '-m', 'pdm.cli', 'config']
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
    first = subprocess.check_output(command, cwd=ROOT, env=env)
    second = subprocess.check_output(command, cwd=ROOT, env=env)
    assert first == second
    assert json.loads(first)['config_hash'] == load_config().config_hash


@pytest.mark.parametrize('section,key,value', [
    ('fleet', 'cycles_per_day', 0),
    ('maintenance', 'planned_duration_days', -1),
    ('model', 'calibration_engine_fraction', 1),
    ('health', 'ema_alpha', 0),
    ('quality', 'stale_decay_multiple', 1),
    ('policy', 'range_low_quantile', .95),
    ('model', 'predicted_rul_bins', [0, 20, 10]),
    ('model', 'window_sizes', [5, 5]),
    ('sweep', 'rul_grid', [0, 80, 0]),
    ('sweep', 'orderings', ['unknown']),
    ('initial_true_rul_cycles', 'min', 100),
    ('fleet', 'part_numbers', ['PN-ENG-A', 'PN-ENG-A']),
])
def test_invalid_config(section, key, value):
    data = load_config().model_dump(mode='json')
    data[section][key] = value
    with pytest.raises(ValidationError):
        Config.model_validate(data)


def test_seed_ranges_disjoint():
    config = load_config()
    ranges = [set(range(a, b + 1)) for a, b in config.seed_ranges.model_dump().values()]
    assert not (ranges[0] & ranges[1] or ranges[0] & ranges[2] or ranges[1] & ranges[2])
    data = config.model_dump(mode='json')
    data['seed_ranges']['report'] = [99, 2000]
    with pytest.raises(ValidationError):
        Config.model_validate(data)


def test_hash_changes_with_parameter():
    data = load_config().model_dump(mode='json')
    data['fleet']['horizon_days'] += 1
    assert Config.model_validate(data).config_hash != load_config().config_hash


def test_unknown_config_key_rejected():
    data = load_config().model_dump(mode='json')
    data['fleet']['horizen_days'] = 10
    with pytest.raises(ValidationError):
        Config.model_validate(data)
