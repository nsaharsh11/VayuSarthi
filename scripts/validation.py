"""Generate the offline paired policy validation report from real calibration errors."""
import argparse
import hashlib
import io
import json
import shutil
from concurrent.futures import ProcessPoolExecutor
from contextlib import redirect_stdout, nullcontext
from dataclasses import asdict, replace
from pathlib import Path

from vayu.quality import read_fleet_pack, planning_state_from_fleet
from vayu.rul import predict_tail
from vayu.schemas import canonical_json
from vayu.sim import (SimulationConfig, calibration_residuals, monte_carlo, write_validation,
                      POLICY_NAMES, STRESS_LEVELS, REPAIR_MULTIPLIERS, stress_inputs, training_fixed_interval,
                      print_week_trace, chosen_tail_differences, validation_cell_rows, ValidationResult,
                      VALIDATION_METRICS, PAIRED_POLICIES, CHOICE_PAIRS, INTERVENTION_POLICIES,
                      HORIZON_DAYS, DESIGN_REVISION, paired_metrics, draw_initial_ages)
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def write_comparison_report(summary: pd.DataFrame, output: Path) -> None:
    """Render all generated mean/CI cells without substituting result values."""
    from vayu.sim import VALIDATION_METRICS, POLICY_NAMES
    lines = ['# Validation comparison','', '**simulated; scenario-based**','',
             'Each cell is mean [95% percentile bootstrap CI] from paired scenarios.',
             'Post-hoc v2 design corrections: v1 results were seen. The corrected rules were frozen before this rerun.',
             'Stress settings and training-derived B1 interval are unchanged; neutral paired ages use its scale.',
             'AOG includes grounded waiting and maintenance; healthy future-slot waiting is excluded.',
             'Repair multipliers are assumed. Ties are retained. AOG is censored at the horizon.','']
    for (level,horizon,multiplier),group in summary.groupby(['stress_level','horizon_days','repair_multiplier'],sort=False):
        lines.extend([f'## {level}; horizon {horizon:g} days; assumed repair {multiplier:g}x','',
                      '| Policy | '+' | '.join(f'{title} ({unit})' for title,unit in VALIDATION_METRICS.values())+' |',
                      '| --- | '+' | '.join('---' for _ in VALIDATION_METRICS)+' |'])
        indexed = group.set_index('policy')
        for policy in POLICY_NAMES:
            cells = []
            for metric in VALIDATION_METRICS:
                values = indexed.loc[policy]
                cells.append(f"{values[metric+'_mean']:.6g} [{values[metric+'_ci_low']:.6g}, {values[metric+'_ci_high']:.6g}]")
            lines.append('| '+policy+' | '+' | '.join(cells)+' |')
        lines.append('')
        for left,right in PAIRED_POLICIES:
            values = indexed.loc[f'{left}-{right}']
            lines.extend([f'### {left} minus {right} (paired)', '',
                          '| Outcome | Mean difference [95% CI] | Exact scenario ties |',
                          '| --- | --- | --- |'])
            for metric in paired_metrics(left,right):
                title,unit = VALIDATION_METRICS[metric]
                lines.append(f"| {title} ({unit}) | {values[metric+'_mean']:.6g} "
                             f"[{values[metric+'_ci_low']:.6g}, {values[metric+'_ci_high']:.6g}] | "
                             f"{values[metric+'_ties_over_n']} |")
            lines.extend(['',f"Combined ties ({values.tie_metric_scope}): {values.ties_over_n}", ''])
        lines.extend(['### Chosen-tail differences', '',
                      '| Policy | Weeks with 2+ candidates / reviews | Any B2/B3/B4/B4b choice difference share | Expedites | Crew shifts | Bays |',
                      '| --- | --- | --- | --- | --- | --- |'])
        for _, values in group[group.row_type == 'policy'].iterrows():
            lines.append(f"| {values.policy} | {int(values.multi_candidate_weeks)}/{int(values.review_weeks)} "
                         f"({values.multi_candidate_share:.6g}) | {values.b2_b3_b4_b4b_different_tail_share:.6g} | "
                         f"{int(values.expedite_spare_count)} | {int(values.add_crew_shift_count)} | {int(values.add_bay_count)} |")
        lines.append('')
        for policy in INTERVENTION_POLICIES:
            lines.append(f"{policy}: {indexed.loc[policy].power_note}")
        values = indexed.loc['B2']
        for left,right in CHOICE_PAIRS:
            key = f'{left.lower()}_{right.lower()}'
            lines.append(f"{key.upper().replace('_','/')} share of differing weeks: {values[key+'_share']:.6g} "
                         f"[{values[key+'_share_ci_low']:.6g}, {values[key+'_share_ci_high']:.6g}]")
        lines.append('')
    (output/'validation_comparison.md').write_text('\n'.join(lines),encoding='utf-8',newline='\n')


