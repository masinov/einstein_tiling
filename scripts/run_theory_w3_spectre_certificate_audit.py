#!/usr/bin/env python
"""Package and audit the exact finite kernel already recovered by A6 Spectre."""

from __future__ import annotations

import json
from pathlib import Path

from einstein.theory.substitution_certificate import (
    SCHEMA,
    VERSION,
    audit_obligations,
    file_sha256,
    parent_overlap_summary,
    physical_language_summary,
    substitution_from_a6,
)
from einstein.theory.spectre_geometry import (
    binary_boundary_prefix,
    boundary_word_recurrence_evidence,
    boundary_simplicity_prefix,
    compare_vendored_translations,
    realized_patch_evidence,
    macro_word_recurrence_evidence,
    verify_binary_geometry_quotient,
    verify_all_level_macro_side_chains,
    verify_stationary_recurrence,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/notebook/assets/a6-spectre-results.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-certificate-v0.json"
VENDOR_TABLE = ROOT / "vendor/spectre/spectre-core/src/tables.rs"
PHYSICAL_LANGUAGE = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
)
PARENT_OVERLAP = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-parent-overlap.json"
)
COMPONENT_LANGUAGE = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
)
RADIUS3_CLOSURE = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-radius3-defect.json"
)
D1_ENTRY = ROOT / "docs/notebook/assets/theory-w3-spectre-d1-entry.json"
EDGE_PATCH_BRIDGE = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-edge-patch-bridge.json"
)
D4_EQUIVALENCE = (
    ROOT / "docs/notebook/assets/theory-w3-spectre-d4-equivalence.json"
)


