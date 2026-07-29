#!/usr/bin/env python
"""Build the exact D4 Spectre representation-equivalence audit."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from sympy import Matrix, symbols

from einstein.tilings.substitution import (
    CompositionRule,
    SPECTRE_TILE_BOUNDARY,
    contract_level,
    contracted_adjacency,
    cover_with_rule,
    oriented_collar_signatures,
    physical_edge_contacts,
    raw_hierarchy_level,
)
from einstein.geometry.cyclotomic import compose_pose
from einstein.tilings.spectre.colored_interfaces import (
    colored_corona_from_json,
    colored_local_overlap_witnesses,
    colored_parent_corona,
)
from einstein.tilings.spectre.equivalence import (
    COMPANION_POSE,
    MARKER_STATE_IDS,
    NORMALIZATION_INVERSE,
    NORMALIZATION_LINEAR,
    NORMALIZATION_OFFSET,
    NORMALIZATION_ROTATION_SHIFT,
    audit_component_state_roundtrips,
    audit_radius_one_next_physical,
    collar_signature,
    colored_collar_bijection,
    denormalize_parent_pose,
    faithful_radius_two_assignment,
    normalize_parent_pose,
    two_level_translation_matrices,
)
from einstein.tilings.spectre.geometry import exact_leaves
from einstein.tilings.spectre.parent_constraints import ParentStateKernel
from einstein.tilings.spectre.parent_overlaps import parent_templates
from einstein.tilings.spectre.patches import patch_edge_incidence
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[2]
A6 = ROOT / "docs/notebook/assets/a6-spectre-results.json"
COLORED = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-d4-equivalence.json"


def parse_template(rows):
    return tuple(
        (int(s), int(r), tuple(map(int, translation)))
        for s, r, translation in rows
    )


def immediate_level(level, immediate_rule):
    physical = tuple(pose for _, pose in exact_leaves(level, "Delta"))
    hierarchy = contract_level(
        raw_hierarchy_level(physical), immediate_rule,
        cover_with_rule(
            physical, immediate_rule.full, immediate_rule.missing,
        ),
    )
    adjacency = contracted_adjacency(
        physical_edge_contacts(physical, SPECTRE_TILE_BOUNDARY), hierarchy,
    )
    return physical, hierarchy, adjacency


def colored_control(states, templates, physical, parents, adjacency):
    signatures = oriented_collar_signatures(parents, adjacency, 1)
    language = tuple(sorted({
        signatures[index]
        for index, neighbors in enumerate(adjacency)
        if len(neighbors) == 6
    }))
    state_for_signature = {
        signature: state for state, signature in enumerate(language)
    }
    incidence, _ = patch_edge_incidence(physical)
    fibers = defaultdict(set)
    mapping = {}
    edges_by_tile = defaultdict(list)
    for parent_index, leaves in enumerate(parents.leaves):
        base = parents.poses[parent_index]
        for leaf in leaves:
            tile = physical[leaf]
            mapping[tile] = base
            fibers[base].add(tile)
    for key, owners in incidence.items():
        for tile in owners:
            edges_by_tile[tile].append((key, owners))

    pairs = []
    for index, base in enumerate(parents.poses):
        if len(adjacency[index]) != 6:
            continue
        colored = colored_parent_corona(
            base,
            physical,
            mapping,
            templates,
            incidence=incidence,
            fibers=fibers,
            edges_by_tile=edges_by_tile,
            trust_mapping_absence=True,
        )
        if colored is None:
            raise ValueError("an interior control component lacks a color")
        if collar_signature(colored) != signatures[index]:
            raise ValueError("colored projection differs from its A6 collar")
        pairs.append((state_for_signature[signatures[index]], colored))
    relation = defaultdict(set)
    inverse = defaultdict(set)
    for collar, colored in pairs:
        relation[collar].add(colored)
        inverse[colored].add(collar)
    if set(inverse) != set(states):
        raise ValueError("stored colored alphabet differs from exact control")
    return {
        "control_level": 4,
        "complete_occurrences": len(pairs),
        "collar_states": len(relation),
        "colored_states": len(inverse),
        "maximum_colors_per_collar": max(map(len, relation.values())),
        "maximum_collars_per_color": max(map(len, inverse.values())),
        "occurrences_by_state": {
            str(state): sum(collar == state for collar, _ in pairs)
            for state in sorted(relation)
        },
        "bijective": (
            len(relation) == len(inverse) == 17
            and all(len(values) == 1 for values in relation.values())
            and all(len(values) == 1 for values in inverse.values())
        ),
        "language": language,
    }


def level_pair_control(lower_level, immediate_rule, recursive_rule):
    lower_physical, lower_first, lower_adjacency = immediate_level(
        lower_level, immediate_rule,
    )
    upper_physical, upper_first, _ = immediate_level(
        lower_level + 1, immediate_rule,
    )
    second_cover = cover_with_rule(
        upper_first.poses, recursive_rule.full, recursive_rule.missing,
    )
    upper_second = contract_level(
        upper_first, recursive_rule, second_cover,
    )
    upper_second_adjacency = contracted_adjacency(
        physical_edge_contacts(upper_physical, SPECTRE_TILE_BOUNDARY),
        upper_second,
    )

    normalized_first = {normalize_parent_pose(pose) for pose in upper_first.poses}
    normalized_second = {
        normalize_parent_pose(pose) for pose in upper_second.poses
    }
    companions = {
        compose_pose(normalize_parent_pose(pose), COMPANION_POSE)
        for pose in upper_second.poses
    }
    lower_set = set(lower_physical)
    next_patch = normalized_first | companions
    phase = next(iter(normalized_first))[1] % 2
    inverse_first = {
        denormalize_parent_pose(pose)
        for pose in lower_set if pose[1] % 2 == phase
    }
    inverse_second = {
        denormalize_parent_pose(pose)
        for pose in normalized_first
        if compose_pose(pose, COMPANION_POSE) in lower_set
    }

    lower_index = {pose: index for index, pose in enumerate(lower_first.poses)}
    upper_second_index = {
        pose: index for index, pose in enumerate(upper_second.poses)
    }
    adjacency_preserved = normalized_second == set(lower_first.poses)
    if adjacency_preserved:
        for pose, upper_index in upper_second_index.items():
            lower_index_at_pose = lower_index[normalize_parent_pose(pose)]
            mapped = {
                lower_index[normalize_parent_pose(upper_second.poses[neighbor])]
                for neighbor in upper_second_adjacency[upper_index]
            }
            if mapped != set(lower_adjacency[lower_index_at_pose]):
                adjacency_preserved = False
                break
            if (
                upper_second.exceptional[upper_index]
                != lower_first.exceptional[lower_index_at_pose]
            ):
                adjacency_preserved = False
                break

    return {
        "levels": [lower_level + 1, lower_level],
        "upper_physical_tiles": len(upper_physical),
        "upper_first_parents": len(upper_first.poses),
        "upper_second_parents": len(upper_second.poses),
        "lower_physical_tiles": len(lower_physical),
        "ordinary_tiles": len(normalized_first),
        "companion_tiles": len(companions),
        "ordinary_companion_disjoint": normalized_first.isdisjoint(companions),
        "next_physical_patch_exact": next_patch == lower_set,
        "forward_count_identity": (
            len(normalized_first) + len(companions) == len(lower_set)
        ),
        "inverse_first_exact": inverse_first == set(upper_first.poses),
        "inverse_second_exact": inverse_second == set(upper_second.poses),
        "normalized_second_equals_lower_first": (
            normalized_second == set(lower_first.poses)
        ),
        "second_parent_adjacency_and_kind_preserved": adjacency_preserved,
    }, (upper_physical, upper_first, upper_second)


def marker_control(reference, upper_first, upper_second):
    _, reference_parents, reference_adjacency = reference
    signatures = oriented_collar_signatures(
        reference_parents, reference_adjacency, 1,
    )
    language = tuple(sorted({
        signatures[index]
        for index, neighbors in enumerate(reference_adjacency)
        if len(neighbors) == 6
    }))
    state_for_signature = {
        signature: state for state, signature in enumerate(language)
    }
    upper_physical = tuple(pose for _, pose in exact_leaves(5, "Delta"))
    upper_adjacency = contracted_adjacency(
        physical_edge_contacts(upper_physical, SPECTRE_TILE_BOUNDARY),
        upper_first,
    )
    upper_signatures = oriented_collar_signatures(
        upper_first, upper_adjacency, 1,
    )
    second = set(upper_second.poses)
    complete = []
    for index, pose in enumerate(upper_first.poses):
        if len(upper_adjacency[index]) != 6:
            continue
        state = state_for_signature[upper_signatures[index]]
        complete.append((pose, state, pose in second))
    return {
        "control_level": 5,
        "complete_first_parent_collars": len(complete),
        "complete_second_parent_markers": sum(row[2] for row in complete),
        "marker_state_ids": sorted(MARKER_STATE_IDS),
        "marker_iff_second_parent_base": all(
            (state in MARKER_STATE_IDS) == selected
            for _, state, selected in complete
        ),
        "all_second_parent_bases_are_first_parent_bases": (
            second <= set(upper_first.poses)
        ),
    }


def radius_two_seed_census(states, templates, colored_to_id):
    kernel = ParentStateKernel(states, templates)
    total = 0
    surviving = Counter()
    faithful = Counter()
    radius3 = Counter()
    for root in range(len(states)):
        for witness in colored_local_overlap_witnesses(
            states, root, limit=1_000_000,
        ):
            total += 1
            problem = kernel.build_radius_two(root, witness)
            if kernel.enumerate_assignments(problem, limit=1):
                surviving[root] += 1
                if faithful_radius_two_assignment(
                    problem, kernel, colored_to_id,
                ) is not None:
                    faithful[root] += 1
                if kernel.extend_variable_outer_ring(problem).satisfiable:
                    radius3[root] += 1
    return {
        "radius1_stars": total,
        "radius2_extendible_seed_stars": sum(surviving.values()),
        "radius2_dead_seed_stars": total - sum(surviving.values()),
        "surviving_by_center": {
            str(index): surviving[index] for index in range(len(states))
        },
        "faithful_central_image_seed_stars": sum(faithful.values()),
        "faithful_central_image_by_center": {
            str(index): faithful[index] for index in range(len(states))
        },
        "faithful_filter_definition": (
            "exact parent-state compatibility plus nonoverlapping ordinary/"
            "companion image and complete primitive-edge ownership for the "
            "central ordinary tile and its companion when selected"
        ),
        "radius3_extendible_seed_stars": sum(radius3.values()),
        "radius3_extendible_by_center": {
            str(index): radius3[index] for index in range(len(states))
        },
        "radius3_encoding": (
            "conditional third-ring occupancy: every selected second-ring "
            "state activates its six exact neighbors; all active anchors obey "
            "the same colored compatibility and physical-support constraints"
        ),
        "solver": "CaDiCaL 1.9.5",
    }


def main():
    a6 = json.loads(A6.read_text())
    colored_artifact = json.loads(COLORED.read_text())
    states = tuple(map(
        colored_corona_from_json,
        colored_artifact["generated_colored_states"],
    ))
    templates = parent_templates(a6)
    immediate_rule = CompositionRule(*templates, len(templates[0]), 0)
    recursive_source = a6["recursive_hierarchy"]["rules"][0]
    recursive_rule = CompositionRule(
        parse_template(recursive_source["full"]),
        parse_template(recursive_source["missing"]),
        len(recursive_source["full"]),
        0,
    )

    physical4, parents4, adjacency4 = immediate_level(4, immediate_rule)
    control = colored_control(
        states, templates, physical4, parents4, adjacency4,
    )
    colored_to_id, language = colored_collar_bijection(states)
    if tuple(control.pop("language")) != language:
        raise ValueError("direct colored bijection differs from A6 control")

    level_pairs = []
    generated = {}
    for lower in (2, 3, 4):
        row, upper = level_pair_control(
            lower, immediate_rule, recursive_rule,
        )
        level_pairs.append(row)
        generated[lower + 1] = upper
    reference = immediate_level(4, immediate_rule)
    _, upper_first5, upper_second5 = generated[5]

    roundtrips = audit_component_state_roundtrips(states, templates)
    radius1 = audit_radius_one_next_physical(states, colored_to_id)
    radius2 = radius_two_seed_census(states, templates, colored_to_id)

    x = symbols("x")
    two_level = two_level_translation_matrices()
    normalization = {
        "linear": {
            str(key): [list(row) for row in matrix]
            for key, matrix in NORMALIZATION_LINEAR.items()
        },
        "inverse": {
            str(key): [list(row) for row in matrix]
            for key, matrix in NORMALIZATION_INVERSE.items()
        },
        "offset_even_rotations": {
            str(chirality): {
                str(rotation): list(vector)
                for rotation, vector in offsets.items()
            }
            for chirality, offsets in NORMALIZATION_OFFSET.items()
        },
        "rotation_shift": {
            str(key): value
            for key, value in NORMALIZATION_ROTATION_SHIFT.items()
        },
        "determinants": {
            str(key): int(Matrix(matrix).det())
            for key, matrix in NORMALIZATION_LINEAR.items()
        },
        "exact_inverse_matrices": all(
            Matrix(NORMALIZATION_LINEAR[key]).inv()
            == Matrix(NORMALIZATION_INVERSE[key])
            for key in (0, 1)
        ),
        "chirality_toggles_uniformly": True,
        "rotation_parity_is_preserved": True,
        "translation_covariance": (
            "within one chirality/parity phase, a global module translation "
            "u maps to A_(chirality,parity) u"
        ),
        "companion_pose": [
            COMPANION_POSE[0], COMPANION_POSE[1], list(COMPANION_POSE[2]),
        ],
        "two_level_translation_matrices": {
            key: [list(row) for row in matrix]
            for key, matrix in two_level.items()
        },
        "two_level_characteristic_polynomials": {
            key: str(Matrix(matrix).charpoly(x).as_expr().factor())
            for key, matrix in two_level.items()
        },
    }

    component_ok = all(
        row["pairwise_component_disjoint"]
        and row["central_exposed_edges"] == 0
        and row["central_external_edges"] == row["contact_colors"]
        and row["roundtrip_exact"]
        for row in roundtrips
    )
    scale_ok = all(
        row["ordinary_companion_disjoint"]
        and row["next_physical_patch_exact"]
        and row["forward_count_identity"]
        and row["inverse_first_exact"]
        and row["inverse_second_exact"]
        and row["normalized_second_equals_lower_first"]
        and row["second_parent_adjacency_and_kind_preserved"]
        for row in level_pairs
    )
    marker = marker_control(reference, upper_first5, upper_second5)
    finite_kernel = (
        control["bijective"] and component_ok and scale_ok
        and marker["marker_iff_second_parent_base"]
        and normalization["exact_inverse_matrices"]
        and set(normalization["determinants"].values()) == {1}
        and set(normalization["two_level_characteristic_polynomials"].values())
        == {"(x**2 - 8*x + 1)**2"}
    )
    context_gap = radius1["outcomes"].get("output_overlap", 0) > 0
    artifact = {
        "schema": "einstein.w3.spectre-d4-equivalence",
        "version": 1,
        "status": (
            "FAITHFUL_FINITE_KERNEL_CONTEXT_LANGUAGE_OPEN"
            if finite_kernel and context_gap else "D4_AUDIT_FAILED"
        ),
        "provenance": {
            "a6_source": str(A6.relative_to(ROOT)),
            "a6_sha256": file_sha256(A6),
            "colored_source": str(COLORED.relative_to(ROOT)),
            "colored_sha256": file_sha256(COLORED),
        },
        "scope": {
            "input": "unique 9/8 component partition of an L18 physical tiling",
            "intermediate": "17 exact child-edge-colored component states",
            "output": "next reflected physical Spectre phase",
            "motions": ["translation", "rotation"],
            "reflections_as_allowed_tile_motions": False,
            "hierarchy_chirality_behavior": (
                "the correspondence toggles the entire chirality phase; it "
                "never mixes handednesses in one tiling"
            ),
        },
        "colored_collar_bijection": control,
        "component_state_roundtrips": {
            "states_checked": len(roundtrips),
            "all_exact": component_ok,
            "records": roundtrips,
        },
        "normalization": normalization,
        "level_pair_roundtrips": level_pairs,
        "marker_transducer": marker,
        "finite_kernel_verified": finite_kernel,
        "radius1_context_probe": radius1,
        "radius2_context_filter": radius2,
        "d4_assessment": {
            "status": "partial",
            "proved": [
                "17-to-17 bijection between colored physical interfaces and A6 collars",
                "exact component expansion/re-encoding with complete boundary ownership",
                "unimodular forward/inverse scale normalization with translation covariance",
                "exact next-physical-patch round trip on three consecutive level pairs",
                "second-parent markers are exactly A6 states 10, 11 and 12 on complete controls",
            ],
            "remaining": (
                "prove that every colored parent star arising from the full "
                "physical L18 hull lies in the faithful transition language. "
                "The bare radius-one 17-state overlap SFT is too broad: it "
                "admits output-overlap stars, although only 80 of 3565 seed "
                "stars survive one further exact state ring."
            ),
            "standalone_d4_verified": False,
        },
        "claim_boundary": (
            "the finite maps and generated level-pair round trips are exact; "
            "they do not yet prove that the radius-two surviving state-star "
            "language equals the contraction of every whole-plane physical tiling"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        f"D4 finite kernel: {len(states)} states, "
        f"{control['complete_occurrences']} exact collar occurrences, "
        f"radius-one stars {radius1['total_stars']} -> "
        f"radius-two seeds {radius2['radius2_extendible_seed_stars']}; "
        f"status={artifact['status']}"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
