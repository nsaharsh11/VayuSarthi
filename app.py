"""Offline Vayu Sarthi: quality-gated fleet decisions and human placement review."""
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from vayu.audit import AuditLog
from vayu.margins import PlannerCache, spare_eta_float
from vayu.planner import plan
from vayu.quality import planning_state_from_fleet, read_pack, validate_fleet_pack
from vayu.rul import DEFAULT_CACHE, predict_tail
from vayu.schemas import FLEET_SCHEMAS, PinnedPlacement, PlanningState
from vayu.sim import (story_silos, POLICY_NAMES, PAIRED_POLICIES, VALIDATION_METRICS,
                      VALIDATION_COLUMNS, VALIDATION_NOTE, CHOICE_PAIRS, INTERVENTION_POLICIES,
                      OUTCOME_METRICS)
from vayu.whatif import ScenarioSnapshot, WhatIfExplorer, default_interventions

ROOT = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get('VAYU_DB_PATH', str(ROOT/'data/maintenance.db')))
VALIDATION_DIR = Path(os.environ.get('VAYU_VALIDATION_DIR', str(ROOT/'artifacts')))
BANNER = 'Fictional fleet and simulated engine data, decision support only'
STORY = 'T-04 story (assumed)'
STATUS_COLORS = {'On time': '#147D92', 'Late': '#C96835', 'Unplanned': '#768798'}
LABEL_COLORS = {'Covered': '#147D92', 'Fragile': '#C98A2B'}
PILL_COLORS = {'Covered': 'green', 'Fragile': 'orange', 'Good': 'green', 'Stale': 'orange', 'Conflict': 'red'}
POLICY_COLORS = {'B0': '#768798', 'B1': '#A9B6C3', 'B2-K0': '#ADAF8B',
                 'B2': '#C98A2B', 'B3': '#147D92', 'B4': '#0B4F5E', 'B4b':'#9263A3'}
STYLE = """
<style>
div[data-testid="stMetric"] {background: linear-gradient(135deg,#F4F9FB,#FFFFFF); border-radius: 12px;}
h1 {letter-spacing: -0.02em;}
</style>
"""


def source_digest(paths: list[Path]) -> str:
    """Invalidate local caches whenever source bytes change or disappear."""
    digest = hashlib.sha256()
    for path in paths:
        digest.update(str(path).encode('utf-8'))
        digest.update(path.read_bytes() if path.is_file() else b'MISSING')
    return digest.hexdigest()


@st.cache_data(max_entries=16, show_spinner=False)
def load_sources(scenario: str, digest: str) -> tuple[dict[str, pd.DataFrame], PlanningState | None]:
    """Read local CSVs; the explicit digest identifies their current contents."""
    if scenario == STORY:
        loaded = read_pack(ROOT/'data/whatif_demo', safety_buffer=0)
        if loaded.issues or loaded.state is None:
            raise ValueError('Story inputs failed validation; regenerate with python scripts/tasks.py whatif-demo')
        return story_silos(loaded.state), loaded.state
    return {name: pd.read_csv(ROOT/'data/fleet'/name, keep_default_na=False)
            for name in FLEET_SCHEMAS if (ROOT/'data/fleet'/name).is_file()}, None


@st.cache_data(max_entries=8, show_spinner=False)
def engine_predictions(engine_ids: tuple[str, ...], model_digest: str) -> dict[str, dict[str, float]]:
    """Load only cached believed predictions; never train or download in the app."""
    return {engine: predict_tail(engine) for engine in engine_ids}


@st.cache_data(max_entries=32, show_spinner=False)
def snapshot(state: PlanningState, radius: int, pins: tuple[PinnedPlacement, ...]) -> ScenarioSnapshot:
    """Cache the immutable planner and full-fleet directional margin results."""
    return WhatIfExplorer(state, (), radius, pins).baseline


@st.cache_data(max_entries=32, show_spinner=False)
def ranked_results(state: PlanningState, radius: int, pins: tuple[PinnedPlacement, ...]) -> list[dict[str, Any]]:
    """Rank the costed capacity actions. Inspection is assumed, not scored."""
    actions = tuple(a for a in default_interventions(state) if a.kind != 'inspect_tail')
    return WhatIfExplorer(state, actions, radius, pins).rank()


@st.cache_data(max_entries=32, show_spinner=False)
def spare_eta_results(state: PlanningState, pins: tuple[PinnedPlacement, ...]) -> list[dict[str, Any]]:
    """Cache day-based ETA probes; numerical probes are not proposed replans."""
    cache = PlannerCache()
    return [spare_eta_float(spare.spare_id, state, pinned_placements=pins, cache=cache)
            for spare in sorted(state.spares, key=lambda item: item.spare_id)]


def badge_column(label: str, options: list[str], colors: list[str]) -> dict[str, Any]:
    """Use native read-only coloured labels, retaining accessible text."""
    return st.column_config.MultiselectColumn(label, options=options, color=colors)


def quality_chips(frame: pd.DataFrame) -> None:
    """Show Good/Stale/Conflict record counts as coloured chips."""
    counts = frame.quality_badge.value_counts() if 'quality_badge' in frame else pd.Series(dtype=int)
    with st.container(horizontal=True):
        for badge in ('Good', 'Stale', 'Conflict'):
            st.badge(f'{badge} · {int(counts.get(badge, 0))}', color=PILL_COLORS[badge])


def fleet_table(state: PlanningState, current: ScenarioSnapshot) -> pd.DataFrame:
    """Format generated fleet values with numeric units and nulls preserved."""
    tails = {t.tail_id: t for t in state.tails}
    attention = {a.tail_id: a for a in current.attention}
    rows = []
    for p in current.plan.placements:
        tail, a = tails[p.tail_id], attention[p.tail_id]
        resource_id = getattr(p, p.binding) if p.binding else None
        rows.append({'Tail': p.tail_id, 'RUL range': f'{tail.lower:.1f} – {tail.upper:.1f}',
                     'Days to deadline': p.deadline_day-state.today,
                     'Decision float': a.float_result.display, 'Deadline slack': a.slack,
                     'Binding resource': f'{p.binding} · {resource_id}' if p.binding else 'None',
                     'Status': p.status, 'Label': [a.label], 'Start day': p.start_day})
    return pd.DataFrame(rows)


