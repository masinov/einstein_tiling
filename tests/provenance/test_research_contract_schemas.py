import json
from pathlib import Path

from einstein.repository.research import (
    PROPOSAL_KINDS,
    PROPOSAL_STATUSES,
    SCOPE_LEVELS,
    validate_research_proposal,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "docs/harness/schemas"


def load(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text())


def test_published_schema_matches_manual_discriminators_and_nested_contracts() -> None:
    schema = load("research_proposal.schema.json")
    properties = schema["properties"]
    definitions = schema["$defs"]

    assert properties["schema_version"]["const"] == 2
    assert set(properties["kind"]["enum"]) == PROPOSAL_KINDS
    assert set(properties["status"]["enum"]) == PROPOSAL_STATUSES
    assert set(properties["scope_level"]["enum"]) == SCOPE_LEVELS
    assert set(definitions["experiment"]["required"]) == {
        "proposition", "command", "budget", "reproducibility", "evidence", "run_record"
    }
    assert set(definitions["budget"]["required"]) == {
        "wall_time_seconds", "memory_bytes", "max_new_artifact_bytes",
        "artifact_roots", "external_supervision",
    }
    assert set(definitions["reproducibility"]["required"]) == {
        "code_revision", "require_clean_tree", "code_paths", "inputs",
        "environment_files", "executables",
    }
    assert set(definitions["executablePin"]["required"]) == {
        "path", "sha256", "version_command", "version_output_sha256"
    }
    assert set(definitions["promotion"]["required"]) == {
        "claim_kind", "claim_id", "requested_label", "source_document",
        "evidence", "literature_sources",
    }


def test_specialized_schemas_reference_the_common_contract() -> None:
    expected = {
        "research_program.schema.json": "research-program",
        "experiment.schema.json": "experiment",
        "promotion.schema.json": "promotion",
    }
    for filename, kind in expected.items():
        schema = load(filename)
        assert schema["allOf"][0]["$ref"] == "research_proposal.schema.json"
        assert schema["allOf"][1]["properties"]["kind"]["const"] == kind
    assert load("admission.schema.json")["properties"]["proposal_sha256"]["pattern"]
    assert load("run_result.schema.json")["properties"]["research_verdict"] == {"type": "null"}


def valid_candidate_promotion() -> dict:
    pin = {"path": "evidence/item.json", "sha256": "0" * 64}
    return {
        "schema_version": 2,
        "id": "RP-2026-07-30-CANDIDATE-CHECK",
        "title": "Exact candidate promotion review",
        "kind": "promotion",
        "status": "ready",
        "program_id": "CONSTRUCTIVE-DISCOVERY",
        "scope_level": "single-instance",
        "thesis": "The exact support satisfies every obligation for the requested candidate label.",
        "mission_connection": "Acceptance would establish a connected unmarked planar aperiodic monotile.",
        "alternatives_considered": "Weaker finite-patch and locally-extensible labels were considered first.",
        "failure_or_pivot": "Any missing all-tilings obligation blocks the requested label completely.",
        "prior_art": {
            "snapshot_date": "2026-07-30",
            "primary_sources": ["source-id"],
            "non_redundancy": "The dated comparison rejects known shape and tiling-system identities.",
            "user_facts_resolved": [],
        },
        "outcomes": [
            {"result": "Every exact promotion obligation passes independently.", "action": "Integrate only the requested evidence-calibrated candidate label."},
            {"result": "At least one exact promotion obligation remains open or fails.", "action": "Block promotion and retain the weakest accurate evidence label."},
        ],
        "stop_rule": {
            "condition": "Stop after checking the fixed dossier against every promotion obligation.",
            "no_automatic_escalation": True,
        },
        "promotion": {
            "claim_kind": "candidate",
            "claim_id": "CANDIDATE-EXACT-1",
            "requested_label": "aperiodic-monotile",
            "source_document": pin,
            "evidence": [pin],
            "literature_sources": ["source-id"],
            "candidate_dossier": {
                "geometry": pin,
                "allowed_isometries": "full-E2",
                "identity_status": "novel-after-audit",
                "identity_evidence": [pin],
                "periodicity_status": "aperiodic-proved",
                "periodicity_evidence": pin,
                "whole_plane_tilability": "proved",
                "tilability_evidence": pin,
                "contact_language": "complete",
                "contact_evidence": pin,
                "all_tilings_aperiodicity": "proved",
                "aperiodicity_evidence": pin,
                "total_decoder": "proved",
                "decoder_evidence": pin,
            },
        },
    }


def test_manual_promotion_contract_blocks_intended_patch_overclaim(tmp_path: Path) -> None:
    proposal = valid_candidate_promotion()
    path = tmp_path / "promotion.json"
    path.write_text(json.dumps(proposal))
    assert validate_research_proposal(path, require_promotion=True) == []

    proposal["promotion"]["candidate_dossier"]["contact_language"] = "partial"
    path.write_text(json.dumps(proposal))
    errors = validate_research_proposal(path, require_promotion=True)
    assert any("contact_language=complete" in error for error in errors)

    proposal["promotion"]["candidate_dossier"]["periodicity_status"] = "periodic"
    path.write_text(json.dumps(proposal))
    errors = validate_research_proposal(path, require_promotion=True)
    assert any("periodic tiling certificate" in error for error in errors)
