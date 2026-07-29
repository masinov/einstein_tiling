import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_consolidation_catalog_is_complete_and_consistent():
    result = subprocess.run(
        [
            str(ROOT / "venv/bin/python"),
            str(ROOT / "scripts/check_consolidation_catalog.py"),
            "--skip-hashes",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert "goal-level claims" in result.stdout
    assert "file dispositions" in result.stdout