def rul_range_chart(state: PlanningState, current: ScenarioSnapshot, selected: str) -> go.Figure:
    """Range bars from lower to upper RUL with the point estimate as a tick."""
    labels = {a.tail_id: a.label for a in current.attention}
    chart = go.Figure()
    for t in sorted(state.tails, key=lambda t: t.tail_id):
        label = labels[t.tail_id]
        chart.add_trace(go.Bar(
            y=[t.tail_id], x=[t.upper-t.lower], base=[t.lower], orientation='h',
            marker=dict(color=LABEL_COLORS[label], line=dict(color='#1B2733' if t.tail_id == selected else 'rgba(0,0,0,0)', width=2)),
            opacity=1 if t.tail_id == selected else .65, showlegend=False,
            hovertemplate=f'{t.tail_id} · {label}<br>Range {t.lower:.1f} – {t.upper:.1f} cycles<extra></extra>'))
        chart.add_trace(go.Scatter(
            x=[t.rul_point], y=[t.tail_id], mode='markers', showlegend=False,
            marker=dict(symbol='line-ns', size=16, line=dict(color='#1B2733', width=3)),
            hovertemplate=f'{t.tail_id} point {t.rul_point:.1f} cycles<extra></extra>'))
    chart.update_layout(height=330, barmode='overlay', margin=dict(l=0, r=0, t=10, b=30),
                        xaxis_title='RUL (flight cycles)<br>tick = point estimate',
                        yaxis=dict(title='', categoryorder='category descending'))
    return chart


def hangar_timeline(state: PlanningState, current: ScenarioSnapshot) -> go.Figure:
    """Gantt of induction intervals with a diamond at each deadline."""
    chart = go.Figure()
    shown: set[str] = set()
    for p in sorted(current.plan.placements, key=lambda p: p.tail_id):
        if p.start_day is not None:
            chart.add_trace(go.Bar(
                y=[p.tail_id], x=[p.end_day-p.start_day], base=[p.start_day], orientation='h',
                marker_color=STATUS_COLORS[p.status], name=p.status, legendgroup=p.status,
                showlegend=p.status not in shown, text=f'{p.bay}', textposition='inside',
                hovertemplate=f'{p.tail_id} · {p.status}<br>Start day {p.start_day} · End day {p.end_day}'
                              f'<br>Bay {p.bay}<br>Crew {p.crew}<br>Spare {p.spare}<extra></extra>'))
            shown.add(p.status)
    unplanned = [p for p in current.plan.placements if p.start_day is None]
    chart.add_trace(go.Scatter(
        x=[p.deadline_day for p in current.plan.placements], y=[p.tail_id for p in current.plan.placements],
        mode='markers', name='Deadline', marker=dict(symbol='diamond', size=11, color='#1B2733'),
        hovertemplate='%{y} deadline day %{x}<extra></extra>'))
    if unplanned:
        chart.add_trace(go.Scatter(
            x=[p.deadline_day for p in unplanned], y=[p.tail_id for p in unplanned], mode='text',
            text=['Unplanned'] * len(unplanned), textposition='middle right', showlegend=False,
            hoverinfo='skip'))
    chart.add_vline(x=state.today, line_dash='dot', line_color='#768798')
    chart.update_layout(height=360, barmode='overlay', margin=dict(l=0, r=0, t=10, b=30),
                        xaxis_title='Day (diamond = induction start deadline)',
                        yaxis=dict(title='', categoryorder='category descending'),
                        legend=dict(orientation='h', y=1.12))
    return chart


def comparison_table(result: dict[str, Any]) -> pd.DataFrame:
    """Show every tail's placement and attention changes, including no effects."""
    rows = []
    for change in result['per_tail_changes']:
        old, new = change['before'], change['after']
        rows.append({'Tail': change['tail'], 'Before start': old['start_day'], 'After start': new['start_day'],
                     'Before resources': f"{old['bay']} / {old['crew']} / {old['spare']}",
                     'After resources': f"{new['bay']} / {new['crew']} / {new['spare']}",
                     'Before label': old['label'], 'After label': new['label'],
                     'Before slack': old['deadline_slack'], 'After slack': new['deadline_slack'],
                     'Before half-width': old['half_width'], 'After half-width': new['half_width'],
                     'Before status': old['status'], 'After status': new['status'],
                     'Placement changed': change['placement_changed']})
    return pd.DataFrame(rows)


def action_name(action: dict[str, Any]) -> str:
    """Plain-language action names drawn from the candidate inputs."""
    kind, target = action['kind'], action['target']
    if kind == 'expedite_spare':
        return f"Expedite {target} by {action['days']} days"
    return 'Add one crew shift' if kind == 'add_crew_shift' else 'Add one bay'


