# Vayu Sarthi

Offline decision support for maintenance planning and fleet availability,
created for the user-supplied SIH26249 problem. All fleet data is fictional or
simulated. NASA C-MAPSS FD001 provides benchmark replay, not aircraft data.
One engine module represents each fictional civilian tail. A human reviews
each proposed plan; recording approval does not execute maintenance.

## Run locally

Python 3.11+ is required. This workspace was verified with Python 3.12.
Run from the repository root:

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
python scripts/tasks.py setup
python scripts/tasks.py data-check
python scripts/tasks.py test
python scripts/tasks.py app
```

Open the loopback URL printed by Streamlit. Dependencies are pinned,
including the resolved dependency closure. Use the wheelhouse procedure below
for a disconnected install. Everything then runs locally without network access, LLMs, cloud
services, external fonts, CDNs or telemetry. SQLite is included in Python.
Plotly assets are served locally.

The shipped fleet, model and generated reports support the demo without
retraining. For the point/quantile model, obtain official FD001 files, review
their terms, and put train_FD001.txt, test_FD001.txt and RUL_FD001.txt in
data/CMAPSS/. This workspace has the supplied files; they are excluded from
Git and must be supplied on a fresh checkout. Missing files produce manual
download instructions and a nonzero training exit.

```powershell
python scripts/tasks.py train
python scripts/tasks.py test
```

Windows uses scripts/tasks.py; Make targets invoke the same checks.

### Offline wheelhouse installation

On a connected preparation computer with the **same operating system, CPU
architecture and Python minor version** as the demo computer, download the
pinned wheels. This preparation step uses the package index; the app does not.
Use the interpreter intended for the demo environment:

```powershell
python -m pip download --only-binary=:all: --dest wheelhouse -r requirements.txt
python -m pip download --only-binary=:all: --dest checker-wheelhouse -r requirements-checker.txt
```

Copy the repository, both wheelhouse directories, shipped model/report assets,
and the manually supplied FD001 files to the disconnected computer. Put the
three FD001 text files in both `data/CMAPSS/` (current pipeline) and `data/raw/`
(retained benchmark-loader tests). The checker
has a separate dependency set and must stay in its own environment. If wheel
preparation fails for the target platform, resolve that before disconnecting;
do not silently substitute package versions or rely on source builds.

```powershell
python -m venv .venv
.venv/Scripts/python.exe -m pip install --no-index --find-links wheelhouse -r requirements.txt
.venv/Scripts/python.exe scripts/tasks.py setup
python -m venv .checker-venv
.checker-venv/Scripts/python.exe -m pip install --no-index --find-links checker-wheelhouse -r requirements-checker.txt
.venv/Scripts/python.exe scripts/tasks.py test
.venv/Scripts/python.exe -m streamlit run app.py
```

`setup` installs this checkout with dependency resolution and build isolation
disabled; its setuptools/wheel build tools are already in requirements.txt.
No package index is consulted by these offline installation commands. Keep
the checker wheels separate from the application wheels and rehearse on the
actual disconnected demo computer. Full model tests also need the local NASA
files; the cached demo itself does not train a model.

## What is implemented

- `vayu/schemas.py`: immutable, validated believed inputs with no evaluation fields.
- `vayu/rul.py`: causal 30-cycle features, engine-separated LightGBM point and
  quantile models, split-conformal ranges and official-test metrics/cache.
- `vayu/quality.py`: CSV validation, conflict rejection, quarantine and idempotent SQLite snapshots.
- `vayu/planner.py`: deterministic deadline/ID ordering and bay, crew and spare assignments.
- `vayu/margins.py`: both-sign whole-fleet decision float, frozen deadline slack and attention labels.
- `vayu/whatif.py`: costed resource/assumed inspection comparisons, ranking and pairs.
- `vayu/sim.py`: seeded fictional packs, paired Monte Carlo policies and separate synthetic tail-day accounting.
- `vayu/audit.py`: append-only hash chain, named placement reviews and persisted pins.
- `app.py`: light-theme Data, Fleet board, What-if, Approvals and Validation tabs,
  an audited Reset demo button, and a model-metrics footer.
- Tests cover every module, UI review/navigation, offline runtime, resource
  reservation, determinism and the ground-truth firewall.

The earlier Phase 0/1 scaffold remains tested in src/pdm/. The former FastAPI,
static UI were superseded by your Streamlit request; they are not part of this
prototype. The current paired policy evaluation is described below. No requested module is pending.
Physical disconnected-browser rehearsal and hackathon eligibility checks
remain human demo preparation; headless tests do not establish those.

## Domain rules

The planner's dictionary entry point is:

```python
from vayu.planner import plan_fleet

