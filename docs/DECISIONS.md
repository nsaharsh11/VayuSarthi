# Build decisions

## Phase 21: offline visual presentation (2026-10-05)

The user published the existing repository and requested images and general
presentation improvements. Add an original locally stored hangar illustration,
a project wordmark, an explanatory workflow graphic, clearer tab introductions,
resource context and a visual README. The hangar scene is a generated concept
illustration, explicitly labelled fictional; it is neither a fleet photograph
nor evidence of resource counts or measured performance. Image generation is
a preparation step only. The app never calls an image service or other model.

Use native Streamlit theme settings and responsive containers, replacing the
existing CSS injection. Keep system fonts and local assets; add no dependency,
remote image, CDN, telemetry, new action type or simulation policy. Preserve
all tab/widget keys, the default T-04 story, the fictional-data banner, the
planning hold, named review requirements, Reset demo, and unscored inspection.
Resource cards read the selected PlanningState; explanatory diagrams contain
no invented result values. Validation continues to read its existing CSV.

The published history is retained. This presentation revision does not rewrite
history, modify recorded result files, rerun validation scenarios, or push.
Add offline asset/UI checks first, run the full test task and commit locally.
Record image provenance and the generation prompt alongside the assets.

## Authorized local-history privacy scrub (2026-10-05)

The user explicitly authorized rewriting unpublished local history and asked
for one clean squashed commit on main, with no push. This supersedes the earlier
publishing rule against history rewriting. The original complete history was
saved and verified as an ignored local bundle before editing tracked content;
the prior index, ignore rules and content digests were also saved locally.
Commit authorship in the new history uses a neutral project identity without
a personal name or email address. Old refs and reflogs must not retain the
superseded history; the ignored bundle is the recovery copy.

Execution and test logs can contain machine-specific Python and workspace
paths. All logs are removed from the publishable tree, including archived v1
logs, but their local files are retained. Local agent configuration, research,
databases, environments, model caches, benchmark sources and installation
archives are ignored as well. This is a privacy/storage correction after
results were seen, not a policy or simulation change. No result values are
edited and no validation scenarios are rerun for this correction.

The v1 archive ledger is updated to cover the retained published evidence.
Log digests move to a separate local-only digest section, so fresh checkouts
do not require ignored private logs to verify the published archive. The
original and revised ledger digests and unchanged result-file digests are
recorded in artifacts/privacy_scrub_manifest.json. Historical reconciliation
counts describe the checks performed before this scrub and remain untouched.
Existing manifests and CSV reports otherwise remain byte-for-byte unchanged.

Scan the candidate tree and every reachable commit, including author and
committer metadata, for absolute user/install paths, local identifiers, emails,
machine names, tool-session locations and credential patterns. Validate the
ignore rules and absence of excluded files in the index and history; inspect
binary screenshot evidence too. Ignored private local files and the backup
intentionally remain on disk. A clean publishable history does not mean those
private recovery files were erased. Run the full offline test task and verify
the archive digests before declaring the scrub complete. Do not add a remote
or push.

## Follow-up corrections and publishing checks (v1 and partial v2 results seen)

The latest request retains the frozen v2 ages, attention rules, stress settings,
action menu, costs, repair multipliers and horizons. Items 1–4 already exist in
the working tree and pass the full test task; finish their existing validation
run rather than repeat completed simulation cells or tune the observed results.
The changes below are declared before their implementation or report refresh.

- Add B4b minus B3 as a scenario-paired comparison, retaining B4b minus B4
  for continuity. The reason is that the requested comparator is B3. Use the
  same bootstrap seed, resampled scenario IDs, outcome definitions and exact
  ties/N. Derive the extra comparison from saved v2 runs; do not invent numbers
  or resimulate unchanged policies. Preserve raw runs, weekly traces, original
  simulation manifests and all v1 bytes. Record report-refresh provenance.
  Original raw CSVs use rounded decimal serialization. When the original
  manifest proves B3 and B4 identical in every scenario and every reported
  metric, B4b-B3 is exactly B4b-B4; retain that original comparison's CIs and
  exact ties instead of reconstructing them from rounded floats. A refresh
  without this proof must fail clearly and request a full-precision rerun.
- Extend repair feasibility tests to every policy, separately withholding each
  of spare, bay and crew through the horizon. The existing delayed-resource
  test covers waiting, but an explicit unavailable-resource test must prove
  that a failed tail cannot start repair without all three resources.
- Add a separate spare-ETA sensitivity, measured in days. Delay exactly one
  spare by each integer from one through five, keeping every other input and
  all valid pins fixed. Reuse the planner cache and the decision-float witness
  comparison (start, bay, spare, status) across the entire fleet. Report the
  first placement change separately from the first observed transition to
  Late: moving a start does not necessarily make it Late. Show the requested
  "becomes Late" wording only when a probe witnesses that transition; otherwise
  explain the actual change or the finite "> 5 days" bound. A delayed ETA that
  invalidates a pin is a placement conflict requiring review, not permission
  to silently move or release the pin. This diagnostic is not a scored action
  and changes neither attention labels nor simulation policies.
- Computation correction after partial v2 results: an uncompleted long-horizon
  cell repeatedly sweeps points for tails with no compatible spare available
  anywhere within the horizon. Such a tail can never consume a spare, bay or
  crew, regardless of its deadline or position in the sort. Therefore changing
  only its point cannot change any four-field placement signature. Prove this
  against exhaustive replanning in tests, then return the same finite bounded
  float without redundant probes. This is an exact shortcut, not a changed
  attention rule. Resume only incomplete cells with the frozen inputs/seeds;
  retain completed raw evidence and record the computation revision separately.
  The same proof applies when compatible spares exist but are all consumed
  by fixed pins and same-part tails preceding the focal tail even at its
  earliest deadline within +/-R. Later deadlines cannot recover a consumed
  spare. Test both this bounded proof and the boundary where a tail CAN move
  ahead of the consumers; do not shortcut that boundary.
  A direction is also provably unchanged when its endpoint retains the entire
  unpinned deadline/ID order and the focal placement's status. Only one deadline
  moves monotonically, so neither order nor status can leave and return within
  that direction. Check order and status explicitly, not just equal endpoint
  signatures. Compare the optimized floats to exhaustive integer probes on
  seeded multi-tail fixtures, including pins and resource shortages. Cache
  tests assert reuse/invalidation rather than requiring redundant calls.
  Within a single integer sweep, memoize plans and four-field witnesses by the complete unpinned
  deadline/ID order. For a repeated order, resource choices/starts are fixed;
  compare the current focal deadline to that placement's start to determine
  status. Call the planner whenever the order is new or status changes. This
  avoids repeated calls between genuine decision boundaries while retaining
  every integer delta, the same first witness, and the same four-field test.
- Before publishing, exclude local environments, caches, NASA source folders,
  model caches, credentials and disposable large generated files. Retain the
  small generated demo reports and immutable v1 evidence. Removing an already
  tracked cache from the current tree must keep the local file and must not
  rewrite history. Check tracked content and report any credential or personal
  information before attempting a push. A missing remote or unnamed destination
  branch is not authorization to invent one.

## Post-hoc design corrections for validation v2 (results were seen)

