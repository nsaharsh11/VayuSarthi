"""Generate and validate the offline fictional four-silo fleet pack."""
import argparse
from pathlib import Path

from vayu.quality import read_fleet_pack
from vayu.sim import generate_fleet_pack


def main() -> int:
    """Generate bytes from explicit seed/day and fail if the quality gate holds."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seed', type=int, default=49)
    parser.add_argument('--today', type=int, default=0)
    parser.add_argument('--output', type=Path, default=Path('data/fleet'))
    args = parser.parse_args()
    generate_fleet_pack(args.output, args.seed, args.today)
    result = read_fleet_pack(args.output, args.today)
    print('Fictional simulated four-silo fleet; no live aircraft data.')
    print(f'Accepted records: {sum(len(frame) for frame in result.accepted.values())}; '
          f'quarantined: {len(result.quarantine)}; planning_hold={result.planning_hold}')
    for reason in result.reasons:
        print(reason)
    return int(result.planning_hold)


if __name__ == '__main__':
    raise SystemExit(main())