def load_unchanged_sources(directory: Path, provenance: dict) -> ValidationResult:
    """Load existing raw evidence, guarding the fleet, model and residual provenance."""
    manifest = json.loads((directory/'validation_manifest.json').read_text(encoding='utf-8'))
    if any(manifest.get(key) != value for key,value in provenance.items()):
        raise ValueError('Unchanged-policy archive provenance does not match current inputs')
    runs = pd.read_csv(directory/'validation_runs.csv')
    weeks = pd.read_csv(directory/'validation_weeks.csv',keep_default_na=False)
    for column in ('action_ids','fragile_tails','candidates','action_types'):
        if column in weeks:
            weeks[column] = weeks[column].map(json.loads)
    if 'action_types' not in weeks:
        def action_types(identifiers: list[str]) -> list[str]:
            kinds = []
            for identifier in identifiers:
                if identifier.startswith('EXPEDITE:'):
                    kinds.append('expedite_spare')
                elif identifier in ('ADD:CREW','ADD:BAY'):
                    kinds.append('add_crew_shift' if identifier == 'ADD:CREW' else 'add_bay')
                else:
                    raise ValueError('Unrecognized scored action in unchanged-policy archive')
            return kinds
        weeks['action_types'] = weeks.action_ids.map(action_types)
    for column in ('tail','top_action'):
        weeks[column] = weeks[column].map(lambda value: None if value == '' else value)
    for column in ('top_benefit','top_benefit_per_cost','chosen_rank'):
        weeks[column] = weeks[column].map(lambda value: None if value == '' else float(value))
    manifest['source_runs_sha256'] = hashlib.sha256((directory/'validation_runs.csv').read_bytes()).hexdigest()
    manifest['source_weeks_sha256'] = hashlib.sha256((directory/'validation_weeks.csv').read_bytes()).hexdigest()
    return ValidationResult(pd.DataFrame(),runs,weeks,manifest)


def preserve_v1_artifacts(output: Path) -> Path | None:
    """Copy pre-correction evidence byte-for-byte once; verify and never overwrite it."""
    archive = output/'validation_v1'
    ledger_path = archive/'archive_manifest.json'
    if archive.exists():
        if not ledger_path.is_file():
            raise ValueError('Incomplete v1 archive; preserve and inspect it before rerunning')
        ledger = json.loads(ledger_path.read_text(encoding='utf-8'))
        for name,digest in ledger['files_sha256'].items():
            path = archive/name
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                raise ValueError('The preserved v1 archive failed its hash check')
        return archive
    if not (output/'validation.csv').is_file():
        return None
    manifest = output/'validation_manifest.json'
    if manifest.is_file() and json.loads(manifest.read_text(encoding='utf-8')).get('design_revision') == DESIGN_REVISION:
        return None  # No v1 existed before a fresh caller's first corrected run.
    names = ['validation.csv','validation_comparison.md','validation_diagnostics.log',
        'validation_manifest.json','validation_preregistered.json','validation_runs.csv','validation_weeks.csv',
        'validation_b1_scenarios.csv','validation_opportunities.csv','validation_phase18_execution.log',
        'validation_phase18_checks.log','test_phase18.log','calibration_residuals.csv']
    archive.mkdir(parents=True)
    if (output/'validation').is_dir():
        shutil.copytree(output/'validation',archive/'validation')
    for name in names:
        if (output/name).is_file():
            shutil.copy2(output/name,archive/name)
    ledger = {'description':'Preserved v1 simulated evidence; results were seen before v2 corrections',
              'files_sha256':{p.relative_to(archive).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in sorted(archive.rglob('*')) if p.is_file()}}
    ledger_path.write_bytes(canonical_json(ledger).encode('utf-8'))
    return archive