@st.cache_data(max_entries=8, show_spinner=False)
def validation_report(path: Path, digest: str) -> pd.DataFrame:
    """Validate the wide CSV and reshape for display without calculating results."""
    table = pd.read_csv(path)
    if not set(VALIDATION_COLUMNS) <= set(table):
        raise ValueError('Validation table has missing metric fields')
    if table.empty or table.duplicated(['stress_level', 'repair_multiplier', 'horizon_days', 'policy']).any():
        raise ValueError('Validation table has duplicate rows')
    if (not table.note.eq(VALIDATION_NOTE).all() or table.n_scenarios.isna().any()
            or not table.n_scenarios.ge(1).all() or not table.n_scenarios.mod(1).eq(0).all()):
        raise ValueError('Validation scenario counts or simulated-note labels are inconsistent')
    if table.horizon_days.isna().any() or not table.horizon_days.ge(1).all() or not table.horizon_days.mod(1).eq(0).all():
        raise ValueError('Validation horizon must be a positive number of days')
    expected = set(POLICY_NAMES) | {f'{left}-{right}' for left,right in PAIRED_POLICIES}
    types = table.policy.map(lambda policy: 'policy' if policy in POLICY_NAMES else 'paired_difference')
    if not table.row_type.eq(types).all():
        raise ValueError('Validation policy row types are inconsistent')
    for _, cell in table.groupby(['stress_level', 'repair_multiplier', 'horizon_days'], dropna=False):
        if set(cell.policy) != expected or cell.n_scenarios.nunique() != 1:
            raise ValueError('Validation table must contain every policy and named paired comparison')
    rows = []
    for values in table.to_dict('records'):
        metrics = OUTCOME_METRICS if values['policy'] == 'B2-B2-K0' else VALIDATION_METRICS
        for metric in metrics:
            numbers = pd.to_numeric(pd.Series([values[f'{metric}_{suffix}'] for suffix in ('mean','ci_low','ci_high')]))
            if numbers.isna().any() or numbers.isin([float('inf'),float('-inf')]).any():
                raise ValueError('Validation metrics must be finite within their comparison scope')
            if numbers.iloc[1] > numbers.iloc[2]:
                raise ValueError('Validation intervals are inconsistent')
            ties = values[f'{metric}_ties']
            if values['row_type'] == 'paired_difference' and (pd.isna(ties) or ties%1 != 0 or
                    not 0 <= ties <= values['n_scenarios']):
                raise ValueError('Validation paired tie counts are inconsistent')
            rows.append({**values, 'metric': metric, 'mean': values[f'{metric}_mean'],
                         'ci_low': values[f'{metric}_ci_low'], 'ci_high': values[f'{metric}_ci_high'],
                         'all_outcomes_ties': values['tie_scenarios'],
                         'tie_scenarios': values[f'{metric}_ties']})
    return pd.DataFrame(rows)


def cell_text(row: pd.Series) -> str:
    """Format a generated mean and confidence interval."""
    return f"{row['mean']:.6g} [{row.ci_low:.6g}, {row.ci_high:.6g}]"


def reset_scenario() -> None:
    """Reset scenario controls while retaining the reviewer's identity."""
    st.session_state.corrupted_pack = False
    st.session_state.last_comparison = None
    for key in ('whatif_tail', 'approval_tail', 'intervention', 'pin_context'):
        st.session_state.pop(key, None)


def reset_demo() -> None:
    """Restore the clean assumed story, auditing pin release and the replan."""
    try:
        log = AuditLog(DATABASE)
        if log.verify_chain() is not None:
            raise ValueError('Audit chain is broken; preserve the database for review')
        paths = [ROOT/'data/whatif_demo'/name for name in
                 ('fleet.csv','spares.csv','resources.csv','health_stream.csv')]
        _, story = load_sources(STORY,source_digest(paths))
        original = plan(story)
        source = log.ensure_plan(original,'day-0')
        cause = 'User requested Reset demo'
        log.reset_demo(source,user='prototype',reason=cause,timestamp='day-0')
        log.record_replan(st.session_state.get('audited_current_plan'),original,
                          user='prototype',cause=cause,timestamp='day-0')
    except (OSError,ValueError) as error:
        st.session_state.reset_error = f'Reset unavailable: {error}'
        return
    reset_scenario()
    for key in ('fleet_board','inspection_factor','decision','note','pin_start','pin_bay',
                'pin_crew','pin_spare','audited_rankings','review_flash','reset_error'):
        st.session_state.pop(key,None)
    st.session_state.update(scenario=STORY,radius=40,main_tabs='Fleet board',
                            audited_current_plan=original)


st.set_page_config(page_title='Vayu Sarthi', page_icon=':material/flight:', layout='wide')
st.markdown(STYLE, unsafe_allow_html=True)
st.title('Vayu Sarthi')
st.caption('SIH26249 · Predictive maintenance & fleet availability · Offline prototype')
st.info(BANNER)
st.session_state.setdefault('corrupted_pack', False)
st.session_state.setdefault('last_comparison', None)
st.session_state.setdefault('review_flash', None)

with st.sidebar:
    st.subheader('Planning snapshot')
    scenario = st.selectbox('Demo pack', [STORY, 'Four-silo fleet'], key='scenario', on_change=reset_scenario)
    st.caption('Assumed ranges and diagnostic checks.' if scenario == STORY else
               'Fictional fleet joined to cached NASA FD001 engine estimates.')
    st.caption('Day 0 · Spare horizon day 40 · Buffer 0 cycles')
    with st.expander('Sensitivity settings'):
        radius = int(st.number_input('Float search bound R (cycles)', min_value=0, max_value=250,
                                     value=40, key='radius'))
    st.caption('Covered / Fragile indicate planning attention. A reviewer decides on every placement.')
    st.button('Reset demo',key='reset_demo',on_click=reset_demo,
              help='Restore the clean T-04 story and release its pins. Audit history and files are preserved.')

if st.session_state.get('reset_error'):
    st.error(st.session_state.reset_error)

gate_notice = st.container()
cards = st.container()
tabs = st.tabs(['Data', 'Fleet board', 'What-if', 'Approvals', 'Validation'], default='Fleet board',
               key='main_tabs', on_change='rerun')
if tabs[0].open:
    with tabs[0]:
        st.subheader('Four data silos')
        st.toggle('Load corrupted pack (demo)', key='corrupted_pack',
                  persist_state='session',
                  help='Changes a copy in memory; original CSV files remain available.')