rows = plan_fleet(
    tails=[{'tail_id': 'T1', 'rul_point': 20, 'rate': 2}],
    spares=[{'spare_id': 'S2', 'available_day': 12}],
    bays=['B1'], crews=['C1'],
    config={'today': 0, 'horizon': 40, 'safety_buffer': 2, 'duration': 3},
)
```

Each row contains `tail`, `deadline_day`, `start_day`, `bay`, `crew`, `spare`,
`status`, `binding_resource` and a plain-language `reason_code`. The typed
`plan(PlanningState)` interface remains available for decision-float analysis.

Optional `pinned_placements` accept `PinnedPlacement` objects or dictionaries
with `tail`/`tail_id`, `start_day`, `bay`, `crew` and `spare`. Pins reserve
capacity first, consume their spares and release bays/crews at induction end.
Automatic jobs use capacity after the last pin on their selected resources;
earlier gaps are not filled. Conflicting or unavailable reservations fail
clearly. Pins keep their start/resources while deadline and status are derived
from the current planning point.

RUL and buffer are flight cycles; utilisation is cycles/day per tail.
Deadline is `floor((point - safety_buffer) / rate)`. An induction must START
by that day. Its start is `max(today+1, spare_available, bay_free, crew_free)`.
A spare is consumed; bay and crew become free at `start+duration`.
The spare horizon is inclusive; an induction may finish after the horizon.

Decision float changes one tail's point in integer steps in both signs and
reruns the entire planner. It compares every tail's `(start, bay, spare,
status)`, including effects on other tails. No change through the bound is
displayed as `> R`. Deadline slack is ordinary deadline slack in cycles:
`point - safety_buffer - rate*(start-today)`, with placement frozen.
The interval half-width is `(upper-lower)/2`.

Covered requires float and slack to cover the half-width; otherwise Fragile.
When `> R` cannot establish this comparison, Fragile is conservative and the
UI explains the limited search. Unplanned slack is undefined and attention
is Fragile. These labels describe planning attention only. Estimates are
snapshots; changing today does not invent a feed.

Tie-breaking and ambiguities are recorded in
[docs/DECISIONS.md](docs/DECISIONS.md). The active revision precedes the
historical specification in [docs/SPEC.md](docs/SPEC.md).

## Generated evidence

Generated benchmark values are in reports/model_metrics.json. Full-training
reproducibility hashes are in reports/model_reproducibility.json. Generated
fictional plan, attention and accounting are in reports/demo_results.json.
No result values are embedded in this documentation or the UI.

See [docs/DEMO_RUNBOOK.md](docs/DEMO_RUNBOOK.md) for the click path and recovery.

## Limitations — one-page briefing

**This is not an airworthiness tool.** It is an offline prototype for comparing
maintenance placements and planning attention. Covered and Fragile compare
decision float and ordinary deadline slack with an estimated interval
half-width. They do not certify an aircraft, authorize a flight, diagnose an
engine, or establish a maintenance release. Approving a placement records a
named review; it executes no maintenance. Qualified personnel and applicable
maintenance procedures remain responsible for operational decisions.

**The engines and fleet are simulated.** Tail IDs, utilisation, technical
records, resource capacities, spare ETAs and the T-04 demonstration ranges
are fictional. NASA C-MAPSS FD001 consists of simulated degradation histories,
used here as a benchmark replay with explicit fictional tail-to-engine
aliases. It is not measured aircraft operating data. The demo uses a fixed
snapshot rather than an aircraft feed. Benchmark RMSE, asymmetric score,
coverage and interval width describe that dataset and model configuration;
they establish no performance on an actual fleet.

**All validation is simulated; scenario-based.** Policies share seeded life
errors and spare delays drawn under the documented assumptions. Calibration
residuals may not represent a different fleet or future operating conditions;
the assumed delay distribution, fixed overhaul interval and short horizon
also shape outcomes. A replacement is assumed serviceable for the remaining
horizon, and each original engine has at most one removal. AOG includes
grounded resource waiting and preventive induction or failure repair; healthy
aircraft awaiting future slots keep flying. Bootstrap intervals
describe variation within these generated scenarios, not uncertainty about
all real-world conditions. Report ties, including B3/B4 ties, as generated;
the setup does not establish a universally superior policy.

**Planning scope covers resources only:** bays, technician crews and spare
engines under a day-based abstraction, using supplied utilisation, durations
and believed RUL. The deterministic greedy rule follows deadline and tail-ID
ordering; it does not always minimise Late count. Pins reserve resources
first, and the scheduler does not fill gaps before the last pin on a resource.
It does not model crew qualifications, task dependencies, aircraft-specific
certification, detailed shifts, transport, tooling, full parts compatibility
or approved maintenance instructions. An extra crew shift is represented by
an additional crew through the horizon. Costs are assumed man-hours, not
observed labor or procurement expenses.

**Ranges and interventions remain assumptions.** Conformal ranges depend on
the calibration population and correlated engine trajectories; observed
coverage can fall below the nominal level. Inspecting a tail narrows its
half-width by the labelled assumed factor, without a diagnostic measurement
or a change to simulated true life. Expedites change ETA assumptions.
Decision float searches only through the chosen finite bound; `> R` does not
identify the threshold beyond it. Slack freezes a placement, while float
replans the fleet. New fleets need independent data, validation and likely
retraining before these estimates could inform an operational process.

**Quality and audit checks have bounded scope.** Badges and quarantine detect
schema errors, stale records, duplicates and defined silo conflicts; they do
not independently verify source truth or mechanical condition. A corrupted
pack holds planning. The local SQLite hash chain detects altered linked
records but has no external anchor or authenticated identity provider. Reset
demo releases the assumed story's pins through new chained events and keeps
all earlier reviews. Preserve a broken database for review: reset cannot
repair or erase its history. The disconnected-install procedure needs a
complete, platform-matched wheelhouse and local benchmark files for full tests.

## Decision margins and measured sweeps

```python
from vayu.margins import deadline_slack, decision_float, full_fleet_sweep, label
from vayu.planner import plan

