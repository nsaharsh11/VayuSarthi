"""Four-silo fictional pack schema, quality and planning-hold contracts."""
from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError

from vayu.quality import read_fleet_pack, validate_fleet_pack
from vayu.schemas import FLEET_SCHEMAS
from vayu.sim import generate_fleet_pack


@pytest.fixture
def pack(tmp_path: Path) -> dict[str, pd.DataFrame]:
    """Load a generated, clean day-14 fictional pack."""
    generate_fleet_pack(tmp_path, seed=49, today=14)
    return {name: pd.read_csv(tmp_path / name) for name in FLEET_SCHEMAS}


def test_clean_and_reproducible(tmp_path: Path) -> None:
    first, second = tmp_path / 'a', tmp_path / 'b'
    generate_fleet_pack(first, seed=49, today=14)
    generate_fleet_pack(second, seed=49, today=14)
    assert {p.name: p.read_bytes() for p in first.iterdir()} == {
        p.name: p.read_bytes() for p in second.iterdir()}
    report = read_fleet_pack(first, today=14)
    assert not report.planning_hold and not report.reasons
    assert report.quarantine.empty
    assert len(report.frames['tails.csv']) == 10
    assert list(report.frames['tails.csv'].tail_id) == [f'T-{i:02d}' for i in range(1, 11)]
    assert report.frames['tails.csv'].utilisation_cycles_per_day.between(1.5, 3).all()
    assert len(report.frames['spares.csv']) == 3
    assert dict(zip(report.frames['resources.csv'].resource,
                    report.frames['resources.csv']['count'])) == {'bay': 2, 'crew': 1}
    assert all(set(frame.quality_badge) == {'Good'} for frame in report.frames.values())
    assert 'Fictional' in (first / 'manifest.json').read_text()


@pytest.mark.parametrize(('source', 'field', 'bad'), [
    ('tails.csv', 'utilisation_cycles_per_day', 1.49),
    ('tails.csv', 'utilisation_cycles_per_day', 3.01),
    ('tails.csv', 'utilisation_cycles_per_day', float('inf')),
    ('tech_records.csv', 'cycles_since_overhaul', -1),
    ('tech_records.csv', 'open_snags', 1.5),
    ('health.csv', 'last_update_day', -1),
    ('spares.csv', 'available_day', -1),
    ('resources.csv', 'count', -1),
    ('resources.csv', 'shift_hours', 25),
])
def test_csv_schemas(pack: dict[str, pd.DataFrame], source: str, field: str, bad: object) -> None:
    row = pack[source].iloc[0].to_dict()
    row[field] = bad
    with pytest.raises(ValidationError):
        FLEET_SCHEMAS[source].model_validate(row)


def test_corrupt_tail_is_quarantined_and_holds(pack: dict[str, pd.DataFrame]) -> None:
    pack['tails.csv'].loc[0, 'utilisation_cycles_per_day'] = 99
    result = validate_fleet_pack(pack, today=14)
    assert result.planning_hold
    assert any('T-01' in reason for reason in result.reasons)
    assert 'T-01' not in set(result.accepted['tails.csv'].tail_id)
    assert (result.frames['tails.csv'].iloc[0].quality_badge == 'Conflict')
    assert ((result.quarantine.source == 'tails.csv') &
            (result.quarantine.row_number == 2)).any()


@pytest.mark.parametrize('source', list(FLEET_SCHEMAS))
def test_missing_columns_and_duplicates(pack: dict[str, pd.DataFrame], source: str) -> None:
    duplicate = {name: frame.copy() for name, frame in pack.items()}
    duplicate[source] = pd.concat([duplicate[source], duplicate[source].iloc[[0]]], ignore_index=True)
    result = validate_fleet_pack(duplicate, today=14)
    rejected = result.quarantine[result.quarantine.source == source]
    assert len(rejected) >= 2
    assert rejected.reason.str.contains('DUPLICATE_ID').all()
    pack[source] = pack[source].drop(columns=pack[source].columns[-1])
    result = validate_fleet_pack(pack, today=14)
    assert (result.quarantine.source == source).any()
    assert result.planning_hold


