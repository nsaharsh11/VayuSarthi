"""Fictional pack, invalid row quarantine and SQLite idempotence."""
from pathlib import Path
import sqlite3

import pandas as pd
import pytest

from vayu.sim import generate_pack
from vayu.quality import read_pack, ingest_pack


@pytest.fixture
def pack(tmp_path):
    root = Path(__file__).resolve().parents[1]
    oof = pd.read_csv(root/'data/processed/oof_predictions.csv')
    generate_pack(oof, tmp_path, seed=31)
    return tmp_path


def test_pack_generation_byte_identical(pack, tmp_path):
    root = Path(__file__).resolve().parents[1]
    other = tmp_path/'other'
    generate_pack(pd.read_csv(root/'data/processed/oof_predictions.csv'), other, seed=31)
    for path in pack.glob('*.csv'):
        assert path.read_bytes() == (other/path.name).read_bytes()
    for name in ('manifest.json', 'simulation_truth.json'):
        assert (pack/name).read_bytes() == (other/name).read_bytes()


def test_clean_pack_and_idempotent_sqlite(pack):
    report = read_pack(pack)
    assert not report.issues and len(report.state.tails) == 6
    database = pack/'test.db'
    first, second = ingest_pack(database, pack), ingest_pack(database, pack)
    assert first.inputs_hash == second.inputs_hash
    with sqlite3.connect(database) as connection:
        assert connection.execute('SELECT count(*) FROM ingest_runs').fetchone()[0] == 1
        assert connection.execute('SELECT count(*) FROM accepted_rows').fetchone()[0] == first.accepted_count


@pytest.mark.parametrize('source,column,value', [('fleet.csv','rate',-1), ('fleet.csv','lower',999),
    ('fleet.csv','duration',1.5), ('spares.csv','available_day',-1),
    ('resources.csv','free_day',1.5), ('health_stream.csv','point',float('inf'))])
def test_invalid_rows_quarantined(pack, source, column, value):
    frame = pd.read_csv(pack/source)
    frame[column] = frame[column].astype(object)
    frame.loc[0,column] = value
    frame.to_csv(pack/source,index=False)
    report = ingest_pack(pack/'invalid.db', pack)
    assert report.issues
    assert any(issue.source == source for issue in report.issues)
    with sqlite3.connect(pack/'invalid.db') as connection:
        assert connection.execute('SELECT count(*) FROM quarantine').fetchone()[0] == len(report.issues)


def test_conflicting_duplicate_tail_rejects_both(pack):
    frame = pd.read_csv(pack/'fleet.csv')
    pd.concat([frame,frame.iloc[[0]]]).to_csv(pack/'fleet.csv',index=False)
    report = read_pack(pack)
    assert sum(issue.reason == 'DUPLICATE_ID' for issue in report.issues) == 2
    assert frame.iloc[0].tail_id not in {t.tail_id for t in report.state.tails}


def test_missing_source_and_firewall(pack):
    (pack/'spares.csv').unlink()
    report = read_pack(pack)
    assert any(issue.reason == 'MISSING_SOURCE' for issue in report.issues)
    assert report.state.spares == ()
    (pack/'simulation_truth.json').write_text('BROKEN')
    assert read_pack(pack).state == report.state


def test_generator_invalid_input(pack):
    with pytest.raises(ValueError):
        generate_pack(pd.DataFrame(),pack,seed=1)