frozen = plan(state)  # A validated PlanningState with estimates in cycles.
slack = deadline_slack(frozen, state.tails,
                       today=state.today, safety_buffer=state.safety_buffer)
tail = state.tails[0]
margin = decision_float(tail.tail_id, state, R=40)
attention = label({'lower': tail.lower, 'upper': tail.upper,
                   'float_min': margin['float_min'], 'deadline_slack': slack[tail.tail_id]})
all_margins = full_fleet_sweep(state, R=40)  # Prints measured sweep time.
```

Slack freezes the supplied placement and makes zero planner calls. Directional
floats are the smallest cycle magnitudes causing any fleet tail's start, bay,
spare or status to change. The result includes `float_down`, `float_up`,
`float_min`, `direction` and before/after witnesses in `what_changed` for both
directions. Equal minima report `both`; absent thresholds report `> R`.
Supply `pinned_placements` when the same reservations must remain fixed.

Spare arrival sensitivity in What-if delays one spare at a time through a
five-day window, with all other inputs fixed. Its ETA float is the smallest
delay changing any tail's start, bay, spare or status. A later transition to
Late is shown separately; a moved start can still be On time. No witnessed
change is reported as `> 5 days`. A delayed ETA that invalidates a pin requires
placement review and does not silently release that pin. These are assumed
planning probes, not scored interventions.

The generated `artifacts/greedy_summary.json` and `artifacts/float_summary.json`
retain the fictional story plan, cycle margins and day-based spare probes.
Regenerate them with `python scripts/tasks.py whatif-demo`; values are computed
from the story CSVs.

`PlannerCache` reuses identical planner inputs across float calculations and
charts. Pass an explicit cache to isolate measurements; `clear()` resets it.
Full-fleet sweeps and `analyze` print elapsed seconds, planner calls and cache
hits. Timings stay outside returned data. Covered/Fragile remains a planning
attention label, using frozen slack and decision float against half-width.

## Independent planner verification

OR-Tools is used only by a test subprocess. It has a separate NumPy requirement,
so install its pinned environment independently from the application:

```powershell
python -m venv .checker-venv
.checker-venv/Scripts/python.exe -m pip install -r requirements-checker.txt
python scripts/tasks.py test
```

The tests discover `.checker-venv` automatically. Set `VAYU_CHECKER_PYTHON` to
another compatible Python executable if needed; otherwise they use the base
interpreter. Install once, then solver checks run offline. Solver failures or
missing dependencies fail the tests explicitly.

CP-SAT independently verifies fixed schedules for resource collisions and
proves no strict Late-count improvement on selected fixtures with at most six
tails. The required greedy rule does not always minimise Late count, even for
three tails; a separate counterexample test records this limitation. These
checks retain the same planned tails and pins, rather than permitting job
removal. Details are in [docs/DECISIONS.md](docs/DECISIONS.md).

## FD001 point estimates and conformal quantile ranges

`python scripts/tasks.py train` writes `artifacts/rul_metrics.json` and
`artifacts/rul_model.joblib`. The metrics report contains test RMSE, NASA
asymmetric score, PICP (interval coverage), MPIW (mean interval width),
fit/calibration engine IDs, selected sensors and input hashes. Targets are
piecewise-linear RUL capped at 125 cycles; official test metrics use the
uncapped final RUL labels. New training never reads test labels for fitting,
feature selection or calibration. `joblib` is pinned in requirements.txt.

```python
from vayu.rul import predict_tail