def main():
    a6 = json.loads(SOURCE.read_text())
    component_language = json.loads(COMPONENT_LANGUAGE.read_text())
    radius3_closure = json.loads(RADIUS3_CLOSURE.read_text())
    d1_entry = json.loads(D1_ENTRY.read_text())
    edge_patch_bridge = json.loads(EDGE_PATCH_BRIDGE.read_text())
    d4_equivalence = json.loads(D4_EQUIVALENCE.read_text())
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "status": "PARTIAL",
        "subject": "Spectre / Tile(1,1) recovered 17-state hierarchy",
        "scope": {
            "claim_domain": (
                "all whole-plane tilings by undeformed Tile(1,1) under the "
                "declared motion convention"
            ),
            "allowed_isometries": ["translation", "rotation"],
            "reflections_allowed": False,
            "formal_all_tilings_language_encoded": True,
            "current_evidence_domain": (
                "the unrestricted fixed-chirality polygonal hull reduces to "
                "the exact 14-segment model, enters L18 by ancestry-free "
                "radius-five exclusion, has a unique parent partition, and "
                "closes under contraction to the 17 generated states"
            ),
        },
        "provenance": {
            "source": str(SOURCE.relative_to(ROOT)),
            "sha256": file_sha256(SOURCE),
            "geometry_source": str(VENDOR_TABLE.relative_to(ROOT)),
            "geometry_sha256": file_sha256(VENDOR_TABLE),
            "physical_language_source": str(PHYSICAL_LANGUAGE.relative_to(ROOT)),
            "physical_language_sha256": file_sha256(PHYSICAL_LANGUAGE),
            "parent_overlap_source": str(PARENT_OVERLAP.relative_to(ROOT)),
            "parent_overlap_sha256": file_sha256(PARENT_OVERLAP),
            "component_language_source": str(COMPONENT_LANGUAGE.relative_to(ROOT)),
            "component_language_sha256": file_sha256(COMPONENT_LANGUAGE),
            "radius3_closure_source": str(RADIUS3_CLOSURE.relative_to(ROOT)),
            "radius3_closure_sha256": file_sha256(RADIUS3_CLOSURE),
            "d1_entry_source": str(D1_ENTRY.relative_to(ROOT)),
            "d1_entry_sha256": file_sha256(D1_ENTRY),
            "edge_patch_bridge_source": str(
                EDGE_PATCH_BRIDGE.relative_to(ROOT)
            ),
            "edge_patch_bridge_sha256": file_sha256(EDGE_PATCH_BRIDGE),
            "d4_equivalence_source": str(D4_EQUIVALENCE.relative_to(ROOT)),
            "d4_equivalence_sha256": file_sha256(D4_EQUIVALENCE),
        },
        "substitution": substitution_from_a6(a6),
        "physical_patch_language": physical_language_summary(
            json.loads(PHYSICAL_LANGUAGE.read_text())
        ),
        "parent_overlap_language": parent_overlap_summary(
            json.loads(PARENT_OVERLAP.read_text())
        ),
        "conditional_l18_composition": {
            "unrestricted_contact_bridge": {
                "status": edge_patch_bridge["status"],
                "scope": edge_patch_bridge["scope"],
                "theorem": edge_patch_bridge["analysis"]["theorem"],
                "claim": edge_patch_bridge["claim"],
                "claim_boundary": edge_patch_bridge["claim_boundary"],
            },
            "edge_to_edge_entry": {
                "status": d1_entry["status"],
                "scope": d1_entry["scope"],
                "theorem": d1_entry["theorem"],
                "claim_boundary": d1_entry["claim_boundary"],
            },
            "component_language": {
                "status": component_language["status"],
                "partition_theorem": component_language["partition_theorem"],
            },
            "radius3_closure": {
                "status": radius3_closure["status"],
                "scope": radius3_closure["scope"],
                "elimination": radius3_closure["elimination"],
            },
            "d4_equivalence": {
                "status": d4_equivalence["status"],
                "scope": d4_equivalence["scope"],
                "colored_collar_bijection": (
                    d4_equivalence["colored_collar_bijection"]
                ),
                "component_state_roundtrips": {
                    key: value for key, value in d4_equivalence[
                        "component_state_roundtrips"
                    ].items() if key != "records"
                },
                "normalization": {
                    "determinants": d4_equivalence["normalization"][
                        "determinants"
                    ],
                    "exact_inverse_matrices": d4_equivalence[
                        "normalization"
                    ]["exact_inverse_matrices"],
                    "chirality_toggles_uniformly": d4_equivalence[
                        "normalization"
                    ]["chirality_toggles_uniformly"],
                    "translation_covariance": d4_equivalence[
                        "normalization"
                    ]["translation_covariance"],
                    "two_level_characteristic_polynomials": d4_equivalence[
                        "normalization"
                    ]["two_level_characteristic_polynomials"],
                },
                "level_pair_roundtrips": d4_equivalence[
                    "level_pair_roundtrips"
                ],
                "marker_transducer": d4_equivalence["marker_transducer"],
                "finite_kernel_verified": d4_equivalence[
                    "finite_kernel_verified"
                ],
                "radius1_context_probe": d4_equivalence[
                    "radius1_context_probe"
                ],
                "radius2_context_filter": d4_equivalence[
                    "radius2_context_filter"
                ],
                "d4_assessment": d4_equivalence["d4_assessment"],
                "claim_boundary": d4_equivalence["claim_boundary"],
            },
        },
    }
    geometry = verify_stationary_recurrence(32)
    geometry["vendored_table_comparison"] = compare_vendored_translations(
        VENDOR_TABLE.read_text()
    )
    geometry["realized_patch_evidence"] = realized_patch_evidence(1)
    geometry["binary_geometry_quotient"] = verify_binary_geometry_quotient()
    geometry["binary_boundary_prefix"] = binary_boundary_prefix(4)
    geometry["boundary_word_recurrence_evidence"] = (
        boundary_word_recurrence_evidence(5)
    )
    geometry["all_level_macro_side_chains"] = (
        verify_all_level_macro_side_chains()
    )
    geometry["macro_word_recurrence_evidence"] = (
        macro_word_recurrence_evidence(5)
    )
    geometry["boundary_simplicity_prefix"] = boundary_simplicity_prefix(7)
    certificate["geometry_recurrence"] = geometry
    certificate["audit"] = audit_obligations(certificate)
    certificate["status"] = (
        "THEOREM_READY" if certificate["audit"]["theorem_ready"]
        else "VALID_PARTIAL_CERTIFICATE"
    )
    OUTPUT.write_text(json.dumps(certificate, indent=1) + "\n")
    kernel = certificate["audit"]["finite_kernel"]
    print(
        f"W3 Spectre: {certificate['status']} — {kernel['states']} states, "
        f"primitive exponent {kernel['primitivity_exponent']}; blockers: "
        + ", ".join(certificate["audit"]["blocking_obligations"])
    )
    print(OUTPUT.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
