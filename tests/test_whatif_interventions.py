"""Assumed T-04 story, cost ranking, no-effect controls and combined scenarios."""
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from vayu.planner import decision_signature
from vayu.quality import read_pack
from vayu.schemas import PinnedPlacement, PlanningState, Resource, Spare, Tail, canonical_json
from vayu.sim import generate_whatif_demo, whatif_demo_state
from vayu.whatif import (Intervention, WhatIfExplorer, apply_intervention,
                          default_interventions, pairs_for_top_k, rank_interventions)


def candidates() -> tuple[Intervention, ...]:
    """Explicit fictional man-hour costs; the assumed inspection factor defaults."""
    return (Intervention('expedite', 'expedite_spare', 8, target='S2', days=5),
            Intervention('crew', 'add_crew_shift', 8, target='CREW-02'),
            Intervention('bay', 'add_bay', 16, target='BAY-02'),
            Intervention('inspect', 'inspect_tail', 4, target='T-04'))


def test_t04_story_and_no_effect_candidate_retained() -> None:
    state = whatif_demo_state()
    explorer = WhatIfExplorer(state, candidates(), radius=40)
    before = explorer.baseline
    focal = next(a for a in before.attention if a.tail_id == 'T-04')
    placement = next(p for p in before.plan.placements if p.tail_id == 'T-04')
    assert focal.label == 'Fragile' and placement.binding == 'spare' and placement.spare == 'S2'
    ranked = explorer.rank()
    by_id = {row['intervention_ids'][0]: row for row in ranked}
    assert len(ranked) == 3 and 'inspect' not in by_id
    row = next(r for r in by_id['expedite']['per_tail_changes'] if r['tail'] == 'T-04')
    assert row['before']['label'] == 'Fragile' and row['after']['label'] == 'Covered'
    assert by_id['crew']['effect'] == 'No effect'
    assert by_id['crew']['benefit_per_cost'] == 0
    assert all(not row['changed_fields'] for row in by_id['crew']['per_tail_changes'])
    # The legacy assumption can still be examined explicitly, never ranked.
    assumed = explorer.evaluate(candidates()[-1])
    assert assumed['assumed']
    assert all(not row['placement_changed'] for row in assumed['per_tail_changes'])
    assert ranked[0]['intervention_ids'] == ['expedite']
    assert ranked[0]['benefit_per_cost'] == 1 / 8
    assert before.plan == explorer.baseline.plan
    assert asdict(state) == asdict(whatif_demo_state())


def test_seed_and_ranking_are_deterministic(tmp_path: Path) -> None:
    state = whatif_demo_state(seed=17)
    first = rank_interventions(state, candidates())
    second = rank_interventions(replace(state, tails=state.tails[::-1], spares=state.spares[::-1]),
                                candidates()[::-1])
    assert canonical_json(first) == canonical_json(second)
    a, b = tmp_path / 'a', tmp_path / 'b'
    generate_whatif_demo(a, seed=17)
    generate_whatif_demo(b, seed=17)
    assert {p.name: p.read_bytes() for p in a.iterdir()} == {p.name: p.read_bytes() for p in b.iterdir()}
    loaded = read_pack(a, safety_buffer=0)
    assert not loaded.issues and loaded.state is not None
    actual = WhatIfExplorer(loaded.state, candidates()).rank()
    assert next(r for r in actual if r['intervention_ids'] == ['crew'])['effect'] == 'No effect'
    assert 'assumed' in (a / 'manifest.json').read_text().lower()


def test_pairs_are_replanned_not_added_single_scores() -> None:
    explorer = WhatIfExplorer(whatif_demo_state(), candidates())
    pairs = explorer.pairs_for_top_k(2)
    assert len(pairs) == 1
    assert all('inspect' not in row['intervention_ids'] for row in pairs)
    assert pairs_for_top_k(2, state=whatif_demo_state(), candidates=candidates()) == pairs
    # Explicit combined evaluation still counts overlapping benefits once.
    combined = explorer.evaluate((candidates()[0], candidates()[-1]))
    assert combined['benefit'] == 1 and combined['cost_man_hours'] == 12
    assert explorer.pairs_for_top_k(0) == explorer.pairs_for_top_k(1) == []
    assert len(explorer.pairs_for_top_k(99)) == 3
    with pytest.raises(ValueError):
        explorer.pairs_for_top_k(-1)


def test_inspection_preserves_asymmetry_point_and_other_inputs() -> None:
    state = whatif_demo_state()
    original = next(t for t in state.tails if t.tail_id == 'T-04')
    asymmetric = replace(original, lower=10, upper=50)
    state = replace(state, tails=tuple(asymmetric if t.tail_id == 'T-04' else t for t in state.tails))
    action = Intervention('inspect', 'inspect_tail', 4, target='T-04')
    changed = apply_intervention(state, action)
    tail = next(t for t in changed.tails if t.tail_id == 'T-04')
    assert (tail.rul_point, tail.lower, tail.upper) == (40, 25, 45)
    assert state.spares == changed.spares and state.bays == changed.bays and state.crews == changed.crews
    assert decision_signature(WhatIfExplorer(state, (action,)).baseline.plan) == decision_signature(
        WhatIfExplorer(changed, (action,)).baseline.plan)


