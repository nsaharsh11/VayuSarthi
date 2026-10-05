"""Append-only hash chains and explicit human decisions."""
import sqlite3
import hashlib
import json
import pytest

from vayu.audit import AuditLog
from vayu.planner import plan
from vayu.schemas import Tail, Spare, Resource, PlanningState


def test_demo_reset_releases_only_its_scope_and_preserves_history(tmp_path):
    from vayu.schemas import PinnedPlacement
    state = PlanningState((Tail('A',10,8,12,1,3),),(Spare('S',0),),(Resource('B'),),(Resource('C'),))
    other = PlanningState((Tail('Z',10,8,12,1,3),),state.spares,state.bays,state.crews)
    log = AuditLog(tmp_path/'reset.db')
    source = log.ensure_plan(plan(state), 'day-0')
    other_source = log.ensure_plan(plan(other), 'day-0')
    for scope, inputs, tail in ((source,state,'A'), (other_source,other,'Z')):
        pinned = plan(inputs, pinned_placements=(PinnedPlacement(tail,3,'B','C','S'),))
        log.review_placement(scope,pinned,tail,'Reviewer','PIN','Keep placement','day-0')
    before = log.rows()
    log.reset_demo(source, user='prototype', reason='User requested Reset demo', timestamp='day-0')
    assert log.pins_for(source) == ()
    assert log.pins_for(other_source)[0].tail_id == 'Z'
    assert log.rows()[1:] == before
    reset = log.rows()[0]
    assert reset['action'] == 'DEMO_RESET' and json.loads(reset['after']) == []
    assert json.loads(reset['before'])[0]['tail_id'] == 'A'
    assert AuditLog(log.path).pins_for(source) == () and log.verify_chain() is None
    pinned = plan(state, pinned_placements=(PinnedPlacement('A',4,'B','C','S'),))
    log.review_placement(source,pinned,'A','Reviewer','PIN','New reservation','day-0')
    assert log.pins_for(source)[0].start_day == 4
    before = log.rows()
    with pytest.raises(ValueError, match='source'):
        log.reset_demo('unknown', user='prototype', reason='Reset', timestamp='day-0')
    assert log.rows() == before
    with sqlite3.connect(log.path) as connection:
        connection.execute('DROP TRIGGER audit_no_update')
        connection.execute("UPDATE audit_log SET reason='altered' WHERE seq=1")
    before = log.rows()
    with pytest.raises(ValueError, match='chain'):
        log.reset_demo(source, user='prototype', reason='Reset', timestamp='day-0')
    assert log.rows() == before


def test_requested_fields_and_every_explicit_replan(tmp_path):
    from vayu.schemas import PinnedPlacement
    state = PlanningState((Tail('A',10,8,12,1,3),),(Spare('S',0),),(Resource('B'),),(Resource('C'),))
    path = tmp_path/'replans.db'
    log = AuditLog(path)
    first = log.replan(state, user='Demo', cause='Initial clean pack', timestamp='day-0')
    source = first.inputs_hash
    pinned = plan(state, pinned_placements=(PinnedPlacement('A', 3, 'B', 'C', 'S'),))
    log.review_placement(source, pinned, 'A', 'Demo', 'PIN', 'Keep day three', 'day-0', before_plan=first)
    restored = AuditLog(path).replan(state, user='Demo', cause='Reload with stored pins',
                                   timestamp='day-1', source_plan_id=source, before=first)
    assert restored.placements[0].start_day == 3
    # Repeating an explicitly requested replan still records its cause.
    log.replan(state, user='Demo', cause='Second explicit replan', timestamp='day-1', source_plan_id=source)
    rows = log.rows()
    assert all({'timestamp','user','action','tail','before','after','reason'} <= row.keys() for row in rows)
    events = [row for row in rows if row['action'] == 'REPLAN']
    assert len(events) == 4
    assert {row['reason'] for row in events} >= {'Initial clean pack', 'Reload with stored pins', 'Second explicit replan'}
    pin = next(row for row in rows if row['action'] == 'PIN')
    assert (pin['user'], pin['tail'], pin['reason']) == ('Demo', 'A', 'Keep day three')
    assert json.loads(pin['before'])['start_day'] == 1
    assert json.loads(pin['after'])['start_day'] == 3
    assert log.verify_chain() is None
    before = log.rows()
    with pytest.raises(ValueError, match='cause'):
        log.replan(state, user='Demo', cause=' ', timestamp='day-0')
    assert log.rows() == before


