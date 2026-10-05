"""Immutable core contracts; observed beliefs and simulator truth stay separate."""
from typing import Annotated, Literal

from pydantic import Field, model_validator

from pdm._base import FrozenModel
from pdm.config import Config

Identifier = Annotated[str, Field(min_length=1)]
PositiveInt = Annotated[int, Field(gt=0)]
NonnegativeInt = Annotated[int, Field(ge=0)]
ContentHash = Annotated[str, Field(pattern=r'^[0-9a-f]{64}$')]
Stratum = Literal['unconstrained', 'spare_constrained', 'tech_constrained', 'data_degraded',
                  'adverse_bias_high', 'adverse_bias_low', 'adverse_late_spare']
PolicyName = Literal['reactive', 'reactive_late_warning', 'point', 'range', 'point_margin']
Mode = Literal['JIT', 'ASAP']
BindingConstraint = Literal['NONE', 'NO_SPARE', 'NO_SLOT', 'NO_TECH', 'DATA_HOLD', 'DEADLINE']


class Estimate(FrozenModel):
    low: float = Field(ge=0)
    point: float = Field(ge=0)
    high: float = Field(ge=0)
    age_days: int = Field(ge=0)
    source: Literal['lightgbm', 'rule_fallback']

    @model_validator(mode='after')
    def ordered(self):
        if not self.low <= self.point <= self.high:
            raise ValueError('Estimate must satisfy low <= point <= high')
        return self


class Tail(FrozenModel):
    """Identity, replay position and observations visible to a planner."""
    tail_id: Identifier
    engine_unit: PositiveInt
    part_number: Identifier | None
    initial_cycle: NonnegativeInt
    status: Literal['OPERATING', 'FAILED', 'PLANNED_MAINT', 'AOG'] = 'OPERATING'
    planning_rul: float | None = None
    planning_hold: bool = False
    open_defects: NonnegativeInt = 0
    estimate: Estimate | None = None
    manual_resolved: bool = False


class SpareUnit(FrozenModel):
    """Believed spare availability only; actual dates belong to ScenarioTruth."""
    unit_id: Identifier
    part_number: Identifier
    believed_available_day: int
    announce_day: NonnegativeInt = 0
    assigned: bool = False


class Agency(FrozenModel):
    """Believed calendars indexed by absolute simulation day, beginning at zero."""
    agency_id: Identifier
    bays_per_day: tuple[NonnegativeInt, ...] = Field(min_length=1)
    techs_per_day: tuple[NonnegativeInt, ...] = Field(min_length=1)
    transit_days: NonnegativeInt = 0
    closed_days: tuple[NonnegativeInt, ...] = ()
    name: str = ''

    @model_validator(mode='after')
    def matching_calendars(self):
        if len(self.bays_per_day) != len(self.techs_per_day):
            raise ValueError('Bay and technician calendars must have matching lengths')
        if len(set(self.closed_days)) != len(self.closed_days):
            raise ValueError('Closed days must be unique')
        return self


class Job(FrozenModel):
    job_id: Identifier
    tail_id: Identifier
    part_number: Identifier | None
    duration: PositiveInt
    techs_required: PositiveInt
    mode: Mode
    earliest_day: NonnegativeInt
    deadline_day: int


class BlockedByCounts(FrozenModel):
    NO_SPARE: NonnegativeInt = 0
    NO_SLOT: NonnegativeInt = 0
    NO_TECH: NonnegativeInt = 0


class Placement(FrozenModel):
    job_id: Identifier
    tail_id: Identifier
    mode: Mode
    deadline_day: int
    status: Literal['ON_TIME', 'LATE', 'UNSCHEDULED', 'DATA_HOLD']
    binding_constraint: BindingConstraint
    start_day: NonnegativeInt | None = None
    end_day: NonnegativeInt | None = None
    agency_id: Identifier | None = None
    spare_unit_id: Identifier | None = None
    duration: PositiveInt
    techs_required: PositiveInt
    transit_days: NonnegativeInt = 0
    displacement_days: NonnegativeInt = 0
    days_late: NonnegativeInt = 0
    blocked_by_counts: BlockedByCounts = Field(default_factory=BlockedByCounts)
    message: str = ''

    @model_validator(mode='after')
    def placement_shape(self):
        reservation = (self.start_day, self.end_day, self.agency_id, self.spare_unit_id)
        if self.status in ('UNSCHEDULED', 'DATA_HOLD'):
            if any(value is not None for value in reservation):
                raise ValueError('Unplaced jobs must not reserve dates or resources')
        else:
            if any(value is None for value in reservation):
                raise ValueError('Placed jobs require dates, agency and spare')
            if self.end_day != self.start_day + self.transit_days + self.duration - 1:
                raise ValueError('End day must include transit and duration, inclusively')
            if self.status == 'ON_TIME' and self.start_day > self.deadline_day:
                raise ValueError('ON_TIME starts must not exceed the deadline')
            if self.status == 'LATE' and self.start_day <= self.deadline_day:
                raise ValueError('LATE starts must exceed the deadline')
        return self


class PlanSummary(FrozenModel):
    late_jobs: NonnegativeInt
    unscheduled_jobs: NonnegativeInt
    total_days_late: NonnegativeInt
    jobs_total: NonnegativeInt


class Plan(FrozenModel):
    placements: tuple[Placement, ...]
    summary: PlanSummary
    inputs_hash: ContentHash
    status: Literal['PROPOSED', 'APPROVED', 'REJECTED'] = 'PROPOSED'


