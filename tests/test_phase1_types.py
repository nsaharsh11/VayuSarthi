import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from pdm.config import load_config
from pdm.types import (
    Agency, AgencyTruth, DataDegradation, Estimate, Job, Placement, Plan,
    PlanningState, PlanSummary, RunMetrics, RunResult, Scenario,
    ScenarioBeliefs, ScenarioTruth, SimulationEvent, SpareTruth, SpareUnit,
    Tail, TailTruth, TechRecord,
)


@pytest.fixture
def objects():
    config = load_config()
    estimate = Estimate(low=3, point=5, high=8, age_days=0, source='rule_fallback')
    tail = Tail(tail_id='TAIL-01', engine_unit=1, part_number='PN-ENG-A', initial_cycle=30,
                status='OPERATING', planning_rul=3, estimate=estimate)
    spare = SpareUnit(unit_id='SP-01', part_number='PN-ENG-A', believed_available_day=0, announce_day=0)
    agency = Agency(agency_id='A-01', bays_per_day=(1,) * 80, techs_per_day=(2,) * 80, transit_days=1)
    job = Job(job_id='J-TAIL-01', tail_id=tail.tail_id, part_number=tail.part_number,
              duration=3, techs_required=2, mode='JIT', earliest_day=0, deadline_day=2)
    placement = Placement(job_id=job.job_id, tail_id=tail.tail_id, mode='JIT',
                          deadline_day=2, start_day=2, end_day=5, agency_id=agency.agency_id,
                          spare_unit_id=spare.unit_id, status='ON_TIME', binding_constraint='NONE',
                          duration=3, techs_required=2, transit_days=1)
    summary = PlanSummary(late_jobs=0, unscheduled_jobs=0, total_days_late=0, jobs_total=1)
    plan = Plan(placements=(placement,), summary=summary, inputs_hash='a' * 64)
    state = PlanningState(today=0, horizon_end=39, tails=(tail,), spares=(spare,), agencies=(agency,),
                          committed_placements=(), config=config)
    record = TechRecord(tail_id=tail.tail_id, engine_serial='E-01', part_number=tail.part_number,
                        open_defects=0, cycles_since_overhaul=30, record_age_days=0)
    truth = ScenarioTruth(tails=(TailTruth(tail_id=tail.tail_id, failure_cycle=40),),
                          spares=(SpareTruth(unit_id=spare.unit_id, actual_available_day=7),),
                          agencies=(AgencyTruth(agency_id=agency.agency_id, bays_per_day=(1,) * 80,
                                                techs_per_day=(2,) * 80, transit_days=1),))
    degradation = DataDegradation(missing_part_number_probability=.35, health_feed_gaps=(), stale_record_ages=())
    beliefs = ScenarioBeliefs(tails=(tail,), spares=(spare,), agencies=(agency,), tech_records=(record,),
                              degradation=degradation, estimate_bias_cycles=12)
    scenario = Scenario(scenario_id='phase1-test', stratum='adverse_late_spare', seed=1,
                        config_hash=config.config_hash, horizon=40, truth=truth, beliefs=beliefs)
    metrics = RunMetrics(availability=.5, operating_tail_days=20, aog_days=17, planned_maint_days=3,
                         unplanned_failures=1, planned_actions=1, unused_life_cycles=5, start_blocked_events=1)
    event = SimulationEvent(day=0, event_type='PLAN_CREATED', tail_id=tail.tail_id)
    result = RunResult(scenario_id=scenario.scenario_id, stratum=scenario.stratum, seed=1,
                       policy='range', config_hash=config.config_hash, metrics=metrics, events=(event,))
    return locals()


