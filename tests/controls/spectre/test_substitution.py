"""Finite W3 substitution-certificate kernel and honesty gates."""

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.spectre.certificates import (
    SCHEMA,
    VERSION,
    audit_obligations,
    primitivity_exponent,
    physical_language_summary,
    parent_overlap_summary,
    substitution_from_a6,
    verify_finite_kernel,
    verify_geometry_kernel,
    recognisability_crosswalk,
)
from einstein.tilings.spectre.geometry import (
    binary_boundary_prefix,
    boundary_word_recurrence_evidence,
    boundary_simplicity_prefix,
    macro_word_recurrence_evidence,
    verify_stationary_recurrence,
)
from einstein.tilings.spectre.geometry import verify_binary_geometry_quotient
from einstein.tilings.spectre.geometry import verify_all_level_macro_side_chains


ROOT = repository_root(Path(__file__))


def test_primitivity_exponent_controls():
    assert primitivity_exponent([[1, 1], [1, 0]]) == 2
    assert primitivity_exponent([[0, 1], [1, 0]]) is None


def test_spectre_finite_kernel_is_primitive_but_not_theorem_ready():
    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": substitution_from_a6(source),
    }
    kernel = verify_finite_kernel(certificate)
    assert kernel["states"] == 17
    assert (kernel["minimum_children"], kernel["maximum_children"]) == (7, 8)
    assert kernel["primitivity_exponent"] == 3
    audit = audit_obligations(certificate)
    assert audit["obligations"]["C2_closure"]["status"] == "verified"
    assert audit["obligations"]["C3_existence_growth"]["status"] == "partial"
    assert audit["obligations"]["C4_recognizability"]["status"] == "partial"
    assert not audit["theorem_ready"]


def test_recognisability_routes_are_separate_and_fail_closed():
    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": substitution_from_a6(source),
    }
    crosswalk = recognisability_crosswalk(certificate)
    walton = crosswalk["walton_theorem_route"]
    direct = crosswalk["direct_local_composition_route"]

    assert not walton["standalone_aperiodicity_route"]
    assert not walton["all_hypotheses_verified"]
    assert {
        name: row["status"] for name, row in walton["hypotheses"].items()
    } == {
        "W1_compact_FLC_pattern_space": "missing",
        "W2_Hausdorff_well_separated": "missing",
        "W3_expansive_linear_automorphism": "missing",
        "W4_surjective_LD_subdivision": "missing",
        "W5_discrete_nonperiodicity_for_injectivity": "missing",
    }
    assert {
        name: row["status"] for name, row in direct["obligations"].items()
    } == {
        "D1_formal_all_tilings_domain": "missing",
        "D2_parent_exists_for_every_tiling": "missing",
        "D3_parent_grouping_is_unique": "partial",
        "D4_equivalence_chain_is_faithful": "missing",
        "D5_hierarchy_iterates_on_same_domain": "partial",
        "D6_local_inverse_or_uniform_recognition_radius": "missing",
        "D7_period_descent_and_scale_growth": "missing",
    }
    assert not crosswalk["standalone_aperiodicity_route_ready"]


def test_exact_geometry_only_partially_advances_both_routes():
    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    geometry = verify_stationary_recurrence(1)
    geometry["vendored_table_comparison"] = {
        "levels": 1,
        "children_per_level": 8,
        "vectors_compared": 8,
        "all_equal": True,
    }
    geometry["binary_geometry_quotient"] = verify_binary_geometry_quotient()
    geometry["all_level_macro_side_chains"] = (
        verify_all_level_macro_side_chains()
    )
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": substitution_from_a6(source),
        "geometry_recurrence": geometry,
    }
    crosswalk = recognisability_crosswalk(certificate)
    assert crosswalk["walton_theorem_route"]["hypotheses"][
        "W3_expansive_linear_automorphism"
    ]["status"] == "partial"
    assert crosswalk["direct_local_composition_route"]["obligations"][
        "D7_period_descent_and_scale_growth"
    ]["status"] == "partial"
    assert not crosswalk["standalone_aperiodicity_route_ready"]


def test_radius3_physical_language_advances_domain_but_not_theorem():
    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    physical = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
    ).read_text())
    summary = physical_language_summary(physical)
    assert summary["unique_parent_radius3_survivors"] == 0
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": substitution_from_a6(source),
        "physical_patch_language": summary,
    }
    audit = audit_obligations(certificate)
    direct = audit["recognisability_crosswalk"][
        "direct_local_composition_route"
    ]["obligations"]
    assert direct["D1_formal_all_tilings_domain"]["status"] == "partial"
    assert direct["D2_parent_exists_for_every_tiling"]["status"] == "partial"
    assert direct["D6_local_inverse_or_uniform_recognition_radius"][
        "status"
    ] == "missing"
    assert audit["obligations"]["C5_global_consistency"]["status"] == "partial"
    assert not audit["theorem_ready"]


