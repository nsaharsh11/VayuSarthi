"""Local UI flows, claims and outbound-network prohibition."""
from pathlib import Path
from dataclasses import replace
import re
import socket
import json

import pytest

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


def test_polished_charts_and_cards_match_the_shipped_fleet(tmp_path, monkeypatch):
    """Charts and cards must display input/plan values, including every deadline."""
    from vayu.quality import read_pack
    monkeypatch.setenv('VAYU_DB_PATH', str(tmp_path/'charts.db'))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    assert not app.exception
    state = read_pack(ROOT/'data/whatif_demo', safety_buffer=0).state
    board = app.dataframe(key='fleet_board').value.set_index('Tail')
    metrics = {item.label:item.value for item in app.metric}
    assert int(metrics['Fictional tails']) == len(state.tails)
    assert int(metrics['Covered']) == sum(list(labels) == ['Covered'] for labels in board.Label)
    assert int(metrics['Fragile']) == sum(list(labels) == ['Fragile'] for labels in board.Label)
    assert int(metrics['Late']) == sum(board.Status == 'Late')
    charts = {item.proto.alt:json.loads(item.proto.spec) for item in app.get('plotly_chart')}
    ranges = next(spec for alt,spec in charts.items() if alt.startswith('Remaining useful life'))
    bars = {trace['y'][0]:trace for trace in ranges['data'] if trace['type'] == 'bar'}
    points = {trace['y'][0]:trace['x'][0] for trace in ranges['data'] if trace['type'] == 'scatter'}
    assert set(bars) == set(points) == set(board.index)
    for tail in state.tails:
        assert bars[tail.tail_id]['base'][0] == pytest.approx(tail.lower)
        assert bars[tail.tail_id]['base'][0] + bars[tail.tail_id]['x'][0] == pytest.approx(tail.upper)
        assert points[tail.tail_id] == tail.rul_point
    timeline = next(spec for alt,spec in charts.items() if alt.startswith('Proposed induction'))
    deadlines = next(trace for trace in timeline['data'] if trace.get('name') == 'Deadline')
    assert dict(zip(deadlines['y'],deadlines['x'])) == board['Days to deadline'].to_dict()
    for trace in (trace for trace in timeline['data'] if trace['type'] == 'bar'):
        tail_id = trace['y'][0]
        assert trace['base'][0] == board.loc[tail_id,'Start day']
        assert trace['x'][0] == next(t.duration for t in state.tails if t.tail_id == tail_id)


def test_quality_chips_and_clear_approval_validation(tmp_path, monkeypatch):
    """Blank reviews are actionable errors; held data retains its quality chips."""
    from vayu.audit import AuditLog
    database = tmp_path/'polish.db'
    monkeypatch.setenv('VAYU_DB_PATH', str(database))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    switch_tab(app, 'Approvals')
    before = len(AuditLog(database).rows())
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert not app.exception
    assert any('Missing required field: user name and reason' in message.value for message in app.error)
    assert len(AuditLog(database).rows()) == before
    switch_tab(app, 'Data')
    assert all(any(f'[{badge} ' in text.value for text in app.markdown)
               for badge in ('Good','Stale','Conflict'))
    app.toggle(key='corrupted_pack').set_value(True)
    switch_tab(app, 'Data')
    assert not app.exception and len(table(app,'quarantine').value) > 0
    assert all(item.value == 'Hold' for item in app.metric if item.label == 'Planning gate')


def switch_tab(app, name):
    """AppTest lacks tab-click simulation; set its documented session key."""
    app.session_state['main_tabs'] = name
    return app.run()


