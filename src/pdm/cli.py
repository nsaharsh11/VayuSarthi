"""Offline project commands."""
import argparse
from pathlib import Path

from pdm.config import ROOT, canonical_json, load_config
from pdm.data.check import check_data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Decision-aware predictive maintenance build utilities')
    subparsers = parser.add_subparsers(dest='command', required=True)
    config_parser = subparsers.add_parser('config', help='Validate configuration and print its content hash')
    config_parser.add_argument('--config', type=Path, default=ROOT / 'config/default.yaml')
    data_parser = subparsers.add_parser('data-check', help='Check the required NASA FD001 files')
    data_parser.add_argument('--data-dir', type=Path, default=ROOT / 'data/raw')
    arguments = parser.parse_args(argv)
    if arguments.command == 'config':
        config = load_config(arguments.config)
        print(canonical_json({'config_hash': config.config_hash, 'config': config.model_dump(mode='json')}))
        return 0
    result = check_data(arguments.data_dir)
    print(result.message)
    return 0 if result.ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
