# Local demo runbook

From the repository root, install the pinned requirements once, then run
`python scripts/tasks.py test` and `python scripts/tasks.py app`.
`python -m streamlit run app.py` also works in the installed environment.
Open Streamlit's printed loopback URL. Runtime assets, fonts and Plotly are
local, and telemetry is disabled. Rehearse with the computer disconnected.

The default scenario is the seeded assumed T-04 story. Its health/technical
annotations and ranges are fictional inputs; they are distinct from measured
NASA FD001 benchmark metrics. The original ten-tail pack is available in
Demo pack as Four-silo fleet, using cached engine predictions and its validated
rates, inventory and resource counts.

Use the timed [three-minute README script](../README.md#three-minute-demo-script)
for presentation and its wheelhouse instructions for disconnected installation.
Start with **Reset demo** in the sidebar. It restores the clean story and
default controls, returns to Fleet board and releases only this story's pins
via a chained event. It preserves reviewer identity, all prior approvals and
audit rows, CSV files and generated reports. Its replan cause is recorded.
The button also recovers from the in-memory corrupted-pack demonstration;
it cannot conceal a broken chain or repair damaged source files.

1. In Fleet board, select T-04. Read the computed RUL range, days to deadline,
   decision float, ordinary deadline slack, binding resource and attention
   label. The Why this plan panel uses the planner's reason code. Float
   replans the fleet; slack freezes the current placement.
2. Open What-if. T-04 is preselected; use the tail selector for other tails.
3. Click Expedite S2 by 5 days. Read the computed label/start change and fleet
   diff. The original placement has not moved. These three clicks reproduce
   the spare story without requiring a configuration change.
4. Expand the inspection note labelled **assumed, not scored**. Inspection is
   excluded from ranked actions. Click Add one crew shift and show its No effect comparison.
   Ranked candidates retain unchanged actions and show assumed costs with
   benefit = (net Covered increase + Late reduction) / man-hours.
5. Open Data. Inspect four silos, record badges and quarantine. Toggle Load
   corrupted pack: the gate holds, quarantined records remain inspectable,
   and Fleet board, What-if and Approvals offer no decision actions. The hold
   persists while switching tabs. Turn the toggle off to restore clean inputs.
6. Open Approvals. Submit a blank user/reason to demonstrate validation, then
   enter a demo reviewer name and reason. Approve/reject records a placement
   annotation only. PIN lets the reviewer edit start/bay/crew/spare; conflicting
   or unavailable choices fail before recording. A valid pin reserves its
   resources first and persists for this input snapshot. Reviewing it does
   not silently release the reservation. **Reset demo** explicitly releases
   story pins while retaining their history; pins in other snapshots persist.
7. Read **Chain verified** in Approvals, then use Verify audit chain to recheck.
   Inspect timestamp, user, action, tail, before/after and reason columns.
   Reopen the app: stored pins are restored and the load cause is recorded.
   Compare the same intervention twice: both explicit comparisons are logged;
   switching tabs alone adds no comparison event. A broken chain holds further
   planning and pin use; preserve the database for review instead of editing
   historical rows. Open Model metrics
   in the footer: RMSE, score, PICP and width come from the generated official
   FD001 report. Coverage is a fraction and makes no aircraft claim.

AppTest covers all five tabs, comparisons, reset, name/reason validation, pins and
holds with outbound connections prohibited; Windows's internal loopback
socketpair is permitted. Browser checks cover coloured labels, actual row
selection and quick actions. Physical disconnected-browser rehearsal remains
human demo preparation.

Recovery: regenerate assumed story inputs/report with
`python scripts/tasks.py whatif-demo`, or the original silo pack with
`python scripts/tasks.py gen-fleet`. Missing cache/metric artifacts require
`python scripts/tasks.py train` with the official files in data/CMAPSS/.
The app never trains or downloads. Missing or quarantined planning inputs
hold decisions; repair the source and rerun. A short float bound returns
`> R` and cannot establish Covered unless it covers the range half-width.

Restart an already running Streamlit server after Python module changes;
this project's file watcher is disabled. Refresh its browser after restart.

For policy validation, first run `python scripts/tasks.py validation`.
Open Validation, read **simulated; scenario-based**, then compare all policy
means and their bootstrap intervals, including the B2-K0 no-intervention
control and B4b direct-float policy. Retain all generated paired tie notes;
do not present the report as evidence that one policy must win. Read total
man-hours and unused weeks alongside all outcomes. For weekly allowance,
selected action and unused reason, inspect the generated per-cell weekly CSV
and validation_diagnostics.log. Download the numeric CSV for exact values.
Scenario assumptions describe the fixed interval, spare delays, AOG accounting
and finite float search. The tab shows a separate generated report for the
four-silo fleet and does not apply the current demo's pins or run Monte Carlo.

Choose Frozen stress level, Horizon (days) and Assumed unplanned repair multiplier
in Validation to show both horizons and all stress/repair sensitivities. Weekly rows include
the start-of-week Fragile set, selected tail, top action/benefit and unused
reason. AOG includes grounded waiting through maintenance; healthy aircraft
awaiting future slots keep flying. B1's interval is frozen from fit-training
engine lifetimes, and failure repair multipliers are labelled assumed.
All generated mean/CI tables are in artifacts/validation_comparison.md;
artifacts/validation_diagnostics.log prints three scenarios per stress level.
The corrected log artifacts/validation_phase19_execution.log also prints B1
per-scenario AOG, waits and interval. The CSV uses one wide row per
stress/repair/horizon/policy plus named paired comparisons, with exact outcome ties/N.
Read competing-candidate and differing-choice shares and applied action
counts before interpreting ties. A "test lacks power" note flags limited
competing-tail opportunities; do not change stress settings to force a winner.
B1 plans future interval deadlines through the same planner. Its frozen
interval remains an assumed training-lifetime proxy, and neutral initial
ages are uniform on that interval's scale. Selected-tail benefit controls
simulated resource-action ranking; B4's combined rule and B4b's direct float
rule both remain visible. The B2-K0 combined outcome tie count excludes
budget columns. AOG and failures appear side by side across repair/horizon
sensitivities. The design is explicitly post-hoc: v1 results were seen, and
v1 reports remain in artifacts/validation_v1/ with a hash ledger.

The polished board keeps snapshot metric cards and Covered/Fragile pills above
the tabs. Range bars show lower/upper RUL and a point-estimate tick; hangar
bars show induction duration with diamonds marking every deadline. Data has
Good/Stale/Conflict chips, and Approvals names missing required fields before
writing a review. The browser rehearsal verified the three-click S2 story,
the No effect crew row, a named/reasoned approval and verified chain, the
cross-tab corruption hold, Reset demo, and stress/repair selectors. Its saved
before/after view is reports/ui_phase17.jpg. Validation reads only the generated
CSV, including paired differences, ties and sensitivity cells.