estimate = predict_tail('E-01')  # Explicit alias for FD001 test engine 1.
# rul_point, lower, upper, half_width; all in flight cycles.
```

Features use the most recent 30 observed cycles: mean, population standard
deviation and least-squares slope. Short initial histories use available
observations only. Constant sensors are selected using fit engines alone.
Point and alpha=0.1/0.9 quantile boosters train on the same fit engines;
calibration engines are entirely separate. Calibration takes a maximum score
per engine to account for correlated cycles, then the finite-sample conformal
rank at nominal coverage 0.8. This can give wider ranges than pooling cycles.
The report measures actual coverage; nominal coverage concerns capped engine
trajectories under exchangeability and does not establish aircraft performance.
Crossing quantiles are sorted and ranges expanded to include the point.

The cache contains locally generated booster strings and latest test-engine
predictions. `predict_tail` uses this fixed simulated snapshot. For causal
predictions on other histories, use `load_cached_model` followed by `predict`.
Existing demo assets in data/demo and reports/model_metrics.json remain a
separate legacy benchmark replay. Its regeneration API is
`train_benchmark(root)` using data/raw; new training uses `train_fd001` and
data/CMAPSS. Neither workflow downloads data.

## Four-silo fictional fleet and quality gate

`data/fleet/` contains the requested aircraft, health, technical-record and
capacity silos, with spares/resources split into separate CSVs. Every value is
fictional; provenance, seed and simulation day are in manifest.json. Regenerate
and validate offline with `python scripts/tasks.py gen-fleet`.
For a different explicit day/seed, run
`python scripts/gen_fleet.py --today 14 --seed 49` in the installed environment.

```python
from pathlib import Path
from vayu.quality import read_fleet_pack

