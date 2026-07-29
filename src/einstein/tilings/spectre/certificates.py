"""Versioned finite kernel for W3 substitution certificates.

This module intentionally separates what the current A6 Spectre artifact can
prove from what W3 still needs.  Closure and primitivity are exact finite
facts.  Sampled forcing data is recorded as provenance, never promoted to an
exhaustive language or global gluing theorem.
"""

from __future__ import annotations

from hashlib import sha256
import json

from einstein.tilings.spectre.geometry import (
    binary_boundary_prefix,
    boundary_word_recurrence_evidence,
    boundary_simplicity_prefix,
    macro_word_recurrence_evidence,
    realized_patch_evidence,
    verify_binary_geometry_quotient,
    verify_all_level_macro_side_chains,
    verify_stationary_recurrence,
)


SCHEMA = "einstein.w3.substitution-certificate"
VERSION = 2


def physical_language_summary(artifact):
    """Validate and compact the separate ancestry-blind corona artifact."""
    if (
        artifact.get("schema")
        != "einstein.w3.spectre-physical-patch-language"
        or artifact.get("version") != 1
        or artifact.get("status") != "COMPLETE_RADIUS3_PREFIX"
    ):
        raise ValueError("unsupported physical patch-language artifact")
    analysis = artifact["analysis"]
    radius1 = analysis["radius1"]
    radius2 = analysis["radius2"]
    radius3 = analysis["radius3"]
    control = analysis["substitution_control"]
    if not (
        analysis["scope"]["ancestry_used_in_enumeration"] is False
        and analysis["scope"]["radius_completed"] == 3
        and radius1["complete_coronas"] == 166
        and radius2["surviving_first_coronas"] == 30
        and radius3["surviving_first_coronas"] == 21
        and radius3["unique_parent_survivors"] == 0
        and radius3["compatible_parent_count_histogram"] == {
            "2": 17, "3": 3, "5": 1,
        }
        and control["observed_first_coronas"] == 18
        and control["all_observed_are_bare_legal"] is True
        and control["all_observed_survive_radius3"] is True
        and control["unobserved_radius3_survivors"] == 3
        and analysis["radius4_targeted_probe"]["all_three_extend"] is True
    ):
        raise ValueError("physical patch-language control invariants failed")
    return {
        "status": artifact["status"],
        "radius_completed": 3,
        "ancestry_blind": True,
        "radius1_coronas": 166,
        "radius2_survivors": 30,
        "radius3_survivors": 21,
        "substitution_observed": 18,
        "unobserved_radius3_survivors": 3,
        "unique_parent_radius3_survivors": 0,
        "all_unobserved_radius3_survivors_have_radius4_witnesses": True,
        "radius1_language_sha256": radius1["language_sha256"],
        "observed_language_sha256": control["observed_language_sha256"],
        "claim_boundary": analysis["scope"]["claim_boundary"],
    }


def parent_overlap_summary(artifact):
    """Validate and compact the coordinated parent-overlap artifact."""
    if (
        artifact.get("schema") != "einstein.w3.spectre-parent-overlap"
        or artifact.get("version") != 1
        or artifact.get("status") != "CONDITIONAL_EXTRAS_REFUTED_RADIUS4"
    ):
        raise ValueError("unsupported parent-overlap artifact")
    analysis = artifact["analysis"]
    summary = analysis["summary"]
    rows = analysis["extra_coronas"]
    signature = [
        (
            row["corona_index"], row["complete_radius2_branches"],
            row["radius3_frontier_states"], row["radius4_frontier_states"],
        )
        for row in rows
    ]
    if not (
        analysis["generated_controls"][
            "all_18_survive_coordinated_radius4"
        ] is True
        and summary["extras_surviving_coordinated_grouping"] == []
        and summary["conditional_language_after_grouping"] == 18
        and summary["radius3_frontier_states_exhausted"] == 224
        and signature == [
            (33, 2, 200, 0), (44, 27, 0, 0), (155, 60, 24, 0)
        ]
    ):
        raise ValueError("parent-overlap control invariants failed")
    return {
        "status": artifact["status"],
        "conditional_on_recovered_parent_language": True,
        "generated_controls_surviving": 18,
        "extra_coronas_refuted": [33, 44, 155],
        "radius3_frontier_states_exhausted": 224,
        "radius4_frontier_states": 0,
        "conditional_language_after_grouping": 18,
        "claim_boundary": analysis["scope"]["claim_boundary"],
    }