def test_whatif_spare_eta_panel_uses_generated_witnesses(tmp_path, monkeypatch):
    """Show Late only when a probe observes it; keep the three-click story."""
    from vayu.margins import spare_eta_float
    from vayu.quality import read_pack
    monkeypatch.setenv('VAYU_DB_PATH', str(tmp_path/'eta.db'))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    switch_tab(app, 'What-if')
    assert not app.exception
    state = read_pack(ROOT/'data/whatif_demo', safety_buffer=0).state
    expected = {spare.spare_id: spare_eta_float(spare.spare_id, state)
                for spare in state.spares}
    panel = next(frame.value for frame in app.dataframe
                 if frame.proto.alt.startswith('Spare ETA sensitivity'))
    assert set(panel.Spare) == set(expected)
    for _, row in panel.iterrows():
        result = expected[row.Spare]
        assert str(row['ETA float (days)']) == str(result['float_min'])
        assert row['Changed tails'] == ', '.join(result['changed_tails'])
    messages = [item.value for item in app.info]
    for spare, result in expected.items():
        if result['late_shift'] is not None:
            for tail in result['late_tails']:
                assert any(f"If spare {spare} arrives {result['late_shift']} days later, "
                           f'{tail} becomes Late' in message for message in messages)
    assert 'quick_EXPEDITE:S2' in [button.key for button in app.button]


def table(app, key):
    """Read-only frames expose accessible names, while selectable ones have keys."""
    if key == 'fleet_board':
        return app.dataframe(key=key)
    names = {'ranked_interventions': 'Ranked costed interventions',
             'plan_diff': 'Before and after resources', 'quarantine': 'Quarantined source records',
             'silo_tails': 'Fleet registry: tails.csv', 'silo_health': 'Engine health: health.csv',
             'silo_technical': 'Technical records: tech_records.csv',
             'silo_spares': 'Spares & maintenance resources: spares.csv',
             'silo_resources': 'Spares & maintenance resources: resources.csv'}
    return next(frame for frame in app.dataframe if frame.proto.alt.startswith(names[key]))


def test_ui_board_and_three_click_story(tmp_path,monkeypatch):
    monkeypatch.setenv('VAYU_DB_PATH',str(tmp_path/'app.db'))
    app = AppTest.from_file(str(ROOT/'app.py'),default_timeout=20).run()
    assert not app.exception
    assert app.title[0].value == 'Vayu Sarthi'
    assert any(element.value == 'Fictional fleet and simulated engine data, decision support only' for element in app.info)
    board = app.dataframe(key='fleet_board').value
    assert {'Tail', 'RUL range', 'Days to deadline', 'Decision float', 'Deadline slack',
            'Binding resource', 'Status', 'Label'} <= set(board)
    assert list(board.loc[board.Tail == 'T-04', 'Label'].iloc[0]) == ['Fragile']
    assert any('Spare S2 available only' in item.value for item in app.markdown)
    switch_tab(app, 'What-if')  # Click 1: open What-if, with T-04 already selected.
    assert app.selectbox(key='whatif_tail').value == 'T-04'
    assert 'No effect' in set(table(app, 'ranked_interventions').value['Effect'])
    tags = table(app, 'ranked_interventions').value
    assert not tags['Intervention'].str.contains('Inspect').any()
    assert any(list(tag) == ['No effect'] for tag in tags['Tag'])
    app.button(key='quick_EXPEDITE:S2').click()  # Click 2.
    switch_tab(app, 'What-if')
    assert not app.exception
    diff = table(app, 'plan_diff').value
    focal = diff.loc[diff.Tail == 'T-04'].iloc[0]
    assert (focal['Before label'], focal['After label']) == ('Fragile', 'Covered')
    assert focal['After start'] < focal['Before start']
    assert any('assumed, not scored' in item.label.lower() for item in app.expander)
    app.button(key='quick_ADD:CREW').click()
    switch_tab(app, 'What-if')
    assert any(item.value.startswith('No effect') for item in app.info)
    assert not table(app, 'plan_diff').value['Placement changed'].any()
    switch_tab(app, 'Fleet board')
    assert list(app.dataframe(key='fleet_board').value.query("Tail == 'T-04'").iloc[0]['Label']) == ['Fragile']


