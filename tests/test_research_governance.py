"""Mechanical checks for the post-ERR-005 experiment admission gate."""

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def load_gate_module():
    path = ROOT / "scripts" / "check_experiment_gate.py"
    spec = importlib.util.spec_from_file_location("check_experiment_gate", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_agent_instructions_make_the_gate_mandatory():
    instructions = (ROOT / "CLAUDE.md").read_text()
    assert "No run without pre-registration" in instructions
    assert "Human checkpoint cadence" in instructions
    assert "User facts are gates" in instructions
    assert "scripts/run_research.py" in instructions
    assert (ROOT / "AGENTS.md").is_file()


def test_checkpoint_policy_is_bounded_and_current():
    data = json.loads((ROOT / "docs" / "HUMAN_CHECKPOINTS.json").read_text())
    assert data["schema_version"] == 1
    assert 1 <= data["policy"]["max_research_sessions"] <= 3
    assert data["policy"]["max_new_artifact_bytes"] <= 1024**3
    assert data["latest"]["through_session"] == 69


def test_stm1_source_correction_is_fail_closed():
    errata = (ROOT / "docs" / "program" / "ERRATA.md").read_text()
    ledger = (ROOT / "docs" / "theory" / "PROOF_LEDGER.md").read_text()
    assert "ERR-006" in errata
    assert "12S+6M+6L" in errata
    assert "ST-M1.E∞" in ledger
    assert "proof-draft; G0 support plus L0 symbolic language transport" in ledger
    assert "ST-M1.L0" in ledger
    assert "proof-draft; O0/I0/D0 closed without atlas enumeration" in ledger
    assert "no finite-`kappa` MLD claim" in ledger


def test_gate_rejects_template_and_accepts_completed_record(tmp_path):
    gate = load_gate_module()
    template = ROOT / "docs" / "notebook" / "EXPERIMENT_TEMPLATE.md"
    assert gate.validate(template)

    note = tmp_path / "2026-07-21-session-58.md"
    note.write_text(
        "# Session 58\n\n## Experiment pre-registration\n\n"
        "### Proposition\n\nDetermine whether a fixed corpus admits an exact coordinate bijection.\n\n"
        "### Prior art and non-redundancy\n\nThe aggregate source artifact was audited; no coordinate-level crosswalk was located.\n\n"
        "### Outcome decisions\n\n- A bijection packages the corpus as a benchmark and closes the comparison.\n"
        "- A mismatch identifies a semantic difference and blocks equivalence claims.\n\n"
        "### Stop rule and finite justification\n\nThe fixed 116-page corpus is finite; stop after every listed shape is processed once.\n\n"
        "### Human checkpoint\n\nUse HC-2026-07-21-01 at session distance one with zero planned large artifacts.\n\n"
        "## Results\n\nNot run.\n"
    )
    assert gate.validate(note) == []
