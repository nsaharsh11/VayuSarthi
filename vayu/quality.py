"""CSV validation, explicit quarantine and idempotent SQLite integration."""
from dataclasses import asdict, dataclass, fields
import hashlib
import json
import math
from pathlib import Path
import sqlite3
from typing import Any, Mapping

import pandas as pd
from pydantic import ValidationError

from vayu.schemas import FLEET_SCHEMAS, PlanningState, Resource, Spare, Tail, canonical_json

SOURCES = ('fleet.csv', 'spares.csv', 'resources.csv', 'health_stream.csv')


@dataclass
class FleetQualityReport:
    """Annotated silo rows, accepted subset, quarantine and explicit hold.

    A Stale badge is advisory. Conflict denotes a hard validation failure;
    those rows never appear in accepted. Inspect planning_hold before using
    any accepted rows to construct a planning state.
    """

    frames: dict[str, pd.DataFrame]
    accepted: dict[str, pd.DataFrame]
    quarantine: pd.DataFrame
    planning_hold: bool
    reasons: tuple[str, ...]
    issues: tuple['QualityIssue', ...]


@dataclass(frozen=True)
class QualityIssue:
    """A rejected source row; its raw values are retained for review."""
    source: str
    row_number: int
    reason: str
    detail: str
    raw_json: str


@dataclass
class QualityReport:
    """Validated inputs and source-specific data-quality evidence."""
    state: PlanningState | None
    issues: tuple[QualityIssue, ...]
    frames: dict[str, pd.DataFrame]
    accepted_count: int
    total_count: int
    inputs_hash: str


def _int(value: Any) -> int:
    number = float(value)
    if not math.isfinite(number) or number != int(number):
        raise ValueError('Expected a finite integer')
    return int(number)


def _raw(row: dict[str, Any]) -> str:
    # CSV nonfinite input must still be retained as valid JSON quarantine evidence.
    return canonical_json({k:(None if v is pd.NA or v is pd.NaT else
                             str(v) if isinstance(v,float) and not math.isfinite(v) else v)
                           for k,v in row.items()})


