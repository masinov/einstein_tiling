import subprocess
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))


def test_consolidation_catalog_is_complete_and_consistent():
    result = subprocess.run(
        [
            str(ROOT / "venv/bin/python"),
            str(ROOT / "scripts/maintenance/check_catalog.py"),
            "--skip-hashes",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "goal-level claims" in result.stdout
    assert "file dispositions" in result.stdout
