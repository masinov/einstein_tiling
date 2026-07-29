from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from einstein.repository import repository_root

from einstein.certificates import FAMILIES, resolve_callable, validate_registry


ROOT = repository_root(Path(__file__))


def test_retained_certificate_registry_is_complete_on_disk():
    validate_registry(ROOT)
    assert len(FAMILIES) == 18
    assert len({item.artifact for item in FAMILIES}) == len(FAMILIES)
    for item in FAMILIES:
        assert callable(resolve_callable(item.build.callable))
        assert callable(resolve_callable(item.verify.callable))


def test_certificate_cli_lists_describes_builds_and_verifies(tmp_path):
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

    output = tmp_path / "contact-kernel.json"
    built = subprocess.run(
        [
            str(ROOT / "venv/bin/python"),
            "scripts/certificates.py",
            "build",
            "contact-kernel",
            "--output",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "built contact-kernel" in built
    assert json.loads(output.read_text()) == json.loads(
        (ROOT / "data/sturmian-source/ahi-section10-contact-kernel.json").read_text()
    )

    verified = subprocess.run(
        [
            str(ROOT / "venv/bin/python"),
            "scripts/certificates.py",
            "verify",
            "contact-kernel",
            "--input",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    assert "verified contact-kernel" in verified


def test_archived_script_manifest_is_hash_pinned_and_parseable():
    manifest = json.loads((ROOT / "scripts/archive/MANIFEST.json").read_text())
    assert manifest["schema_version"] == 2
    assert manifest["script_count"] == 92
    migrated = 0
    for record in manifest["scripts"]:
        assert not (ROOT / record["old_path"]).exists()
        archived = ROOT / record["new_path"]
        assert archived.is_file()
        assert hashlib.sha256(archived.read_bytes()).hexdigest() == record[
            "sha256_archived"
        ]
        if "sha256_before_namespace_migration" in record:
            migrated += 1
            assert record["sha256_before_namespace_migration"] != record[
                "sha256_archived"
            ]
        compile(archived.read_text(), str(archived), "exec")
    assert migrated == 87
