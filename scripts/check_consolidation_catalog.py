#!/usr/bin/env python3
"""Validate consolidation registries, path coverage and artifact hashes."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "docs" / "consolidation"


def load(name: str) -> dict:
    return json.loads((CONTROL / name).read_text())


def repository_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return {line for line in result.stdout.splitlines() if line and (ROOT / line).is_file()}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def ledger_ids() -> set[str]:
    text = (ROOT / "docs/theory/PROOF_LEDGER.md").read_text()
    return {
        match.group(1).strip()
        for match in re.finditer(r"^\|\s*([^|]+?)\s*\|", text, re.MULTILINE)
        if match.group(1).strip() not in {"ID", "Result", "Obligation", "Target", "work"}
        and not set(match.group(1).strip()) <= {"-", ":"}
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-hashes", action="store_true", help="validate structure without rehashing evidence")
    args = parser.parse_args()

    claims = load("CLAIMS.json")
    rules = load("DISPOSITION_RULES.json")
    files = load("FILE_DISPOSITIONS.json")
    artifacts = load("ARTIFACTS.json")

    assert claims["schema_version"] == 1
    assert rules["schema_version"] == 1
    assert files["schema_version"] == 1
    assert artifacts["schema_version"] == 1

    claim_ids = [claim["id"] for claim in claims["claims"]]
    assert len(claim_ids) == len(set(claim_ids)), "duplicate claim ID"
    valid_statuses = set(claims["status_vocabulary"])
    valid_claim_dispositions = set(claims["disposition_vocabulary"])
    valid_goal_relations = set(claims["goal_relation_vocabulary"])
    known_ledger = ledger_ids()
    sources = json.loads((ROOT / "docs/literature/SOURCES.json").read_text())
    known_sources = {source["id"] for source in sources["sources"]}

    for claim in claims["claims"]:
        assert claim["status"] in valid_statuses, claim["id"]
        assert claim["disposition"] in valid_claim_dispositions, claim["id"]
        assert claim["goal_relation"] in valid_goal_relations, claim["id"]
        for dependency in claim["dependencies"]:
            assert dependency in claim_ids, (claim["id"], dependency)
        for ledger_id in claim["ledger_ids"]:
            assert ledger_id in known_ledger, (claim["id"], ledger_id)
        for relative in claim["source_documents"] + claim["artifact_paths"]:
            assert (ROOT / relative).is_file(), (claim["id"], relative)
        for source_id in claim["literature_source_ids"]:
            assert source_id in known_sources, (claim["id"], source_id)

    rule_dispositions = set(rules["dispositions"])
    for rule in rules["rules"]:
        assert rule["disposition"] in rule_dispositions, rule

    file_records = files["files"]
    file_paths = [record["path"] for record in file_records]
    assert len(file_paths) == len(set(file_paths)), "duplicate file disposition"
    expected = repository_files()
    actual = set(file_paths)
    assert actual == expected, {
        "missing": sorted(expected - actual),
        "stale": sorted(actual - expected),
    }
    for record in file_records:
        assert record["disposition"] in rule_dispositions, record["path"]
        if record.get("dynamic_generated_catalog"):
            assert record["size_bytes"] is None, record["path"]
        else:
            assert (ROOT / record["path"]).stat().st_size == record["size_bytes"], record["path"]

    artifact_records = artifacts["artifacts"]
    artifact_paths = [record["path"] for record in artifact_records]
    assert len(artifact_paths) == len(set(artifact_paths)), "duplicate artifact"
    for record in artifact_records:
        path = ROOT / record["path"]
        assert path.is_file(), record["path"]
        assert path.stat().st_size == record["size_bytes"], record["path"]
        assert record["path"] in actual, record["path"]
        if not args.skip_hashes:
            assert sha256(path) == record["sha256"], record["path"]

    summary = files["summary"]
    assert summary["file_count"] == len(file_records)
    assert summary["size_bytes"] == sum(record["size_bytes"] or 0 for record in file_records)
    assert artifacts["summary"]["tracked_or_nonignored_artifact_count"] == len(artifact_records)

    print(
        f"valid: {len(claim_ids)} goal-level claims, {len(file_records)} file dispositions, "
        f"{len(artifact_records)} hash-pinned artifacts, "
        f"{len(artifacts['ignored_research_stores'])} ignored research stores"
    )


if __name__ == "__main__":
    main()
