"""Publication checks for the privacy-corrected evidence package."""

import hashlib
import json
from pathlib import Path
import subprocess

from scripts.validation import preserve_v1_artifacts


ROOT = Path(__file__).resolve().parents[1]


def test_published_v1_archive_verifies_without_local_logs(tmp_path):
    """An installation need not ship private execution logs to verify v1."""
    ledger = json.loads((ROOT / 'artifacts/validation_v1/archive_manifest.json').read_bytes())
    published = ledger['files_sha256']
    assert published and all(not name.endswith('.log') for name in published)
    assert ledger['local_only_files_sha256']
    assert all(name.endswith('.log') for name in ledger['local_only_files_sha256'])
    archive = tmp_path / 'validation_v1'
    archive.mkdir()
    for name, digest in published.items():
        data = (ROOT / 'artifacts/validation_v1' / name).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
        destination = archive / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    (archive / 'archive_manifest.json').write_text(json.dumps(ledger), encoding='utf-8')
    assert preserve_v1_artifacts(tmp_path) == archive


def test_privacy_scrub_preserves_result_evidence():
    """Privacy packaging must preserve measured and simulated result bytes."""
    manifest = json.loads((ROOT / 'artifacts/privacy_scrub_manifest.json').read_bytes())
    assert manifest['result_files_sha256']
    for name, digest in manifest['result_files_sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest
    ledger = ROOT / manifest['updated_archive_ledger']['file']
    assert hashlib.sha256(ledger.read_bytes()).hexdigest() == manifest['updated_archive_ledger']['after_sha256']


def test_local_only_files_are_ignored(tmp_path):
    """Git's actual matching rules exclude local logs, sources and recovery data."""
    (tmp_path / '.gitignore').write_bytes((ROOT / '.gitignore').read_bytes())
    subprocess.run(['git', 'init', '--quiet'], cwd=tmp_path, check=True, capture_output=True)
    paths = [
        '.venv/file', '.checker-venv/file', '__pycache__/module.pyc',
        '.pytest_cache/file', '.tmp_pytest/file', 'artifacts/run.log',
        'artifacts/validation_v1/run.log', 'data/raw/train_FD001.txt',
        'data/CMAPSS/train_FD001.txt', 'artifacts/rul_model.joblib',
        '.local-history-backup/before-scrub.bundle', '.env', '.env.local',
        'private.key', 'wheelhouse/package.whl', 'checker-wheelhouse/package.whl',
        'research/private.md', 'CLAUDE.md', '.hyperresearch/local.db',
        'data/maintenance.db', 'artifacts/large.npz',
    ]
    result = subprocess.run(['git', 'check-ignore', '-z', '--stdin'], cwd=tmp_path,
                            input=('\0'.join(paths) + '\0').encode('utf-8'),
                            check=True, capture_output=True)
    assert result.stdout.decode('utf-8').rstrip('\0').split('\0') == paths