These corrections respond to the audit after v1 outcomes were reviewed.
They are not preregistered claims about unseen results. Preserve the current
validation reports, raw runs, weekly traces, manifests, calibration pool and
execution evidence under artifacts/validation_v1/ before generating v2.
Do not alter the declared stress levels, repair multipliers, resource-action
types, man-hour costs, seeds or existing B2/B3/B4 attention definitions to
obtain a preferred outcome. Evaluate all policies afresh for v2.

1. B1 initial ages must share the frozen training-derived interval's scale.
   The fictional technical counters in v1 were usually already beyond that
   interval, which confounded the interval comparison. For each paired
   scenario, draw each tail's initial age independently and uniformly in
   [0, interval) flight cycles with an explicit numpy Generator seed. Use
   the simulation seed plus 1000 for this separate age stream; draw in
   scenario-ID and tail-ID order. Reuse those ages for every policy and
   stress/repair/horizon comparison. Freeze the interval rule unchanged.
   B1 still schedules future due dates through the same planner. A failure
   already observed at initialization can ground a tail; initial interval
   ages themselves cannot make most of the fleet overdue on Day 0.

2. After selecting an intervention target, score each existing resource
   action by that target's increase in Covered plus reduction in Late,
   divided by its assumed man-hour cost. V1's fleet-total score could help
   other tails while ignoring the selected tail, masking attention-rule
   differences. Retain the existing action menu and deterministic action-ID
   tie-breaking. Exclude No effect and nonpositive target-benefit actions;
   leave the allowance unused if none helps, with no fallback target.
   Keep fleet-total changes as descriptive outputs, separate from the
   target-specific ranking used by simulation policies.

3. Retain B4's half-width minus min(float, slack) attention rule unchanged.
   Add B4b to rank candidates directly by half-width minus decision float.
   Use the same 14-day candidate window, with ties by deadline then tail ID.
   A float above the finite search radius uses that radius conservatively.
   An Unplanned tail has float zero for B4b attention, so its shortfall is
   its half-width; it does not receive an infinite-priority shortfall.
   This explicit rule lets finite float shortfalls affect attention while
   preserving the existing B4 definition for comparison. B4b receives the
   same weekly allowance and target-specific resource-action rule as B2-B4.

4. For B2 versus B2-K0, the all-outcomes exact tie count uses only AOG,
   unplanned failures, wasted life and plan churn. Budget/man-hour/unused
   columns remain reported separately, but cannot break an outcome tie.
   Bootstrap paired differences and metric-specific exact ties remain
   available; name the scope of the combined tie count explicitly.

5. Freeze an 80-day horizon sensitivity alongside the existing 40-day
   horizon before generating v2 results. Apply it to every stress level,
   repair multiplier and policy, using identical initial paired shocks and
   ages. Keep the same initial spares and capacities; do not introduce
   replenishment or change the one-original-engine-removal assumption.
   Grounded waits and maintenance remain censored at the selected horizon.
   Include horizon in every export key and report label to prevent mixing
   cells. This tests whether horizon censoring masks policy differences.

6. If pytest uses --basetemp=.tmp_pytest, ignore that disposable directory
   in Git. This avoids accidental staging of local test scratch files;
   it has no effect on policy or simulation outcomes.

Independent cells may be evaluated in separate local Python processes to
complete the doubled horizon grid efficiently. Each receives the same frozen
inputs and explicit seeds; reports are serialized by the parent in fixed cell
order. This changes computation scheduling only, with no policy or outcome
definition change and no additional dependency or network access.