def validate_fleet_pack(frames: dict[str, pd.DataFrame], today: int = 0,
                        required_tail_ids: tuple[str, ...] | None = None) -> FleetQualityReport:
    """Validate the four silos without mutating inputs or reading truth.

    By default every tail mentioned by tails or technical records is needed
    for planning. An explicit required_tail_ids narrows that set. Reject all
    duplicates, never guess a winner. A tail requires one valid health and
    technical record. Ages greater than seven days are soft Stale badges;
    invalid links/values are Conflict and quarantined. Days are absolute.
    """
    if isinstance(today, bool) or not isinstance(today, int) or today < 0:
        raise ValueError('today must be a nonnegative integer')
    if required_tail_ids is not None and any(
            not isinstance(tail, str) or not tail.strip() for tail in required_tail_ids):
        raise ValueError('Required tail IDs must be nonempty strings')
    inputs: dict[str, pd.DataFrame] = {}
    rows: dict[str, list[dict[str, Any]]] = {}
    faults: dict[str, list[list[tuple[str, str]]]] = {}
    issues: list[QualityIssue] = []
    hold: list[str] = []
    for source, schema in FLEET_SCHEMAS.items():
        columns = list(schema.model_fields)
        frame = frames.get(source)
        if frame is None:
            issues.append(QualityIssue(source, 0, 'MISSING_SOURCE', 'Required CSV is missing', '{}'))
            hold.append(f'{source}: required source missing')
            frame = pd.DataFrame(columns=columns)
        inputs[source] = frame.copy(deep=True).reset_index(drop=True)
        missing = sorted(set(columns) - set(frame.columns))
        if missing:
            detail = f'Missing columns: {", ".join(missing)}'
            issues.append(QualityIssue(source, 0, 'MISSING_COLUMNS', detail, '{}'))
            hold.append(f'{source}: {detail}')
        rows[source], faults[source] = [], []
        for raw in frame.to_dict('records'):
            row_faults: list[tuple[str, str]] = []
            row = raw.copy()
            try:
                row = schema.model_validate(raw).model_dump()
                if source == 'health.csv' and row['last_update_day'] > today:
                    row_faults.append(('FUTURE_RECORD', 'Health update is after today'))
            except ValidationError as error:
                # Avoid embedding implementation URLs or unstable exception reprs.
                detail = '; '.join(f'{".".join(map(str, item["loc"]))}: {item["msg"]}'
                                   for item in error.errors(include_url=False))
                row_faults.append(('MISSING_COLUMNS' if missing else 'INVALID_ROW', detail))
            rows[source].append(row)
            faults[source].append(row_faults)
        keys = ['tail_id', 'engine_id'] if source == 'tails.csv' else [columns[0]]
        for key in keys:
            if key not in frame:
                continue
            values = pd.Series([str(row.get(key, '')).strip() for row in rows[source]], dtype=str)
            for index in values.index[values.duplicated(keep=False)]:
                faults[source][index].append(('DUPLICATE_ID', f'Duplicate {key}; all copies rejected'))

    def valid_rows(source: str) -> list[dict[str, Any]]:
        """Return records surviving checks accumulated so far."""
        return [row for row, errors in zip(rows[source], faults[source]) if not errors]

    raw_tails = {str(row.get('tail_id', '')).strip() for row in rows['tails.csv']} - {''}
    raw_engines = {str(row.get('engine_id', '')).strip() for row in rows['tails.csv']} - {''}
    for source, key, known in (('tech_records.csv', 'tail_id', raw_tails),
                               ('health.csv', 'engine_id', raw_engines)):
        for index, row in enumerate(rows[source]):
            identifier = str(row.get(key, '')).strip()
            if identifier not in known:
                faults[source][index].append(('SILO_CONFLICT', f'{key} {identifier!r} missing from tails.csv'))
    health = {row['engine_id']: row for row in valid_rows('health.csv')}
    technical = {row['tail_id']: row for row in valid_rows('tech_records.csv')}
    for index, row in enumerate(rows['tails.csv']):
        if faults['tails.csv'][index]:
            continue
        if row['engine_id'] not in health:
            faults['tails.csv'][index].append(('SILO_CONFLICT', 'No valid linked health record'))
        if row['tail_id'] not in technical:
            faults['tails.csv'][index].append(('SILO_CONFLICT', 'No valid linked technical record'))

    required = (set(tail.strip() for tail in required_tail_ids) if required_tail_ids is not None
                else raw_tails | {str(row.get('tail_id', '')).strip()
                                  for row in rows['tech_records.csv']} - {''})
    good_tails = {row['tail_id'] for row in valid_rows('tails.csv')}
    if required_tail_ids is None and not raw_tails:
        hold.append('tails.csv: no planning tails provided')
    for tail in sorted(required - good_tails):
        hold.append(f'{tail}: planning tail missing or quarantined; repair its silo records')
    capacity = {row['resource']: row['count'] for row in valid_rows('resources.csv')}
    for kind in ('bay', 'crew'):
        if capacity.get(kind, 0) <= 0:
            hold.append(f'resources.csv: no valid {kind} capacity')

    annotated: dict[str, pd.DataFrame] = {}
    accepted: dict[str, pd.DataFrame] = {}
    rejected: list[dict[str, Any]] = []
    for source, schema in FLEET_SCHEMAS.items():
        badges, details = [], []
        for index, (row, errors) in enumerate(zip(rows[source], faults[source])):
            badge = 'Good'
            if errors:
                badge = 'Conflict'
                reason = '; '.join(dict.fromkeys(code for code, _ in errors))
                detail = '; '.join(message for _, message in errors)
                raw_json = _raw(inputs[source].iloc[index].to_dict())
                issues.append(QualityIssue(source, index + 2, reason, detail, raw_json))
                rejected.append({'source': source, 'row_number': index + 2,
                                 'tail_id': row.get('tail_id'), 'engine_id': row.get('engine_id'),
                                 'quality_badge': badge, 'reason': reason,
                                 'detail': detail, 'raw_json': raw_json})
                details.append(detail)
            else:
                snapshot = row if source == 'health.csv' else health.get(row.get('engine_id'))
                if snapshot is not None and today - snapshot['last_update_day'] > 7:
                    badge = 'Stale'
                details.append('Health update older than 7 days' if badge == 'Stale' else '')
            badges.append(badge)
        columns = list(inputs[source].columns)
        annotated[source] = pd.DataFrame(rows[source], columns=columns)
        annotated[source]['quality_badge'] = pd.Series(badges, dtype=str)
        annotated[source]['quality_detail'] = pd.Series(details, dtype=str)
        accepted[source] = annotated[source].loc[annotated[source].quality_badge != 'Conflict'].copy()
    quarantine = pd.DataFrame(rejected, columns=['source', 'row_number', 'tail_id', 'engine_id',
                                                'quality_badge', 'reason', 'detail', 'raw_json'])
    return FleetQualityReport(annotated, accepted, quarantine, bool(hold),
                              tuple(sorted(set(hold))), tuple(issues))