def test_conditional_parent_overlap_closes_finite_extras_not_theorem():
    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    physical = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
    ).read_text())
    overlap = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-parent-overlap.json"
    ).read_text())
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": substitution_from_a6(source),
        "physical_patch_language": physical_language_summary(physical),
        "parent_overlap_language": parent_overlap_summary(overlap),
    }
    audit = audit_obligations(certificate)
    direct = audit["recognisability_crosswalk"][
        "direct_local_composition_route"
    ]["obligations"]
    assert direct["D2_parent_exists_for_every_tiling"]["status"] == "partial"
    assert direct["D3_parent_grouping_is_unique"]["status"] == "partial"
    assert audit["obligations"]["C5_global_consistency"]["status"] == "partial"
    assert "conditional" in audit["obligations"]["C5_global_consistency"]["reason"]
    assert not audit["theorem_ready"]


def test_edge_patch_bridge_composes_l18_results_over_full_chiral_hull():
    certificate = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-certificate-v0.json"
    ).read_text())
    audit = audit_obligations(certificate)
    crosswalk = audit["recognisability_crosswalk"]
    direct = crosswalk["direct_local_composition_route"]["obligations"]

    assert crosswalk["conditional_l18_composition"] == {
        "unrestricted_contact_bridge": True,
        "unrestricted_l18_entry": True,
        "edge_to_edge_entry": True,
        "unique_parent_partition": True,
        "same_domain_closure": True,
        "d4_finite_kernel": True,
        "d4_full_hull_equivalence": False,
        "scope": (
            "all fixed-chirality straight-Spectre polygonal tilings; "
            "unrestricted contacts reduce to the primitive model and all "
            "complete physical coronas are proved to lie in L18"
        ),
    }
    assert direct["D1_formal_all_tilings_domain"][
        "within_edge_to_edge_status"
    ] == "verified"
    assert direct["D2_parent_exists_for_every_tiling"]["within_L18_status"] == (
        "verified"
    )
    assert direct["D3_parent_grouping_is_unique"]["within_L18_status"] == (
        "verified"
    )
    assert direct["D5_hierarchy_iterates_on_same_domain"][
        "within_L18_status"
    ] == "verified"
    assert direct["D6_local_inverse_or_uniform_recognition_radius"][
        "within_L18_status"
    ] == "verified"
    for obligation in (
        "D2_parent_exists_for_every_tiling",
        "D3_parent_grouping_is_unique",
        "D5_hierarchy_iterates_on_same_domain",
        "D6_local_inverse_or_uniform_recognition_radius",
    ):
        assert direct[obligation]["within_edge_to_edge_status"] == "verified"

    for obligation in (
        "D1_formal_all_tilings_domain",
        "D2_parent_exists_for_every_tiling",
        "D3_parent_grouping_is_unique",
        "D5_hierarchy_iterates_on_same_domain",
        "D6_local_inverse_or_uniform_recognition_radius",
    ):
        assert direct[obligation]["status"] == "verified"

    # The D4 finite kernel is exact, but its 80 surviving state contexts and
    # D7 still prevent a standalone aperiodicity theorem.
    assert direct["D4_equivalence_chain_is_faithful"]["status"] == "partial"
    assert "536 output-overlap stars" in direct[
        "D4_equivalence_chain_is_faithful"
    ]["missing"]
    assert direct["D7_period_descent_and_scale_growth"]["status"] == "partial"
    assert not crosswalk["standalone_aperiodicity_route_ready"]
    assert not audit["theorem_ready"]


def test_kernel_rejects_child_outside_alphabet():
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": {
            "alphabet": [0],
            "rules": [{
                "parent": 0,
                "children": [{"pose": [0, 0, [0, 0, 0, 0]], "state": 1}],
            }],
            "recovered_language_evidence": {},
        },
    }
    try:
        verify_finite_kernel(certificate)
    except ValueError as exc:
        assert "outside" in str(exc)
    else:
        raise AssertionError("invalid child state was accepted")


def test_exact_geometry_strengthens_but_does_not_discharge_c1_or_c3():
    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    geometry = verify_stationary_recurrence(3)
    geometry["vendored_table_comparison"] = {
        "levels": 3,
        "children_per_level": 8,
        "vectors_compared": 24,
        "all_equal": True,
    }
    geometry["binary_geometry_quotient"] = verify_binary_geometry_quotient()
    geometry["binary_boundary_prefix"] = binary_boundary_prefix(1)
    geometry["boundary_word_recurrence_evidence"] = (
        boundary_word_recurrence_evidence(2)
    )
    geometry["all_level_macro_side_chains"] = (
        verify_all_level_macro_side_chains()
    )
    geometry["macro_word_recurrence_evidence"] = macro_word_recurrence_evidence(2)
    geometry["boundary_simplicity_prefix"] = boundary_simplicity_prefix(2)
    certificate = {
        "schema": SCHEMA,
        "version": VERSION,
        "substitution": substitution_from_a6(source),
        "geometry_recurrence": geometry,
    }
    checked = verify_geometry_kernel(certificate)
    assert checked["unimodular"]
    audit = audit_obligations(certificate)
    assert audit["obligations"]["C1_legality"]["status"] == "partial"
    assert audit["obligations"]["C3_existence_growth"][
        "exact_expanding_geometry_recurrence"
    ]
    assert not audit["theorem_ready"]