@pytest.mark.parametrize('column', ['timestamp','user','action','tail','before','after','reason',
                                    'event_key','payload_json','actor','chain_version'])
def test_all_stored_event_content_is_chained(tmp_path, column):
    path = tmp_path/'tamper.db'
    log = AuditLog(path)
    log.append_event(timestamp='day-0', user='Reviewer', action='APPROVE', tail='A',
                     before={'start':1}, after={'start':1}, reason='Reviewed fictional plan')
    assert log.verify_chain() is None
    with sqlite3.connect(path) as connection:
        connection.execute('DROP TRIGGER audit_no_update')
        connection.execute(f'UPDATE audit_log SET "{column}"=? WHERE seq=1', ('altered',))
    assert log.verify_chain() == 1
    with pytest.raises(ValueError, match='chain'):
        log.pins_for('any-source')


def test_additive_legacy_migration_preserves_history(tmp_path):
    from vayu.schemas import canonical_json
    path = tmp_path/'legacy.db'
    payload = {'accepted':3}
    body = canonical_json({'ts':'day-0','actor':'legacy','event_type':'INGEST_RUN','payload':payload})
    digest = hashlib.sha256(('0'*64+body).encode()).hexdigest()
    with sqlite3.connect(path) as connection:
        connection.execute('CREATE TABLE audit_log (seq INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'ts TEXT NOT NULL, actor TEXT NOT NULL, event_type TEXT NOT NULL, '
                           'payload_json TEXT NOT NULL, prev_hash TEXT NOT NULL, row_hash TEXT NOT NULL, event_key TEXT UNIQUE)')
        connection.execute('INSERT INTO audit_log VALUES (1,?,?,?,?,?,?,?)',
                           ('day-0','legacy','INGEST_RUN',canonical_json(payload),'0'*64,digest,'legacy-key'))
    log = AuditLog(path)
    assert log.verify_chain() is None
    log.append_event(timestamp='day-1', user='Demo', action='REPLAN', tail=None,
                     before=None, after={'placements':[]}, reason='Refresh inputs')
    assert log.verify_chain() is None
    with sqlite3.connect(path) as connection:
        assert connection.execute('SELECT row_hash FROM audit_log WHERE seq=1').fetchone()[0] == digest
        assert connection.execute('SELECT prev_hash FROM audit_log WHERE seq=2').fetchone()[0] == digest
        with pytest.raises(sqlite3.IntegrityError, match='append-only'):
            connection.execute('DELETE FROM audit_log')


def test_append_only_and_tamper_detection(tmp_path):
    path = tmp_path/'audit.db'
    log = AuditLog(path)
    log.append('day-0','test','INGEST_RUN',{'accepted':3})
    log.append('day-0','test','COUNTERFACTUAL_RUN',{'changed':False})
    assert log.verify_chain() is None
    for query in ('UPDATE audit_log SET actor="bad" WHERE seq=1','DELETE FROM audit_log WHERE seq=1',
                  'INSERT OR REPLACE INTO audit_log SELECT * FROM audit_log WHERE seq=1'):
        with sqlite3.connect(path) as connection, pytest.raises(sqlite3.IntegrityError,match='append-only'):
            connection.execute(query)
    with sqlite3.connect(path) as connection:
        connection.execute('DROP TRIGGER audit_no_update')
        connection.execute('UPDATE audit_log SET payload_json=? WHERE seq=2',('{"changed":true}',))
    assert log.verify_chain() == 2


