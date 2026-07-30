"""Mechanical checks for research admission and historical correction policy."""

import importlib.util
import json
from pathlib import Path
import subprocess

from einstein.repository import repository_root
from einstein.repository.research import (
    sha256_file,
    validate_research_proposal,
    validate_run_manifest,
)


ROOT = repository_root(Path(__file__))


def load_gate_module():
    path = ROOT / "scripts" / "check_experiment_gate.py"
    spec = importlib.util.spec_from_file_location("check_experiment_gate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


def build_admitted_experiment(root: Path) -> tuple[Path, Path]:
    write_json(
        root / "docs/research/portfolio.json",
        {"programs": [{"id": "CERTIFIED-DISCOVERY-METHODS"}]},
    )
    write_json(
        root / "docs/literature/SOURCES.json",
        {"sources": [{"id": "kaplan-8kites-2023"}]},
    )
    files = {
        "scripts/example.py": b"print('control')\n",
        "scripts/run_research.py": b"# pinned supervisor control\n",
        "src/einstein/repository/research.py": b"# pinned gate control\n",
        "pyproject.toml": b"[project]\nname='control'\n",
        "venv/bin/python": b"pinned executable placeholder\n",
        "scripts/verify_example.py": b"def verify(): return True\n",
    }
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    proposal = {
        "schema_version": 2,
        "id": "RP-2026-07-30-CROSSWALK",
        "title": "Exact coordinate crosswalk control",
        "kind": "experiment",
        "status": "ready",
        "program_id": "CERTIFIED-DISCOVERY-METHODS",
        "scope_level": "recognized-mathematical-family",
        "thesis": "A fixed source corpus may admit an exact canonical coordinate bijection.",
        "mission_connection": "The comparison tests exact identity machinery before future discovery use.",
        "alternatives_considered": "Aggregate equality cannot identify shape-level semantic mismatches.",
        "failure_or_pivot": "Any unmatched shape blocks equivalence and redirects work to semantics diagnosis.",
        "prior_art": {
            "snapshot_date": "2026-07-30",
            "primary_sources": ["kaplan-8kites-2023"],
            "non_redundancy": "Published aggregates do not provide this coordinate-level bijection.",
            "user_facts_resolved": [],
        },
        "outcomes": [
            {
                "result": "Every source shape has one exact canonical repository mate.",
                "action": "Retain the mapping as a finite control and close this comparison.",
            },
            {
                "result": "At least one source shape is absent, duplicated, or mismatched.",
                "action": "Block equivalence and diagnose coordinate semantics before reuse.",
            },
        ],
        "stop_rule": {
            "condition": "Process each member of the fixed corpus exactly once and then stop.",
            "no_automatic_escalation": True,
        },
        "experiment": {
            "proposition": "Decide whether the fixed corpora have an exact canonical bijection.",
            "command": ["venv/bin/python", "scripts/example.py"],
            "budget": {
                "wall_time_seconds": 60,
                "memory_bytes": 1024**3,
                "max_new_artifact_bytes": 1024,
                "artifact_roots": ["data/example-results"],
                "external_supervision": True,
            },
            "reproducibility": {
                "code_revision": "0" * 40,
                "require_clean_tree": True,
                "code_paths": [
                    "scripts/example.py",
                    "scripts/run_research.py",
                    "src/einstein/repository/research.py",
                ],
                "inputs": [],
                "no_external_inputs_reason": "This deterministic control constructs all records internally.",
                "environment_files": [
                    {
                        "path": "pyproject.toml",
                        "sha256": sha256_file(root / "pyproject.toml"),
                    }
                ],
                "executables": [
                    {
                        "path": "venv/bin/python",
                        "sha256": sha256_file(root / "venv/bin/python"),
                        "version_command": ["venv/bin/python", "--version"],
                        "version_output_sha256": "1" * 64,
                    }
                ],
            },
            "evidence": {
                "certificate_or_verifier": "A deterministic table is checked by the pinned exact verifier.",
                "promotion_boundary": "Passing validates identity machinery but establishes no tile novelty.",
                "verifier": {
                    "path": "scripts/verify_example.py",
                    "sha256": sha256_file(root / "scripts/verify_example.py"),
                },
            },
            "run_record": {
                "manifest_path": "data/example-results/manifest.json",
                "stdout_path": "data/example-results/stdout.log",
                "stderr_path": "data/example-results/stderr.log",
            },
        },
    }
    proposal_path = root / "docs/research/proposals/RP-2026-07-30-CROSSWALK.json"
    write_json(proposal_path, proposal)
    admission = {
        "schema_version": 1,
        "proposal_id": proposal["id"],
        "proposal_path": proposal_path.relative_to(root).as_posix(),
        "proposal_sha256": sha256_file(proposal_path),
        "status": "active",
        "admitted_by": "human:repository-owner",
        "authorization_ref": "Explicit authorization recorded in the governing user conversation.",
        "authorized_scope": "Run this exact finite crosswalk once under its declared resource limits.",
        "admitted_at": "2026-07-30T12:00:00Z",
    }
    admission_path = root / f"docs/research/admissions/{proposal['id']}.json"
    write_json(admission_path, admission)
    return proposal_path, admission_path


def test_agent_instructions_separate_research_from_maintenance():
    instructions = (ROOT / "CLAUDE.md").read_text()
    assert "No nontrivial experiment without external admission" in instructions
    assert "Repository maintenance and consolidation" in instructions
    assert "Do not create a numbered" in instructions
    assert "three-session checkpoint cadence is retired" in instructions
    assert "User-supplied" in instructions and "halt conditions" in instructions
    assert "scripts/run_research.py" in instructions
    assert "Externally supervise native solvers" in instructions
    assert "Promotion is a separate boundary" in instructions


def test_retired_checkpoint_record_remains_intact():
    data = json.loads((ROOT / "docs/HUMAN_CHECKPOINTS.json").read_text())
    assert data["schema_version"] == 1
    assert data["latest"]["id"] == "HC-2026-07-29-51"
    assert data["latest"]["through_session"] == 199


def test_stm1_source_correction_is_fail_closed():
    errata = (ROOT / "docs/program/ERRATA.md").read_text()
    ledger = (ROOT / "docs/theory/reference/proof_ledger.md").read_text()
    for identifier in (
        "ERR-006", "ERR-007", "ERR-008", "ERR-009", "ERR-010", "ERR-011",
        "ERR-012", "ERR-013", "ERR-016", "ERR-017",
    ):
        assert identifier in errata
    assert "12S+6M+6L" in errata
    assert "exact support/SAB specialization; all-tilings equivalence remains proof-draft" in ledger
    assert "extensional finite atlas machine-verified; total decoder proof-draft" in ledger
    assert "information redistribution, not state minimization" in ledger
    assert "blocked/frozen after HC-09" in ledger
    assert "primary archive contains Illustrator figures" in ledger


def test_ready_proposal_requires_separate_matching_admission(tmp_path):
    proposal, admission = build_admitted_experiment(tmp_path)
    errors = validate_research_proposal(
        proposal,
        root=tmp_path,
        require_admitted=True,
        require_experiment=True,
        admission_path=admission,
    )
    assert errors == []

    document = json.loads(proposal.read_text())
    document["thesis"] += " Edited after authorization."
    write_json(proposal, document)
    errors = validate_research_proposal(
        proposal,
        root=tmp_path,
        require_admitted=True,
        require_experiment=True,
        admission_path=admission,
    )
    assert any("hash no longer matches" in error for error in errors)


def test_agent_cannot_self_admit_by_changing_status(tmp_path):
    proposal, admission = build_admitted_experiment(tmp_path)
    document = json.loads(proposal.read_text())
    document["status"] = "admitted"
    write_json(proposal, document)
    admission.unlink()
    errors = validate_research_proposal(
        proposal, root=tmp_path, require_admitted=True, require_experiment=True
    )
    assert any("status must be one of" in error for error in errors)
    assert any("status must be ready" in error for error in errors)


def test_primary_sources_must_exist_in_catalog(tmp_path):
    proposal, admission = build_admitted_experiment(tmp_path)
    document = json.loads(proposal.read_text())
    document["prior_art"]["primary_sources"] = ["invented-source-id"]
    write_json(proposal, document)
    errors = validate_research_proposal(
        proposal,
        root=tmp_path,
        require_admitted=True,
        require_experiment=True,
        admission_path=admission,
    )
    assert any("unknown source IDs" in error for error in errors)


def test_public_gate_rejects_unadmitted_templates():
    gate = load_gate_module()
    template = ROOT / "docs/research/proposals/TEMPLATE.json"
    errors = gate.validate(template)
    assert errors
    assert any("admission" in error or "status" in error for error in errors)


def test_run_manifest_cold_verifier_pins_contract_limits_and_logs(tmp_path):
    proposal_path, admission_path = build_admitted_experiment(tmp_path)
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        [
            "git", "-c", "user.name=Control", "-c", "user.email=control@example.invalid",
            "commit", "-qm", "control",
        ],
        cwd=tmp_path,
        check=True,
    )
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    result_root = tmp_path / "data/example-results"
    result_root.mkdir(parents=True)
    stdout = result_root / "stdout.log"
    stderr = result_root / "stderr.log"
    stdout.write_text("exact control output\n")
    stderr.write_text("")
    manifest_path = result_root / "manifest.json"
    manifest = {
        "schema_version": 1,
        "proposal_id": "RP-2026-07-30-CROSSWALK",
        "proposal_path": proposal_path.relative_to(tmp_path).as_posix(),
        "proposal_sha256": sha256_file(proposal_path),
        "admission_path": admission_path.relative_to(tmp_path).as_posix(),
        "admission_sha256": sha256_file(admission_path),
        "pinned_code_revision": "0" * 40,
        "launch_head_revision": revision,
        "command": ["venv/bin/python", "scripts/example.py"],
        "started_at": "2026-07-30T12:00:00Z",
        "finished_at": "2026-07-30T12:00:01Z",
        "elapsed_seconds": 1.0,
        "limits": {
            "wall_time_seconds": 60,
            "memory_bytes": 1024**3,
            "max_new_artifact_bytes": 1024,
        },
        "artifact_bytes": {
            "baseline": {"data/example-results": 0},
            "final_before_manifest": {"data/example-results": 21},
            "final_growth": 21,
            "peak_observed_growth": 21,
            "poll_seconds": 0.25,
        },
        "stdout_path": "data/example-results/stdout.log",
        "stdout_sha256": sha256_file(stdout),
        "stderr_path": "data/example-results/stderr.log",
        "stderr_sha256": sha256_file(stderr),
        "process_return_code": 0,
        "execution_status": "completed",
        "research_verdict": None,
        "supervisor_error": None,
        "interpretation": "Execution completion is not itself a mathematical research verdict.",
    }
    write_json(manifest_path, manifest)
    assert validate_run_manifest(manifest_path, root=tmp_path) == []

    stdout.write_text("tampered\n")
    errors = validate_run_manifest(manifest_path, root=tmp_path)
    assert any("stdout hash mismatch" in error for error in errors)
