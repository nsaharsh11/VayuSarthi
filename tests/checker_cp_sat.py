"""Standalone test-only CP-SAT oracle; JSON stdin/stdout, no application imports."""
import json
import math
import sys
from typing import Any

from ortools.sat.python import cp_model


def check(request: dict[str, Any]) -> dict[str, Any]:
    """Check fixed resource assignments or search for strictly fewer Late tails.

    Fix the planned/unplanned tail set, so an alternative cannot avoid lateness
    by discarding jobs. Pins remain fixed and residual bay/crew capacity starts
    after the reserved prefix, matching the specified production pin semantics.
    """
    state, placements = request['state'], request['placements']
    tails = {tail['tail_id']: tail for tail in state['tails']}
    spares = {spare['spare_id']: spare for spare in state['spares']
              if spare['available_day'] <= state['horizon']}
    bays = {bay['resource_id']: bay['free_day'] for bay in state['bays']}
    crews = {crew['resource_id']: crew['free_day'] for crew in state['crews']}
    pins = {pin['tail_id']: pin for pin in request.get('pins', [])}
    bay_release, crew_release = bays.copy(), crews.copy()
    for pin in pins.values():
        end = pin['start_day'] + tails[pin['tail_id']]['duration']
        bay_release[pin['bay']] = max(bay_release[pin['bay']], end)
        crew_release[pin['crew']] = max(crew_release[pin['crew']], end)
    jobs = [p for p in placements if p['start_day'] is not None]
    limit = max([state['today']+1, *[s['available_day'] for s in spares.values()],
                 *bay_release.values(), *crew_release.values(),
                 *[p['start_day'] for p in jobs]]) + sum(t['duration'] for t in tails.values())
    model = cp_model.CpModel()
    bay_intervals: dict[str, list] = {key: [] for key in bays}
    crew_intervals: dict[str, list] = {key: [] for key in crews}
    spare_assignments: dict[str, list] = {key: [] for key in spares}
    starts, late_vars = {}, []
    for placement in jobs:
        tail_id = placement['tail_id']
        tail = tails[tail_id]
        duration = tail['duration']
        start = model.new_int_var(state['today']+1, limit, f'start_{tail_id}')
        starts[tail_id] = start
        end = model.new_int_var(state['today']+1, limit+duration, f'end_{tail_id}')
        model.add(end == start + duration)
        bay_choices, crew_choices, spare_choices = {}, {}, {}
        for kind, pool, release, choices, intervals in (
                ('bay', bays, bay_release, bay_choices, bay_intervals),
                ('crew', crews, crew_release, crew_choices, crew_intervals)):
            for resource in sorted(pool):
                chosen = model.new_bool_var(f'{tail_id}_{kind}_{resource}')
                choices[resource] = chosen
                model.add(start >= (pool[resource] if tail_id in pins else release[resource])).only_enforce_if(chosen)
                intervals[resource].append(model.new_optional_interval_var(
                    start, duration, end, chosen, f'{tail_id}_{kind}_{resource}_interval'))
            model.add_exactly_one(list(choices.values()))
        for spare_id, spare in sorted(spares.items()):
            if spare['part_number'] != tail['part_number']:
                continue
            chosen = model.new_bool_var(f'{tail_id}_spare_{spare_id}')
            spare_choices[spare_id] = chosen
            spare_assignments[spare_id].append(chosen)
            model.add(start >= spare['available_day']).only_enforce_if(chosen)
        model.add_exactly_one(list(spare_choices.values()))
        deadline = math.floor((tail['rul_point'] - state['safety_buffer']) / tail['rate'])
        late = model.new_bool_var(f'late_{tail_id}')
        model.add(start > deadline).only_enforce_if(late)
        model.add(start <= deadline).only_enforce_if(late.Not())
        late_vars.append(late)
        fixed = placement if request['mode'] == 'fixed' else pins.get(tail_id)
        if fixed is not None:
            model.add(start == fixed['start_day'])
            for key, choices in (('bay', bay_choices), ('crew', crew_choices), ('spare', spare_choices)):
                if fixed[key] not in choices:
                    model.add(False)
                else:
                    model.add(choices[fixed[key]] == 1)
    for intervals in [*bay_intervals.values(), *crew_intervals.values()]:
        model.add_no_overlap(intervals)
    for choices in spare_assignments.values():
        model.add(sum(choices) <= 1)
    if request['mode'] == 'fewer_late':
        model.add(sum(late_vars) < sum(p['status'] == 'Late' for p in placements))
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 0
    solver.parameters.max_time_in_seconds = 10
    status = solver.solve(model)
    result: dict[str, Any] = {'status': solver.status_name(status)}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        result['late_count'] = sum(solver.value(value) for value in late_vars)
        result['starts'] = {key: solver.value(value) for key, value in sorted(starts.items())}
    return result


if __name__ == '__main__':
    print(json.dumps(check(json.load(sys.stdin)), sort_keys=True, separators=(',', ':')))
