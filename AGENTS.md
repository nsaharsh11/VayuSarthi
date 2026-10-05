# Project instructions

- Read docs/SPEC.md before changes. The user authorized the full build; implement phases in dependency order and advance only after the previous phase's Done when checks pass.
- Python 3.11+. Core libraries only: numpy, pandas, scikit-learn, lightgbm, fastapi, uvicorn, pydantic v2, pyyaml, pytest, pyarrow (optional; fall back to CSV).
- Everything must run offline after install. No CDN, runtime network calls, or telemetry.
- Route randomness through numpy Generators seeded from explicit seeds. Identical inputs must yield byte-identical outputs.
- Planner and policy code must never read ground truth. Follow the firewall in docs/SPEC.md section 3.4.
- Never hardcode result numbers in code, UI, or documentation. Results come from generated reports.
- Run make test before declaring a phase done. On Windows without Make, python scripts/tasks.py test is the equivalent. Add phase-specific tests before implementation.
- Log deviations and resolved ambiguities in docs/DECISIONS.md. Do not silently change definitions.
- Do not add features, endpoints, or dependencies outside the spec.
- Commit each completed phase with the requested message. The local repository was initialized for the user-requested Phase 1 commit; do not report commits that did not happen.
