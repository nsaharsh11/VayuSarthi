"""Generate the fictional assumed story pack and computed costed comparisons."""
import argparse
from dataclasses import asdict
from pathlib import Path
from typing import Any

from vayu.quality import read_pack
from vayu.schemas import canonical_json
from vayu.sim import WHATIF_LABEL, generate_whatif_demo
from vayu.whatif import BENEFIT_DEFINITION, WhatIfExplorer, default_interventions


def generate_report(pack: Path, output: Path, *, seed: int = 49,
                    radius: int = 40, top_k: int = 3) -> dict[str, Any]:
    """Regenerate a labelled input pack, quality-check it, then compute results.

    Reading the written CSVs makes the report reproducible from the shipped
    precision. Wall-clock sweep measurements stay outside the serialized report.
    """
    generate_whatif_demo(pack, seed)
    loaded = read_pack(pack, safety_buffer=0)
    if loaded.issues or loaded.state is None:
        raise ValueError(f'Assumed what-if pack failed quality checks: {loaded.issues}')
    explorer = WhatIfExplorer(loaded.state, default_interventions(loaded.state), radius)
    report = {'data_label': WHATIF_LABEL, 'seed': seed, 'radius': radius, 'top_k': top_k,
              'benefit_definition': BENEFIT_DEFINITION,
              'baseline': asdict(explorer.baseline),
              'singles': explorer.rank(), 'pairs': explorer.pairs_for_top_k(top_k)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(canonical_json(report).encode('utf-8'))
    return report


def write_demo_summaries(pack: Path, output: Path, radius: int = 40) -> None:
    """Export small computed plan/float/ETA artifacts from the shipped story CSVs."""
    from vayu.margins import PlannerCache, spare_eta_float
    loaded = read_pack(pack, safety_buffer=0)
    if loaded.issues or loaded.state is None:
        raise ValueError('Demo summaries require a clean story pack')
    state = loaded.state
    baseline = WhatIfExplorer(state, (), radius).baseline
    cache = PlannerCache()
    greedy = {'data_label': WHATIF_LABEL, 'plan': asdict(baseline.plan)}
    floats = {'data_label': WHATIF_LABEL, 'rul_float_unit': 'flight cycles',
              'spare_eta_unit': 'days', 'radius_cycles': radius,
              'tails': [{'tail': item.tail_id, 'decision_float': item.float_result.to_dict(),
                         'deadline_slack_cycles': item.slack, 'half_width_cycles': item.half_width,
                         'label': item.label} for item in baseline.attention],
              'spare_eta': [spare_eta_float(spare.spare_id, state, cache=cache)
                            for spare in sorted(state.spares, key=lambda item: item.spare_id)]}
    output.mkdir(parents=True, exist_ok=True)
    for name, payload in (('greedy_summary.json', greedy), ('float_summary.json', floats)):
        (output/name).write_bytes(canonical_json(payload).encode('utf-8'))


def main() -> int:
    """Write the offline comparison report with explicit reproducible settings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=49)
    parser.add_argument('--radius', type=int, default=40)
    parser.add_argument('--top-k', type=int, default=3)
    parser.add_argument('--pack', type=Path, default=Path('data/whatif_demo'))
    parser.add_argument('--output', type=Path, default=Path('reports/whatif_demo.json'))
    parser.add_argument('--summaries-dir', type=Path, default=Path('artifacts'))
    args = parser.parse_args()
    report = generate_report(args.pack, args.output, seed=args.seed,
                             radius=args.radius, top_k=args.top_k)
    write_demo_summaries(args.pack, args.summaries_dir, args.radius)
    print(report['data_label'])
    print(f"Computed {len(report['singles'])} single comparisons and "
          f"{len(report['pairs'])} pairs; report: {args.output}")
    for row in report['singles']:
        print(f"{','.join(row['intervention_ids'])}: {row['effect']}; "
              f"benefit/man-hour={row['benefit_per_cost']:g}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