source_paths = ([ROOT/'data/whatif_demo'/name for name in ('fleet.csv', 'spares.csv', 'resources.csv', 'health_stream.csv')]
                if scenario == STORY else [ROOT/'data/fleet'/name for name in FLEET_SCHEMAS])
source_error = None
try:
    frames, story_state = load_sources(scenario, source_digest(source_paths))
except (OSError, ValueError) as error:
    frames, story_state = {}, None
    source_error = str(error)
if st.session_state.corrupted_pack and 'tails.csv' in frames:
    frames = {name: frame.copy(deep=True) for name, frame in frames.items()}
    frames['tails.csv'].loc[frames['tails.csv'].tail_id == 'T-04', 'utilisation_cycles_per_day'] = 0
    frames['tech_records.csv'].loc[0, 'tail_id'] = 'T-MISSING'
quality = validate_fleet_pack(frames)
planning_hold = quality.planning_hold or source_error is not None
state = None
if not planning_hold:
    try:
        if story_state is not None:
            state = story_state
        else:
            engine_ids = tuple(sorted(quality.accepted['tails.csv'].engine_id))
            predictions = engine_predictions(engine_ids, source_digest([ROOT/DEFAULT_CACHE]))
            state = planning_state_from_fleet(quality, predictions, safety_buffer=0)
    except (OSError, ValueError, KeyError) as error:
        planning_hold, source_error = True, f'Planning estimates unavailable: {error}'

current = None
pins: tuple[PinnedPlacement, ...] = ()
log = AuditLog(DATABASE)
if state is not None and not planning_hold:
    try:
        broken = log.verify_chain()
        if broken is not None:
            raise ValueError(f'Audit chain is broken at sequence {broken}')
        original = plan(state)
        source_plan_id = log.ensure_plan(original, 'day-0')
        pins = log.pins_for(source_plan_id)
        current = snapshot(state, radius, pins)
        previous = st.session_state.get('audited_current_plan')
        if previous is None or previous.inputs_hash != current.plan.inputs_hash:
            cause = (f'Load validated {scenario} with stored pins' if previous is None else
                     f'Planning inputs or stored pins changed for {scenario}')
            log.record_replan(previous, current.plan, user='prototype', cause=cause, timestamp='day-0')
            st.session_state.audited_current_plan = current.plan
    except ValueError as error:
        planning_hold, source_error = True, f'Planning audit or pinned placement needs review: {error}'

if planning_hold:
    with gate_notice:
        st.error('Planning hold — repair quarantined or unavailable inputs before planning or review.')
        for reason in (*quality.reasons, *((source_error,) if source_error else ())):
            st.caption(reason)

with cards:
    with st.container(horizontal=True):
        if current is not None and not planning_hold:
            st.metric('Fictional tails', len(state.tails), border=True)
            st.metric('Covered', sum(a.label == 'Covered' for a in current.attention), border=True)
            st.metric('Fragile', sum(a.label == 'Fragile' for a in current.attention), border=True)
            st.metric('Late', sum(p.status == 'Late' for p in current.plan.placements), border=True)
        st.metric('Planning gate', 'Hold' if planning_hold else 'Ready', border=True)
    if current is not None and not planning_hold:
        with st.container(horizontal=True):
            for a in sorted(current.attention, key=lambda a: a.tail_id):
                st.badge(f'{a.tail_id} · {a.label}', color=PILL_COLORS[a.label])

if tabs[0].open:
    with tabs[0]:
        st.caption('This selected story uses assumed fictional health and technical annotations.' if scenario == STORY else
                   'Original fictional ten-tail CSV pack; planning uses its validated rates and capacity.')
        with st.container(horizontal=True):
            st.metric('Source records', sum(len(f) for f in quality.frames.values()), border=True)
            st.metric('Quarantined', len(quality.quarantine), border=True)
            st.metric('Planning gate', 'Hold' if planning_hold else 'Ready', border=True)
        st.caption('Record quality across all silos')
        quality_chips(pd.concat([f for f in quality.frames.values() if 'quality_badge' in f], ignore_index=True)
                      if quality.frames else pd.DataFrame())
        silo_groups = [('Fleet registry', (('tails.csv', 'silo_tails'),)),
                       ('Engine health', (('health.csv', 'silo_health'),)),
                       ('Technical records', (('tech_records.csv', 'silo_technical'),)),
                       ('Spares & maintenance resources', (('spares.csv', 'silo_spares'), ('resources.csv', 'silo_resources')))]
        for heading, sources in silo_groups:
            with st.expander(heading, expanded=True):
                for name, key in sources:
                    displayed = quality.frames[name].copy()
                    quality_chips(displayed)
                    displayed['quality_badge'] = displayed.quality_badge.map(lambda badge: [badge])
                    st.dataframe(displayed, hide_index=True, key=key,
                                 column_config={'quality_badge': badge_column('Quality', ['Good', 'Stale', 'Conflict'],
                                                                             ['#147D92', '#A76A17', '#B84736'])},
                                 alt=f'{heading}: {name} with record quality badges')
        st.subheader('Quarantine')
        st.dataframe(quality.quarantine, hide_index=True, key='quarantine', alt='Quarantined source records and reasons')
        st.caption('Stale means a health update older than seven days. Conflict rows fail hard checks and are excluded.')