result = read_fleet_pack(Path('data/fleet'), today=0)
if result.planning_hold:
    print(result.reasons)  # Stop planning and repair the offending silo rows.
else:
    tails = result.accepted['tails.csv']
quarantined_rows = result.quarantine
annotated_health = result.frames['health.csv']
```

Each source record has a Good, Stale or Conflict badge. Health older than seven
days is Stale and advisory. Hard schema failures, duplicates and conflicts are
quarantined, with source, line number, reason and original values. A rejected
planning tail or invalid/missing linked health/technical record holds planning;
missing sources or usable bay/crew capacity also hold. An optional
`required_tail_ids=('T-01', 'T-02')` scopes the planning-tail set.

The pack has no RUL estimates or induction durations; those are required before
constructing a planning state. Streamlit reads `data/whatif_demo/` for the
assumed story or `data/fleet/` joined to cached predictions for Four-silo fleet.
Run `python scripts/tasks.py test` for both pack formats and the
rest of the project.

## Costed what-if comparisons

`vayu.whatif` supports `Intervention` objects for `expedite_spare`,
`add_crew_shift`, `add_bay` and `inspect_tail`. Each takes a positive
`cost_man_hours` and a target ID. Expedites take `days`; inspections take an
assumed narrowing `factor`, default 0.5. Inspection scales the range about the
unchanged point. It supplies no diagnostic measurement or airworthiness label.
The day-based planner represents a crew shift as an additional whole crew
available from tomorrow throughout the planning horizon.

```python
from vayu.sim import whatif_demo_state
from vayu.whatif import Intervention, WhatIfExplorer