def validate(root: Path, config: SimulationConfig | None = None, *, workers: int = 1,
             resume_frozen: bool = False) -> None:
    """Use the validated four-silo pack; no model training or download is attempted."""
    settings = config or SimulationConfig()
    if isinstance(workers,bool) or not isinstance(workers,int) or workers < 1:
        raise ValueError('workers must be a positive integer')
    pack = read_fleet_pack(root/'data/fleet')
    if pack.planning_hold:
        raise ValueError('Validation fleet is on planning hold: '+ '; '.join(pack.reasons))
    model = root/'artifacts/rul_model.joblib'
    predictions = {engine:predict_tail(engine,model) for engine in sorted(pack.accepted['tails.csv'].engine_id)}
    state = planning_state_from_fleet(pack,predictions,safety_buffer=0)
    pool = calibration_residuals(root/'data/CMAPSS',model)
    settings = replace(settings,fixed_interval_cycles=training_fixed_interval(root/'data/CMAPSS',model))
    ages = draw_initial_ages(state,settings)
    provenance = dict(fleet='data/fleet',model_sha256=hashlib.sha256(model.read_bytes()).hexdigest(),
        calibration_residuals_sha256=hashlib.sha256(pool.to_csv(index=False,lineterminator='\n',float_format='%.17g').encode()).hexdigest(),
        fleet_files_sha256={path.name:hashlib.sha256(path.read_bytes()).hexdigest()
                           for path in sorted((root/'data/fleet').glob('*.csv'))})
    output = root/'artifacts'
    preserve_v1_artifacts(output)
    preregistered = {'design_revision':DESIGN_REVISION,'post_hoc':True,'v1_results_were_seen':True,
                    'horizon_days':HORIZON_DAYS,'stress_levels':[asdict(level) for level in STRESS_LEVELS],
                    'repair_multipliers':REPAIR_MULTIPLIERS,'base_config':asdict(settings),
                    'fixed_interval_rule':'ceil(median terminal TRAIN cycles of fit engines only); assumed',
                    'training_file_sha256':hashlib.sha256((root/'data/CMAPSS/train_FD001.txt').read_bytes()).hexdigest(),
                    'attention_rule':'14-day candidates; earliest deadline / slack shortfall / min(float,slack) shortfall',
                    'b1_rule':'preplan interval deadlines inside horizon, using technical age; no model buffer',
                    'initial_age_rule':'independent uniform [0, frozen interval); same paired ages across every cell',
                    'initial_age_seed':settings.seed+1000,
                    'initial_ages_sha256':hashlib.sha256(canonical_json(ages).encode()).hexdigest(),
                    'action_score':'selected-tail Covered increase plus Late reduction per man-hour; no fallback target',
                    'b4b_rule':'half-width minus float; > R uses R; Unplanned float zero; ties deadline then tail ID',
                    'control_comparison_metrics':['aog_days','unplanned_failures','wasted_life_cycles','plan_churn'],
                    'control':'B2-K0 shares urgency planning with no interventions',
                    'sim_source_sha256':hashlib.sha256((ROOT/'vayu/sim.py').read_bytes()).hexdigest(),
                    **provenance}
    frozen = canonical_json(preregistered).encode()
    if resume_frozen:
        frozen = (output/'validation_preregistered.json').read_bytes()
        original = json.loads(frozen)
        ignored = {'sim_source_sha256'}  # The paired export list changed; policies did not.
        if canonical_json({k:v for k,v in original.items() if k not in ignored}) != canonical_json(
                {k:v for k,v in preregistered.items() if k not in ignored}):
            raise ValueError('Resume inputs or assumptions differ from the frozen design')
    else:
        (output/'validation_preregistered.json').write_bytes(frozen)
    print('Frozen assumptions before comparison: '+frozen.decode(),flush=True)
    pd.DataFrame([{'scenario_id':index,'tail_id':tail,'initial_age_cycles':age,
                  'fixed_interval_cycles':settings.fixed_interval_cycles,'age_seed':settings.seed+1000,
                  'source':'assumed uniform initial technical age; post-hoc v2'}
                  for index,row in enumerate(ages) for tail,age in sorted(row.items())]).to_csv(
        output/'validation_initial_ages.csv',index=False,lineterminator='\n',float_format='%.17g')
    trace_parts: list[str] = []

    def emit_trace(result: ValidationResult, title: str) -> None:
        """Print and retain the same generated weekly evidence for offline review."""
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print(title)
            print_week_trace(result)
            print(chosen_tail_differences(result.weeks).to_string(index=False))
        trace = '\n'.join(line.rstrip() for line in buffer.getvalue().splitlines())+'\n'
        print(trace,end='',flush=True)
        trace_parts.append(trace)
    pool.to_csv(output/'calibration_residuals.csv',index=False,lineterminator='\n',float_format='%.17g')
    # Preserve a diagnostic run on the original pack rather than substituting
    # its inputs silently with a stress pack. Only three paired draws are needed.
    diagnostic_path = output/'validation/original_diagnostic'
    if resume_frozen and (diagnostic_path/'validation_manifest.json').is_file():
        diagnostic = load_unchanged_sources(diagnostic_path, {'design_revision': DESIGN_REVISION})
    else:
        diagnostic = monte_carlo(state,pool,ages[:3],replace(settings,n_scenarios=3),progress=False)
        write_validation(diagnostic,diagnostic_path)
    emit_trace(diagnostic,'Original-pack diagnostic')
    summaries, b1_reports, cases = [], [], []
    for level in STRESS_LEVELS:
        inputs,level_config = stress_inputs(state,level,settings)
        for horizon in HORIZON_DAYS:
            for multiplier in REPAIR_MULTIPLIERS:
                cases.append((level,horizon,multiplier,replace(inputs,horizon=inputs.today+horizon),
                              replace(level_config,repair_multiplier=multiplier)))
    completed = {}
    if resume_frozen:
        for index,(level,horizon,multiplier,inputs,cell_config) in enumerate(cases):
            directory = output/'validation'/level.name/f'horizon_{horizon}'/f'repair_{multiplier:g}'.replace('.', 'p')
            if not (directory/'validation_manifest.json').is_file():
                continue
            stored = load_unchanged_sources(directory, provenance)
            if (stored.manifest['preregistered_sha256'] != hashlib.sha256(frozen).hexdigest() or
                stored.manifest['config'] != asdict(cell_config) or
                stored.manifest['initial_ages_sha256'] != preregistered['initial_ages_sha256'] or
                stored.manifest['state_sha256'] != hashlib.sha256(canonical_json(inputs).encode()).hexdigest()):
                raise ValueError('Completed cell does not match the frozen resume inputs')
            if set(stored.runs.policy) != set(POLICY_NAMES) or any(
                len(group) != settings.n_scenarios or set(group.scenario_id) != set(range(settings.n_scenarios))
                for _,group in stored.runs.groupby('policy')):
                raise ValueError('Completed resume cell has incomplete scenarios')
            expected_weeks = {(scenario, week, policy) for scenario in range(settings.n_scenarios)
                              for week in range((horizon + 6)//7) for policy in POLICY_NAMES}
            if len(stored.weeks) != len(expected_weeks) or set(zip(stored.weeks.scenario_id,
                    stored.weeks.week, stored.weeks.policy)) != expected_weeks:
                raise ValueError('Completed resume cell has incomplete weekly evidence')
            completed[index] = stored
    with ProcessPoolExecutor(max_workers=workers) if workers > 1 else nullcontext() as executor:
        futures = {index:executor.submit(monte_carlo,inputs,pool,ages,cell_config)
                   for index,(_,_,_,inputs,cell_config) in enumerate(cases) if index not in completed} if executor else {}
        for index,(level,horizon,multiplier,inputs,cell_config) in enumerate(cases):
            print(f'\nStress {level.name}; horizon {horizon}; assumed repair multiplier {multiplier:g}',flush=True)
            name = f'repair_{multiplier:g}'.replace('.','p')
            directory = output/'validation'/level.name/f'horizon_{horizon}'/name
            if index in completed:
                result = completed[index]
                print('Retained complete frozen cell; no policy rerun',flush=True)
            else:
                result = futures[index].result() if executor else monte_carlo(inputs,pool,ages,cell_config,progress=True)
                result.manifest.update(**provenance,stress_level=asdict(level),
                    preregistered_sha256=hashlib.sha256(frozen).hexdigest(),
                    post_hoc=True,initial_age_rule=preregistered['initial_age_rule'],initial_age_seed=settings.seed+1000,
                    fixed_interval_rule=preregistered['fixed_interval_rule'])
                write_validation(result,directory)
            b1 = result.runs[result.runs.policy == 'B1'][['scenario_id','aog_days','unplanned_failures',
                'waiting_spare_days','waiting_bay_days','waiting_crew_days','waiting_slot_days','maintenance_days',
                'initial_overdue_tails','inductions_before_due']].assign(stress_level=level.name,
                repair_multiplier=multiplier,horizon_days=horizon,fixed_interval_cycles=cell_config.fixed_interval_cycles)
            print('B1 per-scenario AOG, waits and frozen interval',flush=True)
            print(b1.to_string(index=False),flush=True)
            b1_reports.append(b1)
            if multiplier == 2.:
                emit_trace(result,f'Diagnostic traces: three scenarios, {level.name}; horizon {horizon}; assumed 2x repair')
            exported = pd.read_csv(directory/'validation.csv')
            if 'B4b-B3' not in set(exported.policy):
                extra = exact_b4b_b3(exported, result.manifest)
                exported = pd.concat([exported, extra], ignore_index=True)
            summaries.append(exported)
            if level.name == 'stressed' and multiplier == 2. and horizon == 40 and index not in completed:
                write_validation(result,output)  # Compatible default for existing readers.
    comparison = pd.concat(summaries,ignore_index=True)
    comparison.to_csv(output/'validation.csv',index=False,lineterminator='\n',float_format='%.12g')
    comparison[comparison.row_type == 'policy'][['stress_level','repair_multiplier','horizon_days','policy',*[
        column for column in comparison if column in ('multi_candidate_share','review_weeks','multi_candidate_weeks',
        'b2_b3_b4_different_tail_share','b2_b3_b4_b4b_different_tail_share',
        'expedite_spare_count','add_crew_shift_count','add_bay_count','power_note')]]
        ].to_csv(output/'validation_opportunities.csv',index=False,lineterminator='\n',float_format='%.12g')
    pd.concat(b1_reports,ignore_index=True).to_csv(output/'validation_b1_scenarios.csv',index=False,
                                                 lineterminator='\n',float_format='%.12g')
    (output/'validation_diagnostics.log').write_text(''.join(trace_parts),encoding='utf-8',newline='\n')
    write_comparison_report(comparison,output)
    if resume_frozen:
        ledger = {'description':'Resume unfinished cells with frozen v2 inputs; completed evidence retained',
                  'retained_cells':len(completed),'evaluated_cells':len(cases)-len(completed),
                  'frozen_design_sha256':hashlib.sha256(frozen).hexdigest(),
                  'current_sim_source_sha256':hashlib.sha256((ROOT/'vayu/sim.py').read_bytes()).hexdigest(),
                  'current_margins_source_sha256':hashlib.sha256((ROOT/'vayu/margins.py').read_bytes()).hexdigest(),
                  'computation_correction':'Proved bounded spare exhaustion and monotonic deadline-order/status shortcuts; no policy definition change'}
        (output/'validation_resume_manifest.json').write_bytes(canonical_json(ledger).encode('utf-8'))


def exact_b4b_b3(existing: pd.DataFrame, manifest: dict) -> pd.DataFrame:
    """Use original unrounded equality evidence to retain exact CIs and ties."""
    ties = {row['metric']: row for row in manifest['b3_b4']}
    count = manifest['config']['n_scenarios']
    if not all(metric in ties and ties[metric]['all_scenarios_tied'] and
               ties[metric]['exact_scenario_ties'] == count for metric in VALIDATION_METRICS):
        raise ValueError('Exact B4b-B3 refresh needs unrounded evidence: use a full-precision rerun')
    extra = existing[existing.policy == 'B4b-B4'].copy()
    if len(extra) != 1:
        raise ValueError('The original B4b-B4 comparison is missing')
    extra['policy'] = 'B4b-B3'
    extra['policy_name'] = 'B4b minus B3 (paired)'
    return extra


def refresh_exports(root: Path) -> None:
    """Add the requested B4b-B3 comparison from frozen v2 raw evidence only.

    Keep existing policy estimates/CIs, raw runs and simulation manifests.
    Validate every cell before writing any report; no planner is called here.
    """
    output = root/'artifacts'
    preserve_v1_artifacts(output)
    frozen = (output/'validation_preregistered.json').read_bytes()
    provenance = json.loads(frozen)
    if provenance.get('design_revision') != DESIGN_REVISION:
        raise ValueError('Report refresh requires the frozen v2 design')
    frames, cells, inputs = [], [], {}
    for level in STRESS_LEVELS:
        for horizon in HORIZON_DAYS:
            for multiplier in REPAIR_MULTIPLIERS:
                directory = output/'validation'/level.name/f'horizon_{horizon}'/f'repair_{multiplier:g}'.replace('.', 'p')
                result = load_unchanged_sources(directory, {'design_revision': DESIGN_REVISION})
                if result.manifest.get('preregistered_sha256') != hashlib.sha256(frozen).hexdigest():
                    raise ValueError('Stored validation cell does not match the frozen v2 design')
                config = SimulationConfig(**result.manifest['config'])
                if result.manifest['horizon_days'] != horizon or config.repair_multiplier != multiplier:
                    raise ValueError('Stored validation cell does not match its sensitivity key')
                expected_ids = set(range(config.n_scenarios))
                if set(result.runs.policy) != set(POLICY_NAMES) or any(
                    set(group.scenario_id) != expected_ids or len(group) != config.n_scenarios
                    for _, group in result.runs.groupby('policy')):
                    raise ValueError('Stored validation cell lacks complete paired policy scenarios')
                existing = pd.read_csv(directory/'validation.csv')
                if existing[existing.row_type == 'policy'].policy.tolist() != list(POLICY_NAMES):
                    raise ValueError('Stored validation report has an incomplete policy set')
                # The executed, unrounded manifest proves B3 == B4 exactly.
                # Preserve original CIs/ties instead of rounding raw differences.
                extra = exact_b4b_b3(existing, result.manifest)
                # Retain the old estimates and their original serialized precision.
                frame = pd.concat([existing[existing.policy != 'B4b-B3'], extra], ignore_index=True)
                frames.append(frame)
                cells.append((directory/'validation.csv', frame))
                for name in ('validation_runs.csv', 'validation_weeks.csv', 'validation_manifest.json'):
                    path = directory/name
                    inputs[path.relative_to(output).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    comparison = pd.concat(frames, ignore_index=True)
    for path, frame in cells:
        frame.to_csv(path, index=False, lineterminator='\n', float_format='%.12g')
    comparison.to_csv(output/'validation.csv', index=False, lineterminator='\n', float_format='%.12g')
    write_comparison_report(comparison, output)
    ledger = {'description': 'Post-hoc report-only B4b-B3 addition; no policies or scenarios rerun',
              'exact_tie_proof': 'Original unrounded manifests prove B3 == B4 in every scenario/metric; B4b-B3 equals original B4b-B4',
              'input_files_sha256': inputs,
              'simulation_source_sha256': provenance['sim_source_sha256'],
              'frozen_design_sha256': hashlib.sha256(frozen).hexdigest(),
              'paired_export_source_sha256': hashlib.sha256((ROOT/'vayu/sim.py').read_bytes()).hexdigest(),
              'export_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'output_files_sha256': {path.relative_to(output).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                     for path in [*(path for path, _ in cells), output/'validation.csv',
                                                  output/'validation_comparison.md']}}
    (output/'validation_refresh_manifest.json').write_bytes(canonical_json(ledger).encode('utf-8'))
    print(f'Refreshed {len(cells)} frozen sensitivity cells; reports contain {len(comparison)} generated rows.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Offline paired validation; simulated; scenario-based')
    parser.add_argument('--seed',type=int,default=26249)
    parser.add_argument('--scenarios',type=int,default=200)
    parser.add_argument('--workers',type=int,default=2,help='Local independent cell workers; all corrected policies evaluated afresh')
    parser.add_argument('--refresh-summary', action='store_true', help='Add paired comparisons from existing complete v2 raw runs')
    parser.add_argument('--resume-frozen', action='store_true', help='Retain complete frozen v2 cells and evaluate only unfinished cells')
    arguments = parser.parse_args()
    if arguments.refresh_summary:
        refresh_exports(ROOT)
    else:
        validate(ROOT,SimulationConfig(seed=arguments.seed,n_scenarios=arguments.scenarios),workers=arguments.workers,
                 resume_frozen=arguments.resume_frozen)
