from pathlib import Path

import pytest

from pdm.data.check import check_data


def write_fixture(directory: Path):
    # A format fixture only; never used as benchmark or model training data.
    rows = ''.join(' '.join(map(str, [unit, 1] + [0.0] * 24)) + '   \n' for unit in range(1, 101))
    for name in ('train_FD001.txt', 'test_FD001.txt'):
        (directory / name).write_text(rows, encoding='utf-8')
    (directory / 'RUL_FD001.txt').write_text('10\n' * 100, encoding='utf-8')


def test_missing_files_report_download_instruction(tmp_path):
    result = check_data(tmp_path)
    assert not result.ok
    assert 'NASA' in result.message
    assert all(name in result.message for name in ('train_FD001.txt', 'test_FD001.txt', 'RUL_FD001.txt'))


def test_valid_format_and_trailing_whitespace(tmp_path):
    write_fixture(tmp_path)
    assert check_data(tmp_path).ok


@pytest.mark.parametrize('filename,content,reason', [
    ('train_FD001.txt', '1 1 0\n', '26 columns'),
    ('test_FD001.txt', ' '.join(['1', '1'] + ['0'] * 24) + '\n', '100 engines'),
    ('RUL_FD001.txt', '1\n', '100 rows'),
    ('RUL_FD001.txt', '-1\n' * 100, 'non-negative'),
    ('RUL_FD001.txt', 'nan\n' * 100, 'finite'),
    ('RUL_FD001.txt', '1 2\n' * 100, 'one column'),
    ('train_FD001.txt', ' '.join(['1.5', '1'] + ['0'] * 24) + '\n', 'integer'),
])
def test_invalid_data(tmp_path, filename, content, reason):
    write_fixture(tmp_path)
    (tmp_path / filename).write_text(content, encoding='utf-8')
    result = check_data(tmp_path)
    assert not result.ok
    assert reason in result.message


def test_duplicate_unit_cycle_rejected(tmp_path):
    write_fixture(tmp_path)
    path = tmp_path / 'train_FD001.txt'
    contents = path.read_text(encoding='utf-8')
    path.write_text(contents + contents.splitlines()[0] + '\n', encoding='utf-8')
    assert 'duplicate' in check_data(tmp_path).message