state = whatif_demo_state(seed=49)
actions = (
    Intervention('expedite-S2', 'expedite_spare', 8, target='S2', days=5),
    Intervention('crew', 'add_crew_shift', 8, target='CREW-02'),
)
explorer = WhatIfExplorer(state, actions, radius=40)
ranked = explorer.rank()
pairs = explorer.pairs_for_top_k(3)
```

Ranking uses net increase in Covered tails plus reduction in Late tails,
divided by man-hours, with action IDs breaking ties. Each result includes new
label counts, Late and Unplanned counts, minimum deadline slack in cycles,
per-tail before/after placements and margins, benefit components and assumptions.
No effect actions remain visible. Pairs replan their combined inputs against
the original baseline; costs sum, while overlapping benefits are counted once.
Pass `pinned_placements` to retain fixed inductions in every scenario.

`default_interventions(state, ...)` supplies configurable resource-action costs.
Inspection is an assumption helper, excluded from scored rankings and top-k
pairs even if explicitly supplied. The UI keeps only a collapsed note labelled
**assumed, not scored**. `rank_interventions(state, candidates)` and
`pairs_for_top_k(k, state=state, candidates=candidates)` are standalone helpers;
calling the latter with only k uses the seeded assumed story.

Run `python scripts/tasks.py whatif-demo` to regenerate the separate fictional
`data/whatif_demo/` pack and computed `reports/whatif_demo.json`. The story tests
cover T-04's S2 constraint, spare expedition, assumed inspection with unchanged
placement and an added crew with no effect. Costs and ranges are hypothetical
inputs, and Covered/Fragile are planning-attention labels only. Streamlit
defaults to this assumed story and also offers the original ten-tail four-silo
pack joined to cached NASA FD001 engine estimates.

## Streamlit walkthrough

Launch with `python -m streamlit run app.py` in the installed environment,
or `python scripts/tasks.py app`. The banner reads "Fictional fleet and
simulated engine data, decision support only".

### Three-minute demo script

Before presenting, run the full test task, launch Streamlit, and open its
loopback URL. Keep the sidebar visible. Click **Reset demo** before each
rehearsal: it selects the clean assumed T-04 story, restores the default float
bound and inspection factor, clears comparisons/reason text, and returns to
Fleet board. It retains the reviewer name and all audit history; its chained
reset event releases only this story snapshot's pins and logs the replan cause.
Source CSVs, model assets, validation results and other snapshot pins remain.

| Time | Click and show | Say |
| --- | --- | --- |
| 0:00–0:25 | Reset demo, then Fleet board and the fictional-data banner. | “This offline board proposes resource placements. Every fleet and engine shown here is fictional or simulated.” |
| 0:25–0:55 | Select T-04; show **Fragile**, **spare · S2**, and **Why this plan**. | “S2 sets this induction's start. The reason code explains its availability. Fragile requests planning attention: the estimated half-width exceeds a planning margin.” |
| 0:55–1:35 | Open What-if with T-04 selected. Show the benefit-per-man-hour ranking, including the crew **No effect** row. Click **Expedite S2 by 5 days** and read the before/after diff. | “Expediting the binding spare makes T-04 Covered in this story. Adding a crew changes nothing, and we still show that candidate. Inspection is an unscored assumption in a collapsed note.” |
| 1:35–2:15 | Open Approvals, select T-04 and APPROVE. Enter user **Demo reviewer** and reason **Reviewed fictional T-04 placement and S2 availability**; click Record decision. | “A name and reason are mandatory. This records review of the current placement. The what-if diff was a comparison; it did not apply an intervention or execute maintenance.” |
| 2:15–2:35 | Show **Chain verified** and the latest approval's user, action, before/after and reason. Use Verify audit chain. | “Each event links to the previous hash. Reset preserves this review trail.” |
| 2:35–3:00 | Open Data; enable **Load corrupted pack (demo)**. Show Conflict badges, quarantine and **Planning hold**; open Fleet board to show the hold. Finish with Reset demo. | “Hard input failures stop planning and reviews. We can inspect the quarantined rows. Reset restores the clean story, keeping the audit log.” |

The board → T-04 → What-if quick expedition path remains reproducible within
three clicks. The approval step reviews the current plan; use PIN separately
to demonstrate a persistent edited reservation. Reset is available during a
corrupted-copy hold, but a broken audit chain or damaged source files must be
repaired through review rather than hidden by reset.

Select the T-04 fleet row, open What-if, then click "Expedite S2 by 5 days".
Results are computed from the shipped inputs. A second quick button compares
an extra crew shift. Comparisons preserve the current
plan. The Data tab's corrupted-pack toggle shows quarantine and a planning
hold blocking all decision actions.

Approvals requires a user name and reason for approve, reject or pin. Edited
pin resources/start are checked by the planner and stored in SQLite; the same
snapshot restores them after reruns or a fresh browser session. Reviews
execute no maintenance. The footer reads generated RMSE, NASA asymmetric
score, PICP and interval width from the local benchmark report.

Approvals shows **Chain verified** after checking the local SHA-256 chain.
Its trail includes timestamp, user, action, tail, before/after snapshots and
reason. Triggers reject edits, deletion and replacement of audit rows. A broken
chain holds planning and prevents restoring untrusted pins. Existing history
keeps its original hashes when the schema is extended.

```python
from pathlib import Path
from vayu.audit import AuditLog
from vayu.sim import whatif_demo_state

audit = AuditLog(Path('data/maintenance.db'))
scheduled = audit.replan(whatif_demo_state(seed=49), user='Demo reviewer',
                        cause='Reload validated fictional inputs', timestamp='day-0')