def test_data_quality_hold_blocks_all_planning_actions(tmp_path, monkeypatch):
    from vayu.audit import AuditLog
    path = tmp_path / 'hold.db'
    monkeypatch.setenv('VAYU_DB_PATH', str(path))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    switch_tab(app, 'Data')
    for key in ('silo_tails', 'silo_health', 'silo_technical', 'silo_spares', 'silo_resources'):
        assert 'quality_badge' in table(app, key).value
    assert table(app, 'quarantine').value.empty
    before = len(AuditLog(path).rows())
    app.toggle(key='corrupted_pack').set_value(True)
    switch_tab(app, 'Data')
    assert not app.exception and any('Planning hold' in item.value for item in app.error)
    assert not table(app, 'quarantine').value.empty
    switch_tab(app, 'Fleet board')
    assert not any(item.key == 'fleet_board' for item in app.dataframe)
    switch_tab(app, 'What-if')
    assert all(button.key == 'reset_demo' or button.disabled for button in app.button)
    switch_tab(app, 'Approvals')
    assert all(button.key == 'reset_demo' or button.disabled for button in app.button)
    assert len(AuditLog(path).rows()) == before
    switch_tab(app, 'Data')
    app.toggle(key='corrupted_pack').set_value(False)
    switch_tab(app, 'Data')
    app.selectbox(key='scenario').set_value('Four-silo fleet')
    switch_tab(app, 'Data')
    assert len(table(app, 'silo_tails').value) == 10
    assert len(table(app, 'silo_spares').value) == 3
    switch_tab(app, 'Fleet board')
    assert not app.exception and len(app.dataframe(key='fleet_board').value) == 10


def test_approval_name_reason_rejection_and_pins(tmp_path, monkeypatch):
    from vayu.audit import AuditLog
    path = tmp_path/'review.db'
    monkeypatch.setenv('VAYU_DB_PATH', str(path))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    switch_tab(app, 'Approvals')
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert app.error and not app.exception
    app.text_input(key='officer').set_value('Demo reviewer')
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert app.error  # A name alone is insufficient.
    app.text_input(key='note').set_value('Reviewed fictional placement')
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert any('APPROVE' in item.value for item in app.success)
    app.selectbox(key='decision').set_value('REJECT')
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert any('REJECT' in item.value for item in app.success)
    app.selectbox(key='decision').set_value('PIN')
    switch_tab(app, 'Approvals')
    before_pin = len(AuditLog(path).rows())
    app.number_input(key='pin_start').set_value(14)
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert app.error and len(AuditLog(path).rows()) == before_pin
    app.number_input(key='pin_start').set_value(16)
    app.button(key='record_decision').click()
    switch_tab(app, 'Approvals')
    assert not app.exception and any('PIN' in item.value for item in app.success)
    switch_tab(app, 'Fleet board')
    assert app.dataframe(key='fleet_board').value.query("Tail == 'T-04'").iloc[0]['Start day'] == 16
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    assert app.dataframe(key='fleet_board').value.query("Tail == 'T-04'").iloc[0]['Start day'] == 16
    assert AuditLog(path).verify_chain() is None
    switch_tab(app, 'Approvals')
    assert not app.exception
    app.button(key='verify_chain').click()
    switch_tab(app, 'Approvals')
    assert not app.exception and any(item.value == 'Chain verified' for item in app.success)
    assert any('FD001' in item.value for item in app.caption)


def test_replans_log_causes_without_display_duplicates(tmp_path, monkeypatch):
    from vayu.audit import AuditLog
    path = tmp_path/'causes.db'
    monkeypatch.setenv('VAYU_DB_PATH', str(path))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    log = AuditLog(path)
    replans = [row for row in log.rows() if row['action'] == 'REPLAN']
    assert len(replans) == 1 and replans[0]['reason']
    switch_tab(app, 'Approvals')
    assert len(log.rows()) == 2  # Initial plan and initial proposed replan only.
    switch_tab(app, 'What-if')
    candidates = [row for row in log.rows() if row['action'] == 'REPLAN']
    assert len(candidates) > 1 and all(row['reason'] for row in candidates)
    count = len(log.rows())
    switch_tab(app, 'Fleet board')
    switch_tab(app, 'What-if')
    assert len(log.rows()) == count
    for _ in range(2):
        app.button(key='quick_ADD:CREW').click()
        switch_tab(app, 'What-if')
    comparisons = [row for row in log.rows() if row['event_type'] == 'COUNTERFACTUAL_RUN']
    assert len(comparisons) == 2
    assert all(row['reason'] and row['before'] != 'null' and row['after'] != 'null' for row in comparisons)
    assert log.verify_chain() is None


