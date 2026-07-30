"""Mechanical checks for research proposal and historical correction policy."""

import importlib.util
import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))


def load_gate_module():
    path = ROOT / "scripts" / "check_experiment_gate.py"
    spec = importlib.util.spec_from_file_location("check_experiment_gate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_agent_instructions_separate_research_from_maintenance():
    instructions = (ROOT / "CLAUDE.md").read_text()
    assert "No nontrivial experiment without an admitted proposal" in instructions
    assert "Repository maintenance and consolidation" in instructions
    assert "Do not create a numbered" in instructions
    assert "three-session checkpoint cadence is retired" in instructions
    assert "User-supplied" in instructions and "halt conditions" in instructions
    assert "scripts/run_research.py" in instructions
    assert "Externally supervise native solvers" in instructions
    assert (ROOT / "AGENTS.md").is_file()


def test_retired_checkpoint_record_remains_intact():
    data = json.loads((ROOT / "docs" / "HUMAN_CHECKPOINTS.json").read_text())
    assert data["schema_version"] == 1
    assert 1 <= data["policy"]["max_research_sessions"] <= 3
    assert data["policy"]["max_new_artifact_bytes"] <= 1024**3
    assert data["latest"]["id"] == "HC-2026-07-29-51"
    assert data["latest"]["through_session"] == 199


def test_stm1_source_correction_is_fail_closed():
    errata = (ROOT / "docs" / "program" / "ERRATA.md").read_text()
    ledger = (
        ROOT / "docs" / "theory" / "reference" / "proof_ledger.md"
    ).read_text()
    assert "ERR-006" in errata
    assert "ERR-007" in errata
    assert "ERR-008" in errata
    assert "ERR-009" in errata
    assert "ERR-010" in errata
    assert "ERR-011" in errata
    assert "ERR-012" in errata
    assert "ERR-013" in errata
    assert "ERR-016" in errata
    assert "ERR-017" in errata
    assert "12S+6M+6L" in errata
    assert "ST-M1.E∞" in ledger
    assert "exact support/SAB specialization; all-tilings equivalence remains proof-draft" in ledger
    assert "ST-M1.L0" in ledger
    assert "extensional finite atlas machine-verified; total decoder proof-draft" in ledger
    assert "no finite-`kappa` MLD claim" in ledger
    assert "source orders `s in {-1,0,1}`" in ledger
    assert "source conjugate outside `[0,1]`" in ledger
    assert "ST-M1.K1D" in ledger
    assert "information redistribution, not state minimization" in ledger
    assert "ST-M1.K2G" in ledger
    assert "blocked/frozen after HC-09" in ledger
    assert "ST-M1.K1P" in ledger
    assert "ST-M1.N5" in ledger
    assert "ST-M1.K2H" in ledger
    assert "ST-M1.N6" in ledger
    assert "ST-M1.N7" in ledger
    assert "ST-M1.N8" in ledger
    assert "ST-M1.N9" in ledger
    assert "ST-M1.K2C" in ledger
    assert "ST-M1.K2V" in ledger
    assert "ST-M1.K2J" in ledger
    assert "blocked/frozen after HC-09" in ledger
    assert "ST-M1.SER0" in ledger
    assert "primary archive contains Illustrator figures" in ledger
    assert "ST-M1.SYN0" in ledger


def test_gate_rejects_template_and_accepts_admitted_experiment(tmp_path):
    gate = load_gate_module()
    template = ROOT / "docs" / "research" / "proposals" / "TEMPLATE.json"
    assert gate.validate(template)

    proposal = tmp_path / "RP-2026-07-30-CROSSWALK.json"
    proposal.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": "RP-2026-07-30-CROSSWALK",
                "title": "Exact coordinate crosswalk control",
                "kind": "experiment",
                "status": "admitted",
                "program_id": "CERTIFIED-DISCOVERY-METHODS",
                "scope_level": "recognized-mathematical-family",
                "thesis": (
                    "A fixed source corpus and repository corpus may admit an "
                    "exact canonical coordinate bijection."
                ),
                "mission_connection": (
                    "The result tests whether retained exact identity machinery "
                    "is trustworthy before future discovery use."
                ),
                "alternatives_considered": (
                    "Aggregate equality was considered but cannot identify "
                    "shape-level semantic mismatches."
                ),
                "failure_or_pivot": (
                    "Any unmatched shape blocks equivalence and redirects the "
                    "work to coordinate-semantics diagnosis."
                ),
                "prior_art": {
                    "snapshot_date": "2026-07-30",
                    "primary_sources": ["kaplan-8kites-2023"],
                    "non_redundancy": (
                        "The source publishes aggregate records but the admitted "
                        "test concerns a coordinate-level bijection."
                    ),
                    "user_facts_resolved": [],
                },
                "outcomes": [
                    {
                        "result": (
                            "Every source shape has one exact canonical repository "
                            "mate with matching classification."
                        ),
                        "action": (
                            "Retain the crosswalk as a finite external control and "
                            "close this comparison without extension."
                        ),
                    },
                    {
                        "result": (
                            "At least one source shape is absent, duplicated, or "
                            "classified differently by exact identity."
                        ),
                        "action": (
                            "Block equivalence claims and diagnose the coordinate "
                            "or classification semantics before reuse."
                        ),
                    },
                ],
                "stop_rule": {
                    "condition": (
                        "Process each member of the fixed finite corpus exactly "
                        "once and stop after the final record."
                    ),
                    "no_automatic_escalation": True,
                },
                "experiment": {
                    "proposition": (
                        "Decide whether the two fixed finite corpora are related "
                        "by an exact canonical coordinate bijection."
                    ),
                    "command": ["venv/bin/python", "scripts/example.py"],
                    "budget": {
                        "wall_time_seconds": 60,
                        "max_new_artifact_bytes": 1024,
                        "artifact_roots": ["data/example-results"],
                        "external_supervision": True,
                    },
                    "evidence": {
                        "certificate_or_verifier": (
                            "A deterministic per-shape mapping table is checked "
                            "by an independent exact identity verifier."
                        ),
                        "promotion_boundary": (
                            "A passing crosswalk validates identity machinery but "
                            "does not establish tile or method novelty."
                        ),
                    },
                },
            },
            indent=2,
        )
    )
    assert gate.validate(proposal) == []