Archive storage correction discovered during staging: Git's Windows line-ending
conversion can change archived log bytes on checkout and invalidate the v1 hash
ledger. Mark artifacts/validation_v1/** as raw, non-text Git content so every
preserved byte survives checkout. This is an evidence-storage correction after
results were seen; it changes neither the simulation nor the frozen rules.

Write phase-specific tests before implementation, regenerate all stress,
repair and horizon cells, retain ties and adverse outcomes as generated,
run the full test task and commit the completed correction phase. README
and UI values must come from generated reports, never copied result numbers.

## Phase 18: validation follow-up, with no tuning toward B4

Keep the declared fleet, residual pool, seeds, capacity/ETA stress levels,
repair multipliers, attention rules, budget, costs and benefit definition.
Export one wide row per stress/repair/policy. Named comparison rows B4-B3,
B3-B2 and B2-B2-K0 use paired scenario differences; every outcome has its
own mean/CI and exact ties/N, plus an all-outcomes tie count. B2-K0 runs the
same urgency planner and grounding rule with no interventions or budget.
An unused-weeks count is zero when there is no budget to leave unused.

B1 previously admitted a tail only once its interval was due. Correct this
by submitting future interval deadlines within the remaining horizon to the
same earliest-feasible planner, alongside observed failures. Do not induct
tails whose interval due date is outside the horizon solely for being healthy.
Interval deadlines use observed technical age and rate, with no model safety
buffer. Keep the fit-training median interval unchanged. Healthy waiting
tails fly until induction, observed failure, or their fixed-interval due date;
already-overdue tails cannot benefit retroactively from advance scheduling.
Per-scenario B1 reports include interval, waits, AOG, failures and the number
of initially overdue tails and inductions started before their due date.

Diagnostics count scheduled weekly reviews, including empty candidate sets;
choices differing from None count as different choices. Report each policy's
share with at least two candidates, pairwise and any-three differing-choice
shares, and applied resource-action counts. A descriptive low-opportunity
warning uses a competing-candidate share below one quarter; it is labelled
"test lacks power" and is not a formal power calculation. No threshold affects
policy choice, scoring or stress settings. Even plentiful candidates need
different effective actions for outcome differences; ties do not establish
policy equivalence.

Lower B0 AOG can coexist with more failures. Preventive policies ground a tail
at its believed deadline if it has no slot, and that aircraft may remain
grounded awaiting a spare for the rest of the censored horizon. B0 keeps it
flying until an observed failure, so its grounded waiting can begin later.
All policies count the same grounded waits and maintenance; B0 failures wait
for all resources and incur the same longer assumed repair. Compare AOG and
failures side by side at each multiplier, rather than interpreting AOG alone
as policy superiority. Limited spares, initially overdue technical ages,
one removal per original engine and serviceable replacements further limit
what these scenarios establish. Result numbers come from generated reports.

For efficient regeneration, unchanged committed B0/B2/B3/B4 source runs may
be reused only after exact state, shock, config and input-provenance hash
checks. B1 and B2-K0 are always evaluated under the corrected code. Reject
invalid or incomplete archives; record which policies were reused. Tests
compare resumed and fresh evaluation. This reuses simulated evidence and
never substitutes manually entered results.

## Phase 17: finish the inherited offline UI polish

Preserve the cards, native coloured attention/quality badges, range bars and
deadline-marked timeline already present in the inherited working tree.
Charts display the same local input and plan values as the board; tests check
range endpoints, point estimates, induction duration and every deadline.
Wrap the range axis title so it stays readable in a narrow side panel.
Approval errors explicitly name missing fields before recording anything.
Validation remains a read-only CSV view; no UI operation recomputes scenario
results or reads truth. Existing tests prohibit outbound connections.
Use a named prototype reviewer and a fictional reason for the local browser
rehearsal; those append-only test review events remain identifiable in the log.
Reset preserves that history and restores the original unpinned demo.

## Phase 16b: frozen attention rules (written before the rerun; do not tune)

Diagnosis of the prior export found choices differing between B2 and B3/B4,
but B3/B4 choices tied in the sampled diagnostic weeks. The old rule placed
deadline bands ahead of margins, limiting when float could alter a choice.
Unused weeks arose when the selected tail had no positive-benefit action
under the agreed Covered-plus-Late score. Generated traces and counts,
rather than copied result numbers, are retained in artifacts/validation/.
The attention rules are therefore changed, once, as follows, and frozen:

- Candidates: waiting tails with deadline within 14 days of the review day
  (overdue included). No candidate: week unused, reason "No tail with deadline
  within 14 days". K=1 and no fallback tail if the chosen tail has no
  positive-benefit action.
- B2 picks the earliest deadline. B3 picks the largest shortfall
  half-width - slack. B4 picks the largest shortfall of half-width -
  min(float, slack). Unplanned slack is an infinite shortfall; a float above R
  counts as R. Ties break by earlier deadline, then tail ID.
- B4 is not expected to win. All ties and any lack of difference are reported.
- Inspection is removed from the scored, ranked intervention menu in the
  simulation and the UI. It remains only as a collapsed note labelled
  "assumed, not scored". The library whatif code retains it as an unscored
  assumption helper; neither rank() nor top-k pairs include it, even when a
  caller explicitly supplies inspection. Default menus contain resource
  actions only. Legacy explicit assumption evaluation remains available.
- artifacts/validation.csv is the single generated source for the Validation
  tab: all stress/repair cells, B4-B3 paired differences with CIs and exact tie
  counts, and tail-difference shares.

## Phase 16 takeover: complete exports without repeating completed runs

The last committed phase was Phase 15. The attention rules above, stress
settings and grounding accounting were already present in the inherited
working tree. Preserve those choices and the completed paired scenario cells.
An end-to-end export test exposed a missing POLICY_NAMES import after the
aggregate CSV was written. Repair that final report path and render its
comparison from existing source runs. Reconcile all aggregate mean/CI rows
against the stored runs, check paired shock hashes across repair sensitivities,
and verify that disjoint waiting plus maintenance components equal AOG.

The diagnostic print includes both top-ranked and applied action IDs, so an
unused or excluded action cannot be mistaken for an executed intervention.
artifacts/validation_diagnostics.log prints the first three scenarios per
stress level at the default assumed repair multiplier, plus full-run choice
counts. No result numbers are copied into this document or the README.
The aggregate CSV retains every paired difference and tie, even when choices
differ but measured outcomes do not. No input, score or stress setting is
changed in response to that outcome.

## Phase 16: simulator diagnosis and predeclared stress comparison

Freeze these illustrative levels before policy comparison; do not revise them
based on which policy wins. Benign: 3 bays, 2 crews, nominal spare ETA times 1,
uniform additional delay 0..2 days, signed calibration residual times 0.5.
Moderate: 2 bays, 1 crew, ETA times 2, delay 0..7, residual times 1.
Stressed: 1 bay, 1 crew, ETA times 5, delay 0..21, residual times 2.
Use the same original fleet points/ranges, rates, spares and technical ages.
ETA multiplication applies to believed lead times relative to today; random
additional delays remain hidden. Resource counts describe alternative fictional
capacity packs, not measurements. Freeze seed 26249, 200 draws per level,
bootstrap seed 26250 and 2000 resamples. Publish all levels and all ties.

The original initial pack has Fragile and Unplanned tails,
so lack of Fragile labels is not the cause. All original initial candidate
benefits are zero under the previously agreed Covered-plus-Late benefit;
physical changes with zero benefit must still leave the week's budget unused.
No spare procurement action or benefit override is introduced.

The user explicitly selected grounding-based AOG: start at observed failure,
the preventive floor-RUL deadline, or B1's fixed-interval due event; finish at
completion, counting resource waits and maintenance. A healthy future-slot
reservation does not ground a tail. Grounding is persistent and stops cycles
and new failures until completion. Preventive maintenance started earlier
grounds the tail at induction start. AOG is censored at the simulation horizon,
and decomposition assigns waiting to spare, bay, crew, then permitted slot in
that order, avoiding double counting simultaneous unavailable resources.
Unplanned repairs require the same three resources and ceil(normal duration
times an assumed multiplier). User-requested sensitivities are 1.5, 2 and 3,
using identical shocks. Failures discovered on a previously proposed start day
also extend that job; later planners see the longer resource reservation.

The user additionally requested a training-derived B1 interval. Freeze
ceil(median terminal TRAIN cycle among model fit engines) before comparisons;
this lifetime proxy is an assumed interval, not an approved maintenance rule.
Calibration and TEST targets are excluded. Validation writes the predeclared
levels, resolved training-derived interval and input hashes before any runs.
All nine level/multiplier cells use 200 draws with the same base seeds and
complete outputs. Root validation.csv contains every mean/CI, paired
difference and chosen-tail share; root source-run/weekly/manifest files retain
the stressed assumed 2x cell for compatibility. A three-scenario
diagnostic on the unchanged input pack also remains separate and prints the
full weekly trace. No tuning or forced action is allowed after comparison.

## Phase 15: repeatable demonstration and offline handover

Reset demo means restoring the clean shipped assumed T-04 story, default
R=40, inspection factor=0.5 and Fleet board, clearing comparisons, reason text
and transient pin controls. Keep the reviewer identity. Existing persistent
pins would otherwise prevent the promised story on a fresh session, so the
explicit reset releases only pins belonging to the original story input hash.
It appends DEMO_RESET with before/after pin snapshots and then REPLAN with
the cause "User requested Reset demo". pins_for folds resets and later pins
in sequence order: later PIN events still persist normally. Other snapshots,
CSV files, model caches, generated metrics and all historical rows are kept.
Reset does not undo approval/rejection records or claim to repair source
files; a broken chain blocks both the reset and further planning. System reset
events use actor prototype, consistent with existing automatic load events;
placement review still requires a human name and reason.

The README timed walkthrough approves the original current placement, since
what-if comparisons do not apply actions. It explicitly identifies assumed
inspection and unchanged crew candidates. Offline handover downloads binary
wheels on a connected computer matching target OS, architecture and Python
minor version; installation uses no-index and local wheel directories. The
OR-Tools checker remains isolated with its own wheelhouse/environment because
its NumPy requirement differs. Full tests need the manually supplied FD001
files even though the cached demo does not retrain. Documentation corrects
stale tab/simulation descriptions and presents limitations without invented
performance values.

The full test task exposed a Windows locale decoding error when its claims
check read UTF-8 Markdown containing typographic quotation marks as cp1252.
That check now explicitly reads UTF-8; the claim restrictions remain unchanged.

## Phase 14: paired Monte Carlo and Validation tab

The user resolved K as one intervention per simulated week for B2/B3/B4;
B0/B1 receive no interventions. Selection has two separate steps: choose one
tail with the policy attention rule, then apply the common what-if action
ranking. Do not search another tail if its top helpful action is absent.
The shared menu includes that tail's inspection, its assigned spare expedite
(all compatible unused spares when Unplanned) and shared bay/crew additions.
WhatIfExplorer.rank supplies the selected benefit/man-hour definition.
No effect and nonpositive-benefit rows are excluded. If none remain, the
week is unused; no forced action, budget transfer or policy-specific cost.
Weekly CSV rows record the selected tail, unused reason, action IDs, count,
benefit and man-hours. Total man-hours and unused weeks are summary outcomes.

Defaults are explicit SimulationConfig inputs: seed 26249, 200 scenarios,
integral independent spare delays uniformly from zero through seven days,
fixed overhaul interval 1000 flight cycles, float bound 40 cycles, bootstrap
seed 26250 and 2000 resamples. The overhaul interval is an assumed baseline
setting, not a NASA model result or an aircraft maintenance requirement.
All policies start with the same validated data/fleet pack and resources;
technical ages come from its fictional tech_records.csv. The existing assumed
story is retained for tests/UI and is not substituted for the validation fleet.

Signed errors are capped target minus point prediction on calibration TRAIN
engines, with at least thirty observations. CQR scores are nonnegative
nonconformity measures and are not substituted for signed residuals. No fit
engine or official TEST target contributes to the pool. Draw an engine
uniformly, then a row within that engine; this avoids weighting longer engines
more heavily. Empirical errors are fixed per original engine for the run.
All scenario RUL/errors and spare delays are drawn before evaluating any policy,
and reused by every policy. Nonpositive point+error draws are preserved and
count as initially observed failures; no silent resampling. Calibration pool,
model, fleet and scenario hashes are stored with the generated report.

B0 submits only observed failed tails. B1 submits tails reaching the assumed
fixed cycle interval, plus observed failures for repair; its ordering uses
observed interval overrun rather than predicted life. B2/B3/B4 submit all
remaining original engines to the exact same preventive planner. B2 chooses
the earliest believed deadline. B3/B4 group urgency into overdue, due within
seven days and later. B3 uses lowest frozen slack within a band; B4 uses the
minimum of float and slack, then slack. Deadline/tail ID break remaining ties.
Bounded > R floats use R conservatively, never an unbounded value. Separate
select_tail/choose_intervention functions receive believed PlanningState only.

The simulator translates each current snapshot into relative days (today=0),
then translates plan dates back to execution days. This preserves the exact
deadline formula while believed remaining life decays with observed flight
cycles. Only actual arrivals and failures are observable. A missed spare ETA
updates the forecast to tomorrow until arrival; policies never see its hidden
future date. An expedite moves forecast and hidden ETA by the same days;
inspection narrows belief only and cannot change sampled life. Added bay/crew
capacity persists to the horizon, matching the existing what-if abstraction.
Daily order observes failures/completions, attempts prior proposed starts,
reviews interventions at week starts, replans waiting tails, then flies.
Committed active inductions retain their bay/crew until completion and consume
one spare. Replacement engines are assumed serviceable to the horizon.

The new AOG outcome means all aircraft-days unserviceable, including preventive
maintenance and failed waiting/repair. It differs from the historical fixed-plan
simulate() metric that separates PLANNED_MAINT; that API remains unchanged.
Wasted life sums positive remaining cycles at actual removal. Failure counts
are incident failures observed inside the horizon, including initially failed
draws. Plan churn counts changed future start/bay/crew/spare, excluding first
assignment and normal completion; there is no churn just from a status label.
Partial final weeks count as review weeks; B0/B1 unused_weeks is zero because
they have no allowance. Simulation replans carry causes in their returned
evaluation trace and do not write operational SQLite proposals or use pins
from the interactive demo.

Bootstrap intervals resample scenario IDs, using the same index matrix for
every metric/policy. These are marginal percentile intervals at confidence
level 0.95, not a claim of statistical superiority. B3/B4 output includes the
paired mean difference and exact scenario ties for each metric, without ranking
winners or adjusting inputs to create a gain. The generated four-silo run
reported no helpful intervention for selected tails and tied B2/B3/B4 outcomes;
the shipped artifacts preserve that finding. A separate hand-built attention
test selects different tails and the assumed story incurs intervention cost,
so equality in this report is not a stubbed policy or disabled action path.

Streamlit reads generated tables only; it never runs Monte Carlo on tab load.
The Validation tab identifies its report fleet, independent of the selected
demo/pins, and shows the exact "simulated; scenario-based" note. It includes
the full numeric CSV download, all means/intervals, tie notes, per-scenario weekly
cost log and scenario assumptions. Missing or malformed reports give a clear
offline regeneration command. The Streamlit skill's native lazy tabs, bounded
cache and data-display references were used. No dependency/network call added.
Tests were written before implementation and failed on absent simulation APIs
and Validation tab; focused checks then passed before generating the report.

The full python scripts/tasks.py test task passed. The complete default
validation command was repeated; summary and per-scenario metric CSV hashes
were byte-identical. Browser checks confirmed the scenario note, mean/interval
table, explicit ties and expanded weekly log; browser error logs were empty.
reports/ui_validation.jpg records the rendered report. The loopback app remains
available on port 8502; physical disconnected rehearsal remains a human step.

## Phase 13: audit fields, integrity and explicit replan causes

The requested timestamp/user/action/tail/before/after/reason columns are added
to the existing audit_log table without updating any historical row or hash.
Before/after are canonical JSON; a null tail means a whole-fleet event. New
version-2 hashes cover every event column, the original payload/aliases,
deduplication key and chain version, prefixed by the preceding row hash.
Historical version-1 rows retain their original hash algorithm; requested
fields are projected for display, with missing causes described as unrecorded.
The old event_key was not covered by the historical hash algorithm; migration
does not retroactively invent that protection. SQL triggers reject updates,
deletes and replacement inserts. Tests explicitly remove a trigger to simulate
stored-row tampering, which verify_chain reports by the first broken sequence.

Timestamps remain explicit logical planning days for deterministic replay.
Callers can supply ISO timestamps through the same API. User and cause/reason
are mandatory on the new event and audited replan APIs. New proposals and
their replan event share a transaction; pin review and its resulting replan
also share a transaction. The named review records the actual previous
placement and its replacement. Existing approvals APIs remain compatible.

AuditLog.replan restores pins from verified SQLite history, then calls the
pure planner and records its cause. Pins default to the original unpinned
input hash; an explicit source_plan_id keeps the same scope across changed
planning inputs. The UI uses that scope for reruns and hypothetical candidates,
and its state does not silently release pins. A broken chain holds planning
before further plan writes or use of stored pins.

"Every replan" refers to a requested fleet proposal or hypothetical scenario:
initial load, changed fleet/pins, each newly evaluated ranked candidate, every
explicit comparison click (including repeated No effect comparisons), and
each pin submission. Cached display refreshes reuse those results and add no
events. The many +/- sensitivity probes are numerical calculations, not new
proposals; the pure planner/cache does not write SQLite. What-if audits store
all per-tail before/after placements and margins, while baseline/pin replans
store full plan snapshots. The Streamlit skill's native Session State and
controls are retained; Approvals displays "Chain verified" automatically and
offers an explicit recheck button. No dependency or network call is added.

Tests were added first and failed on missing APIs/fields; the replacement-insert
test exposed SQLite REPLACE bypassing ordinary delete triggers, so a separate
insert trigger now rejects existing sequence/key replacement. Tests also check
legacy migration without re-signing, fixed-timestamp identical rows, concurrent
transactional appends, invalid-call rollback, pin restoration, tampering every
new column and a UI hold preserving corrupted history.

The full python scripts/tasks.py test task passed all collected tests. The
restarted loopback app showed "Chain verified" in Approvals and its explicit
recheck preserved that result. The existing local database verified across
both chain versions. reports/ui_audit.jpg records the rendered review trail.

## Phase 12: four-tab offline Streamlit UI

The new app replaces workspace radio navigation with the four requested tabs.
Fleet board opens on the seeded assumed T-04 story. Its four-silo view describes
the same six tails, rates, spares and resource counts; health update days and
technical counters are fictional annotations. Story RUL, durations and part
compatibility remain assumed Phase 11 inputs. The original data/fleet pack is
selectable with its ten tails, three spares, two bays and one crew. Accepted
rates/engine IDs join cached FD001 predictions. Three-day inductions and zero
buffer are explicit assumed UI inputs absent from those silo CSVs.

Both scenarios pass the four-silo quality gate before planning. Corruption
changes copies in memory, never CSVs: the focal rate fails bounds and a
technical record conflicts with the registry. The hold persists across lazy
tabs and hides planning, comparison and review actions. Missing estimates or
source errors also hold. Native coloured badges retain readable text. Fleet
row selection opens a panel using actual reason codes. The UI reads no
evaluation-value file and uses only planning-attention terminology.

What-if uses Phase 11 ranking for all inventory/capacity actions plus the
selected tail's inspection, keeping No effect rows and assumed costs/factors.
Quick actions make the three-click story: select T-04, open What-if, expedite
S2. T-04 is preselected too. A compact computed label/start comparison and
whole-fleet diff show effects without moving the original placements or pins.

Approvals reviews individual placements. APPROVE/REJECT are audited human
annotations. PIN edits start/bay/crew/spare, validates through the planner
first and restores its reservation from SQLite for the original unpinned
input hash. A different snapshot has a different pin scope. Approve/reject
does not release a pin. Name and reason are mandatory for all actions,
including the retained whole-plan API. Plan persistence and review share one
transaction, so invalid reviews leave no partial plan event. Footer metrics
read artifacts/rul_metrics.json; the assumed story is distinguished from
measured benchmark results.

The developing-with-streamlit skill and installed version's local references
were used. Native light theme, controls and locally served Plotly avoid
external fonts, CSS and new dependencies. Bounded caches include source bytes
and all planning/margin inputs; inactive tabs skip expensive work. Corruption
and reviewer fields persist across tab switches. AppTest cannot click canvas
rows or fully model tab state; tests use documented Session State and table
accessible names, with row selection and quick actions checked in the browser.
Tests were updated first and failed against the old UI/APIs. The full
python scripts/tasks.py test task passed. The app started on loopback port
8502; browser verification confirmed coloured labels, changed detail panels,
quarantine and the computed spare comparison. reports/ui_story.jpg records
that generated comparison view. The tests also cover inspection without
moving placements, the No effect crew comparison, missing review fields,
invalid pins, restored pins and atomic rejection of an unknown review source.

## Phase 11: costed interventions and assumed fictional story

The user explicitly selected benefit = (Covered_after - Covered_before +
Late_before - Late_after) / total_man_hours. Coverage gain and lateness
reduction receive equal count weight. Components remain visible; zero and
negative scores stay in the ranking. Equal scores sort by intervention ID.
No effect means all reported per-tail placements, deadlines, reasons and
margin values are unchanged. A narrowed range with no label gain is still
an effect, with zero benefit under the chosen count definition.

Intervention costs must be finite and positive. Default costs are configurable
illustrative inputs, never measured effort. Expedite days are nonnegative
integers; availability is floored at day zero. Added bay/crew IDs must be
unused in their resource collection. The Master Brief planner has whole-day
resources and no hourly shift calendar, so an added crew shift means one
additional whole crew from tomorrow for the planning horizon. This assumption
is included in each crew comparison. Adding a bay uses the same start day.

Inspection is explicitly assumed, not an observation, trained-model prediction
or recalibration. Its configurable factor lies in (0,1], default 0.5; each
endpoint's distance from the unchanged point is scaled, preserving asymmetry.
The resulting half-width scales by that factor. It does not change the point,
utilisation, duration, spares or reusable resources. Every scenario still runs
the planner and margins; pins and the full bounded sweep settings are retained.
Undefined Unplanned slack is excluded from the minimum; all-Unplanned returns
None, with a separate Unplanned count to prevent silently omitting these tails.

WhatIfExplorer shares the deterministic planner cache across baseline, singles
and pairs. Each pair is applied to the original inputs and jointly replanned;
costs sum but single benefits never sum. This tests both overlapping benefits
and complementary capacity additions. pairs_for_top_k(k) also has a standalone
default using the seeded story, without hidden last-ranking global state.

The new data/whatif_demo pack is separate from the four-silo pack and existing
NASA replay demo. It contains explicitly assumed fictional planning inputs
chosen to demonstrate the requested T-04 story; no output labels or performance
values are hardcoded. scripts/whatif_demo.py regenerates its CSVs, quality-checks
the written precision and computes reports/whatif_demo.json. Timings print
outside the deterministic JSON. Existing compare/apply_change interfaces and
the Streamlit demo are preserved; this phase provides the new Python APIs and
generated report without changing the UI. No dependency is added.

Tests were written before implementation and initially failed on the absent
new APIs and report script. Verification covers the story, both benefit
components, asymmetric inspection, positive parameter validation, immutable
inputs, zero-effect actions, Unplanned slack, combined capacity with a fixed
placement, overlapping pair gains and byte-identical pack/report generation.
The full python scripts/tasks.py test task passed, including the existing
model, planner, CP-SAT, audit, quality, Streamlit and offline checks. The demo
script generated the shipped report from the quality-checked fictional CSVs.

## Phase 10: directional decision float and frozen deadline slack

The latest margin request extends the existing typed UI helpers with direct
dictionary interfaces. decision_float(tail_id, PlanningState_or_tails, R=...)
returns exactly float_down, float_up, float_min, direction and what_changed.
Separate tail inputs require spares, bays, crews and config; normalisation is
shared with the planner rather than implemented with an extra planning call.
Existing decision_float(state,tail_id,radius) still returns DecisionFloat for
the demo, now with both directional thresholds/witnesses retained.

Floats are positive cycle magnitudes, not signed deltas. Down/up each search
successive integer magnitudes until their first witness or the explicit bound.
No assumption of monotonicity is made. Once a direction's first witness is
found, greater magnitudes cannot reduce its minimum and need not be recomputed;
the other direction continues independently. The chart sweep still enumerates
every delta including zero. Only the focal point is overridden, including
mathematical negative values; interval estimates, other tails and pins remain
fixed. Compare exactly every tail's start, bay, spare and status. Changes to
deadline, crew, binding or reason alone are excluded. Each directional witness
reports sorted affected tails, changed fields and before/after values.

Resolved return conventions: absent directional/minimum thresholds are None
in typed results and > R strings in dictionaries. A tie for minimum direction
is both; the legacy single witness chooses down first. With no witness,
direction is None and directional change lists are empty. R=0 is valid and
reports > 0 without perturbation probes. No unbounded values are introduced.

deadline_slack(plan,tails,today=...,safety_buffer=...) only reads the supplied
placements and applies point-buffer-rate*(start-today), returning a sorted
per-tail map. Pass the original planning settings explicitly; the standalone
record form defaults to day zero and zero buffer, since Plan does not contain
config. The legacy (state,tail,placement) scalar form uses the state's settings.
Matching IDs and explicit start_day are required. Unplanned slack is None.
No planner/cache lookup or scheduling mutation occurs inside either slack form.
The worked example was tested while the planner was patched to fail if called.

label(tail_mapping) accepts the range (or half_width/h), float_min and frozen
deadline_slack/slack. Typed tails accept a DecisionFloat and slack separately.
Covered requires both margins >= half-width, including equality. For > R,
coverage is established conservatively only when R >= half-width and slack
covers it; a smaller bound remains Fragile. Undefined placement slack remains
Fragile. These are planning-attention labels only.

PlannerCache is a bounded in-memory LRU storing immutable Plan objects. Keys
include all sorted planning inputs, exact point overrides, fixed pins and the
planner callable, preserving numeric JSON types and distinguishing changed
resources, rates, days, horizon and buffer. It never reuses one tail's probe
for another. All full-fleet calculations share one baseline; zero-delta chart
rows reuse it. Cache counters and measured perf_counter timing are printed
outside returned results, preserving deterministic serialized outputs.
DEFAULT_CACHE supports existing callers; an explicit cache permits independent
measurements and clear/reset. No dependency is added.

Tests were added before implementation and initially failed on absent direct
APIs/cache/timing. Targeted tests then passed for exact frozen slack, a first
downward change at six cycles, upward ordering effects on other tails, bounds,
half-width equality, cache reuse/changed inputs/pins and measured clock output.
An actual six-tail demo script ran cold and warm R=40 sweeps, printed measured
times/planner call counts and asserted byte-identical results. Performance is
scenario-specific; no times are embedded in code or documentation. The full
python scripts/tasks.py test task passed, including the existing model,
planner, CP-SAT, audit, quality, Streamlit and offline dependency checks.

## Phase 9: deterministic planner records and pinned reservations

The latest user request retains the exact Master Brief deadline-first greedy
planner and adds a dictionary adapter, plain-language reasons, pins and a
test-only CP-SAT checker. plan(state, point_overrides, pinned_placements) remains
the typed API. plan_fleet(tails, spares, bays, crews, config, pinned_placements)
returns the requested per-tail dictionaries, with no extra output fields.
Tail mappings accept tail_id or tail, require rul_point/rate, and use the
configured duration unless given individually. PlannerConfig contains today,
horizon, safety_buffer and the default duration. Unknown mapping fields fail.

Tie-breaking is unchanged: tail (deadline, ID); resource candidate (start,
spare available day, spare ID, bay ID, crew ID); binding ties spare, bay, crew.
Tomorrow-only binding is None, explained as the earliest permitted induction
day. Unplanned means no unused compatible spare within the inclusive horizon.
Scheduled start may be later than the horizon when reusable capacity delays it.
The existing point-perturbation API and input hash remain unchanged without pins.
Pinned records are included in canonical hashes, sorted independently of input
order. Placements are returned in deadline/ID order even though pins reserve
capacity first. All work happens on local copies of input resources.

Resolved pin ambiguity: pins form a reserved prefix. A spare and its tail are
removed from automatic allocation. Bays/crews are reusable after the last
pinned end day; gaps before future pins are not backfilled, preserving the
Master Brief's single free-day/resource formula. Pins may share resources only
in nonoverlapping half-open induction intervals. Unknown IDs, duplicated tails,
reused/incompatible spares, pre-tomorrow/pre-availability starts and overlaps
fail before any schedule is returned. Deadline/status are recomputed from the
current point; pinning fixes placement, not the planning estimate. A manual pin
has no spare/bay/crew binding resource; its reason states the honoured pin.

The requested universal strict-fewer-Late optimality check conflicts with the
mandatory greedy rule. This was surfaced to the user while implementation
continued under the explicitly requested Master Brief rule. A test-only CP-SAT
counterexample proves the incompatibility: the first deadline's long induction
delays shorter later-deadline jobs, while a different order can reduce Late
count. No optimiser was substituted into production. CP-SAT proves no strictly
better schedule on specified one-to-six-tail fixtures, checks seeded varied
resource cases for feasibility, and deliberately exposes the counterexample.
Alternative checks keep the same planned tail set and pins, preventing the
solver from reducing lateness by dropping jobs. Its start bound includes all
releases/fixed starts plus the total induction duration. Unknown/time-limit
statuses never count as proofs of infeasibility.

OR-Tools is authorised explicitly by the new request for tests only. Its
installed version requires NumPy >=2, while the verified application lock uses
NumPy 1.26.4. The checker runs in a separate Python subprocess with no runtime
application imports. requirements-checker.txt pins an independent compatible
environment; the tests select VAYU_CHECKER_PYTHON, then .checker-venv, then the
base interpreter. This workstation's existing base OR-Tools installation was
used; application dependencies were not changed. Fresh setups must install the
checker environment separately before running these mandatory tests.

Pin/record tests were written first and failed on missing imports. Targeted
hand-calculation, pin validation, order invariance and CP-SAT tests then passed.
All solver calls are offline, single-worker and seeded; production has no
solver dependency or ground-truth reads. The full python scripts/tasks.py test
task passed, including all planner, margin, audit, model, quality and existing
Streamlit/offline checks. The CP-SAT infeasibility results apply to the selected
fixtures; the tested counterexample prevents any universal optimality claim.

## Phase 8: engine-separated conformal quantile regression

The user's new RUL request supersedes residual-percentile calibration for new
training. Point, lower-alpha=0.1 and upper-alpha=0.9 LightGBM models train on
identical fit engines only, with the explicit numpy seed controlling the engine
permutation and booster seed. Training is single-threaded and deterministic.
The default fit/calibration split uses the existing fraction of 0.2. Sensors
are selected from fit-engine population variance only. The new training entry
point uses exactly rolling mean/std/slope at window 30; the old feature helper
still exposes last values and other windows for legacy compatibility, but new
boosters receive only the requested rolling statistics. Initial histories use
available observations (min_periods=1), population std (ddof=0) and cycle-index
OLS slopes; a single observation has zero std/slope.

Resolved CQR ambiguity: pooling calibration cycles treats correlated rows as
independent. Instead each calibration engine contributes one maximum capped-
trajectory nonconformity score max(q_low-y, y-q_high). The finite-sample rank is
ceil((n_engines+1)*0.8). This is conservative for final-observation coverage and
can yield wider intervals. Negative corrections are clamped to zero; quantile
crossings are sorted. Nonnegative support and inclusion of the point only
expand the resulting interval. At least four calibration engines are needed
for a finite nominal-coverage-0.8 conformal rank; smaller sets fail clearly.
The old tiny unit fixture was enlarged to satisfy this statistical requirement.

The capped target is used for both fitting and calibration. Official TEST
metrics use uncapped RUL at the last observed cycle per test engine, as in the
previous NASA evaluation. The report explicitly distinguishes this evaluation
from the capped-trajectory nominal calibration scope. NASA score sums
exp(-error/13)-1 for early predictions and exp(error/10)-1 for late predictions,
where error=prediction-official_RUL. Coverage is inclusive and width upper-lower.
TEST engine numbers reuse the TRAIN namespace in NASA files but are distinct
engines/datasets; no test observations or labels enter training/calibration.

User-supplied files already existed in data/raw. They were copied byte-for-byte
to the requested data/CMAPSS path locally, without downloads; both raw locations
are excluded from Git. The new train task fails with printed manual NASA
download/extraction instructions when any required file is missing. It writes
artifacts/rul_metrics.json and rul_model.joblib. Joblib was already pinned as a
resolved dependency; it is now also declared directly in pyproject.toml.
Cache payloads contain booster strings and deterministic scalar structures,
without timestamps, paths, raw targets or unstable native booster pickle state.

predict_tail returns the latest cached FD001 test-unit snapshot. Integer IDs,
numeric strings and the fictional E-NN aliases resolve explicitly to test unit
NN; this is simulated benchmark mapping, not an actual tail telemetry feed.
Unknown IDs fail. Existing demo JSON and OOF artifacts remain available through
legacy loading/regeneration APIs; new fits use CQR. Existing reports are not
silently relabelled as conformal results.

Tests were added before implementation and initially failed on missing CQR
imports. Targeted checks passed against real FD001, including independent
byte-identical metric/cache regeneration, held-out-label isolation across all
three boosters, engine separation, quantile objectives, finite conformal ranks
and missing-data instructions. The full training task produced the new report
and cache; all reported benchmark values come from that generated file. After
adding exact rolling-window and restored-cache/metric recalculation checks,
python scripts/tasks.py test passed the entire suite, including existing
Streamlit flows, planner firewall and pinned dependency checks.

## Phase 7: four-silo fleet pack and quality gate

The latest request adds data/fleet independently of the earlier data/demo
benchmark replay. Four silos use five CSVs: aircraft registry, health,
technical records, and capacity split into spares/resources. Pydantic v2
already exists in the pinned dependencies; no dependency is added.

All pack values are fictional. The generator uses an explicit numpy seed and
today, fixed row/column order, LF CSV and canonical JSON manifest. The manifest
labels provenance without adding columns outside the requested CSV schemas.
The generated pack contains no RUL estimates or evaluation truth; it is an
ingestion fixture, not a replacement for the model-derived demo planning state.

Resolved validation ambiguities: identifiers must be nonempty; tail IDs and
engine assignments are unique. All duplicates are rejected, with no selected
winner. Days, cycles and snag counts are nonnegative integers; resource counts
are nonnegative integers. Resource names are bay/crew; shift_hours is greater
than zero and at most 24. Shift hours are metadata and do not change the
planner's duration-in-days rule. No unspecified upper bounds on cycles, snags
or availability days are invented. Unknown CSV columns are hard failures,
including evaluation-only fields.

Health updates after today are hard failures. Age exactly seven is Good; older
is Stale, which is advisory and does not itself quarantine or hold planning.
Tail badges inherit linked health staleness. Orphan health engines and orphan
technical tails are conflicts. A tail without valid linked health or technical
records is also quarantined; this prevents partial-silo acceptance from silently
making an incomplete tail eligible. By default every ID mentioned in either
tails or technical records is required for planning. An explicit required-tail
set permits scoped planning. A missing required tail, missing/malformed source,
missing required columns, absent fleet or zero valid bay/crew capacity holds
planning. Unrelated rejected spare records are quarantined; they alone do not
imply a tail hold. Quarantine retains original row data and CSV line numbers;
all input frames are copied before annotation.

Tests were written first and initially failed on missing gate imports. After
implementation, python scripts/tasks.py gen-fleet test generated the committed
pack and passed the full suite, including physical corrupted-copy, per-schema
bounds/duplicates/columns, staleness boundary, linked-record hold, scoped-tail
hold, malformed CSV, nullable cells and byte-identical regeneration checks.

## Active Vayu Sarthi revision (2026-10-04)

The latest user request replaces the previous large FastAPI/static-UI product
with the vayu/ modules and Streamlit prototype. The historical specification and
Phase 1 types remain intact; docs/SPEC.md now states the active domain rules and
dependency gates explicitly. Streamlit, Plotly and openpyxl are authorized by
the latest request. SQLite uses the Python standard library. Python 3.12 is the
installed interpreter; code targets Python 3.11+ and does not require 3.12 APIs.

Deadline follows the user's exact floor((point-buffer)/rate) formula, even for
nonzero today: no inferred offset or minus-one is added. Slack separately uses
start-today exactly as requested. Spares are consumed; bays and whole crews
are reused at the exclusive end day start+duration. A horizon limits spare
eligibility, not the end of maintenance. Spare compatibility uses part_number.
Choose the earliest candidate start, then earliest spare availability, spare
ID, bay ID and crew ID; binding ties use spare, bay, crew priority. Tomorrow
alone binding has no resource. No unused eligible spare means Unplanned.

Perturbations may take the planning point below zero for the mathematical float
search; this is not a new health estimate and is handled only inside analysis.
Comparison uses precisely all tails' start/bay/spare/status; deadline, crew and
binding changes alone do not count. Unplanned slack is undefined and the label
is Fragile. When no decision change is found through R, Covered requires both
R and slack to cover h. Otherwise Fragile is conservative because the search
bound cannot establish the requested comparison. UI explains this limitation.

Grouped residual calibration uses fallback global residual quantiles for empty
predicted-RUL bins. All sensor selection is from training data; calibration
and evaluation engines are separated from fit engines. Reports are generated
from NASA inputs and no coverage target is tuned to. CSV is the deterministic
artifact format even when optional Parquet support is installed.

Phase 2 completed: tests were added before implementation, real FD001 grouped
training and official-test evaluation generated the committed model, OOF CSV
and model_metrics.json. Two full training runs yielded identical bytes for all
three artifacts (hashes in reports/model_reproducibility.json). The full test
task passed including generated-report coverage and fold-disjointness checks.

The revised fleet pack contains fleet.csv (health estimates and technical
planning attributes), spares.csv, resources.csv and health_stream.csv.
manifest.json labels the pack and records its seed. simulation_truth.json is
evaluation-only. OOF estimates for selected distinct engines provide the
fictional health replay; their current benchmark remaining life is available
only to pack generation and simulation. Crew means a whole crew, not individual
technician headcount. Generated inputs and histories are never real aircraft.

Invalid, future-dated and duplicate rows are quarantined; all conflicting
duplicates are rejected rather than choosing one silently. Valid tails may
still be planned and the UI must expose omitted rows. Missing spares produce
an empty spare set; missing bay/crew blocks planning. SQLite records canonical
accepted and rejected source snapshots keyed by content and settings hash;
repeat ingestion does not duplicate rows. Git attributes keep artifact line
endings stable on Windows and fresh checkouts.

Phase 3 completed: pre-implementation tests failed on the absent modules,
then the full test task passed after implementation. The demo CSV pack was
generated and clean-ingested; deterministic regeneration, row quarantine,
truth-file isolation and SQLite idempotence were exercised.

Phase 4 completed: scheduler tests were written before implementation and the
full test task passed. Hand calculations include fractional utilisation,
negative/past deadlines, binding ties and consumed/incompatible/late spares.
Seeded resource tests cover bay/crew occupancy and unique spare use. Input
order does not change the plan or hash. Planner source scanning rejects I/O
and evaluation-field access. The planner has no randomness or global state.

Simulation in the revised prototype evaluates one fixed plan over days today
through horizon-1. It separately receives synthetic remaining cycles, never
passes them to the planner, counts an exhausting flying day as operating and
failure from the following day, and assumes a completed replacement remains
serviceable for the rest of the horizon. Failed waiting and failed repair days
are AOG. Duration is the given duration, with no inferred extra repair days.
This small scenario accounting is not the historical seven-stratum/five-policy
evaluation, which the revised request superseded. No extra policies are added.

What-if changes one existing spare/bay/crew's availability in a copy of state;
it does not mutate the current plan. The comparison reports no effect when a
control makes no difference. No prices, new resource types or extra endpoints
are introduced. Float witnesses list any changed fleet tail, even when the
focal tail's own start/bay/spare/status remains identical.

Phase 5 completed: pre-implementation tests exercised both signs, a change to
another tail while the focal signature is unchanged, finite search bounds,
half-width equality, undefined Unplanned slack, one-resource state diffs and
simulation accounting. The full test task passed; repeated synthetic e2e
reports were byte-identical. reports/demo_results.json is generated from the
shipped pack; adverse results are retained as generated, without tuning the
pack to improve outcomes.

The offline UI test prohibits all outbound socket connections and the high-
level connection helper; Windows asyncio's internal loopback socketpair is
permitted because it is process coordination on this device. Streamlit binds
to loopback with telemetry disabled and uses bundled Plotly/fonts. The physical
disconnected-browser rehearsal remains explicit in the runbook. The app uses
logical day timestamps for deterministic audit payloads, with sequential IDs
distinguishing multiple actions on the same day. No wall-clock timestamps are
introduced into model or scenario artifacts.

Pinned requirements include the resolved closure of the requested libraries
and retained Pydantic/PyYAML scaffold, rather than unrelated packages from the
system environment. Streamlit's own Starlette dependency supersedes the old
FastAPI requirement; the revised app has no API and FastAPI is removed from
project dependencies. Existing system-wide packages are not modified. The
existing workspace venv inherits system libraries; a new plain venv with
requirements.txt is the documented installation for an isolated environment.

During final packaging the shared system NumPy changed after initial training.
The pinned NumPy was installed inside the project's venv, without modifying the
system installation. A dependency-version regression test now checks every pin
against the executing environment. Setuptools and wheel are pinned too, so a
fresh Python 3.12 venv can perform the offline editable setup without relying
on inherited build packages.

Phase 6 completed: audit and UI tests were added before implementation.
The full test task passed after final packaging, including every module,
human review, tamper detection, outbound-network prohibition and all pinned
dependency versions. Offline editable setup, FD001 data-check and e2e passed;
pip's no-index dry-run resolved the complete installed lock without downloads.
The local server started successfully and the rendered fleet and tail charts
were inspected; browser error logs were empty. Physical disconnected-browser
rehearsal remains a documented human step, not a claim of the automated checks.

## Build scope and phase gates

The user's request to build authorizes the whole project. The supplied document is the implementation specification, including its dependency order and phase gates. Its suggested per-phase prompts are workflow examples. The supplied spec has been copied unchanged to docs/SPEC.md.

Phase 0's code and unit checks can be completed independently. Its data-check gate and Phase 1's real-data loader checks cannot pass without the three NASA FD001 files. No benchmark data was present in the workspace or among matching files in Downloads at build start. Later phases remain pending, including the rule fallback; that fallback does not waive the real-data gates. Test-generated files are format fixtures in pytest temporary directories, never training or evaluation inputs.

Initial validation: `python scripts/tasks.py setup test data-check` successfully installed the local project, then passed all 33 scaffolding tests. The final data-check command exited with status 1 and listed the three missing files. That initial data gate was subsequently resolved by the user-supplied archive, as recorded below.

## Windows tooling and installation

GNU Make is unavailable on this machine. All required Makefile targets delegate to scripts/tasks.py, which can also be invoked directly on Windows. Both entry points execute the same checks. Future-phase commands return a nonzero status with an explicit pending-phase message.

Setup uses a workspace-local .venv with access to the already installed core libraries, then performs an editable installation without dependency resolution, build isolation or package-index access. A fresh machine must first install the pyproject.toml dependencies. No runtime download is introduced. This is an environment accommodation rather than a claim that dependency installation always works offline on a fresh machine.

The workspace initially had no Git repository. The user explicitly requested a Phase 1 commit; a local repository was initialized for it using the existing configured Git identity. The initial commit necessarily includes the existing Phase 0 scaffold. Raw benchmark files and the local environment remain excluded by .gitignore.

## Validation and determinism

Configuration models reject unknown fields, nonfinite numeric values, invalid intervals, overlapping seed ranges, unordered bins, invalid quantiles and duplicate catalog entries. Hashes use UTF-8 canonical JSON with sorted keys and compact separators; dates use ISO strings. Tuples and frozen models prevent accidental configuration mutation.

FD001 format validation also rejects duplicate unit/cycle rows, invalid identifiers and nonfinite values. Passing format validation does not verify provenance; the human must obtain the dataset from NASA and review its terms.

## Open items carried forward

Date ingestion will use the explicit formats in the spec and exclude ambiguous US month/day/year parsing. Exact moderate-resource settings, manual resolution details, development scenario calibration and fresh-seed demo confirmation remain phase-specific decisions. No parameters have been adjusted against report seeds.

## Phase 1: data and core contracts

The user supplied `6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip`, containing a nested CMAPSSData.zip. Only the three FD001 files were extracted byte-for-byte into data/raw. No generated or substituted benchmark data is used. The existing data-check passed before Phase 1 tests or implementation were added.

Tests were written first and run: collection failed because the loader and core types did not yet exist. After implementation, the full suite passed all 61 tests against the extracted files. This includes integer train targets ending at zero and decreasing one cycle at a time, data-derived sensor selection, immutable core types, Scenario JSON round trips, schema separation and recursive planner/policy source scanning. Phase 2 and later phases have not been started.

Schema choices: all core models use frozen Pydantic v2 models and tuple collections, including nested calendars and records. Scenario stores metadata, horizon, ScenarioTruth and ScenarioBeliefs. Truth contains keyed tail failure cycles, spare actual dates and actual agency calendars. Beliefs contain Tail, SpareUnit, Agency, technical records, resolved degradation windows/ages and estimate bias. PlanningState uses only belief types and the validated Config, with no actual dates or failure cycles. FAILED is an observed tail status distinct from daily AOG accounting. Manual resolution is an observed boolean for subsequent policies. No policy or simulation logic is implemented here.

Agency calendars are indexed by absolute simulation day beginning at zero. Job duration is work duration, and Placement.end_day is inclusive of transit and work. Unplaced jobs use null dates/resources rather than fabricated placements. Diagnostic counts and run metrics use typed frozen models rather than mutable dictionaries. The shared FrozenModel was moved to pdm/_base.py to avoid a dependency cycle between the Config and PlanningState models; pdm.types continues to expose it.

Loader choices: load_fd001 returns three DataFrames (train, test, rul), preserving all raw sensor columns. Train adds uncapped true_rul only. The RUL DataFrame uses columns unit and rul; unit is explicitly associated with each official test-engine row in ascending ID order. Unit, cycle and RUL values use integer dtypes. The function validates the supplied files and never downloads or rewrites them.

drop_constant_sensors returns the names to drop and does not mutate its DataFrame. Population variance (ddof=0) is computed across training rows only; results follow canonical sensor order. The small threshold is configurable as model.constant_sensor_variance_threshold, defaulting to 1e-12, to follow the global rule that tunables live in configuration. The sensor list itself is never hardcoded. This numeric tolerance detects effectively constant values while retaining sensors with observed variation; it is not a fitted model setting. Adding this field changes the configuration hash as expected. No dependency was added.
