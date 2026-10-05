"""Direct script entry point, usable before editable installation."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from pdm.cli import main

if __name__ == '__main__':
    raise SystemExit(main(['data-check', *sys.argv[1:]]))