if tabs[1].open and current is not None and not planning_hold:
    with tabs[1]:
        st.subheader('Proposed fleet placements')
        board = fleet_table(state, current)
        default_row = int(board.index[board.Tail == 'T-04'][0]) if 'T-04' in set(board.Tail) else 0
        selection = st.dataframe(board, hide_index=True, key='fleet_board', on_select='rerun',
                                 selection_mode='single-row', selection_default={'selection': {'rows': [default_row]}},
                                 column_config={'Label': badge_column('Label', ['Covered', 'Fragile'], ['#147D92', '#A76A17']),
                                                'Deadline slack': st.column_config.NumberColumn('Deadline slack', format='%.1f', help='Flight cycles, frozen placement'),
                                                'RUL range': st.column_config.TextColumn(help='Flight cycles'),
                                                'Decision float': st.column_config.TextColumn(help='Flight cycles; > R is a bounded search')},
                                 alt='Fictional fleet board with planning margins and selectable tail rows')
        st.caption('Select a row to inspect it. RUL, float and deadline slack use flight cycles; deadline uses days.')
        rows = selection.selection.rows
        selected = int(rows[0]) if rows and 0 <= rows[0] < len(board) else default_row
        tail_id = str(board.iloc[selected].Tail)
        placement = next(p for p in current.plan.placements if p.tail_id == tail_id)
        a = next(a for a in current.attention if a.tail_id == tail_id)
        detail, ranges = st.columns([1, 1.2])
        with detail.container(border=True):
            st.subheader(f'Why this plan · {tail_id}')
            st.badge(a.label, color=PILL_COLORS[a.label])
            st.markdown(placement.reason_code)
            st.caption(f'Start: day {placement.start_day} · Deadline: day {placement.deadline_day}')
            st.caption(f'Bay {placement.bay} · Crew {placement.crew} · Spare {placement.spare}')
            st.markdown(a.reason)
            st.caption(f'Range half-width: {a.half_width:.1f} cycles. Float replans; deadline slack freezes this placement.')
        with ranges:
            st.markdown('**RUL ranges**')
            st.plotly_chart(rul_range_chart(state, current, tail_id), key='rul_ranges',
                            alt='Remaining useful life range bars with point estimates for each fictional tail',
                            config={'displaylogo': False})
        st.markdown('**Hangar timeline**')
        st.plotly_chart(hangar_timeline(state, current), key='hangar_timeline',
                        alt='Proposed induction intervals for the fictional fleet with deadline markers',
                        config={'displaylogo': False})
        if scenario == STORY and not pins:
            st.caption('Three-click story: select T-04 → open What-if → Expedite S2 by 5 days.')

if tabs[2].open and current is not None and not planning_hold:
    with tabs[2]:
        st.subheader('Ranked what-if interventions')
        ids = sorted(t.tail_id for t in state.tails)
        tail_id = st.selectbox('Tail', ids, index=ids.index('T-04') if 'T-04' in ids else 0, key='whatif_tail')
        ranked = ranked_results(state, radius, pins)
        by_id = {r['intervention_ids'][0]: r for r in ranked}
        names = {key: action_name(row['interventions'][0]) for key, row in by_id.items()}

        def tag(row: dict[str, Any]) -> list[str]:
            """No effect rows stay visible with an explicit tag."""
            return ['No effect'] if row['effect'] == 'No effect' else ['Helps'] if row['benefit'] > 0 else ['Other']

        ranking = pd.DataFrame([{'Rank': i, 'Intervention': names[r['intervention_ids'][0]], 'Tag': tag(r),
                                 'Cost (man-hours)': r['cost_man_hours'],
                                 'Benefit per cost': r['benefit_per_cost'], 'Covered': r['label_counts']['Covered'],
                                 'Fragile': r['label_counts']['Fragile'], 'Late': r['late_count'],
                                 'Min slack (cycles)': r['min_slack'], 'Effect': r['effect']}
                                for i, r in enumerate(ranked, start=1)])
        st.dataframe(ranking, hide_index=True, key='ranked_interventions',
                     alt='Ranked costed interventions, including No effect candidates',
                     column_config={'Benefit per cost': st.column_config.NumberColumn(format='%.3f'),
                                    'Tag': badge_column('Tag', ['Helps', 'No effect', 'Other'],
                                                        ['#147D92', '#768798', '#A76A17'])})
        st.caption('Benefit per man-hour = (increase in Covered + reduction in Late) / cost. Costs are assumed inputs. No effect rows remain visible.')
        context = (current.plan.inputs_hash, radius, tail_id)
        seen = st.session_state.setdefault('audited_rankings', set())
        if context not in seen:
            for candidate in ranked:
                log.append('day-0', 'prototype', 'REPLAN', {
                    'plan_id': current.plan.inputs_hash, 'interventions': candidate['interventions'],
                    'cause': f"What-if candidate: {names[candidate['intervention_ids'][0]]}; comparison only",
                    'before': [row['before'] for row in candidate['per_tail_changes']],
                    'after': [row['after'] for row in candidate['per_tail_changes']]})
            seen.add(context)
        requested_comparison = None
        focal = next(p for p in current.plan.placements if p.tail_id == tail_id)
        quick = [key for key in (f'EXPEDITE:{focal.spare}', 'ADD:CREW') if key in by_id]
        with st.container(horizontal=True):
            for key in quick:
                if st.button(names[key], key=f'quick_{key}', type='primary' if key.startswith('EXPEDITE:') else 'secondary'):
                    st.session_state.last_comparison = (context, key)
                    requested_comparison = key
        with st.form('whatif'):
            chosen = st.selectbox('Intervention', list(by_id), format_func=names.get, key='intervention')
            if st.form_submit_button('Compare before / after', key='compare'):
                st.session_state.last_comparison = (context, chosen)
                requested_comparison = chosen
        saved = st.session_state.last_comparison
        if saved and saved[0] == context and saved[1] in by_id:
            result = by_id[saved[1]]
            st.subheader(f'Before / after · {names[saved[1]]}')
            for assumption in result['assumptions']:
                if result['assumed']:
                    st.warning(assumption)
                else:
                    st.caption(assumption)
            with st.container(horizontal=True):
                st.metric('Covered after', result['label_counts']['Covered'],
                          result['benefit_components']['covered_increase'], border=True)
                st.metric('Late after', result['late_count'], -result['benefit_components']['late_reduction'],
                          delta_color='inverse', border=True)
                st.metric('Benefit per man-hour', f"{result['benefit_per_cost']:.3f}", border=True)
            st.info(result['effect'] + ' · Comparison only; current placements are unchanged.')
            change = next(row for row in result['per_tail_changes'] if row['tail'] == tail_id)
            old, new = change['before'], change['after']
            old_color = 'blue' if old['label'] == 'Covered' else 'orange'
            new_color = 'blue' if new['label'] == 'Covered' else 'orange'
            with st.container(border=True):
                st.markdown(f"**{tail_id}** · :{old_color}[{old['label']}] → :{new_color}[{new['label']}]")
                st.caption(f"Start day {old['start_day']} → {new['start_day']} · "
                           f"Half-width {old['half_width']:.1f} → {new['half_width']:.1f} cycles")
                st.markdown(new['reason_code'])
                st.caption('Resources moved.' if change['placement_changed'] else 'Placement unchanged.')
            st.dataframe(comparison_table(result), hide_index=True, key='plan_diff', alt='Before and after resources, starts, labels, slack and assumed width for every tail')
            if requested_comparison is not None:
                log.append('day-0', 'prototype', 'COUNTERFACTUAL_RUN', {
                    'plan_id': current.plan.inputs_hash, 'intervention': result['interventions'],
                    'cause': f'User requested comparison: {names[requested_comparison]}',
                    'before': [row['before'] for row in result['per_tail_changes']],
                    'after': [row['after'] for row in result['per_tail_changes']],
                    'changed_tails': result['changed_tails'], 'benefit': result['benefit']})
        with st.expander('Spare arrival sensitivity', expanded=True):
            eta_results = spare_eta_results(state, pins)
            st.caption('Assumed single-spare delays. ETA float uses days and observes every tail; '
                       'RUL decision float on the board uses flight cycles. These probes are not scored actions.')
            st.dataframe(pd.DataFrame([{
                'Spare': row['spare'], 'ETA float (days)': str(row['float_min']),
                'Changed tails': ', '.join(row['changed_tails']),
                'First new Late (days)': str(row['late_shift']) if row['late_shift'] is not None else
                                        f"> {row['max_delay_days']} days" if not row['blocked_reason'] else 'Pin conflict',
                'Late tails': ', '.join(row['late_tails'])} for row in eta_results]),
                hide_index=True, key='spare_eta',
                alt='Spare ETA sensitivity with first placement changes and separate Late transitions')
            for row in eta_results:
                if row['late_shift'] is not None:
                    for identifier in row['late_tails']:
                        st.info(f"If spare {row['spare']} arrives {row['late_shift']} days later, "
                                f'{identifier} becomes Late.')
                elif row['what_changed']:
                    change = row['what_changed'][0]
                    after = change['after']
                    before = change['before']
                    if after['status'] == 'Unplanned':
                        outcome = f"{change['tail']} becomes Unplanned"
                    elif 'start_day' in change['fields']:
                        outcome = f"{change['tail']} starts on day {after['start_day']} ({after['status']})"
                    elif 'spare' in change['fields']:
                        outcome = f"{change['tail']} uses spare {after['spare']} instead of {before['spare']}"
                    else:
                        outcome = f"{change['tail']} changes placement ({after['status']})"
                    st.caption(f"If spare {row['spare']} arrives {row['float_min']} days later, {outcome}.")
                    if not row['blocked_reason']:
                        st.caption(f"No new Late placement observed through {row['max_delay_days']} days.")
                if row['blocked_reason']:
                    st.warning(row['blocked_reason'])
        with st.expander('Inspection (assumed, not scored)'):
            st.caption('A diagnostic inspection could narrow a tail\'s RUL range, but no inspection observation is '
                       'modelled here. It is not ranked, costed, scored or simulated in this prototype.')

