"""Local append-only audit chain and explicit human plan approval."""
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
import sqlite3
from typing import Any

from vayu.schemas import PinnedPlacement, Plan, PlanningState, canonical_json

GENESIS = '0'*64
EVENT_TYPES = {'INGEST_RUN','PLAN_GENERATED','PLAN_APPROVAL','COUNTERFACTUAL_RUN',
               'PLACEMENT_REVIEW', 'REPLAN', 'AUDIT_EVENT', 'DEMO_RESET'}
EVENT_COLUMNS = ('timestamp', 'user', 'action', 'tail', 'before', 'after', 'reason')
HASH_COLUMNS = ('ts', 'actor', 'event_type', 'payload_json', 'event_key',
                *EVENT_COLUMNS, 'chain_version')


class AuditLog:
    """Use transactions to keep plan decisions and audit entries consistent."""

    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True,exist_ok=True)
        with sqlite3.connect(path) as connection:
            connection.executescript('''
                CREATE TABLE IF NOT EXISTS audit_log (seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts TEXT NOT NULL, actor TEXT NOT NULL, event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL, prev_hash TEXT NOT NULL, row_hash TEXT NOT NULL,
                    event_key TEXT UNIQUE);
                CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit_log
                    BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
                CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit_log
                    BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
                CREATE TRIGGER IF NOT EXISTS audit_no_replace BEFORE INSERT ON audit_log
                    WHEN EXISTS (SELECT 1 FROM audit_log WHERE seq=NEW.seq OR
                                 (NEW.event_key IS NOT NULL AND event_key=NEW.event_key))
                    BEGIN SELECT RAISE(ABORT, 'audit_log is append-only'); END;
                CREATE TABLE IF NOT EXISTS proposed_plans (plan_id TEXT PRIMARY KEY,
                    plan_json TEXT NOT NULL, status TEXT NOT NULL);
            ''')
            # Add columns without updating or re-signing historical events.
            # Version 1 retains its original hash; all new rows use version 2.
            connection.execute('BEGIN IMMEDIATE')
            columns = {row[1] for row in connection.execute('PRAGMA table_info(audit_log)')}
            for name in EVENT_COLUMNS:
                if name not in columns:
                    connection.execute(f'ALTER TABLE audit_log ADD COLUMN "{name}" TEXT')
            if 'chain_version' not in columns:
                connection.execute('ALTER TABLE audit_log ADD COLUMN chain_version INTEGER NOT NULL DEFAULT 1')

    @staticmethod
    def _append(connection: sqlite3.Connection, ts: str, actor: str, event_type: str,
                payload: dict[str,Any], event_key: str | None = None,
                *, details: dict[str, Any] | None = None) -> None:
        if not ts.strip() or not actor.strip() or event_type not in EVENT_TYPES:
            raise ValueError('Timestamp, actor and supported event type required')
        if event_key and connection.execute('SELECT 1 FROM audit_log WHERE event_key=?',(event_key,)).fetchone():
            return
        row = connection.execute('SELECT row_hash FROM audit_log ORDER BY seq DESC LIMIT 1').fetchone()
        previous = row[0] if row else GENESIS
        details = details or {
            'action': payload.get('decision', event_type), 'tail': payload.get('tail_id'),
            'before': payload.get('before'), 'after': payload.get('after', payload),
            'reason': payload.get('reason') or payload.get('note') or payload.get('cause')
                      or event_type.replace('_', ' ').capitalize()}
        event = {'ts': ts, 'actor': actor, 'event_type': event_type,
                 'payload_json': canonical_json(payload), 'event_key': event_key,
                 'timestamp': ts, 'user': actor, 'action': details['action'],
                 'tail': details['tail'], 'before': canonical_json(details['before']),
                 'after': canonical_json(details['after']), 'reason': details['reason'],
                 'chain_version': 2}
        body = canonical_json(event)
        row_hash = hashlib.sha256((previous+body).encode('utf-8')).hexdigest()
        columns = (*HASH_COLUMNS, 'prev_hash', 'row_hash')
        names = ','.join(f'"{name}"' for name in columns)
        parameters = ','.join('?' for _ in columns)
        event.update(prev_hash=previous, row_hash=row_hash)
        connection.execute(f'INSERT INTO audit_log ({names}) VALUES ({parameters})',
                           tuple(event[name] for name in columns))

    def append_event(self, *, timestamp: str, user: str, action: str, tail: str | None,
                     before: Any, after: Any, reason: str) -> None:
        """Append requested audit fields; snapshots are canonical JSON, never SQL text.

        Timestamp is explicit (logical day or caller-supplied ISO time). A null
        tail denotes a whole-fleet event. Every explicit call adds a new event.
        """
        user, action, reason = user.strip(), action.strip(), reason.strip()
        if not user or not action or not reason or (tail is not None and not tail.strip()):
            raise ValueError('User, action, reason and a nonempty tail when supplied required')
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            self._append(connection, timestamp, user, 'AUDIT_EVENT', {}, details={
                'action': action, 'tail': tail, 'before': before, 'after': after, 'reason': reason})

    def record_replan(self, before: Plan | None, after: Plan, *, user: str,
                      cause: str, timestamp: str) -> str:
        """Atomically persist the resulting proposal and the replan's explicit cause."""
        user, cause = user.strip(), cause.strip()
        if not user or not cause:
            raise ValueError('User and nonempty replan cause required')
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            plan_id = self._ensure_plan(connection, after, timestamp)
            self._append(connection, timestamp, user, 'REPLAN', {
                'plan_id': plan_id, 'cause': cause,
                'before': asdict(before) if before else None, 'after': asdict(after)})
        return plan_id

    def replan(self, state: PlanningState, *, user: str, cause: str, timestamp: str,
               source_plan_id: str | None = None, before: Plan | None = None) -> Plan:
        """Run the deterministic planner with stored pins and audit every invocation.

        By default pins belong to the original unpinned input hash. Supply its
        source_plan_id to keep that scope when explicitly changing planning inputs.
        Pure sensitivity probes continue to use vayu.planner.plan directly.
        """
        from vayu.planner import plan
        if not user.strip() or not cause.strip():
            raise ValueError('User and nonempty replan cause required')
        original = plan(state)
        pins = self.pins_for(source_plan_id or original.inputs_hash)
        scheduled = plan(state, pinned_placements=pins) if pins else original
        self.record_replan(before, scheduled, user=user, cause=cause, timestamp=timestamp)
        return scheduled

    def append(self, ts: str, actor: str, event_type: str, payload: dict[str,Any],
               event_key: str | None = None) -> None:
        """Append at an explicit logical timestamp; optional key deduplicates reruns."""
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            self._append(connection,ts,actor,event_type,payload,event_key)

    def ensure_plan(self, scheduled: Plan, ts: str) -> str:
        """Persist a PROPOSED plan once; never approve automatically."""
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            return self._ensure_plan(connection, scheduled, ts)

    @classmethod
    def _ensure_plan(cls, connection: sqlite3.Connection, scheduled: Plan, ts: str) -> str:
        """Persist and audit a plan inside the caller's existing transaction."""
        plan_id,encoded = scheduled.inputs_hash,canonical_json(scheduled)
        existing = connection.execute('SELECT plan_json FROM proposed_plans WHERE plan_id=?',(plan_id,)).fetchone()
        if existing:
            if existing[0] != encoded:
                raise ValueError('Stored plan differs for identical input hash')
        else:
            connection.execute('INSERT INTO proposed_plans VALUES (?,?,?)',(plan_id,encoded,'PROPOSED'))
            cls._append(connection,ts,'prototype','PLAN_GENERATED',
                        {'plan_id':plan_id,'placements':len(scheduled.placements),
                         'reason': 'New proposal for these planning inputs',
                         'before': None, 'after': asdict(scheduled)},'plan:'+plan_id)
        return plan_id

    def plan_status(self, plan_id: str) -> str:
        """Read the local decision state without treating it as execution."""
        with sqlite3.connect(self.path) as connection:
            row = connection.execute('SELECT status FROM proposed_plans WHERE plan_id=?',(plan_id,)).fetchone()
        if row is None:
            raise ValueError('Unknown plan')
        return row[0]

    def decide(self, plan_id: str, officer: str, decision: str, note: str, ts: str) -> None:
        """Record a single officer's APPROVE/REJECT decision atomically."""
        officer = officer.strip()
        note = note.strip()
        if not officer or not note or decision not in ('APPROVE','REJECT'):
            raise ValueError('User name, reason and APPROVE/REJECT decision required')
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            row = connection.execute('SELECT status FROM proposed_plans WHERE plan_id=?',(plan_id,)).fetchone()
            if row is None or row[0] != 'PROPOSED':
                raise ValueError('Only an existing PROPOSED plan can be decided')
            status = 'APPROVED' if decision == 'APPROVE' else 'REJECTED'
            connection.execute('UPDATE proposed_plans SET status=? WHERE plan_id=?',(status,plan_id))
            self._append(connection,ts,officer,'PLAN_APPROVAL',
                         {'plan_id':plan_id,'decision':decision,'note':note,
                          'before': {'status': row[0]}, 'after': {'status': status}})

    def review_placement(self, source_plan_id: str, scheduled: Plan, tail_id: str,
                         actor: str, decision: str, reason: str, ts: str,
                         *, before_plan: Plan | None = None) -> None:
        """Audit a placement review; PIN persists its exact resource reservation.

        source_plan_id identifies the original unpinned input snapshot. Callers
        validate any edited pin using the planner before recording this event.
        Approve/reject are human annotations and do not release existing pins.
        """
        actor, reason = actor.strip(), reason.strip()
        if not actor or not reason or decision not in ('APPROVE', 'REJECT', 'PIN'):
            raise ValueError('User name, reason and APPROVE/REJECT/PIN decision required')
        placement = next((p for p in scheduled.placements if p.tail_id == tail_id), None)
        if placement is None:
            raise ValueError('Unknown placement tail')
        if decision == 'PIN' and placement.start_day is None:
            raise ValueError('An Unplanned tail has no placement to pin')
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            source = connection.execute('SELECT plan_json FROM proposed_plans WHERE plan_id=?',
                                        (source_plan_id,)).fetchone()
            if source is None:
                raise ValueError('Unknown source plan')
            before = json.loads(canonical_json(before_plan)) if before_plan else json.loads(source[0])
            prior = next((p for p in before['placements'] if p['tail_id'] == tail_id), None)
            plan_id = self._ensure_plan(connection, scheduled, ts)
            self._append(connection, ts, actor, 'PLACEMENT_REVIEW', {
                'source_plan_id': source_plan_id, 'plan_id': plan_id, 'tail_id': tail_id,
                'decision': decision, 'reason': reason, 'before': prior, 'after': asdict(placement),
                'placement': {'tail_id': tail_id, 'start_day': placement.start_day,
                              'bay': placement.bay, 'crew': placement.crew, 'spare': placement.spare}})
            if decision == 'PIN':
                self._append(connection, ts, actor, 'REPLAN', {
                    'source_plan_id': source_plan_id, 'plan_id': plan_id, 'tail_id': tail_id,
                    'cause': f'Pinned placement for {tail_id}: {reason}',
                    'before': before, 'after': asdict(scheduled)})

    def reset_demo(self, source_plan_id: str, *, user: str, reason: str, timestamp: str) -> None:
        """Release this demo snapshot's pins through a new event, preserving history.

        Other input snapshots and later PIN events retain their reservations.
        A broken chain or unknown source prevents the reset from being recorded.
        """
        user, reason = user.strip(), reason.strip()
        if not user or not reason:
            raise ValueError('User and reset reason required')
        pins = self.pins_for(source_plan_id)
        with sqlite3.connect(self.path) as connection:
            connection.execute('BEGIN IMMEDIATE')
            if not connection.execute('SELECT 1 FROM proposed_plans WHERE plan_id=?',
                                      (source_plan_id,)).fetchone():
                raise ValueError('Unknown source plan')
            self._append(connection,timestamp,user,'DEMO_RESET',{
                'source_plan_id':source_plan_id,'reason':reason,
                'before':[asdict(pin) for pin in pins],'after':[]})

    def pins_for(self, source_plan_id: str) -> tuple[PinnedPlacement, ...]:
        """Restore pins after the latest explicit demo reset for this input hash."""
        broken = self.verify_chain()
        if broken is not None:
            raise ValueError(f'Audit chain is broken at sequence {broken}; stored pins cannot be trusted')
        with sqlite3.connect(self.path) as connection:
            rows = connection.execute("SELECT event_type,payload_json FROM audit_log "
                                      "WHERE event_type IN ('PLACEMENT_REVIEW','DEMO_RESET') ORDER BY seq").fetchall()
        pins: dict[str, PinnedPlacement] = {}
        for event_type, encoded in rows:
            payload = json.loads(encoded)
            if payload['source_plan_id'] != source_plan_id:
                continue
            if event_type == 'DEMO_RESET':
                pins.clear()
            elif payload['decision'] == 'PIN':
                pins[payload['tail_id']] = PinnedPlacement(**payload['placement'])
        return tuple(pins[key] for key in sorted(pins))

    def rows(self, limit: int = 100) -> list[dict[str,Any]]:
        """Return recent audit rows, newest first."""
        if not isinstance(limit,int) or limit < 1:
            raise ValueError('Positive row limit required')
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute('SELECT * FROM audit_log ORDER BY seq DESC LIMIT ?',(limit,)).fetchall()
        result = [dict(row) for row in rows]
        for row in result:
            if row['chain_version'] == 1:
                # Display projection only: do not rewrite historical database content.
                payload = json.loads(row['payload_json'])
                row.update(timestamp=row['ts'], user=row['actor'],
                           action=payload.get('decision', row['event_type']),
                           tail=payload.get('tail_id'), before=canonical_json(payload.get('before')),
                           after=canonical_json(payload.get('after', payload)),
                           reason=payload.get('reason') or payload.get('note') or 'Legacy event; cause not recorded')
        return result

    def verify_chain(self) -> int | None:
        """Return the first broken sequence, or None for a valid local chain."""
        with sqlite3.connect(self.path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute('SELECT * FROM audit_log ORDER BY seq').fetchall()
        previous,expected_seq = GENESIS,1
        for row in rows:
            seq = row['seq']
            try:
                payload = json.loads(row['payload_json'])
                if row['payload_json'] != canonical_json(payload):
                    return seq
                if row['chain_version'] == 1:
                    if any(row[name] is not None for name in EVENT_COLUMNS):
                        return seq
                    body = canonical_json({'ts':row['ts'],'actor':row['actor'],
                                           'event_type':row['event_type'],'payload':payload})
                elif row['chain_version'] == 2:
                    for name in ('before', 'after'):
                        if row[name] != canonical_json(json.loads(row[name])):
                            return seq
                    body = canonical_json({name: row[name] for name in HASH_COLUMNS})
                else:
                    return seq
            except (ValueError,TypeError):
                return seq
            expected_hash = hashlib.sha256((previous+body).encode('utf-8')).hexdigest()
            if seq != expected_seq or row['prev_hash'] != previous or row['row_hash'] != expected_hash:
                return seq
            previous,expected_seq = row['row_hash'],seq+1
        return None
