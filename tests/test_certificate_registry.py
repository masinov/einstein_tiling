from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from einstein.certificates import FAMILIES, validate_registry


ROOT = Path(__file__).resolve().parents[1]


def test_retained_certificate_registry_is_complete_on_disk():
    validate_registry(ROOT)
    assert len(FAMILIES) == 18
    assert len({item.artifact for item in FAMILIES}) == len(FAMILIES)


def test_certificate_cli_lists_and_describes_without_running_builders():
    listed = subprocess.run(
        [str(ROOT / "venv/bin/python"), "scripts/certificates.py", "list"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "source-atlas" in listed
    assert "stade-physical-contacts" in listed

    described = subprocess.run(
        [
            str(ROOT / "venv/bin/python"),
            "scripts/certificates.py",
            "describe",
            "contact-kernel",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert json.loads(described)["artifact"].endswith("contact-kernel.json")

    dry_run = subprocess.run(
        [
            str(ROOT / "venv/bin/python"),
            "scripts/certificates.py",
            "run",
            "contact-kernel",
            "verify",
            "--dry-run",
            "--",
            "ATLAS",
            "KERNEL",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "verify_sturmian_contact_kernel.py ATLAS KERNEL" in dry_run


def test_archived_script_manifest_is_hash_pinned_and_parseable():
    manifest = json.loads((ROOT / "scripts/archive/MANIFEST.json").read_text())
    assert manifest["script_count"] == 92
    for record in manifest["scripts"]:
        assert not (ROOT / record["old_path"]).exists()
        archived = ROOT / record["new_path"]
        assert archived.is_file()
        assert hashlib.sha256(archived.read_bytes()).hexdigest() == record[
            "sha256_archived"
        ]
        compile(archived.read_text(), str(archived), "exec")