if tabs[3].open and current is not None and not planning_hold:
    with tabs[3]:
        st.subheader('Human placement review')
        st.caption('Approve or reject a proposed placement, or pin exact resources and a start day. Recording a review executes no maintenance.')
        flash = st.session_state.pop('review_flash', None)
        if flash:
            st.success(flash)
        ids = sorted(t.tail_id for t in state.tails)
        tail_id = st.selectbox('Placement tail', ids, index=ids.index('T-04') if 'T-04' in ids else 0, key='approval_tail')
        decision = st.selectbox('Decision', ['APPROVE', 'REJECT', 'PIN'], key='decision')
        p = next(p for p in current.plan.placements if p.tail_id == tail_id)
        st.markdown(f'**{tail_id}** · {p.status} · Start day {p.start_day} · {p.bay} / {p.crew} / {p.spare}')
        pin_context = (current.plan.inputs_hash, tail_id)
        if st.session_state.get('pin_context') != pin_context:
            st.session_state.pin_context = pin_context
            for key in ('pin_start', 'pin_bay', 'pin_crew', 'pin_spare'):
                st.session_state.pop(key, None)
        st.caption('Required for every decision: your name and a reason. A PIN also needs a feasible start day and available resources.')
        with st.form('approval'):
            officer = st.text_input('User name (required)', key='officer', persist_state='session')
            note = st.text_input('Reason (required)', key='note', persist_state='session')
            if decision == 'PIN':
                pin_start = int(st.number_input('Pinned start day', min_value=1, max_value=365,
                                                value=p.start_day or 1, key='pin_start'))
                bays, crews, spares = [r.resource_id for r in state.bays], [r.resource_id for r in state.crews], [s.spare_id for s in state.spares]
                bay = st.selectbox('Pinned bay', bays, index=bays.index(p.bay) if p.bay in bays else 0, key='pin_bay')
                crew = st.selectbox('Pinned crew', crews, index=crews.index(p.crew) if p.crew in crews else 0, key='pin_crew')
                spare = st.selectbox('Pinned spare', spares, index=spares.index(p.spare) if p.spare in spares else 0,
                                      key='pin_spare', help='The planner checks availability, compatibility and existing reservations.')
            submitted = st.form_submit_button('Record decision', key='record_decision', disabled=decision == 'PIN' and not state.spares)
        if submitted:
            try:
                missing = [label for label, value in (('user name', officer), ('reason', note)) if not value.strip()]
                if missing:
                    raise ValueError('Not recorded. Missing required field: ' + ' and '.join(missing) + '.')
                reviewed = current.plan
                if decision == 'PIN':
                    requested = PinnedPlacement(tail_id, pin_start, bay, crew, spare)
                    candidate_pins = tuple(pin for pin in pins if pin.tail_id != tail_id) + (requested,)
                    reviewed = plan(state, pinned_placements=candidate_pins)
                log.review_placement(source_plan_id, reviewed, tail_id, officer, decision, note, 'day-0',
                                     before_plan=current.plan)
                message = f'{decision} recorded for {tail_id}. Maintenance has not been executed.'
                if decision == 'PIN':
                    st.session_state.audited_current_plan = reviewed
                    st.session_state.review_flash = message
                    st.rerun()
                st.success(message)
            except ValueError as error:
                st.error(f'Not recorded: {error}' if not str(error).startswith('Not recorded') else str(error))
        if pins:
            st.caption('Pinned placements remain reserved across reruns. Approve/reject annotations do not release those reservations.')
        st.subheader('Local review trail')
        st.button('Verify audit chain', key='verify_chain')
        broken = log.verify_chain()
        if broken is None:
            st.success('Chain verified')
        else:
            st.error(f'Audit chain is broken at sequence {broken}.')
        audit_columns = ['seq', 'timestamp', 'user', 'action', 'tail', 'before', 'after', 'reason',
                         'prev_hash', 'row_hash', 'chain_version']
        st.dataframe(pd.DataFrame(log.rows())[audit_columns], hide_index=True, key='audit_rows',
                     alt='Append-only local planning, comparison and named review events')
        st.caption('Logical timestamps use the planning day. Before/after snapshots and reasons are chained locally.')