def read_fleet_pack(directory: Path, today: int = 0,
                    required_tail_ids: tuple[str, ...] | None = None) -> FleetQualityReport:
    """Read only the five specified CSVs, then apply the fleet quality gate."""
    frames: dict[str, pd.DataFrame] = {}
    read_issues: list[QualityIssue] = []
    for source in FLEET_SCHEMAS:
        path = directory / source
        if not path.is_file():
            continue
        try:
            frames[source] = pd.read_csv(path, keep_default_na=False)
        except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeError, OSError) as error:
            read_issues.append(QualityIssue(source, 0, 'BAD_CSV', str(error), '{}'))
    result = validate_fleet_pack(frames, today, required_tail_ids)
    result.issues = tuple(read_issues) + result.issues
    if read_issues:
        result.reasons = tuple(sorted(set(result.reasons) |
                                      {f'{issue.source}: unreadable CSV ({issue.reason})'
                                       for issue in read_issues}))
    return result


def planning_state_from_fleet(report: FleetQualityReport,
                             predictions: Mapping[str, Mapping[str, float]], *,
                             today: int = 0, horizon: int = 40, safety_buffer: float = 0,
                             duration: int = 3) -> PlanningState:
    """Join accepted silo rates to externally supplied believed RUL estimates.

    Health predictions must be keyed by engine ID. The adapter never reads
    evaluation values and refuses to construct planning inputs during a hold.
    Induction duration is an explicit assumed input absent from the silo CSVs.
    """
    if report.planning_hold:
        raise ValueError('Planning hold: ' + '; '.join(report.reasons))
    tails = []
    for row in report.accepted['tails.csv'].sort_values('tail_id').to_dict('records'):
        estimate = predictions.get(row['engine_id'])
        if estimate is None:
            raise ValueError(f"Missing RUL prediction for {row['engine_id']}")
        tails.append(Tail(row['tail_id'], estimate['rul_point'], estimate['lower'], estimate['upper'],
                          row['utilisation_cycles_per_day'], duration))
    spares = tuple(Spare(row['spare_id'], int(row['available_day']))
                   for row in report.accepted['spares.csv'].sort_values('spare_id').to_dict('records'))
    capacity = {row['resource']: int(row['count'])
                for row in report.accepted['resources.csv'].to_dict('records')}
    return PlanningState(tuple(tails), spares,
                         tuple(Resource(f'BAY-{i:02d}') for i in range(1, capacity['bay']+1)),
                         tuple(Resource(f'CREW-{i:02d}') for i in range(1, capacity['crew']+1)),
                         today=today, horizon=horizon, safety_buffer=safety_buffer)