def recognisability_crosswalk(certificate, kernel=None, geometry=None):
    """Audit the two logically different routes to recognisability.

    Walton's general theorem and a Chéritat-style direct local-composition
    proof are not interchangeable.  For a return-discrete tiling hull,
    Walton's strict-injectivity conclusion assumes exactly the absence of
    periodic tilings that W3 ultimately wants to prove.  The direct route must
    instead establish total and unique parent grouping on *every* admitted
    whole-plane tiling, before using scale descent to exclude periods.

    The current certificate deliberately supplies no user-editable status
    switches here.  Every row is derived from independently checked finite
    evidence, and unsupported theorem hypotheses remain red.
    """
    if kernel is None:
        kernel = verify_finite_kernel(certificate)
    if geometry is None:
        geometry = verify_geometry_kernel(certificate)
    evidence = certificate["substitution"]["recovered_language_evidence"]
    sampled_forcing = bool(
        evidence.get("all_states_checked")
        and evidence.get("unique_composition_on_recovered_language")
        and evidence.get("ambiguous_instances") == 0
        and evidence.get("legal_candidates_outside_known_cover") == 0
    )
    physical_prefix = certificate.get("physical_patch_language")
    finite_physical_domain = bool(
        physical_prefix
        and physical_prefix.get("status") == "COMPLETE_RADIUS3_PREFIX"
        and physical_prefix.get("radius_completed") == 3
        and physical_prefix.get("ancestry_blind") is True
    )
    grouping_prefix = certificate.get("parent_overlap_language")
    finite_conditional_grouping = bool(
        grouping_prefix
        and grouping_prefix.get("status")
        == "CONDITIONAL_EXTRAS_REFUTED_RADIUS4"
        and grouping_prefix.get("conditional_language_after_grouping") == 18
        and grouping_prefix.get("radius4_frontier_states") == 0
    )
    l18 = certificate.get("conditional_l18_composition") or {}
    unrestricted_contact = l18.get("unrestricted_contact_bridge") or {}
    edge_to_edge_entry = l18.get("edge_to_edge_entry") or {}
    component_language = l18.get("component_language") or {}
    radius3_closure = l18.get("radius3_closure") or {}
    d4_equivalence = l18.get("d4_equivalence") or {}
    edge_to_edge_l18_entry = bool(
        edge_to_edge_entry.get("status")
        == "EDGE_TO_EDGE_L18_ENTRY_PROVED_RADIUS5"
        and edge_to_edge_entry.get("scope", {}).get("contact_model")
        == "edge-to-edge unit-edge tilings"
        and edge_to_edge_entry.get("scope", {}).get(
            "ancestry_or_parent_data_used_in_ring_enumeration"
        ) is False
    )
    unrestricted_contact_bridge = bool(
        unrestricted_contact.get("status")
        == "UNRESTRICTED_EDGE_PATCH_BRIDGE_PROVED"
        and unrestricted_contact.get("scope", {}).get("reflections_allowed")
        is False
        and unrestricted_contact.get("theorem", {}).get(
            "unrestricted_contacts_reduce_to_primitive_edge_to_edge"
        ) is True
    )
    unrestricted_l18_entry = bool(
        unrestricted_contact_bridge and edge_to_edge_l18_entry
    )
    l18_unique_partition = bool(
        component_language.get("status")
        == "PARENT_PARTITION_PROVED_CLOSURE_OPEN_RADIUS9"
        and component_language.get("partition_theorem", {}).get("verdict")
        == "unique-parent-anchor fibers form a full/missing partition"
    )
    l18_same_domain_closure = bool(
        radius3_closure.get("status")
        == "RADIUS3_ELIMINATES_ALL_EXTRA_STATES_WITHIN_L18"
        and radius3_closure.get("elimination", {}).get(
            "all_extra_states_eliminated"
        ) is True
        and radius3_closure.get("elimination", {}).get(
            "conditional_contraction_closure"
        ) is True
    )
    d4_finite_kernel = bool(
        d4_equivalence.get("status")
        == "FAITHFUL_FINITE_KERNEL_CONTEXT_LANGUAGE_OPEN"
        and d4_equivalence.get("finite_kernel_verified") is True
        and d4_equivalence.get("colored_collar_bijection", {}).get(
            "bijective"
        ) is True
        and d4_equivalence.get("component_state_roundtrips", {}).get(
            "all_exact"
        ) is True
        and d4_equivalence.get("normalization", {}).get(
            "exact_inverse_matrices"
        ) is True
        and all(
            row.get("next_physical_patch_exact") is True
            and row.get("inverse_first_exact") is True
            and row.get("inverse_second_exact") is True
            for row in d4_equivalence.get("level_pair_roundtrips", ())
        )
        and d4_equivalence.get("radius2_context_filter", {}).get(
            "radius2_extendible_seed_stars"
        ) == 80
    )
    d4_full_hull = bool(
        d4_finite_kernel
        and d4_equivalence.get("d4_assessment", {}).get(
            "standalone_d4_verified"
        ) is True
    )

    walton = {
        "control": "walton-recognisability-2026",
        "theorem": "Theorem 5.2 and Corollary 5.5",
        "conclusion": (
            "unique composition modulo translation; for return-discrete "
            "tiling spaces, strict injectivity iff the hull has no periodic "
            "elements"
        ),
        "role_in_W3": (
            "post-aperiodicity recognisability theorem and consistency "
            "control, not a standalone proof of aperiodicity"
        ),
        "hypotheses": {
            "W1_compact_FLC_pattern_space": {
                "status": "missing",
                "maps_to": ["C1_legality", "C5_global_consistency"],
                "missing": (
                    "a formal admitted hull and a proof that its complete "
                    "translation patch language has finite local complexity"
                ),
            },
            "W2_Hausdorff_well_separated": {
                "status": "missing",
                "maps_to": ["C1_legality", "C5_global_consistency"],
                "missing": (
                    "a return-discreteness or well-separation witness for "
                    "the encoded whole-plane tiling space"
                ),
            },
            "W3_expansive_linear_automorphism": {
                "status": "partial" if geometry else "missing",
                "maps_to": ["C3_existence_growth"],
                "evidence": (
                    "an exact expanding recurrent rank-four geometry factor "
                    "is verified, but it is not yet encoded as one Euclidean "
                    "linear automorphism L on the admitted hull"
                    if geometry else None
                ),
            },
            "W4_surjective_LD_subdivision": {
                "status": "missing",
                "maps_to": ["C2_closure", "C4_recognizability", "C5_global_consistency"],
                "missing": (
                    "a local-derivation subdivision S:LΩ→Ω defined and "
                    "surjective on every admitted whole-plane tiling"
                ),
            },
            "W5_discrete_nonperiodicity_for_injectivity": {
                "status": "missing",
                "maps_to": ["C4_recognizability", "T3_aperiodicity"],
                "missing": (
                    "an independent proof that the admitted hull contains no "
                    "periodic element; using this hypothesis to prove the same "
                    "claim would be circular"
                ),
            },
        },
    }
    walton["all_hypotheses_verified"] = all(
        row["status"] == "verified" for row in walton["hypotheses"].values()
    )
    walton["standalone_aperiodicity_route"] = False

    direct = {
        "control": "cheritat-spectre-clusters-2024",
        "result": "Corollary 63 (whole-plane, rotations only, unique hierarchy)",
        "scope_warning": (
            "the published argument concerns all whole-plane Tile(1,1) "
            "tilings without reflections, not merely generated patches"
        ),
        "obligations": {
            "D1_formal_all_tilings_domain": {
                "status": (
                    "verified" if unrestricted_l18_entry
                    else "partial" if finite_physical_domain else "missing"
                ),
                "within_edge_to_edge_status": (
                    "verified" if edge_to_edge_l18_entry else "missing"
                ),
                "maps_to": ["C1_legality", "C5_global_consistency"],
                "missing": (
                    None if unrestricted_l18_entry else
                    "the radius-five certificate proves L18 entry for every "
                    "fixed-chirality edge-to-edge tiling, but the unrestricted "
                    "geometric domain still lacks a proof excluding T-junction "
                    "or other non-edge-to-edge contacts"
                    if edge_to_edge_l18_entry else
                    "the exact ancestry-blind language is complete only "
                    "through radius three, not for every admitted whole-plane "
                    "tiling"
                    if finite_physical_domain else
                    "a machine-readable language for every geometrically "
                    "admitted whole-plane tiling under the declared motions"
                ),
            },
            "D2_parent_exists_for_every_tiling": {
                "status": (
                    "verified"
                    if unrestricted_l18_entry and l18_unique_partition
                    else "partial" if finite_physical_domain else "missing"
                ),
                "within_L18_status": (
                    "verified" if l18_unique_partition else "missing"
                ),
                "within_edge_to_edge_status": (
                    "verified"
                    if edge_to_edge_l18_entry and l18_unique_partition
                    else "missing"
                ),
                "maps_to": ["C3_existence_growth", "C4_recognizability"],
                "missing": (
                    None
                    if unrestricted_l18_entry and l18_unique_partition else
                    "the coordinated filter excludes all three extra local "
                    "branches conditional on the recovered parent language, "
                    "but presupposing such a grouping cannot prove that every "
                    "whole-plane tiling has one"
                    if finite_conditional_grouping else
                    "the radius-three audit still has three unobserved local "
                    "branches and does not prove a parent decomposition on "
                    "every whole-plane tiling"
                    if finite_physical_domain else
                    "an exhaustive local-case proof that every admitted tiling "
                    "has a parent decomposition"
                ),
            },
            "D3_parent_grouping_is_unique": {
                "status": (
                    "verified"
                    if unrestricted_l18_entry and l18_unique_partition
                    else "partial" if sampled_forcing else "missing"
                ),
                "within_L18_status": (
                    "verified" if l18_unique_partition else "missing"
                ),
                "within_edge_to_edge_status": (
                    "verified"
                    if edge_to_edge_l18_entry and l18_unique_partition
                    else "missing"
                ),
                "maps_to": ["C4_recognizability"],
                "evidence": (
                    "the unrestricted edge-patch bridge enters L18 and the "
                    "418-case transducer plus radius-six component audit prove "
                    "one unique parent-anchor partition"
                    if unrestricted_l18_entry and l18_unique_partition else
                    "sampled generated interiors have unique composition and "
                    "the coordinated finite filter removes the three extra "
                    "corona types, but neither result proves unique grouping "
                    "over the whole legal hull"
                    if sampled_forcing and finite_conditional_grouping else
                    "sampled generated interiors have unique composition, but "
                    "this does not quantify over the whole legal hull"
                    if sampled_forcing else None
                ),
            },
            "D4_equivalence_chain_is_faithful": {
                "status": (
                    "verified" if d4_full_hull
                    else "partial" if d4_finite_kernel else "missing"
                ),
                "maps_to": ["C1_legality", "C5_global_consistency"],
                "evidence": (
                    "the exact colored-interface/A6-collar bijection, all 17 "
                    "component boundary round trips, unimodular forward and "
                    "inverse normalization, and three consecutive generated "
                    "level-pair physical round trips verify"
                    if d4_finite_kernel else None
                ),
                "missing": (
                    None if d4_full_hull else
                    "prove that every colored parent star arising from the "
                    "full physical L18 hull lies in the faithful transition "
                    "language; the bare 17-state radius-one overlap SFT "
                    "admits 536 output-overlap stars, and 80 of its 3,565 "
                    "seed stars survive one further exact state ring"
                    if d4_finite_kernel else
                    "bijective local encodings between physical tiles, "
                    "collared states and parent objects, including boundaries"
                ),
            },
            "D5_hierarchy_iterates_on_same_domain": {
                "status": (
                    "verified"
                    if unrestricted_l18_entry and l18_same_domain_closure
                    else "partial" if kernel["closed"] else "missing"
                ),
                "within_L18_status": (
                    "verified" if l18_same_domain_closure else "missing"
                ),
                "within_edge_to_edge_status": (
                    "verified"
                    if edge_to_edge_l18_entry and l18_same_domain_closure
                    else "missing"
                ),
                "maps_to": ["C2_closure", "C4_recognizability", "C5_global_consistency"],
                "evidence": (
                    "the unrestricted hull enters L18 and radius-three defect "
                    "elimination proves contraction to exactly the 17 "
                    "generated states"
                    if unrestricted_l18_entry and l18_same_domain_closure else
                    "radius-three defect elimination proves equality with "
                    "the 17-state generated language inside L18, but entry of "
                    "the all-tilings hull into L18 remains open"
                    if l18_same_domain_closure else
                    "the finite state rules close, but closure of their state "
                    "alphabet is not equality with the all-tilings hull"
                    if kernel["closed"] else None
                ),
            },
            "D6_local_inverse_or_uniform_recognition_radius": {
                "status": (
                    "verified"
                    if unrestricted_l18_entry and l18_unique_partition
                    else "partial" if l18_unique_partition else "missing"
                ),
                "within_L18_status": (
                    "verified" if l18_unique_partition else "missing"
                ),
                "within_edge_to_edge_status": (
                    "verified"
                    if edge_to_edge_l18_entry and l18_unique_partition
                    else "missing"
                ),
                "maps_to": ["C4_recognizability"],
                "missing": (
                    None
                    if unrestricted_l18_entry and l18_unique_partition else
                    "the 418-entry radius-three transducer is total and unique "
                    "inside L18, but D1 entry of every admitted geometric "
                    "tiling into L18 remains open"
                    if l18_unique_partition else
                    "a finite all-tilings recognition table proving existence, "
                    "uniqueness and overlap agreement; the present table is "
                    "conditional on already using the recovered parents"
                    if finite_conditional_grouping else
                    "a finite recognition radius or an exhaustive equivalent "
                    "case table for parent ownership"
                ),
            },
            "D7_period_descent_and_scale_growth": {
                "status": "partial" if geometry else "missing",
                "maps_to": ["C3_existence_growth", "T3_aperiodicity"],
                "evidence": (
                    "expanding algebra is known, but no theorem yet links "
                    "every legal hierarchy to shrinking translational periods"
                    if geometry else None
                ),
            },
        },
    }
    direct["all_obligations_verified"] = all(
        row["status"] == "verified" for row in direct["obligations"].values()
    )
    direct["standalone_aperiodicity_route"] = direct[
        "all_obligations_verified"
    ]
    return {
        "claim": "no independent recognisability or aperiodicity theorem yet",
        "walton_theorem_route": walton,
        "direct_local_composition_route": direct,
        "standalone_aperiodicity_route_ready": direct[
            "standalone_aperiodicity_route"
        ],
        "finite_physical_prefix": physical_prefix,
        "finite_parent_overlap_prefix": grouping_prefix,
        "conditional_l18_composition": {
            "unrestricted_contact_bridge": unrestricted_contact_bridge,
            "unrestricted_l18_entry": unrestricted_l18_entry,
            "edge_to_edge_entry": edge_to_edge_l18_entry,
            "unique_parent_partition": l18_unique_partition,
            "same_domain_closure": l18_same_domain_closure,
            "d4_finite_kernel": d4_finite_kernel,
            "d4_full_hull_equivalence": d4_full_hull,
            "scope": (
                "all fixed-chirality straight-Spectre polygonal tilings; "
                "unrestricted contacts reduce to the primitive model and all "
                "complete physical coronas are proved to lie in L18"
                if unrestricted_l18_entry else
                "fixed-chirality edge-to-edge tilings whose complete physical "
                "coronas are now proved to lie in L18"
            ),
        },
    }