if tabs[4].open:
    with tabs[4]:
        st.subheader('Monte Carlo policy validation')
        st.info(VALIDATION_NOTE)
        try:
            csv_path = VALIDATION_DIR/'validation.csv'
            table = validation_report(csv_path, source_digest([csv_path]))
            st.caption('Post-hoc design corrections; v1 results were seen. Preserved v1 evidence is in artifacts/validation_v1/.')
            levels = list(dict.fromkeys(table.stress_level))
            stress = st.selectbox('Frozen stress level', levels, key='validation_stress',
                                  index=levels.index('stressed') if 'stressed' in levels else 0)
            repairs = sorted(table[table.stress_level == stress].repair_multiplier.dropna().unique())
            cell = table[table.stress_level == stress]
            horizons = sorted(map(int,cell.horizon_days.unique()))
            horizon = st.selectbox('Horizon (days)',horizons,key='validation_horizon',
                                   index=horizons.index(40) if 40 in horizons else 0)
            cell = cell[cell.horizon_days == horizon]
            multiplier = None
            if repairs:
                multiplier = st.selectbox('Assumed unplanned repair multiplier', repairs, key='validation_repair',
                                          index=repairs.index(2.) if 2. in repairs else 0)
                cell = cell[cell.repair_multiplier == multiplier]
                st.caption(f'Stress level {stress}; assumed repair multiplier {multiplier:g}. Horizon {horizon} days.')
            scenarios = int(cell.n_scenarios.max())
            st.caption(f'{scenarios} paired scenarios · cells show mean [95% bootstrap CI] · '
                       f'weekly K = {int(cell.weekly_budget.iloc[0])} for B2/B3/B4/B4b · '
                       'B0/B1/B2-K0 have no interventions. Source: validation.csv only.')
            st.caption(f'B1 schedules future interval deadlines through the same planner. '
                       f'Frozen training-derived interval: {int(cell.fixed_interval_cycles.iloc[0])} flight cycles (assumed).')
            st.caption(f'Initial-age rule: {cell.initial_age_rule.iloc[0]}.')
            policies = cell[cell.policy.isin(list(POLICY_NAMES))].set_index(['policy', 'metric'])
            grid = pd.DataFrame([{'Policy': policy, **{f'{title} ({unit})': cell_text(policies.loc[(policy, metric)])
                                                      for metric, (title, unit) in VALIDATION_METRICS.items()}}
                                 for policy in POLICY_NAMES])
            st.dataframe(grid, hide_index=True, key='validation_summary',
                         alt='Monte Carlo policy means and bootstrap confidence intervals, including ties')
            st.caption(' · '.join(f'{key}: {value}' for key, value in POLICY_NAMES.items()))
            metric = st.selectbox('Chart metric', list(VALIDATION_METRICS), key='validation_metric',
                                  format_func=lambda key: VALIDATION_METRICS[key][0])
            chart = go.Figure()
            for policy in POLICY_NAMES:
                row = policies.loc[(policy, metric)]
                chart.add_trace(go.Bar(x=[policy], y=[row['mean']], marker_color=POLICY_COLORS[policy], showlegend=False,
                                       error_y=dict(type='data', symmetric=False, array=[row.ci_high-row['mean']],
                                                    arrayminus=[row['mean']-row.ci_low])))
            chart.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=20),
                                yaxis_title=f'{VALIDATION_METRICS[metric][0]} ({VALIDATION_METRICS[metric][1]})')
            st.plotly_chart(chart, key='validation_chart', alt='Policy means with 95 percent bootstrap intervals',
                            config={'displaylogo': False})
            for left, right in PAIRED_POLICIES:
                difference = cell[cell.policy == f'{left}-{right}']
                st.markdown(f'**{left} minus {right} (paired scenarios)**')
                shown = difference.assign(**{'Metric': difference.metric.map(lambda m: VALIDATION_METRICS[m][0]),
                                             'Mean difference': difference['mean'],
                                             'CI low': difference.ci_low, 'CI high': difference.ci_high,
                                             'Scenarios tied': difference.tie_scenarios.astype('Int64'),
                                             'Scenarios': difference.n_scenarios})
                st.dataframe(shown[['Metric', 'Mean difference', 'CI low', 'CI high', 'Scenarios tied', 'Scenarios']],
                             hide_index=True, key=f'validation_difference_{left}_{right}',
                             alt=f'{left} minus {right} paired differences with confidence intervals and tie counts')
                ties = int(difference.all_outcomes_ties.iloc[0])
                outcome = 'tie in every scenario' if ties == scenarios else 'observed differences'
                scope = 'AOG, failures, wasted life and churn' if left == 'B2' and right == 'B2-K0' else 'all reported metrics'
                st.caption(f'{right} / {left}: {outcome}; {scope} exactly tied '
                           f'in {ties}/{scenarios} scenarios. The table retains outcome-specific ties.')
            st.markdown('**Candidate opportunities and actions actually applied**')
            diagnostic = cell[cell.row_type == 'policy'].drop_duplicates('policy')
            opportunity = diagnostic.rename(columns={'policy': 'Policy', 'review_weeks': 'Reviews',
                'multi_candidate_weeks': 'Weeks with 2+ candidates', 'multi_candidate_share': 'Share with 2+ candidates',
                'b2_b3_b4_b4b_different_tail_share': 'Share with different B2/B3/B4/B4b choices',
                'expedite_spare_count': 'Expedites', 'add_crew_shift_count': 'Crew shifts', 'add_bay_count': 'Bays'})
            st.dataframe(opportunity[['Policy', 'Reviews', 'Weeks with 2+ candidates', 'Share with 2+ candidates',
                                      'Share with different B2/B3/B4/B4b choices', 'Expedites', 'Crew shifts', 'Bays']],
                         hide_index=True, key='validation_opportunities',
                         alt='Candidate opportunities, differing choices and applied resource action counts')
            for note in diagnostic[diagnostic.policy.isin(INTERVENTION_POLICIES)].power_note.drop_duplicates():
                if 'test lacks power' in note:
                    st.warning(note)
                else:
                    st.caption(note)
            values = diagnostic[diagnostic.policy == 'B2'].iloc[0]
            tails = pd.DataFrame([{'Pair': f'{left}/{right}',
                                  'Share of weeks': f"{values[key+'_share']:.6g} "
                                      f"[{values[key+'_share_ci_low']:.6g}, {values[key+'_share_ci_high']:.6g}]"}
                                 for left,right in CHOICE_PAIRS for key in [f'{left.lower()}_{right.lower()}']])
            st.dataframe(tails, hide_index=True, key='validation_tails',
                         alt='Share of weeks with different chosen tails, with paired bootstrap intervals')
            sensitivity = table[(table.stress_level == stress) & table.policy.isin(list(POLICY_NAMES)) &
                                table.metric.isin(['aog_days', 'unplanned_failures'])].dropna(subset=['repair_multiplier'])
            if not sensitivity.empty:
                st.markdown('**Assumed repair-duration and horizon sensitivities**')
                wide = sensitivity.assign(Value=sensitivity.apply(cell_text, axis=1),
                                          Repair=sensitivity.repair_multiplier.map(lambda v: f'{v:g}x')
                                          ).pivot(index=['horizon_days','Repair', 'policy'], columns='metric', values='Value').reset_index()
                st.dataframe(wide.rename(columns={'horizon_days':'Horizon (days)','policy': 'Policy', 'aog_days': 'AOG (aircraft-days)',
                                                 'unplanned_failures': 'Unplanned failures'}),
                             hide_index=True, key='validation_repair_table',
                             alt='Repair multiplier sensitivity for AOG and failures')
            st.download_button('Download validation CSV', data=csv_path.read_bytes(),
                               file_name='validation.csv', mime='text/csv', key='download_validation')
        except (OSError, ValueError, KeyError) as error:
            st.warning(f'Generated validation report unavailable: {error}. Run python scripts/tasks.py validation offline.')

