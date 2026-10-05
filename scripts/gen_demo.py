"""Generate the local fictional fleet from held-out FD001 predictions."""
from pathlib import Path
import pandas as pd
from vayu.sim import generate_pack

if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    path = root/'data/processed/oof_predictions.csv'
    if not path.is_file():
        raise SystemExit('Run python scripts/tasks.py train first; no benchmark estimates are fabricated.')
    generate_pack(pd.read_csv(path),root/'data/demo',seed=7)
    print('Generated fictional fleet CSV pack in data/demo')