def test_stale_boundary_is_soft(pack: dict[str, pd.DataFrame]) -> None:
    pack['health.csv'].loc[0, 'last_update_day'] = 7
    pack['health.csv'].loc[1, 'last_update_day'] = 6
    result = validate_fleet_pack(pack, today=14)
    assert list(result.frames['health.csv'].quality_badge[:2]) == ['Good', 'Stale']
    assert list(result.frames['tails.csv'].quality_badge[:2]) == ['Good', 'Stale']
    assert result.quarantine.empty and not result.planning_hold


def test_orphan_and_missing_links_hold(pack: dict[str, pd.DataFrame]) -> None:
    pack['tech_records.csv'].loc[0, 'tail_id'] = 'T-99'
    result = validate_fleet_pack(pack, today=14)
    assert result.planning_hold
    assert result.quarantine.reason.str.contains('SILO_CONFLICT').any()
    assert any('T-99' in reason for reason in result.reasons)
    assert 'T-01' not in set(result.accepted['tails.csv'].tail_id)


def test_future_health_and_duplicate_engine_hold(pack: dict[str, pd.DataFrame]) -> None:
    pack['health.csv'].loc[0, 'last_update_day'] = 15
    assert validate_fleet_pack(pack, today=14).planning_hold
    pack['tails.csv'].loc[1, 'engine_id'] = pack['tails.csv'].loc[0, 'engine_id']
    result = validate_fleet_pack(pack, today=14)
    assert result.frames['tails.csv'].quality_badge[:2].eq('Conflict').all()


def test_missing_file_empty_pack_and_no_input_mutation(tmp_path: Path,
                                                     pack: dict[str, pd.DataFrame]) -> None:
    before = {name: frame.copy(deep=True) for name, frame in pack.items()}
    validate_fleet_pack(pack, today=14)
    for name in pack:
        pd.testing.assert_frame_equal(pack[name], before[name])
    generate_fleet_pack(tmp_path, today=14)
    (tmp_path / 'health.csv').unlink()
    result = read_fleet_pack(tmp_path, today=14)
    assert result.planning_hold and any('health.csv' in reason for reason in result.reasons)
    assert validate_fleet_pack({}, today=14).planning_hold
    empty = {name: frame.iloc[:0] for name, frame in pack.items()}
    assert validate_fleet_pack(empty, today=14).planning_hold


def test_required_tail_scope_and_argument_checks(pack: dict[str, pd.DataFrame]) -> None:
    pack['tails.csv'].loc[0, 'utilisation_cycles_per_day'] = 99
    assert not validate_fleet_pack(pack, today=14, required_tail_ids=('T-02',)).planning_hold
    assert validate_fleet_pack(pack, today=14, required_tail_ids=('T-99',)).planning_hold
    with pytest.raises(ValueError):
        validate_fleet_pack(pack, today=-1)
    with pytest.raises(ValueError):
        generate_fleet_pack(Path('.'), today=-1)


def test_disk_corrupted_copy_and_committed_pack(tmp_path: Path) -> None:
    """The committed fixture passes; a separate corrupted CSV copy holds."""
    committed = Path(__file__).resolve().parents[1] / 'data' / 'fleet'
    assert not read_fleet_pack(committed).planning_hold
    generate_fleet_pack(tmp_path)
    frame = pd.read_csv(tmp_path / 'tech_records.csv')
    frame.loc[0, 'tail_id'] = 'T-99'
    frame.to_csv(tmp_path / 'tech_records.csv', index=False)
    result = read_fleet_pack(tmp_path)
    assert result.planning_hold and not result.quarantine.empty
    assert result.frames['tech_records.csv'].iloc[0].quality_badge == 'Conflict'


def test_unreadable_and_nullable_records(tmp_path: Path,
                                        pack: dict[str, pd.DataFrame]) -> None:
    """Unreadable files and pandas nullable cells retain useful evidence."""
    generate_fleet_pack(tmp_path)
    (tmp_path / 'tails.csv').write_text('tail_id,engine_id\n"unclosed', encoding='utf-8')
    result = read_fleet_pack(tmp_path)
    assert result.planning_hold
    assert any(issue.reason == 'BAD_CSV' for issue in result.issues)
    pack['tails.csv']['engine_id'] = pack['tails.csv']['engine_id'].astype('string')
    pack['tails.csv'].loc[0, 'engine_id'] = pd.NA
    result = validate_fleet_pack(pack, today=14)
    assert result.planning_hold
    assert 'null' in result.quarantine.iloc[0].raw_json