def test_tampered_chain_holds_planning_and_preserves_history(tmp_path, monkeypatch):
    import sqlite3
    from vayu.audit import AuditLog
    path = tmp_path/'broken.db'
    monkeypatch.setenv('VAYU_DB_PATH', str(path))
    app = AppTest.from_file(str(ROOT/'app.py'), default_timeout=20).run()
    with sqlite3.connect(path) as connection:
        connection.execute('DROP TRIGGER audit_no_update')
        connection.execute("UPDATE audit_log SET reason='altered' WHERE seq=1")
    before = AuditLog(path).rows()
    switch_tab(app, 'Approvals')
    assert not app.exception and any('Planning hold' in item.value for item in app.error)
    assert any('Audit chain is broken' in item.value for item in app.caption)
    assert all(button.key == 'reset_demo' for button in app.button)
    app.button(key='reset_demo').click().run()
    assert not app.exception and any('Reset unavailable' in item.value for item in app.error)
    assert AuditLog(path).rows() == before


def test_reset_demo_restores_story_from_pin_and_hold_without_erasing_audit(tmp_path, monkeypatch):
    from vayu.audit import AuditLog
    from vayu.planner import plan
    from vayu.schemas import PinnedPlacement
    from vayu.quality import read_pack
    path = tmp_path/'reset-ui.db'
    monkeypatch.setenv('VAYU_DB_PATH',str(path))
    log = AuditLog(path)
    state = read_pack(ROOT/'data/whatif_demo',safety_buffer=0).state
    original = plan(state)
    source = log.ensure_plan(original,'day-0')
    pinned = plan(state,pinned_placements=(PinnedPlacement('T-04',16,'BAY-01','CREW-01','S2'),))
    log.review_placement(source,pinned,'T-04','Reviewer','PIN','Rehearsal reservation','day-0')
    app = AppTest.from_file(str(ROOT/'app.py'),default_timeout=20).run()
    assert table(app,'fleet_board').value.query("Tail == 'T-04'").iloc[0]['Start day'] == 16
    app.number_input(key='radius').set_value(8)
    switch_tab(app,'What-if')
    app.button(key='quick_ADD:CREW').click()
    switch_tab(app,'What-if')
    switch_tab(app,'Data')
    app.toggle(key='corrupted_pack').set_value(True)
    switch_tab(app,'Data')
    before = log.rows(limit=1000)
    assert app.error
    app.button(key='reset_demo').click().run()
    assert not app.exception and not app.error
    assert app.selectbox(key='scenario').value == 'T-04 story (assumed)'
    assert app.number_input(key='radius').value == 40
    assert app.session_state['corrupted_pack'] is False
    assert app.session_state['last_comparison'] is None
    focal = table(app,'fleet_board').value.query("Tail == 'T-04'").iloc[0]
    assert focal['Start day'] == next(p.start_day for p in original.placements if p.tail_id == 'T-04')
    assert list(focal['Label']) == ['Fragile'] and focal['Binding resource'] == 'spare · S2'
    assert log.pins_for(source) == ()
    after = log.rows(limit=1000)
    assert after[2:] == before
    assert [r['action'] for r in after[:2]] == ['REPLAN','DEMO_RESET']
    assert after[0]['reason'] == 'User requested Reset demo'
    assert log.verify_chain() is None
    switch_tab(app,'What-if')
    assert 'No effect' in set(table(app,'ranked_interventions').value['Effect'])
    app.button(key='quick_EXPEDITE:S2').click()
    switch_tab(app,'What-if')
    assert table(app,'plan_diff').value.query("Tail == 'T-04'").iloc[0]['After label'] == 'Covered'
    fresh = AppTest.from_file(str(ROOT/'app.py'),default_timeout=20).run()
    assert table(fresh,'fleet_board').value.query("Tail == 'T-04'").iloc[0]['Start day'] == focal['Start day']