def all_property_names(value):
    if isinstance(value, dict):
        yield from value
        yield from value.get('properties', {})
        for nested in value.values():
            yield from all_property_names(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from all_property_names(nested)


def test_planning_state_has_no_truth_fields(objects):
    forbidden = {'truth', 'failure_cycle', 'true_rul', 'actual_available_day'}
    assert not forbidden.intersection(all_property_names(PlanningState.model_json_schema()))
    assert not forbidden.intersection(all_property_names(objects['state'].model_dump(mode='json')))
    for key in ('failure_cycle', 'true_rul', 'truth'):
        data = objects['state'].model_dump(mode='json')
        data[key] = 10
        with pytest.raises(ValidationError):
            PlanningState.model_validate(data)
        tail_data = objects['tail'].model_dump(mode='json')
        tail_data[key] = 10
        with pytest.raises(ValidationError):
            Tail.model_validate(tail_data)


@pytest.mark.parametrize('name', ['tail', 'spare', 'agency', 'estimate', 'job', 'placement', 'plan', 'state', 'scenario', 'result', 'truth', 'beliefs', 'metrics'])
def test_frozen_core_types_reject_mutation(objects, name):
    instance = objects[name]
    field = next(iter(type(instance).model_fields))
    with pytest.raises(ValidationError):
        setattr(instance, field, getattr(instance, field))


def test_nested_collections_are_immutable(objects):
    with pytest.raises(TypeError):
        objects['agency'].bays_per_day[0] = 8
    with pytest.raises(AttributeError):
        objects['state'].tails.append(objects['tail'])
    with pytest.raises(ValidationError):
        objects['scenario'].truth.tails[0].failure_cycle = 100


def test_scenario_round_trip_and_separation(objects):
    scenario = objects['scenario']
    encoded = scenario.model_dump_json()
    assert Scenario.model_validate_json(encoded) == scenario
    assert Scenario.model_validate_json(encoded).model_dump_json() == encoded
    payload = json.loads(encoded)
    assert payload['truth']['spares'][0]['actual_available_day'] == 7
    assert payload['beliefs']['spares'][0]['believed_available_day'] == 0
    assert not {'failure_cycle', 'actual_available_day', 'true_rul'}.intersection(all_property_names(ScenarioBeliefs.model_json_schema()))
    assert 'failure_cycle' not in json.dumps(payload['beliefs'])
    assert 'actual_available_day' not in json.dumps(payload['beliefs'])


def test_all_core_types_round_trip(objects):
    for name in ('tail', 'spare', 'agency', 'estimate', 'job', 'placement', 'plan', 'state', 'scenario', 'result'):
        value = objects[name]
        assert type(value).model_validate_json(value.model_dump_json()) == value


def test_invalid_capacity_and_job_rejected(objects):
    with pytest.raises(ValidationError):
        Agency(agency_id='A', bays_per_day=(1,), techs_per_day=(-1,))
    with pytest.raises(ValidationError):
        Agency(agency_id='A', bays_per_day=(1,), techs_per_day=(2, 2))
    data = objects['job'].model_dump()
    data['duration'] = 0
    with pytest.raises(ValidationError):
        Job.model_validate(data)


def test_missing_placement_has_no_reserved_resources(objects):
    data = objects['placement'].model_dump()
    data.update(status='UNSCHEDULED', binding_constraint='NO_SPARE', start_day=None, end_day=None,
                agency_id=None, spare_unit_id=None)
    assert Placement.model_validate(data).start_day is None
    data['start_day'] = 0
    with pytest.raises(ValidationError):
        Placement.model_validate(data)


def test_scenario_entity_keys_must_match(objects):
    data = objects['scenario'].model_dump()
    data['truth']['tails'][0]['tail_id'] = 'TAIL-99'
    with pytest.raises(ValidationError):
        Scenario.model_validate(data)


def test_static_ground_truth_firewall():
    root = Path(__file__).resolve().parents[1] / 'src/pdm'
    for package in ('planner', 'policies'):
        for path in (root / package).rglob('*.py'):
            source = path.read_text(encoding='utf-8')
            assert 'failure_cycle' not in source, path
            assert 'true_rul' not in source, path
            assert 'scenario.truth' not in source, path
