import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
DOCS = ROOT / "docs"
RESEARCH = DOCS / "research"


def flattened(text: str) -> str:
    return " ".join(text.split())


def test_current_research_authority_chain_is_small_and_explicit():
    instructions = (ROOT / "CLAUDE.md").read_text()
    documentation = (DOCS / "README.md").read_text()

    for relative in (
        "docs/research/charter.md",
        "docs/research/portfolio.json",
        "docs/research/status.md",
        "docs/theory/README.md",
    ):
        assert (ROOT / relative).is_file()
        assert relative in instructions

    assert "RESEARCH_RETURN_AUDIT.md" not in instructions
    normalized = flattened(documentation)
    assert "chronological provenance" in normalized
    assert "They are not current authorization" in normalized


def test_portfolio_is_machine_readable_and_program_level():
    portfolio = json.loads((RESEARCH / "portfolio.json").read_text())
    programs = portfolio["programs"]

    assert portfolio["mission"]["id"] == "EINSTEIN-PLANE"
    assert len(programs) >= 4
    assert len({program["id"] for program in programs}) == len(programs)
    assert all(program["terminal_outcomes"] for program in programs)
    assert all(program["scope_level"] for program in programs)
    assert portfolio["selection"]["research_commitment"] == (
        "none-during-authority-cutover"
    )


def test_creativity_is_not_forced_through_evidence_admission():
    charter = (RESEARCH / "charter.md").read_text()
    ideas = (RESEARCH / "ideas" / "README.md").read_text()
    workspaces = (RESEARCH / "workspaces" / "README.md").read_text()

    assert "Free exploration" in charter
    assert "does not require a formal proposal" in charter
    assert "gates commitment and promotion, not creativity" in charter
    assert "An idea needs no formal proposal" in ideas
    assert "without turning every work unit into a numbered session" in flattened(
        workspaces
    )


def test_historical_program_and_notebook_guides_point_to_current_authority():
    program = (DOCS / "program" / "README.md").read_text()
    notebook = (DOCS / "notebook" / "README.md").read_text()

    assert "superseded by" in program
    assert "../research/charter.md" in notebook
    assert "../research/portfolio.json" in notebook
    assert "STURMIAN_REALIZATION_BOUNDARY.md" not in notebook
    assert "GENERAL_REALIZATION_THEOREMS.md" not in notebook


def test_experiment_gate_uses_current_proposals_not_checkpoint_sessions():
    instructions = (ROOT / "CLAUDE.md").read_text()
    rules = json.loads(
        (DOCS / "consolidation" / "DISPOSITION_RULES.json").read_text()
    )["rules"]
    by_glob = {rule["glob"]: rule for rule in rules}

    assert "No nontrivial experiment without an admitted proposal" in instructions
    assert by_glob["scripts/run_research.py"]["disposition"] == "retained-toolbox"
    assert by_glob["docs/notebook/EXPERIMENT_TEMPLATE.md"]["disposition"] == (
        "archive-provenance"
    )