def test_offline_runtime(tmp_path,monkeypatch):
    attempts = []
    def forbid(*args,**kwargs):
        attempts.append(args)
        raise AssertionError('Outbound network is prohibited')
    original_connect = socket.socket.connect
    def local_only(sock,address):
        # Windows asyncio implements its internal socketpair over loopback.
        if isinstance(address,tuple) and address[0] in ('127.0.0.1','::1'):
            return original_connect(sock,address)
        return forbid(sock,address)
    monkeypatch.setattr(socket,'create_connection',forbid)
    monkeypatch.setattr(socket.socket,'connect',local_only)
    monkeypatch.setenv('VAYU_DB_PATH',str(tmp_path/'offline.db'))
    app = AppTest.from_file(str(ROOT/'app.py'),default_timeout=20).run()
    for workspace in ('Data','What-if','Approvals','Fleet board','Validation'):
        switch_tab(app, workspace)
        assert not app.exception
    switch_tab(app, 'What-if')
    app.button(key='compare').click()
    switch_tab(app, 'What-if')
    assert not app.exception
    assert not attempts


def test_validation_reads_generated_table_and_preserves_ties(tmp_path, monkeypatch):
    from vayu.sim import SimulationConfig, monte_carlo, validation_cell_rows
    from vayu.schemas import PlanningState, Resource, Spare, Tail
    state = PlanningState((Tail('A',8,6,10,1,2),),(Spare('S',0),),
        (Resource('B'),),(Resource('C'),),horizon=6,safety_buffer=0)
    config = SimulationConfig(n_scenarios=5,weekly_budget=0,bootstrap_samples=50)
    report = monte_carlo(state,[-1.,0.,1.],{'A':0},config)
    directory = tmp_path/'validation'
    directory.mkdir()
    validation_cell_rows(report,config,'stressed',2.).to_csv(directory/'validation.csv',index=False)
    monkeypatch.setenv('VAYU_VALIDATION_DIR',str(directory))
    monkeypatch.setenv('VAYU_DB_PATH',str(tmp_path/'validation-ui.db'))
    def forbid(*args, **kwargs):
        raise AssertionError('Validation tab must not rerun Monte Carlo')
    monkeypatch.setattr('vayu.sim.monte_carlo',forbid)
    app = AppTest.from_file(str(ROOT/'app.py'),default_timeout=20).run()
    switch_tab(app,'Validation')
    assert not app.exception
    assert any(item.value == 'simulated; scenario-based' for item in app.info)
    grid = next(frame.value for frame in app.dataframe if frame.proto.alt.startswith('Monte Carlo policy means'))
    assert len(grid) == 7 and set(grid['Policy']) == {'B0','B1','B2-K0','B2','B3','B4','B4b'}
    assert grid.query("Policy == 'B3'").iloc[0].drop('Policy').equals(
        grid.query("Policy == 'B4'").iloc[0].drop('Policy'))
    assert any('B3 / B4' in item.value and 'tie' in item.value.lower() for item in app.caption)
    diff = next(frame.value for frame in app.dataframe if frame.proto.alt.startswith('B4 minus B3'))
    assert (diff['Scenarios tied'] == diff['Scenarios']).all()
    assert any(frame.proto.alt.startswith('B3 minus B2') for frame in app.dataframe)
    assert any(frame.proto.alt.startswith('B4b minus B3') for frame in app.dataframe)
    assert any(frame.proto.alt.startswith('B2 minus B2-K0') for frame in app.dataframe)
    control = next(frame.value for frame in app.dataframe if frame.proto.alt.startswith('B2 minus B2-K0'))
    assert len(control) == 4 and 'Intervention cost' not in set(control.Metric)
    assert any(frame.proto.alt.startswith('B4b minus B4') for frame in app.dataframe)
    opportunities = next(frame.value for frame in app.dataframe if frame.proto.alt.startswith('Candidate opportunities'))
    assert {'Reviews', 'Weeks with 2+ candidates', 'Expedites', 'Crew shifts', 'Bays'} <= set(opportunities)
    assert any('test lacks power' in item.value for item in app.warning)
    assert [path.name for path in directory.iterdir()] == ['validation.csv']  # The only file the tab can read.
    (directory/'validation.csv').unlink()
    switch_tab(app,'Validation')
    assert not app.exception and any('validation' in item.value.lower() for item in app.warning)


