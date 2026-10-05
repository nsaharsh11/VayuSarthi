"""Validated configuration with canonical, content-addressed hashes."""
from datetime import date
import hashlib
import json
from pathlib import Path
from typing import Annotated, Literal

from pydantic import Field, model_validator
import yaml

from pdm._base import FrozenModel

ROOT = Path(__file__).resolve().parents[2]
PositiveInt = Annotated[int, Field(gt=0)]
NonnegativeInt = Annotated[int, Field(ge=0)]
Ordering = Literal['deadline_tail', 'deadline_tail_desc', 'longest_first', 'least_slack_first']


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def validate_grid(grid):
    start, end, step = grid
    if start < 0 or end < start or step <= 0 or (end - start) % step:
        raise ValueError('Grid requires nonnegative start, end >= start, positive step and reachable end')


class SeedRanges(FrozenModel):
    dev: tuple[NonnegativeInt, NonnegativeInt]
    tuning: tuple[NonnegativeInt, NonnegativeInt]
    report: tuple[NonnegativeInt, NonnegativeInt]

    @model_validator(mode='after')
    def disjoint(self):
        intervals = list(self.model_dump().values())
        if any(a > b for a, b in intervals):
            raise ValueError('Seed range start must not exceed end')
        for i, (a, b) in enumerate(intervals):
            for c, d in intervals[i + 1:]:
                if max(a, c) <= min(b, d):
                    raise ValueError('Dev, tuning and report seed ranges must be disjoint')
        return self


class Fleet(FrozenModel):
    n_tails: PositiveInt
    horizon_days: PositiveInt
    cycles_per_day: PositiveInt
    start_date: date
    tail_prefix: str = Field(min_length=1)
    part_numbers: tuple[str, ...] = Field(min_length=1)

    @model_validator(mode='after')
    def unique_parts(self):
        if len(set(self.part_numbers)) != len(self.part_numbers) or any(not p.strip() for p in self.part_numbers):
            raise ValueError('Part numbers must be nonempty and unique')
        return self


class InitialRul(FrozenModel):
    min: PositiveInt
    max: PositiveInt
    min_history_cycles: PositiveInt

    @model_validator(mode='after')
    def interval(self):
        if self.min > self.max:
            raise ValueError('Initial RUL min must not exceed max')
        return self


class Maintenance(FrozenModel):
    planned_duration_days: PositiveInt
    unplanned_extra_days: NonnegativeInt
    defect_extra_days_per_defect: NonnegativeInt
    techs_required: PositiveInt
    max_overrun_days: NonnegativeInt
    manual_resolution_delay_days: NonnegativeInt


class Policy(FrozenModel):
    safety_buffer_days: NonnegativeInt
    reactive_late_warning_cycles: NonnegativeInt
    range_low_quantile: float = Field(gt=0, lt=1)
    range_high_quantile: float = Field(gt=0, lt=1)
    margin_grid: tuple[int, int, int]

    @model_validator(mode='after')
    def ranges(self):
        validate_grid(self.margin_grid)
        if not self.range_low_quantile < .5 < self.range_high_quantile:
            raise ValueError('Range quantiles must straddle the median')
        return self


class LightGBM(FrozenModel):
    n_estimators: PositiveInt
    learning_rate: float = Field(gt=0, le=1)
    num_leaves: int = Field(ge=2)
    seed: NonnegativeInt


class Model(FrozenModel):
    rul_cap: PositiveInt
    constant_sensor_variance_threshold: float = Field(default=1e-12, ge=0)
    cv_folds: int = Field(ge=2)
    calibration_engine_fraction: float = Field(gt=0, lt=1)
    window_sizes: tuple[PositiveInt, ...] = Field(min_length=1)
    predicted_rul_bins: tuple[NonnegativeInt, ...] = Field(min_length=2)
    eval_checkpoints_true_rul: tuple[NonnegativeInt, ...] = Field(min_length=1)
    lgbm: LightGBM

    @model_validator(mode='after')
    def increasing(self):
        for sequence in (self.window_sizes, self.predicted_rul_bins, self.eval_checkpoints_true_rul):
            if any(a >= b for a, b in zip(sequence, sequence[1:])):
                raise ValueError('Windows, bins and checkpoints must be strictly increasing')
        if self.predicted_rul_bins[0] != 0 or self.predicted_rul_bins[-1] <= self.rul_cap:
            raise ValueError('Predicted RUL bins must start at zero and extend beyond the cap')
        return self


class Health(FrozenModel):
    ema_alpha: float = Field(gt=0, le=1)
    trend_window_cycles: int = Field(ge=2)


class Quality(FrozenModel):
    fresh_days: PositiveInt
    stale_decay_multiple: float = Field(gt=1)


class Costs(FrozenModel):
    expedite_per_day_advanced: float = Field(ge=0)
    extra_tech_per_tech_day: float = Field(ge=0)
    unit: str = Field(min_length=1)


class Sweep(FrozenModel):
    rul_grid: tuple[int, int, int]
    orderings: tuple[Ordering, ...] = Field(min_length=1)

    @model_validator(mode='after')
    def valid(self):
        validate_grid(self.rul_grid)
        if len(set(self.orderings)) != len(self.orderings):
            raise ValueError('Orderings must be unique')
        return self


class Evaluation(FrozenModel):
    bootstrap_resamples: PositiveInt
    bootstrap_seed: NonnegativeInt
    tie_epsilon: float = Field(ge=0)


class Config(FrozenModel):
    seed_ranges: SeedRanges
    fleet: Fleet
    initial_true_rul_cycles: InitialRul
    maintenance: Maintenance
    policy: Policy
    model: Model
    health: Health
    quality: Quality
    costs: Costs
    sweep: Sweep
    eval: Evaluation

    @property
    def config_hash(self) -> str:
        return hashlib.sha256(canonical_json(self.model_dump(mode='json')).encode('utf-8')).hexdigest()


def load_config(path: str | Path = ROOT / 'config/default.yaml') -> Config:
    with Path(path).open(encoding='utf-8') as handle:
        return Config.model_validate(yaml.safe_load(handle))