def file_sha256(path):
    digest = sha256()
    with open(path, "rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def _pose(value):
    if (not isinstance(value, list) or len(value) != 3
            or value[0] not in (0, 1) or not isinstance(value[1], int)
            or not isinstance(value[2], list) or len(value[2]) != 4
            or not all(isinstance(item, int) for item in value[2])):
        raise ValueError("invalid exact module pose")
    return value[0], value[1], tuple(value[2])


def substitution_from_a6(a6_result):
    """Extract the exact stationary state rules from an A6 v2 result."""
    source = a6_result["radius1_collared_substitution"]
    states = tuple(source["states"])
    rules = []
    for parent in states:
        row = source["rules"].get(str(parent), source["rules"].get(parent))
        if row is None:
            raise ValueError(f"missing rule for state {parent}")
        children = []
        for pose, state in row["children"]:
            parsed = _pose(pose)
            children.append({
                "pose": [parsed[0], parsed[1], list(parsed[2])],
                "state": state,
            })
        rules.append({"parent": parent, "children": children})
    forcing = a6_result["radius1_composition_sat"]
    return {
        "alphabet": list(states),
        "rules": rules,
        "recovered_language_evidence": {
            "source": "sampled Delta level-4/5 interiors",
            "exhaustive_for_all_legal_tilings": False,
            "states_checked": forcing["states_checked"],
            "all_states_checked": forcing["all_states_checked"],
            "complete_context_instances": forcing["complete_context_instances"],
            "unique_instances": forcing["unique_instances"],
            "ambiguous_instances": forcing["ambiguous_instances"],
            "legal_candidates_outside_known_cover": forcing[
                "legal_candidates_outside_known_cover"
            ],
            "unique_composition_on_recovered_language": forcing[
                "unique_composition"
            ],
        },
    }


def incidence_matrix(certificate):
    states = certificate["substitution"]["alphabet"]
    index = {state: i for i, state in enumerate(states)}
    matrix = [[0] * len(states) for _ in states]
    for rule in certificate["substitution"]["rules"]:
        row = matrix[index[rule["parent"]]]
        for child in rule["children"]:
            row[index[child["state"]]] += 1
    return matrix


def primitivity_exponent(matrix):
    """Least positive ``e`` with ``matrix**e`` entrywise positive, or None."""
    size = len(matrix)
    if not size or any(len(row) != size for row in matrix):
        raise ValueError("incidence matrix must be nonempty and square")
    positive = [[i == j for j in range(size)] for i in range(size)]
    adjacency = [[value > 0 for value in row] for row in matrix]
    # Wielandt's bound for a primitive n-by-n nonnegative matrix.
    for exponent in range(1, (size - 1) ** 2 + 2):
        positive = [[
            any(positive[i][k] and adjacency[k][j] for k in range(size))
            for j in range(size)
        ] for i in range(size)]
        if all(all(row) for row in positive):
            return exponent
    return None


def verify_finite_kernel(certificate):
    """Verify schema, deterministic closure and exact matrix primitivity."""
    if certificate.get("schema") != SCHEMA or certificate.get("version") != VERSION:
        raise ValueError("unsupported substitution certificate schema")
    substitution = certificate["substitution"]
    states = tuple(substitution["alphabet"])
    if not states or len(set(states)) != len(states):
        raise ValueError("alphabet must contain distinct states")
    state_set = set(states)
    rules = substitution["rules"]
    if {rule["parent"] for rule in rules} != state_set or len(rules) != len(states):
        raise ValueError("substitution must have exactly one rule per state")
    child_counts = []
    for rule in rules:
        seen_poses = set()
        for child in rule["children"]:
            parsed = _pose(child["pose"])
            if child["state"] not in state_set:
                raise ValueError("child state lies outside the alphabet")
            if parsed in seen_poses:
                raise ValueError("two children occupy the same exact pose")
            seen_poses.add(parsed)
        if not seen_poses:
            raise ValueError("empty substitution rule")
        child_counts.append(len(seen_poses))
    matrix = incidence_matrix(certificate)
    exponent = primitivity_exponent(matrix)
    return {
        "deterministic": True,
        "closed": True,
        "states": len(states),
        "minimum_children": min(child_counts),
        "maximum_children": max(child_counts),
        "primitive": exponent is not None,
        "primitivity_exponent": exponent,
        "incidence_matrix": matrix,
    }


def verify_geometry_kernel(certificate):
    """Verify an optional exact Spectre geometry recurrence payload."""
    stored = certificate.get("geometry_recurrence")
    if stored is None:
        return None
    levels = stored.get("levels_verified")
    if not isinstance(levels, int) or levels < 1:
        raise ValueError("geometry recurrence has invalid level count")
    expected = verify_stationary_recurrence(levels)
    for key in (
        "dimension",
        "levels_verified",
        "matrix",
        "determinant",
        "annihilating_polynomial_constant_first",
        "expanding_linear_factor",
        "expanding_two_level_factor",
        "initial_quad",
        "child_frames",
        "final_quad",
    ):
        if stored.get(key) != expected[key]:
            raise ValueError(f"geometry recurrence mismatch in {key}")
    comparison = stored.get("vendored_table_comparison", {})
    if not (
        comparison.get("all_equal") is True
        and comparison.get("levels") == levels
        and comparison.get("children_per_level") == 8
        and comparison.get("vectors_compared") == 8 * levels
    ):
        raise ValueError("invalid vendored-table comparison claim")
    realized = stored.get("realized_patch_evidence")
    if realized is not None:
        complete_levels = realized.get("complete_levels")
        if not isinstance(complete_levels, int) or complete_levels < 0:
            raise ValueError("invalid realized-patch level count")
        if realized != realized_patch_evidence(complete_levels):
            raise ValueError("stored realized-patch evidence is not reproducible")
    binary_quotient = stored.get("binary_geometry_quotient")
    if binary_quotient != verify_binary_geometry_quotient():
        raise ValueError("invalid full/missing geometry quotient")
    boundary_prefix = stored.get("binary_boundary_prefix")
    if boundary_prefix is not None:
        maximum_level = boundary_prefix.get("maximum_level")
        if not isinstance(maximum_level, int) or maximum_level < 0:
            raise ValueError("invalid binary boundary prefix")
        if boundary_prefix != binary_boundary_prefix(maximum_level):
            raise ValueError("stored binary boundary prefix is not reproducible")
    boundary_recurrence = stored.get("boundary_word_recurrence_evidence")
    if boundary_recurrence is not None:
        maximum_level = boundary_recurrence.get("maximum_level")
        if not isinstance(maximum_level, int) or maximum_level < 1:
            raise ValueError("invalid boundary-word recurrence prefix")
        if boundary_recurrence != boundary_word_recurrence_evidence(maximum_level):
            raise ValueError("stored boundary-word recurrence is not reproducible")
    macro_chains = stored.get("all_level_macro_side_chains")
    if macro_chains != verify_all_level_macro_side_chains():
        raise ValueError("invalid all-level macro-side chain certificate")
    macro_words = stored.get("macro_word_recurrence_evidence")
    if macro_words is not None:
        maximum_level = macro_words.get("maximum_level")
        if not isinstance(maximum_level, int) or maximum_level < 0:
            raise ValueError("invalid macro-word recurrence prefix")
        if macro_words != macro_word_recurrence_evidence(maximum_level):
            raise ValueError("stored macro-word recurrence is not reproducible")
    simplicity = stored.get("boundary_simplicity_prefix")
    if simplicity is not None:
        maximum_level = simplicity.get("maximum_level")
        if not isinstance(maximum_level, int) or maximum_level < 1:
            raise ValueError("invalid boundary-simplicity prefix")
        if simplicity != boundary_simplicity_prefix(maximum_level):
            raise ValueError("stored boundary-simplicity prefix is not reproducible")
    return {
        "exact_stationary_recurrence": True,
        "dimension": expected["dimension"],
        "unimodular": abs(expected["determinant"]) == 1,
        "levels_verified_against_vendor": levels,
        "realized_patch_levels": (
            realized["complete_levels"] if realized is not None else None
        ),
        "realized_patches_exactly_legal": (
            realized["patches_checked"] if realized is not None else 0
        ),
        "geometric_support_types": binary_quotient["geometric_support_types"],
        "abstract_disk_prefix_through_level": (
            boundary_prefix["maximum_level"] if boundary_prefix else None
        ),
        "boundary_word_recurrence_checked_through_level": (
            boundary_recurrence["maximum_level"] if boundary_recurrence else None
        ),
        "all_level_macro_side_endpoints": macro_chains[
            "all_level_endpoint_identity"
        ],
        "macro_word_recurrence_checked_through_level": (
            macro_words["maximum_level"] if macro_words else None
        ),
        "exact_simple_boundary_prefix_through_level": (
            simplicity["maximum_level"] if simplicity else None
        ),
        "expanding_linear_factor": expected["expanding_linear_factor"],
        "expanding_two_level_factor": expected["expanding_two_level_factor"],
    }


def audit_obligations(certificate):
    """Return an honest C1--C5 audit; missing evidence stays explicitly red."""
    kernel = verify_finite_kernel(certificate)
    geometry = verify_geometry_kernel(certificate)
    evidence = certificate["substitution"]["recovered_language_evidence"]
    sampled_forcing = (
        evidence.get("all_states_checked")
        and evidence.get("unique_composition_on_recovered_language")
        and evidence.get("ambiguous_instances") == 0
        and evidence.get("legal_candidates_outside_known_cover") == 0
    )
    recognisability = recognisability_crosswalk(
        certificate, kernel=kernel, geometry=geometry
    )
    obligations = {
        "C1_legality": {
            "status": "partial" if geometry else "missing",
            "exact_recursive_geometry": bool(geometry),
            "reason": (
                "exact recursive child geometry and a finite prefix of realized "
                "leaf patches are verified, but no boundary-induction proof yet "
                "extends legality to every level/collared state"
                if geometry else
                "collared states do not yet carry exact realized metatile supports"
            ),
        },
        "C2_closure": {
            "status": "verified",
            "reason": "one deterministic rule per state; every child state is in the alphabet",
        },
        "C3_existence_growth": {
            "status": "partial",
            "primitive": kernel["primitive"],
            "primitivity_exponent": kernel["primitivity_exponent"],
            "exact_expanding_geometry_recurrence": bool(geometry),
            "expanding_two_level_factor": (
                geometry["expanding_two_level_factor"] if geometry else None
            ),
            "missing": (
                "a certified inball-radius growth witness linking the exact "
                "recurrence to realized metatile supports"
                if geometry else
                "certified metatile supports and an inball-radius growth witness"
            ),
        },
        "C4_recognizability": {
            "status": "partial" if sampled_forcing else "missing",
            "sampled_language_unique": bool(sampled_forcing),
            "missing": (
                "D1/D2/D3/D5/D6 are verified on the unrestricted fixed-"
                "chirality hull; D4 now has an exact finite equivalence "
                "kernel, but equality of its 80 surviving radius-two context "
                "seeds with the physical-derived hull remains open; Walton cannot "
                "replace it without independently assuming the absence of "
                "periodic tilings"
                if recognisability["conditional_l18_composition"][
                    "unrestricted_l18_entry"
                ] else
                "D1/D2/D3/D5/D6 are verified for the fixed-chirality "
                "edge-to-edge domain, but reduction of the unrestricted "
                "geometric hull to edge-to-edge contacts and D4 faithful hull "
                "equivalence are open; Walton cannot fill this gap without "
                "independently assuming the absence of periodic tilings"
                if recognisability["conditional_l18_composition"][
                    "edge_to_edge_entry"
                ] else
                "D2/D3/D5/D6 are verified inside L18, but D1 entry into L18 "
                "and D4 faithful hull equivalence are open; Walton cannot fill "
                "this gap without independently assuming the absence of "
                "periodic tilings"
                if recognisability["conditional_l18_composition"][
                    "same_domain_closure"
                ] else
                "the direct route lacks total and unique parent grouping over "
                "the formal all-tilings hull; Walton cannot fill this gap "
                "without independently assuming the absence of periodic tilings"
            ),
        },
        "C5_global_consistency": {
            "status": (
                "partial" if recognisability["finite_physical_prefix"]
                else "missing"
            ),
            "reason": (
                "the unrestricted edge-patch bridge, radius-five L18 entry, "
                "unique parent partition and 17-state contraction closure all "
                "verify; D4's 17-state bijection and exact scale round trips "
                "also verify, but its surviving context language has not yet "
                "been proved equal to the physical-derived hull"
                if recognisability["conditional_l18_composition"][
                    "unrestricted_l18_entry"
                ] else
                "the radius-five ancestry-free certificate proves L18 entry, "
                "the parent partition is total and unique, and contraction "
                "closes to the 17 generated states throughout the declared "
                "edge-to-edge domain; reduction of unrestricted contacts and "
                "D4 faithful hull equivalence remain unproved"
                if recognisability["conditional_l18_composition"][
                    "edge_to_edge_entry"
                ] else
                "inside L18 the parent partition is total and unique and the "
                "radius-three defect certificate closes contraction to the "
                "17 generated states; D1 entry into L18 and D4 faithful hull "
                "equivalence remain unproved"
                if recognisability["conditional_l18_composition"][
                    "same_domain_closure"
                ] else
                "coordinated parent-overlap removes all three extra physical "
                "corona types and leaves the 18 generated controls, but only "
                "conditional on the recovered 9/8 parent language; parent "
                "existence, uniqueness and equality with the all-tilings hull "
                "remain unproved"
                if recognisability["finite_parent_overlap_prefix"] else
                "the ancestry-blind physical language is complete through "
                "radius three, but three locally extendable types remain "
                "outside the observed substitution language and no finite "
                "equality-with-hull theorem is proved"
                if recognisability["finite_physical_prefix"] else
                "no exhaustive parent-overlap/gluing table over the legal language"
            ),
        },
    }
    return {
        "finite_kernel": kernel,
        "geometry_kernel": geometry,
        "recognisability_crosswalk": recognisability,
        "obligations": obligations,
        "theorem_ready": all(
            row["status"] == "verified" for row in obligations.values()
        ),
        "blocking_obligations": [
            name for name, row in obligations.items() if row["status"] != "verified"
        ],
    }


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