def test_active_claims_and_telemetry_config():
    for path in (ROOT/'app.py',ROOT/'README.md',ROOT/'docs/DEMO_RUNBOOK.md'):
        assert not re.search(r'digital twin|real-time|live IoT|optimal|guarantee|no feasible plan exists',path.read_text(encoding='utf-8'),re.I)
    config = (ROOT/'.streamlit/config.toml').read_text(encoding='utf-8')
    assert 'gatherUsageStats = false' in config
    assert '127.0.0.1' in config
    assert 'base = "light"' in config
    assert not re.search(r'\brisk\b', (ROOT/'app.py').read_text(encoding='utf-8'), re.I)
    for path in (ROOT/'README.md',ROOT/'docs/DEMO_RUNBOOK.md'):
        assert not re.search(r'\d\s*%',path.read_text(encoding='utf-8'))


def test_validation_selects_generated_stress_and_assumed_repair_sensitivity(tmp_path,monkeypatch):
    import pandas as pd
    from vayu.sim import SimulationConfig,monte_carlo,validation_cell_rows
    from vayu.schemas import PlanningState,Resource,Spare,Tail
    directory = tmp_path/'reports'
    directory.mkdir()
    state = PlanningState((Tail('A',8,6,10,1,2),),(Spare('S',0),),
                          (Resource('B'),),(Resource('C'),),horizon=6,safety_buffer=0)
    cells = []
    for level,multiplier,horizon in (('stressed',2.,40),('stressed',2.,80),('benign',2.,40),('benign',1.5,40)):
        config = SimulationConfig(n_scenarios=3,weekly_budget=0,bootstrap_samples=20,repair_multiplier=multiplier)
        result = monte_carlo(replace(state,horizon=horizon),[-1.,1.],{'A':0},config)
        cells.append(validation_cell_rows(result,config,level,multiplier))
    pd.concat(cells,ignore_index=True).to_csv(directory/'validation.csv',index=False)
    monkeypatch.setenv('VAYU_VALIDATION_DIR',str(directory))
    monkeypatch.setenv('VAYU_DB_PATH',str(tmp_path/'stress-ui.db'))
    app = AppTest.from_file(str(ROOT/'app.py'),default_timeout=20).run()
    switch_tab(app,'Validation')
    assert not app.exception
    assert app.selectbox(key='validation_stress').value == 'stressed'
    app.selectbox(key='validation_horizon').set_value(80)
    switch_tab(app,'Validation')
    assert not app.exception and any('Horizon 80 days' in item.value for item in app.caption)
    app.selectbox(key='validation_stress').set_value('benign')
    switch_tab(app,'Validation')
    app.selectbox(key='validation_repair').set_value(1.5)
    switch_tab(app,'Validation')
    assert not app.exception
    assert all('test lacks power' in item.value for item in app.warning)
    assert any('assumed repair multiplier 1.5' in item.value for item in app.caption)


def test_pinned_dependencies_match_environment():
    from importlib.metadata import version
    for line in (ROOT/'requirements.txt').read_text().splitlines():
        if line and not line.startswith('#'):
            name,pinned = line.split('==')
            assert version(name) == pinned, f'{name}: install the pinned requirements'