st.divider()
with st.expander('Model metrics · NASA FD001 benchmark'):
    metrics_path = ROOT/'artifacts/rul_metrics.json'
    try:
        metrics = json.loads(metrics_path.read_text(encoding='utf-8'))
        test = metrics['test']
        st.caption(metrics['data_label'])
        with st.container(horizontal=True):
            st.metric('RMSE (cycles)', f"{test['rmse']:.3f}", border=True)
            st.metric('NASA asymmetric score', f"{test['nasa_asymmetric_score']:.3f}", border=True)
            st.metric('Coverage (PICP)', f"{test['picp']:.3f}", border=True)
            st.metric('Mean range width (cycles)', f"{test['mpiw']:.3f}", border=True)
        st.caption('Coverage is a measured test fraction. Benchmark metrics describe simulated FD001 engines; the T-04 story uses assumed inputs.')
    except (OSError, ValueError, KeyError):
        st.warning('Generated model metrics unavailable. Train offline with python scripts/tasks.py train after supplying the NASA files.')
with st.expander('Definitions & limitations'):
    st.markdown('Deadline = floor((point − buffer) / cycles-per-day). Induction must start on or before it. '
                'An induction consumes a spare and reserves one bay and one crew for its duration.')
    st.markdown('Decision float perturbs one point in integer steps and replans all tails. A > R value is a finite search bound. '
                'Deadline slack = point − buffer − rate × (start − today), with placement frozen. '
                'Covered requires both margins to cover half-width; otherwise Fragile. Unplanned slack is undefined.')
    st.caption('All fleet records are fictional. Crew-shift capacity is assumed and inspection is assumed, not scored. '
               'New fleets need validation and likely retraining. This prototype makes no airworthiness decision.')