def unique_keys(items, attribute):
    keys = tuple(getattr(item, attribute) for item in items)
    if len(set(keys)) != len(keys):
        raise ValueError(f'Duplicate {attribute} values')
    return set(keys)


class PlanningState(FrozenModel):
    """Only observed state and beliefs; contains no simulator truth."""
    today: NonnegativeInt
    horizon_end: NonnegativeInt
    tails: tuple[Tail, ...]
    spares: tuple[SpareUnit, ...]
    agencies: tuple[Agency, ...]
    committed_placements: tuple[Placement, ...] = ()
    config: Config

    @model_validator(mode='after')
    def snapshot_shape(self):
        if self.today > self.horizon_end:
            raise ValueError('Today must not exceed the planning horizon')
        tail_ids = unique_keys(self.tails, 'tail_id')
        spare_ids = unique_keys(self.spares, 'unit_id')
        agency_ids = unique_keys(self.agencies, 'agency_id')
        unique_keys(self.committed_placements, 'job_id')
        for placement in self.committed_placements:
            if placement.status not in ('ON_TIME', 'LATE'):
                raise ValueError('Only started placements can be committed')
            if placement.start_day > self.today or placement.end_day < self.today:
                raise ValueError('Committed placements must be active today')
            if (placement.tail_id not in tail_ids or placement.agency_id not in agency_ids
                    or placement.spare_unit_id not in spare_ids):
                raise ValueError('Committed placement references an unknown entity')
        return self


class TailTruth(FrozenModel):
    tail_id: Identifier
    failure_cycle: PositiveInt


class SpareTruth(FrozenModel):
    unit_id: Identifier
    actual_available_day: int


class AgencyTruth(Agency):
    """Actual resource calendar, stored exclusively inside ScenarioTruth."""


class ScenarioTruth(FrozenModel):
    tails: tuple[TailTruth, ...]
    spares: tuple[SpareTruth, ...]
    agencies: tuple[AgencyTruth, ...]


class TechRecord(FrozenModel):
    tail_id: Identifier
    engine_serial: Identifier
    part_number: Identifier | None
    open_defects: NonnegativeInt = 0
    cycles_since_overhaul: NonnegativeInt = 0
    record_age_days: NonnegativeInt = 0


class HealthFeedGap(FrozenModel):
    tail_id: Identifier
    start_day: NonnegativeInt
    end_day: NonnegativeInt

    @model_validator(mode='after')
    def interval(self):
        if self.end_day < self.start_day:
            raise ValueError('Health gap end must not precede its start')
        return self


class StaleRecordAge(FrozenModel):
    tail_id: Identifier
    age_days: NonnegativeInt


class DataDegradation(FrozenModel):
    missing_part_number_probability: float = Field(default=0, ge=0, le=1)
    health_feed_gaps: tuple[HealthFeedGap, ...] = ()
    stale_record_ages: tuple[StaleRecordAge, ...] = ()


class ScenarioBeliefs(FrozenModel):
    tails: tuple[Tail, ...]
    spares: tuple[SpareUnit, ...]
    agencies: tuple[Agency, ...]
    tech_records: tuple[TechRecord, ...] = ()
    degradation: DataDegradation = Field(default_factory=DataDegradation)
    estimate_bias_cycles: float = 0


class Scenario(FrozenModel):
    scenario_id: Identifier
    stratum: Stratum
    seed: NonnegativeInt
    config_hash: ContentHash
    horizon: PositiveInt
    truth: ScenarioTruth
    beliefs: ScenarioBeliefs

    @model_validator(mode='after')
    def matching_entities(self):
        for name, attribute in (('tails', 'tail_id'), ('spares', 'unit_id'), ('agencies', 'agency_id')):
            if unique_keys(getattr(self.truth, name), attribute) != unique_keys(getattr(self.beliefs, name), attribute):
                raise ValueError(f'Truth and beliefs must contain matching {name} identities')
        tail_ids = {tail.tail_id for tail in self.beliefs.tails}
        for records in (self.beliefs.tech_records, self.beliefs.degradation.health_feed_gaps,
                        self.beliefs.degradation.stale_record_ages):
            if any(record.tail_id not in tail_ids for record in records):
                raise ValueError('Record references an unknown tail')
        return self


class RunMetrics(FrozenModel):
    availability: float = Field(ge=0, le=1)
    operating_tail_days: NonnegativeInt
    aog_days: NonnegativeInt
    planned_maint_days: NonnegativeInt
    unplanned_failures: NonnegativeInt
    planned_actions: NonnegativeInt
    unused_life_cycles: NonnegativeInt
    start_blocked_events: NonnegativeInt


class SimulationEvent(FrozenModel):
    day: NonnegativeInt
    event_type: Literal['FAILURE', 'PLAN_CREATED', 'START', 'COMPLETION', 'START_BLOCKED']
    tail_id: Identifier | None = None
    job_id: Identifier | None = None
    spare_unit_id: Identifier | None = None
    agency_id: Identifier | None = None
    message: str = ''


class RunResult(FrozenModel):
    scenario_id: Identifier
    stratum: Stratum
    seed: NonnegativeInt
    policy: PolicyName
    config_hash: ContentHash
    metrics: RunMetrics
    events: tuple[SimulationEvent, ...] = ()
