"""Offline FD001 point/quantile training and official-test evaluation."""
import argparse
from pathlib import Path
from vayu.rul import train_fd001


def main() -> int:
    """Use local NASA files; print manual instructions and exit on missing data."""
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path, default=root / 'data/CMAPSS')
    parser.add_argument('--artifact-dir', type=Path, default=root / 'artifacts')
    parser.add_argument('--seed', type=int, default=7)
    parser.add_argument('--n-estimators', type=int, default=400)
    args = parser.parse_args()
    try:
        report = train_fd001(args.data_dir, args.artifact_dir, args.seed, args.n_estimators)
    except FileNotFoundError:
        return 1  # train_fd001 already printed specific manual download instructions.
    print(f'Generated {args.artifact_dir / "rul_metrics.json"} and rul_model.joblib')
    print(report['data_label'])
    print(report['test'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
