"""Cross-platform Makefile companion. All subprocesses use argument arrays."""
import argparse
import os
from pathlib import Path
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parents[1]
VENV = ROOT / '.venv'
VENV_PYTHON = VENV / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
FUTURE_TARGETS = ('gen-demo', 'ingest', 'train', 'eval-dev', 'eval-report', 'e2e', 'api', 'precompute')


def run(command):
    env = {**os.environ, 'PYTHONPATH': os.pathsep.join((str(ROOT), str(ROOT / 'src'))), 'PIP_NO_INDEX': '1', 'PIP_DISABLE_PIP_VERSION_CHECK': '1'}
    return subprocess.run(command, cwd=ROOT, env=env, check=False).returncode


def execute(target):
    python = str(VENV_PYTHON if VENV_PYTHON.exists() else Path(sys.executable))
    if target == 'setup':
        if not VENV_PYTHON.exists():
            venv.EnvBuilder(with_pip=True, system_site_packages=True).create(VENV)
        return run([str(VENV_PYTHON), '-m', 'pip', 'install', '--no-deps', '--no-build-isolation', '-e', '.'])
    if target == 'test':
        return run([python, '-m', 'pytest'])
    if target == 'data-check':
        return run([python, '-m', 'pdm.cli', 'data-check'])
    if target == 'config':
        return run([python, '-m', 'pdm.cli', 'config'])
    if target == 'train':
        return run([python, str(ROOT / 'scripts/train.py')])
    if target == 'gen-demo':
        return run([python, str(ROOT / 'scripts/gen_demo.py')])
    if target == 'gen-fleet':
        return run([python, str(ROOT / 'scripts/gen_fleet.py')])
    if target == 'whatif-demo':
        return run([python, str(ROOT / 'scripts/whatif_demo.py')])
    if target == 'validation':
        return run([python, str(ROOT / 'scripts/validation.py')])
    if target == 'ingest':
        return run([python, '-c', 'from pathlib import Path; from vayu.quality import ingest_pack; r=ingest_pack(Path("data/maintenance.db"), Path("data/demo")); print(f"Accepted {r.accepted_count}; quarantined {len(r.issues)}")'])
    if target in ('e2e','eval-dev','eval-report'):
        return run([python, str(ROOT / 'scripts/evaluate.py')])
    if target == 'app':
        return run([python, '-m', 'streamlit', 'run', str(ROOT / 'app.py')])
    if target == 'clean':
        # Only disposable bytecode in the project's own code directories.
        for directory in ('src', 'tests', 'scripts'):
            for cache in (ROOT / directory).rglob('*.pyc'):
                resolved = cache.resolve()
                if resolved.is_relative_to(ROOT) and resolved.parent.name == '__pycache__':
                    resolved.unlink()
        return 0
    print(f'{target}: superseded by the Vayu Sarthi revision. Use train, gen-demo, '
          'ingest, eval-report, e2e or app.', file=sys.stderr)
    return 2


def main():
    parser = argparse.ArgumentParser(description='Offline build tasks; Windows equivalent of make')
    parser.add_argument('targets', nargs='+', choices=('setup', 'test', 'data-check', 'config', 'clean', 'app', 'gen-fleet', 'whatif-demo', 'validation', *FUTURE_TARGETS))
    arguments = parser.parse_args()
    for target in arguments.targets:
        code = execute(target)
        if code:
            return code
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