assert audit.verify_chain() is None  # Otherwise returns the first broken sequence.
```

`AuditLog.replan` restores stored pins by the original input hash; pass
`source_plan_id` to retain a pin scope across explicitly changed inputs.
Pass `before` to record the preceding plan. `append_event` accepts the seven
requested fields directly; before/after serialize as canonical JSON. Explicit
timestamps accept logical days or ISO timestamps supplied by the caller.
Every proposal, pin replan, newly evaluated what-if candidate and comparison
records its cause, including repeated comparisons. Cached display refreshes
and internal sensitivity calculations do not create new proposal events.

## Scenario validation

Run `python scripts/tasks.py validation` (or `make validation`) to evaluate
200 paired seeded Monte Carlo scenarios per frozen stress/sensitivity cell
offline. It uses the validated
four-silo fleet, cached FD001 estimates and signed held-out calibration
residuals. The same RUL draws, initial ages and spare delays are paired for
B0–B4, B4b and B2-K0. The current v2 design is a **post-hoc correction**:
v1 results were seen. The corrections and their reasons were recorded in
docs/DECISIONS.md before the rerun; preserved v1 evidence and its hash ledger
are in `artifacts/validation_v1/`.

B0 repairs observed failures and replans after each failure. Before comparison,
B1's assumed fixed interval is frozen as the median terminal TRAIN cycle of
fit engines only, rounded up; calibration engines and TEST labels are excluded.
B1 submits future interval deadlines within the remaining horizon to the same
planner. Each scenario uses neutral initial ages independently uniform in
[0, interval), drawn from a separate seeded stream and paired across all
policies, stresses and sensitivities. These assumed ages replace the
fictional pack counters only in validation; the original CSVs are retained.
Healthy aircraft keep flying while awaiting a future slot. The interval is
still a training-lifetime proxy, rather than an approved overhaul interval.
B2-K0 uses the same urgency planner and grounding rules as B2, with no
interventions. It provides a paired control for the effect of interventions.
B2–B4 and B4b share the preventive planner and one intervention per week. Their
frozen attention rules choose a tail among waiting tails whose deadlines are
within 14 days (including overdue tails): B2 earliest deadline; B3 largest
half-width minus slack; B4 largest half-width minus min(float, slack).
B4b ranks half-width minus float directly, treating an Unplanned tail's float
as zero. Both B4 and B4b remain reported.
Ties use deadline then tail ID. Unplanned slack has the greatest shortfall;
a float above the search bound uses that bound conservatively. The same
`vayu.whatif` action ranking then uses **the selected tail's** Covered increase
plus Late reduction per man-hour; improvement to other tails does not score.
Fleet-total changes remain descriptive outputs. Unhelpful weeks remain unused.
Inspection is assumed, not scored, and is excluded from policy actions.
All costs are assumed man-hour inputs; an unhelpful chosen tail has no fallback.

Open **Validation** for the generated means and percentile bootstrap
intervals at confidence level 0.95. The note reads **simulated; scenario-based**.
AOG starts at observed failure, preventive RUL deadline, fixed-interval due
date or induction start, and ends at completion (censored at the horizon).
It includes waiting for a spare, bay or crew and maintenance duration. Healthy
future-slot waiting is excluded. Grounded tails stop cycles and cannot newly
fail. Unplanned repairs require all three resources for an assumed multiplier
of normal duration, rounded up; wasted life
is cycles remaining at removal. Churn measures changed future placements.
The tab retains B4-B3, B3-B2, B4b-B3, B4b-B4 and B2-B2-K0 paired differences and exact ties/N.
The B2-K0 comparison uses AOG, failures, wasted life and churn only; budget
columns cannot break an outcome tie. Each policy's man-hours and unused weeks
are still separate reported outcomes. The tab
shows total man-hours and unused weeks, and offers
the numeric CSV download. Results describe the report fleet independently
of the currently selected demo or pins; the tab does not run simulations.

Outputs: `artifacts/validation.csv` (one wide row per stress/repair/horizon/policy,
plus named paired-comparison rows; all outcome means, intervals, exact
tie counts and chosen-tail difference shares), `validation_runs.csv`
(paired outcomes), `validation_weeks.csv` (weekly action/cost log),
`validation_manifest.json` (seeds, assumptions, provenance and ties), and
`calibration_residuals.csv` (signed calibration pool). Missing NASA files or
model cache fail clearly; the script never downloads or trains implicitly.
SimulationConfig exposes assumed interval, delay, float and bootstrap settings.

Stress levels were declared before comparisons in docs/DECISIONS.md and
`artifacts/validation_preregistered.json`: benign/moderate/stressed capacity,
spare lead-time and delay spread, and signed residual scales. Each level runs
assumed repair multipliers 1.5, 2 and 3 with paired identical draws across
sensitivities, at both 40- and 80-day horizons. All policies receive the same
resources and shocks within a cell. The initial fleet and spares are unchanged
for the longer horizon; no replenishment is introduced. Corrected settings
remain frozen regardless of policy ordering. The legacy filename
`validation_preregistered.json` records the frozen v2 design with explicit
post-hoc and results-seen flags; it does not claim unseen-result preregistration.

`artifacts/validation.csv` and generated `validation_comparison.md`
report every cell, including man-hours and unused weeks. Complete individual
reports live in `artifacts/validation/<level>/horizon_<days>/repair_<multiplier>/` (decimal
points use `p`). Root source-run, weekly and manifest files show stressed
with assumed 2x repair and the 40-day horizon for existing readers. The
Validation tab reads only validation.csv and offers level, repair and horizon
selectors. Old per-cell paths remain preserved v1 evidence.
`validation_diagnostics.log` prints three scenarios per stress/horizon at assumed 2x repair;
weekly CSVs show Fragile tails at the week start, the policy's chosen tail,
top-ranked action/benefit and unused reason. The separate three-scenario
`validation/original_diagnostic/` evaluates the original capacity pack under
the corrected rules. Physical changes with zero target benefit remain unused; a tie
or a lower B0 AOG is printed as generated, without forcing actions or winners.

`validation_opportunities.csv` reports competing-candidate weeks, differing
choices and applied expedition/crew/bay counts per policy and cell. Reviews
with empty candidate sets remain in the denominator. Few competing weeks
carry a descriptive "test lacks power" warning; this is not a formal power
calculation or a reason to alter the frozen stresses. Even differing choices
can lead to the same action and outcomes. The full export is generated in
`validation_phase19_execution.log`, including three weekly traces per level
and horizon. `validation_initial_ages.csv` contains the paired assumed ages
and their seed/interval, independently of sampled engine life.
`validation_b1_scenarios.csv` prints B1 AOG, disjoint grounded waits, interval,
initially overdue tails and advance inductions for every scenario and cell.
The Validation tab shows AOG and failures side by side at each assumed repair
multiplier. Lower B0 AOG can coexist with more failures because it continues
flying until failure while preventive policies ground at their deadlines and
wait for capacity; compare both outcomes. B0 counts the same waiting and
longer repair durations. Results are censored at the simulation horizon.

The corrected validation task evaluates every policy afresh. It verifies the
preserved v1 archive before writing new reports. Independent cells may run
in local worker processes; all reports are serialized in fixed order with
explicit seeds. No installation or network access occurs during validation.

`python scripts/validation.py --refresh-summary` adds the follow-up B4b-B3
comparison from complete saved v2 evidence without rerunning a policy. It
requires the original unrounded manifests to prove that B3 and B4 tied in
every scenario and outcome; the new comparison then equals the original
B4b-B4 comparison, including its exact ties and confidence intervals.
It preserves raw evidence and records source/output hashes in
`artifacts/validation_refresh_manifest.json`. If the proof is absent, it
fails clearly rather than infer exact ties from rounded raw CSV values.
