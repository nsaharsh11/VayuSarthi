"""Immutable planner contracts; no evaluation-only fields are accepted."""
from dataclasses import asdict, dataclass, is_dataclass
import json
import math
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

DATA_LABEL = 'Fictional simulated fleet. NASA C-MAPSS benchmark replay; no live aircraft data.'


class FleetCSVRow(BaseModel):
    """Frozen silo row: unknown fields and nonfinite numbers are hard failures."""

    model_config = ConfigDict(extra='forbid', frozen=True, allow_inf_nan=False,
                              str_strip_whitespace=True)

    @field_validator('*', mode='before')
    @classmethod
    def reject_booleans(cls, value: Any) -> Any:
        """CSV numbers and identifiers must not silently accept boolean values."""
        if isinstance(value, bool):
            raise ValueError('Boolean values are not CSV numbers or identifiers')
        return value


class TailCSV(FleetCSVRow):
    """Fictional aircraft-to-engine association and cycles/day utilisation."""

    tail_id: str = Field(min_length=1)
    utilisation_cycles_per_day: float = Field(ge=1.5, le=3.0)
    engine_id: str = Field(min_length=1)


class HealthCSV(FleetCSVRow):
    """Engine health snapshot age, expressed in nonnegative simulation days."""

    engine_id: str = Field(min_length=1)
    last_update_day: int = Field(ge=0)


class TechRecordCSV(FleetCSVRow):
    """Tail technical record with nonnegative integral cycles and snag count."""

    tail_id: str = Field(min_length=1)
    cycles_since_overhaul: int = Field(ge=0)
    open_snags: int = Field(ge=0)


class SpareCSV(FleetCSVRow):
    """One spare engine's believed availability day."""

    spare_id: str = Field(min_length=1)
    available_day: int = Field(ge=0)


class ResourceCSV(FleetCSVRow):
    """Aggregate bay/crew capacity; shift hours are descriptive metadata."""

    resource: Literal['bay', 'crew']
    count: int = Field(ge=0)
    shift_hours: float = Field(gt=0, le=24)


FLEET_SCHEMAS: dict[str, type[FleetCSVRow]] = {
    'tails.csv': TailCSV,
    'health.csv': HealthCSV,
    'tech_records.csv': TechRecordCSV,
    'spares.csv': SpareCSV,
    'resources.csv': ResourceCSV,
}


def canonical_json(value: Any) -> str:
    """Encode reproducibly without wall-clock timestamps or nonfinite values."""
    return json.dumps(asdict(value) if is_dataclass(value) else value,
                      sort_keys=True, separators=(',', ':'), allow_nan=False)


def _integer(value: int, name: str, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f'{name} must be an integer >= {minimum}')


@dataclass(frozen=True)
class Tail:
    """A planning estimate in cycles with its individual cycles/day rate."""
    tail_id: str
    rul_point: float
    lower: float
    upper: float
    rate: float
    duration: int
    part_number: str = 'PN-ENG-A'

    def __post_init__(self) -> None:
        if not self.tail_id or not self.part_number:
            raise ValueError('Tail and part IDs are required')
        if not all(math.isfinite(v) for v in (self.rul_point, self.lower, self.upper, self.rate)):
            raise ValueError('Estimates and rate must be finite')
        if not 0 <= self.lower <= self.rul_point <= self.upper or self.rate <= 0:
            raise ValueError('Require 0 <= lower <= point <= upper and positive rate')
        _integer(self.duration, 'duration', 1)


@dataclass(frozen=True)
class Spare:
    """An unused consumable engine with believed availability."""
    spare_id: str
    available_day: int
    part_number: str = 'PN-ENG-A'

    def __post_init__(self) -> None:
        if not self.spare_id or not self.part_number:
            raise ValueError('Spare and part IDs are required')
        _integer(self.available_day, 'available_day')


@dataclass(frozen=True)
class Resource:
    """A bay or a whole technician crew, free from the named day onward."""
    resource_id: str
    free_day: int = 0

    def __post_init__(self) -> None:
        if not self.resource_id:
            raise ValueError('Resource ID is required')
        _integer(self.free_day, 'free_day')


@dataclass(frozen=True)
class PlanningState:
    """Believed scheduling inputs only; horizon is an inclusive spare cutoff."""
    tails: tuple[Tail, ...]
    spares: tuple[Spare, ...]
    bays: tuple[Resource, ...]
    crews: tuple[Resource, ...]
    today: int = 0
    horizon: int = 40
    safety_buffer: float = 2

    def __post_init__(self) -> None:
        _integer(self.today, 'today')
        _integer(self.horizon, 'horizon')
        if self.horizon < self.today or not math.isfinite(self.safety_buffer) or self.safety_buffer < 0:
            raise ValueError('Invalid horizon or safety buffer')
        if not self.bays or not self.crews:
            raise ValueError('At least one bay and one crew are required')
        for values, key in ((self.tails, 'tail_id'), (self.spares, 'spare_id'),
                            (self.bays, 'resource_id'), (self.crews, 'resource_id')):
            if not isinstance(values, tuple):
                raise ValueError('Collections must be immutable tuples')
            ids = [getattr(item, key) for item in values]
            if len(ids) != len(set(ids)):
                raise ValueError('Duplicate entity IDs')


@dataclass(frozen=True)
class Placement:
    """An induction interval [start_day,end_day), or an unplanned tail."""
    tail_id: str
    deadline_day: int
    start_day: int | None
    end_day: int | None
    bay: str | None
    crew: str | None
    spare: str | None
    status: str
    binding: str | None
    reason_code: str = ''


@dataclass(frozen=True)
class PlannerConfig:
    """Absolute planning days, flight-cycle buffer and default induction duration."""
    today: int = 0
    horizon: int = 40
    safety_buffer: float = 2
    duration: int = 3

    def __post_init__(self) -> None:
        _integer(self.today, 'today')
        _integer(self.horizon, 'horizon')
        _integer(self.duration, 'duration', 1)
        if self.horizon < self.today or not math.isfinite(self.safety_buffer) or self.safety_buffer < 0:
            raise ValueError('Invalid horizon or safety buffer')


@dataclass(frozen=True)
class PinnedPlacement:
    """An immutable induction reservation; status/deadline remain derived values."""
    tail_id: str
    start_day: int
    bay: str
    crew: str
    spare: str

    def __post_init__(self) -> None:
        _integer(self.start_day, 'Pinned start_day')
        if any(not isinstance(value, str) or not value for value in
               (self.tail_id, self.bay, self.crew, self.spare)):
            raise ValueError('Pinned tail and resource IDs must be nonempty strings')


@dataclass(frozen=True)
class Plan:
    """Deterministic placements and a hash of sorted planning inputs."""
    placements: tuple[Placement, ...]
    inputs_hash: str
