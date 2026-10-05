from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_ground_truth_firewall():
    for directory in ('planner', 'policies'):
        for path in (ROOT / 'src/pdm' / directory).glob('*.py'):
            assert not re.search(r'scenario\.truth|failure_cycle|true_rul', path.read_text(encoding='utf-8'))


def test_claims_policy():
    paths = [ROOT / 'README.md'] + list((ROOT / 'ui').glob('*.html')) + list((ROOT / 'ui').glob('*.js'))
    runbook = ROOT / 'docs/DEMO_RUNBOOK.md'
    if runbook.exists():
        paths.append(runbook)
    for path in paths:
        assert not re.search(r'digital twin|real-time|live IoT|optimal|guarantee|no feasible plan exists', path.read_text(encoding='utf-8'), re.I)


def test_no_hardcoded_results():
    for path in [ROOT / 'README.md'] + list((ROOT / 'ui').glob('*.*')):
        assert not re.search(r'\d\s*%', path.read_text(encoding='utf-8'))


def test_spec_preserved_and_required_directories_exist():
    assert (ROOT / 'docs/SPEC.md').is_file()
    for relative in ('data/raw', 'data/processed', 'data/scenarios', 'data/demo', 'reports', 'ui/vendor'):
        assert (ROOT / relative).is_dir()