def test_fixed_timestamp_produces_identical_rows_and_atomic_failures(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    state = PlanningState((Tail('A',10,8,12,1,3),),(Spare('S',0),),(Resource('B'),),(Resource('C'),))
    logs = [AuditLog(tmp_path/f'{name}.db') for name in ('a', 'b')]
    for log in logs:
        log.replan(state, user='Demo', cause='Clean input', timestamp='day-0')
        before = log.rows()
        with pytest.raises(ValueError, match='Timestamp'):
            log.record_replan(None, plan(state), user='Demo', cause='Invalid timestamp', timestamp=' ')
        assert log.rows() == before
    assert logs[0].rows() == logs[1].rows()
    # Concurrent writers must each chain from the committed preceding event.
    def append(index):
        logs[0].append_event(timestamp='day-0', user='Demo', action='REVIEW', tail='A',
                             before=index, after=index, reason='Concurrent fictional review')
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(append, range(8)))
    assert logs[0].verify_chain() is None and len(logs[0].rows()) == 10


def test_plan_idempotence_and_officer_required(tmp_path):
    log = AuditLog(tmp_path/'audit.db')
    state = PlanningState((Tail('A',10,8,12,1,3),),(Spare('S',0),),(Resource('B'),),(Resource('C'),))
    scheduled = plan(state)
    plan_id = log.ensure_plan(scheduled,'day-0')
    assert log.ensure_plan(scheduled,'day-0') == plan_id
    assert len(log.rows()) == 1
    for officer,decision in (('','APPROVE'),('  ','REJECT'),('Name','WRONG')):
        with pytest.raises(ValueError):
            log.decide(plan_id,officer,decision,'','day-0')
    assert log.plan_status(plan_id) == 'PROPOSED'
    log.decide(plan_id,'Demo officer','APPROVE','Reviewed','day-0')
    assert log.plan_status(plan_id) == 'APPROVED'
    assert log.verify_chain() is None
    with pytest.raises(ValueError):
        log.decide(plan_id,'Demo officer','REJECT','','day-0')


def test_invalid_event_and_unknown_plan(tmp_path):
    log = AuditLog(tmp_path/'audit.db')
    with pytest.raises(ValueError):
        log.append('day-0','','INGEST_RUN',{})
    with pytest.raises(ValueError):
        log.decide('missing','Officer','APPROVE','','day-0')


def test_placement_review_requires_actor_reason_and_pins_persist(tmp_path):
    log = AuditLog(tmp_path/'placements.db')
    state = PlanningState((Tail('A',10,8,12,1,3),),(Spare('S',0),),(Resource('B'),),(Resource('C'),))
    scheduled = plan(state)
    source = log.ensure_plan(scheduled, 'day-0')
    for actor, reason in (('', 'Reviewed'), ('Name', ''), ('Name', '  ')):
        with pytest.raises(ValueError):
            log.review_placement(source, scheduled, 'A', actor, 'PIN', reason, 'day-0')
    assert log.pins_for(source) == ()
    log.review_placement(source, scheduled, 'A', 'Name', 'PIN', 'Hold this placement', 'day-0')
    assert log.pins_for(source)[0].start_day == scheduled.placements[0].start_day
    assert log.pins_for('different-inputs') == ()
    log.review_placement(source, scheduled, 'A', 'Name', 'REJECT', 'Needs another review', 'day-0')
    assert log.pins_for(source)  # Review does not silently release a pinned resource.
    assert log.verify_chain() is None
    with pytest.raises(ValueError):
        log.review_placement(source, scheduled, 'MISSING', 'Name', 'PIN', 'Reviewed', 'day-0')
    with pytest.raises(ValueError):
        log.decide(source, 'Name', 'APPROVE', '', 'day-0')
    from dataclasses import replace
    changed = plan(replace(state, safety_buffer=0))
    before = log.rows()
    with pytest.raises(ValueError, match='source plan'):
        log.review_placement('missing', changed, 'A', 'Name', 'PIN', 'Reviewed', 'day-0')
    assert log.rows() == before
