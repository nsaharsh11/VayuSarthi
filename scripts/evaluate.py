"""Generate reviewable synthetic plan, attention and day-accounting reports."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path

from vayu.margins import analyze
from vayu.planner import plan
from vayu.quality import read_pack
from vayu.schemas import canonical_json
from vayu.sim import simulate


def evaluate(root: Path, radius: int = 40) -> dict:
    """Read local demo inputs; only simulation receives evaluation values."""
    state = read_pack(root/'data/demo').state
    if state is None:
        raise ValueError('Demo pack lacks valid capacity')
    scheduled = plan(state)
    truth = json.loads((root/'data/demo/simulation_truth.json').read_text())['remaining_cycles']
    report = {'data_label':'Fictional simulated fleet; scheduling decision support only',
              'plan':asdict(scheduled),'attention':[asdict(a) for a in analyze(state,radius)],
              'simulation':simulate(state,scheduled,truth)}
    (root/'reports').mkdir(parents=True,exist_ok=True)
    (root/'reports/demo_results.json').write_bytes(canonical_json(report).encode())
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--radius',type=int,default=40)
    arguments = parser.parse_args()
    report = evaluate(Path(__file__).resolve().parents[1],arguments.radius)
    for p in report['plan']['placements']:
        print(f"{p['tail_id']} | start={p['start_day']} | {p['status']} | binding={p['binding']}")
    print(canonical_json(report['simulation']['metrics']))