def read_pack(directory: Path, today: int = 0, horizon: int = 40,
              safety_buffer: float = 2) -> QualityReport:
    """Validate believed inputs only; never open simulation_truth.json."""
    issues: list[QualityIssue] = []
    frames: dict[str,pd.DataFrame] = {}
    entities: dict[str,list] = {'fleet.csv':[], 'spares.csv':[], 'resources.csv':[]}
    digest = hashlib.sha256()
    digest.update(canonical_json({'today':today,'horizon':horizon,'safety_buffer':safety_buffer}).encode())
    total = 0
    tail_fields = {field.name for field in fields(Tail)}
    for source in SOURCES:
        path = directory/source
        digest.update(source.encode())
        if not path.is_file():
            issues.append(QualityIssue(source,0,'MISSING_SOURCE','Required CSV is missing','{}'))
            frames[source] = pd.DataFrame()
            continue
        digest.update(path.read_bytes())
        try:
            frame = pd.read_csv(path,keep_default_na=False)
        except (pd.errors.ParserError,pd.errors.EmptyDataError,UnicodeError) as error:
            issues.append(QualityIssue(source,0,'BAD_CSV',str(error),'{}'))
            frames[source] = pd.DataFrame()
            continue
        total += len(frame)
        key = {'fleet.csv':['tail_id'],'spares.csv':['spare_id'],
               'resources.csv':['kind','resource_id'],'health_stream.csv':['tail_id','cycle']}[source]
        missing_keys = not set(key) <= set(frame)
        duplicates = frame.duplicated(key,keep=False) if not missing_keys else pd.Series(False,index=frame.index)
        accepted = []
        for index,row in enumerate(frame.to_dict('records')):
            reason = 'INVALID_ROW'
            try:
                if missing_keys:
                    raise ValueError('Missing required ID columns')
                if duplicates.iloc[index]:
                    reason = 'DUPLICATE_ID'
                    raise ValueError('Conflicting or duplicated entity; all duplicates quarantined')
                if {'truth','true_rul','failure_cycle','actual_available_day'} & set(row):
                    raise ValueError('Evaluation fields are not accepted as planning inputs')
                if source == 'fleet.csv':
                    data = {name:row[name] for name in tail_fields}
                    data['duration'] = _int(data['duration'])
                    for name in ('rul_point','lower','upper','rate'):
                        data[name] = float(data[name])
                    if _int(row.get('updated_day',today)) > today:
                        raise ValueError('Future-dated estimate')
                    entity = Tail(**data)
                elif source == 'spares.csv':
                    entity = Spare(str(row['spare_id']),_int(row['available_day']),str(row['part_number']))
                elif source == 'resources.csv':
                    if row['kind'] not in ('bay','crew'):
                        raise ValueError('Resource kind must be bay or crew')
                    entity = (row['kind'],Resource(str(row['resource_id']),_int(row['free_day'])))
                else:
                    if row['tail_id'] not in {tail.tail_id for tail in entities['fleet.csv']}:
                        raise ValueError('Health row has no validated fleet tail')
                    cycle = _int(row['cycle'])
                    lower,point,upper = (float(row[name]) for name in ('lower','point','upper'))
                    if cycle < 1 or not all(math.isfinite(v) for v in (lower,point,upper)) or not 0 <= lower <= point <= upper:
                        raise ValueError('Invalid health cycle or interval')
                    entity = None
                if entity is not None:
                    entities[source].append(entity)
                accepted.append(row)
            except (KeyError,TypeError,ValueError,OverflowError) as error:
                issues.append(QualityIssue(source,index+2,reason,str(error),_raw(row)))
        frames[source] = pd.DataFrame(accepted,columns=frame.columns)
    bays = tuple(resource for kind,resource in entities['resources.csv'] if kind == 'bay')
    crews = tuple(resource for kind,resource in entities['resources.csv'] if kind == 'crew')
    state = None
    if bays and crews:
        state = PlanningState(tuple(entities['fleet.csv']),tuple(entities['spares.csv']),bays,crews,
                              today,horizon,safety_buffer)
    else:
        issues.append(QualityIssue('resources.csv',0,'MISSING_CAPACITY','Need a valid bay and crew','{}'))
    return QualityReport(state,tuple(issues),frames,sum(len(f) for f in frames.values()),total,digest.hexdigest())


def ingest_pack(database: Path, directory: Path, today: int = 0, horizon: int = 40,
                safety_buffer: float = 2) -> QualityReport:
    """Integrate accepted records and preserve quarantine by immutable run hash."""
    report = read_pack(directory,today,horizon,safety_buffer)
    database.parent.mkdir(parents=True,exist_ok=True)
    with sqlite3.connect(database) as connection:
        connection.executescript('''
            CREATE TABLE IF NOT EXISTS ingest_runs (run_hash TEXT PRIMARY KEY, accepted INTEGER, rejected INTEGER);
            CREATE TABLE IF NOT EXISTS accepted_rows (run_hash TEXT, source TEXT, row_number INTEGER, row_json TEXT,
                PRIMARY KEY(run_hash,source,row_number));
            CREATE TABLE IF NOT EXISTS quarantine (run_hash TEXT, source TEXT, row_number INTEGER, reason TEXT,
                detail TEXT, raw_json TEXT, PRIMARY KEY(run_hash,source,row_number,reason));
        ''')
        connection.execute('INSERT OR IGNORE INTO ingest_runs VALUES (?,?,?)',
                           (report.inputs_hash,report.accepted_count,len(report.issues)))
        for source,frame in report.frames.items():
            connection.executemany('INSERT OR IGNORE INTO accepted_rows VALUES (?,?,?,?)',
                [(report.inputs_hash,source,index,_raw(row)) for index,row in enumerate(frame.to_dict('records'))])
        connection.executemany('INSERT OR IGNORE INTO quarantine VALUES (?,?,?,?,?,?)',
            [(report.inputs_hash,issue.source,issue.row_number,issue.reason,issue.detail,issue.raw_json)
             for issue in report.issues])
    return report