@pytest.mark.parametrize('settings', [{'cost_man_hours': 0}, {'cost_man_hours': float('inf')},
                                     {'factor': 0}, {'factor': 1.1}, {'days': -1},
                                     {'days': 1.5}, {'kind': 'unsupported'}])
def test_invalid_intervention_parameters(settings: dict) -> None:
    values = {'intervention_id': 'bad', 'kind': 'inspect_tail', 'cost_man_hours': 2, 'target': 'T-04'}
    values.update(settings)
    with pytest.raises(ValueError):
        Intervention(**values)


def test_unknown_targets_resource_collisions_and_duplicate_ids() -> None:
    state = whatif_demo_state()
    for kind, target in (('expedite_spare', 'BAD'), ('inspect_tail', 'BAD'),
                         ('add_bay', 'BAY-01'), ('add_crew_shift', 'CREW-01')):
        with pytest.raises(ValueError):
            apply_intervention(state, Intervention('bad', kind, 1, target=target, days=1))
    with pytest.raises(ValueError, match='Duplicate'):
        WhatIfExplorer(state, (candidates()[0], candidates()[0]))


def test_zero_day_expedite_and_factor_one_no_effect() -> None:
    actions = (Intervention('zero', 'expedite_spare', 1, target='S2', days=0),
               Intervention('same', 'inspect_tail', 1, target='T-04', factor=1))
    rows = rank_interventions(whatif_demo_state(), actions)
    assert all(row['effect'] == 'No effect' for row in rows)
    assert all(row['label_counts']['Covered'] + row['label_counts']['Fragile'] == 6 for row in rows)
    assert len(default_interventions(whatif_demo_state())) == 8
    assert all(a.kind != 'inspect_tail' for a in default_interventions(whatif_demo_state()))
    assert [r['intervention_ids'] for r in rows] == [['zero']]


def test_benefit_counts_both_coverage_gain_and_lateness_reduction() -> None:
    state = PlanningState((Tail('A', 8, 6, 10, 1, 3),), (Spare('S', 10),),
                          (Resource('B'),), (Resource('C'),), safety_buffer=0)
    row = rank_interventions(state, (Intervention('expedite', 'expedite_spare', 4,
                                                  target='S', days=10),))[0]
    assert row['before']['late_count'] == 1 and row['late_count'] == 0
    assert row['benefit_components'] == {'covered_increase': 1, 'late_reduction': 1}
    assert row['benefit'] == 2 and row['benefit_per_cost'] == .5


def test_added_capacity_replans_and_pinned_placement_stays_fixed() -> None:
    state = PlanningState((Tail('A', 2, 1, 3, 1, 4), Tail('B', 3, 2, 4, 1, 4)),
                          (Spare('S1', 0), Spare('S2', 0)), (Resource('B1'),),
                          (Resource('C1'),), safety_buffer=0)
    bay = Intervention('bay', 'add_bay', 4, target='B2')
    crew = Intervention('crew', 'add_crew_shift', 4, target='C2')
    explorer = WhatIfExplorer(state, (bay, crew),
                             pinned_placements=(PinnedPlacement('A', 1, 'B1', 'C1', 'S1'),))
    assert all(row['late_count'] == 1 for row in explorer.rank())
    combined = explorer.pairs_for_top_k(2)[0]
    assert combined['late_count'] == 0
    a, b = combined['per_tail_changes']
    assert a['tail'] == 'A' and not a['placement_changed']
    assert b['after']['start_day'] == 1 and (b['after']['bay'], b['after']['crew']) == ('B2', 'C2')


def test_unplanned_slack_is_absent_and_assumed_inspection_does_not_schedule() -> None:
    state = replace(whatif_demo_state(), spares=())
    action = Intervention('inspect', 'inspect_tail', 4, target='T-04')
    assert rank_interventions(state, (action,)) == []
    row = WhatIfExplorer(state, (action,)).evaluate(action)
    assert row['min_slack'] is None and row['unplanned_count'] == len(state.tails)
    assert row['label_counts']['Covered'] == 0 and row['benefit'] == 0
    assert row['effect'] == 'Effect'  # Narrower assumed range, even without label benefit.
    assert all(not change['placement_changed'] for change in row['per_tail_changes'])


def test_generated_report_is_reproducible_and_comes_from_computed_rows(tmp_path: Path) -> None:
    from scripts.whatif_demo import generate_report
    output = tmp_path / 'report.json'
    first = generate_report(tmp_path / 'pack', output, seed=49, radius=40, top_k=3)
    expected = output.read_bytes()
    assert 'assumed' in first['data_label'].lower()
    assert first['baseline']['plan']['placements']
    assert len(first['singles']) == len(default_interventions(whatif_demo_state()))
    assert len(first['pairs']) == 3
    assert any(row['effect'] == 'No effect' for row in first['singles'])
    assert generate_report(tmp_path / 'pack', output, seed=49, radius=40, top_k=3) == first
    assert output.read_bytes() == expected
