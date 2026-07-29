"""Build deterministic non-destructive consolidation inventories.

This is repository-maintenance tooling, not a research runner.  It reads Git's
tracked/untracked file view, applies the explicit disposition rules, hashes
versioned evidence, and summarizes ignored research stores.  It never mutates
research data or moves a file.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
CONTROL = ROOT / "docs" / "consolidation"
RULES_PATH = CONTROL / "DISPOSITION_RULES.json"
FILE_OUTPUT = CONTROL / "FILE_DISPOSITIONS.json"
ARTIFACT_OUTPUT = CONTROL / "ARTIFACTS.json"

ARTIFACT_ROOTS = (
    "docs/notebook/assets/",
    "data/sturmian-source/",
    "docs/literature/anchors/",
)
ARTIFACT_FILES = {"tests/fixtures/polykites-n8.sqlite"}
REFERENCE_ROOTS = ("docs/", "scripts/", "src/", "tests/")
IGNORED_RESEARCH_ROOTS = (
    "data/a0-compiled",
    "data/a1-compiled",
    "data/a2-compiled",
    "data/literature",
    "data/w3-frontiers",
    "docs/notebook/assets",
    "spectre.tar.gz",
)


def git_lines(*args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def repository_files() -> list[str]:
    paths = git_lines("ls-files", "--cached", "--others", "--exclude-standard")
    return sorted(set(paths))


def tracked_files() -> set[str]:
    return set(git_lines("ls-files"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def line_count(path: Path) -> int | None:
    try:
        with path.open("rb") as handle:
            return sum(block.count(b"\n") for block in iter(lambda: handle.read(1024 * 1024), b""))
    except (OSError, UnicodeError):
        return None


def apply_rule(path: str, rules: list[dict]) -> dict:
    for index, rule in enumerate(rules):
        if fnmatch.fnmatchcase(path, rule["glob"]):
            return {
                "rule_index": index,
                "rule_glob": rule["glob"],
                "category": rule["category"],
                "disposition": rule["disposition"],
                "rationale": rule["rationale"],
            }
    raise AssertionError(f"No disposition rule matched {path}")


def build_file_dispositions() -> tuple[dict, dict[str, dict]]:
    rules_document = json.loads(RULES_PATH.read_text())
    rules = rules_document["rules"]
    tracked = tracked_files()
    records: list[dict] = []
    dispositions: Counter[str] = Counter()
    categories: Counter[str] = Counter()

    for relative in repository_files():
        path = ROOT / relative
        if not path.is_file():
            continue
        applied = apply_rule(relative, rules)
        generated_catalog = relative in {
            str(FILE_OUTPUT.relative_to(ROOT)),
            str(ARTIFACT_OUTPUT.relative_to(ROOT)),
        }
        record = {
            "path": relative,
            "tracked": relative in tracked,
            "size_bytes": None if generated_catalog else path.stat().st_size,
            **applied,
        }
        if generated_catalog:
            record["dynamic_generated_catalog"] = True
        elif path.suffix.lower() in {".py", ".md", ".json", ".toml", ".txt", ".yml", ".yaml"}:
            record["line_count"] = line_count(path)
        records.append(record)
        dispositions[record["disposition"]] += 1
        categories[record["category"]] += 1

    document = {
        "schema_version": 1,
        "snapshot_date": date.today().isoformat(),
        "generated_by": "scripts/maintenance/build_catalog.py",
        "source_rules": "docs/consolidation/DISPOSITION_RULES.json",
        "semantics": "Non-destructive per-file planning map. A disposition does not authorize moving or deleting the file.",
        "summary": {
            "file_count": len(records),
            "tracked_file_count": sum(record["tracked"] for record in records),
            "untracked_nonignored_file_count": sum(not record["tracked"] for record in records),
            "size_bytes": sum(record["size_bytes"] or 0 for record in records),
            "dynamic_generated_catalog_count": sum(
                bool(record.get("dynamic_generated_catalog")) for record in records
            ),
            "by_disposition": dict(sorted(dispositions.items())),
            "by_category": dict(sorted(categories.items())),
        },
        "files": records,
    }
    by_path = {record["path"]: record for record in records}
    return document, by_path


def reference_text(files: list[str]) -> str:
    chunks: list[str] = []
    for relative in files:
        if not relative.startswith(REFERENCE_ROOTS):
            continue
        path = ROOT / relative
        if not path.is_file() or path.stat().st_size > 5 * 1024 * 1024:
            continue
        try:
            chunks.append(path.read_text(errors="strict"))
        except (OSError, UnicodeError):
            continue
    return "\n".join(chunks)


def artifact_kind(relative: str) -> str:
    name = Path(relative).name
    suffix = Path(relative).suffix.lower()
    if relative == "tests/fixtures/polykites-n8.sqlite":
        return "database-fixture"
    if relative.startswith("data/sturmian-source/"):
        return "source-reconstruction-certificate"
    if relative.startswith("docs/literature/anchors/"):
        return "literature-anchor"
    if "drat" in relative.lower():
        return "sat-proof-payload"
    if suffix == ".smt2":
        return "solver-formula"
    if suffix == ".json":
        return "certificate-or-result"
    if suffix in {".svg", ".png"}:
        return "visualization"
    if suffix == ".md":
        return "artifact-policy"
    return "research-artifact"


def ignored_group(relative: str) -> str:
    if relative.startswith("docs/notebook/assets/"):
        remainder = relative.removeprefix("docs/notebook/assets/")
        first = remainder.split("/", 1)[0]
        return f"docs/notebook/assets/{first}" if "/" in remainder else "docs/notebook/assets/ignored-loose-files"
    for root in IGNORED_RESEARCH_ROOTS:
        if relative == root or relative.startswith(root + "/"):
            return root
    return "other"


def ignored_research_files() -> list[str]:
    command = ["ls-files", "--others", "--ignored", "--exclude-standard", "--", *IGNORED_RESEARCH_ROOTS]
    return sorted(set(git_lines(*command)))


def build_artifacts(dispositions: dict[str, dict]) -> dict:
    tracked = tracked_files()
    repo_files = repository_files()
    artifact_paths = [
        relative
        for relative in repo_files
        if relative in ARTIFACT_FILES or relative.startswith(ARTIFACT_ROOTS)
    ]
    corpus = reference_text(repo_files)
    records: list[dict] = []
    kinds: Counter[str] = Counter()
    lifecycle: Counter[str] = Counter()

    for relative in artifact_paths:
        path = ROOT / relative
        if not path.is_file():
            continue
        disposition = dispositions[relative]
        kind = artifact_kind(relative)
        record = {
            "path": relative,
            "tracked": relative in tracked,
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "kind": kind,
            "disposition": disposition["disposition"],
            "category": disposition["category"],
            "reference_count": corpus.count(relative) + corpus.count(Path(relative).name),
        }
        records.append(record)
        kinds[kind] += 1
        lifecycle[record["disposition"]] += 1

    groups: dict[str, dict] = defaultdict(lambda: {"file_count": 0, "size_bytes": 0, "examples": []})
    for relative in ignored_research_files():
        path = ROOT / relative
        if not path.is_file():
            continue
        group = ignored_group(relative)
        entry = groups[group]
        entry["file_count"] += 1
        entry["size_bytes"] += path.stat().st_size
        if len(entry["examples"]) < 5:
            entry["examples"].append(relative)

    ignored_groups = []
    for group, entry in sorted(groups.items()):
        if group in {"data/literature", "spectre.tar.gz"}:
            disposition = "source-cache"
        else:
            disposition = "generated-cache" if group.startswith("data/a") or group == "data/w3-frontiers" else "externalize-after-manifest"
        ignored_groups.append({"group": group, "tracked": False, "disposition": disposition, **entry})

    return {
        "schema_version": 1,
        "snapshot_date": date.today().isoformat(),
        "generated_by": "scripts/maintenance/build_catalog.py",
        "semantics": "Tracked evidence is hash-pinned individually. Ignored stores are storage inventories only and are not promoted to mathematical evidence.",
        "summary": {
            "tracked_or_nonignored_artifact_count": len(records),
            "tracked_or_nonignored_size_bytes": sum(record["size_bytes"] for record in records),
            "ignored_group_count": len(ignored_groups),
            "ignored_file_count": sum(group["file_count"] for group in ignored_groups),
            "ignored_size_bytes": sum(group["size_bytes"] for group in ignored_groups),
            "by_kind": dict(sorted(kinds.items())),
            "by_disposition": dict(sorted(lifecycle.items())),
        },
        "artifacts": records,
        "ignored_research_stores": ignored_groups,
    }


def write_json(path: Path, document: dict) -> None:
    path.write_text(json.dumps(document, indent=2, sort_keys=False) + "\n")


def main() -> None:
    file_document, dispositions = build_file_dispositions()
    write_json(FILE_OUTPUT, file_document)
    artifact_document = build_artifacts(dispositions)
    write_json(ARTIFACT_OUTPUT, artifact_document)
    print(
        f"wrote {FILE_OUTPUT.relative_to(ROOT)} ({file_document['summary']['file_count']} files)\n"
        f"wrote {ARTIFACT_OUTPUT.relative_to(ROOT)} "
        f"({artifact_document['summary']['tracked_or_nonignored_artifact_count']} artifacts, "
        f"{artifact_document['summary']['ignored_group_count']} ignored groups)"
    )
