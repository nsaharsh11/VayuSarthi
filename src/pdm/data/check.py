"""Validate the user-supplied FD001 pack without acquiring data."""
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

FILES = ('train_FD001.txt', 'test_FD001.txt', 'RUL_FD001.txt')


@dataclass(frozen=True)
class DataCheck:
    ok: bool
    message: str


def check_data(directory: str | Path) -> DataCheck:
    directory = Path(directory)
    missing = [name for name in FILES if not (directory / name).is_file()]
    if missing:
        return DataCheck(False, f'Missing FD001 data: {", ".join(missing)}.\n'
                         'Download the C-MAPSS FD001 dataset from the NASA Prognostics Center data repository, '
                         f'review its terms, and place the three files in {directory.resolve()}.\n'
                         'Model training and later phase gates require these real benchmark files.')
    errors = []
    for name in FILES:
        try:
            frame = pd.read_csv(directory / name, sep=r'\s+', header=None)
            expected_columns = 1 if name == 'RUL_FD001.txt' else 26
            if frame.shape[1] != expected_columns:
                description = 'one column' if expected_columns == 1 else '26 columns'
                errors.append(f'{name}: expected {description}; found {frame.shape[1]}')
                continue
            values = frame.to_numpy(dtype=float)
            if not np.isfinite(values).all():
                errors.append(f'{name}: all values must be numeric and finite')
                continue
            if name == 'RUL_FD001.txt':
                if len(frame) != 100:
                    errors.append(f'{name}: expected 100 rows; found {len(frame)}')
                if (values < 0).any():
                    errors.append(f'{name}: RUL must be non-negative')
                if (values != np.floor(values)).any():
                    errors.append(f'{name}: RUL must use integer cycles')
            else:
                identifiers = values[:, :2]
                if (identifiers < 1).any() or (identifiers != np.floor(identifiers)).any():
                    errors.append(f'{name}: unit and cycle must be positive integer values')
                    continue
                if set(frame[0]) != set(range(1, 101)):
                    errors.append(f'{name}: expected 100 engines with unit IDs 1 through 100; found {frame[0].nunique()}')
                if frame.duplicated([0, 1]).any():
                    errors.append(f'{name}: duplicate unit/cycle rows')
                if any(not group[1].is_monotonic_increasing for _, group in frame.groupby(0)):
                    errors.append(f'{name}: cycles must increase within each engine')
        except (ValueError, OSError, pd.errors.ParserError) as error:
            errors.append(f'{name}: cannot parse numeric whitespace-separated data: {error}')
    if errors:
        return DataCheck(False, '\n'.join(errors))
    return DataCheck(True, 'FD001 format checks passed: 26-column train/test files, 100 engines each, 100 RUL rows.\n'
                     'Format validation does not certify dataset provenance; use the NASA files.')
