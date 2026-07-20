#!/usr/bin/env python
"""Independent finite-kernel verifier for a W3 substitution certificate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from einstein.theory.substitution_certificate import (
    audit_obligations,
    file_sha256,
    parent_overlap_summary,
    physical_language_summary,
)
from einstein.theory.spectre_geometry import compare_vendored_translations


ROOT = Path(__file__).resolve().parents[1]


def verify(path):
    certificate = json.loads(Path(path).read_text())
    source = ROOT / certificate["provenance"]["source"]
    if file_sha256(source) != certificate["provenance"]["sha256"]:
        return False, "source hash mismatch"
    geometry_source_name = certificate["provenance"].get("geometry_source")
    if geometry_source_name:
        geometry_source = ROOT / geometry_source_name
        if file_sha256(geometry_source) != certificate["provenance"].get(
            "geometry_sha256"
        ):
            return False, "geometry source hash mismatch"
        try:
            comparison = compare_vendored_translations(geometry_source.read_text())
        except ValueError as exc:
            return False, f"geometry table comparison failed: {exc}"
        stored_comparison = certificate.get("geometry_recurrence", {}).get(
            "vendored_table_comparison"
        )
        if comparison != stored_comparison:
            return False, "stored geometry comparison does not match vendor table"
    physical_source_name = certificate["provenance"].get(
        "physical_language_source"
    )
    if physical_source_name:
        physical_source = ROOT / physical_source_name
        if file_sha256(physical_source) != certificate["provenance"].get(
            "physical_language_sha256"
        ):
            return False, "physical language source hash mismatch"
        try:
            physical_summary = physical_language_summary(
                json.loads(physical_source.read_text())
            )
        except ValueError as exc:
            return False, f"physical language summary failed: {exc}"
        if certificate.get("physical_patch_language") != physical_summary:
            return False, "physical language summary mismatch"
    parent_source_name = certificate["provenance"].get("parent_overlap_source")
    if parent_source_name:
        parent_source = ROOT / parent_source_name
        if file_sha256(parent_source) != certificate["provenance"].get(
            "parent_overlap_sha256"
        ):
            return False, "parent-overlap source hash mismatch"
        try:
            overlap_summary = parent_overlap_summary(
                json.loads(parent_source.read_text())
            )
        except ValueError as exc:
            return False, f"parent-overlap summary failed: {exc}"
        if certificate.get("parent_overlap_language") != overlap_summary:
            return False, "parent-overlap summary mismatch"
    conditional = certificate.get("conditional_l18_composition", {})
    bridge_source_name = certificate["provenance"].get(
        "edge_patch_bridge_source"
    )
    if bridge_source_name:
        bridge_source = ROOT / bridge_source_name
        if file_sha256(bridge_source) != certificate["provenance"].get(
            "edge_patch_bridge_sha256"
        ):
            return False, "edge-patch bridge source hash mismatch"
        bridge = json.loads(bridge_source.read_text())
        expected_bridge = {
            "status": bridge["status"],
            "scope": bridge["scope"],
            "theorem": bridge["analysis"]["theorem"],
            "claim": bridge["claim"],
            "claim_boundary": bridge["claim_boundary"],
        }
        if conditional.get("unrestricted_contact_bridge") != expected_bridge:
            return False, "edge-patch bridge summary mismatch"
    d4_source_name = certificate["provenance"].get("d4_equivalence_source")
    if d4_source_name:
        d4_source = ROOT / d4_source_name
        if file_sha256(d4_source) != certificate["provenance"].get(
            "d4_equivalence_sha256"
        ):
            return False, "D4 equivalence source hash mismatch"
        d4 = json.loads(d4_source.read_text())
        expected_d4 = {
            "status": d4["status"],
            "scope": d4["scope"],
            "colored_collar_bijection": d4["colored_collar_bijection"],
            "component_state_roundtrips": {
                key: value for key, value in d4[
                    "component_state_roundtrips"
                ].items() if key != "records"
            },
            "normalization": {
                "determinants": d4["normalization"]["determinants"],
                "exact_inverse_matrices": d4["normalization"][
                    "exact_inverse_matrices"
                ],
                "chirality_toggles_uniformly": d4["normalization"][
                    "chirality_toggles_uniformly"
                ],
                "translation_covariance": d4["normalization"][
                    "translation_covariance"
                ],
                "two_level_characteristic_polynomials": d4[
                    "normalization"
                ]["two_level_characteristic_polynomials"],
            },
            "level_pair_roundtrips": d4["level_pair_roundtrips"],
            "marker_transducer": d4["marker_transducer"],
            "finite_kernel_verified": d4["finite_kernel_verified"],
            "radius1_context_probe": d4["radius1_context_probe"],
            "radius2_context_filter": d4["radius2_context_filter"],
            "d4_assessment": d4["d4_assessment"],
            "claim_boundary": d4["claim_boundary"],
        }
        if conditional.get("d4_equivalence") != expected_d4:
            return False, "D4 equivalence summary mismatch"
    component_source_name = certificate["provenance"].get(
        "component_language_source"
    )
    if component_source_name:
        component_source = ROOT / component_source_name
        if file_sha256(component_source) != certificate["provenance"].get(
            "component_language_sha256"
        ):
            return False, "component-language source hash mismatch"
        component = json.loads(component_source.read_text())
        expected_component = {
            "status": component["status"],
            "partition_theorem": component["partition_theorem"],
        }
        if conditional.get("component_language") != expected_component:
            return False, "component-language summary mismatch"
    radius3_source_name = certificate["provenance"].get(
        "radius3_closure_source"
    )
    if radius3_source_name:
        radius3_source = ROOT / radius3_source_name
        if file_sha256(radius3_source) != certificate["provenance"].get(
            "radius3_closure_sha256"
        ):
            return False, "radius-three closure source hash mismatch"
        radius3 = json.loads(radius3_source.read_text())
        expected_radius3 = {
            "status": radius3["status"],
            "scope": radius3["scope"],
            "elimination": radius3["elimination"],
        }
        if conditional.get("radius3_closure") != expected_radius3:
            return False, "radius-three closure summary mismatch"
    d1_source_name = certificate["provenance"].get("d1_entry_source")
    if d1_source_name:
        d1_source = ROOT / d1_source_name
        if file_sha256(d1_source) != certificate["provenance"].get(
            "d1_entry_sha256"
        ):
            return False, "D1 entry source hash mismatch"
        d1 = json.loads(d1_source.read_text())
        expected_d1 = {
            "status": d1["status"],
            "scope": d1["scope"],
            "theorem": d1["theorem"],
            "claim_boundary": d1["claim_boundary"],
        }
        if conditional.get("edge_to_edge_entry") != expected_d1:
            return False, "D1 entry summary mismatch"
    expected = audit_obligations(certificate)
    if expected != certificate.get("audit"):
        return False, "stored audit does not match independent recomputation"
    expected_status = (
        "THEOREM_READY" if expected["theorem_ready"]
        else "VALID_PARTIAL_CERTIFICATE"
    )
    if certificate.get("status") != expected_status:
        return False, "certificate status overstates or understates its audit"
    return True, (
        f"{expected_status}; primitive exponent "
        f"{expected['finite_kernel']['primitivity_exponent']}; "
        f"{len(expected['blocking_obligations'])} blockers"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate")
    args = parser.parse_args()
    ok, message = verify(args.certificate)
    print(("PASS" if ok else "FAIL") + ": " + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
