"""Independent small-fleet constraint proofs and the greedy-rule limitation."""
from dataclasses import asdict
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pytest

from vayu.planner import plan
from vayu.schemas import PinnedPlacement, PlanningState, Resource, Spare, Tail


def oracle(state: PlanningState, mode: str, pins: tuple[PinnedPlacement, ...] = (),
           placements: list[dict] | None = None) -> dict:
    """Run the test-only solver with its separately compatible Python runtime."""
    root = Path(__file__).resolve().parents[1]
    local_checker = root / '.checker-venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    python = os.environ.get('VAYU_CHECKER_PYTHON',
                            str(local_checker) if local_checker.is_file() else sys._base_executable)
    payload = {'state': asdict(state), 'mode': mode, 'pins': [asdict(p) for p in pins],
               'placements': placements if placements is not None else
                             [asdict(p) for p in plan(state, pinned_placements=pins).placements]}
    result = subprocess.run([python, str(Path(__file__).with_name('checker_cp_sat.py'))],
                            input=json.dumps(payload), text=True, capture_output=True, timeout=30,
                            check=False)
    assert result.returncode == 0, ('CP-SAT checker failed. Install requirements-checker.txt in a '
                                    'separate venv and set VAYU_CHECKER_PYTHON.\n' + result.stderr)
    return json.loads(result.stdout)


@pytest.mark.parametrize('count', range(1, 7))
def test_small_equal_duration_deadlines_have_no_strictly_better_schedule(count: int) -> None:
    """In these equal-duration fixtures, deadline-first maximises on-time starts."""
    state = PlanningState(tuple(Tail(f'T{i}', 3, 1, 5, 1, 2) for i in range(count)),
                          tuple(Spare(f'S{i}', 0) for i in range(count)),
                          (Resource('B'),), (Resource('C'),))
    assert oracle(state, 'fixed')['status'] == 'OPTIMAL'
    assert oracle(state, 'fewer_late')['status'] == 'INFEASIBLE'


def test_pinned_case_and_intentionally_double_booked_plan() -> None:
    state = PlanningState((Tail('A', 4, 2, 6, 1, 2), Tail('B', 5, 3, 7, 1, 2)),
                          (Spare('S1', 0), Spare('S2', 0)), (Resource('B'),), (Resource('C'),))
    pins = (PinnedPlacement('A', 1, 'B', 'C', 'S1'),)
    assert oracle(state, 'fixed', pins)['status'] == 'OPTIMAL'
    assert oracle(state, 'fewer_late', pins)['status'] == 'INFEASIBLE'
    placements = [asdict(p) for p in plan(state).placements]
    placements[1]['start_day'] = 1
    assert oracle(state, 'fixed', placements=placements)['status'] == 'INFEASIBLE'


def test_greedy_counterexample_is_exposed_not_hidden() -> None:
    """The required greedy order cannot satisfy a universal lateness optimum."""
    state = PlanningState((Tail('A', 3, 1, 5, 1, 10), Tail('B', 4, 2, 6, 1, 1),
                           Tail('C', 5, 3, 7, 1, 1)),
                          tuple(Spare(f'S{i}', 0) for i in range(3)),
                          (Resource('B'),), (Resource('C'),))
    assert sum(p.status == 'Late' for p in plan(state).placements) == 2
    alternative = oracle(state, 'fewer_late')
    assert alternative['status'] == 'OPTIMAL' and alternative['late_count'] <= 1


def test_seeded_resource_safety_and_solver_repeatability() -> None:
    rng = np.random.default_rng(49)
    for _ in range(6):
        state = PlanningState(tuple(Tail(f'T{i}', float(rul), 0, float(rul+2), 1,
                                        int(rng.integers(1, 5)))
                                    for i, rul in enumerate(rng.integers(0, 20, 6))),
                              tuple(Spare(f'S{i}', int(day)) for i, day in enumerate(rng.integers(0, 10, 6))),
                              (Resource('B1'), Resource('B2')), (Resource('C1'), Resource('C2')))
        assert oracle(state, 'fixed')['status'] == 'OPTIMAL'
    assert oracle(state, 'fewer_late') == oracle(state, 'fewer_late')
