#!/usr/bin/env python
"""Independent replay of the W3 Spectre D4 finite equivalence kernel."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from einstein.repository import repository_root

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
)
from einstein.tilings.spectre.equivalence import (
    COMPANION_POSE,
    MARKER_STATE_IDS,
    NORMALIZATION_INVERSE,
    NORMALIZATION_LINEAR,
    audit_component_state_roundtrips,
    audit_radius_one_next_physical,
    collar_signature,
    colored_collar_bijection,
    denormalize_parent_pose,
    normalize_parent_pose,
    two_level_translation_matrices,
)
from einstein.tilings.spectre.geometry import exact_leaves
from einstein.tilings.spectre.parent_constraints import ParentStateKernel
from einstein.tilings.spectre.parent_overlaps import parent_templates
from einstein.tilings.spectre.certificates import file_sha256


ROOT = repository_root(Path(__file__))
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-d4-equivalence.json"


def template(rows):
    return tuple((s, r, tuple(t)) for s, r, t in rows)


def immediate(physical, rule):
    level = contract_level(
        raw_hierarchy_level(physical), rule,
        cover_with_rule(physical, rule.full, rule.missing),
    )
    adjacency = contracted_adjacency(
        physical_edge_contacts(physical, SPECTRE_TILE_BOUNDARY), level,
    )
    return level, adjacency


def main():
    artifact = json.loads(OUTPUT.read_text())
    assert artifact["schema"] == "einstein.w3.spectre-d4-equivalence"
    assert artifact["version"] == 1
    provenance = artifact["provenance"]
    for prefix in ("a6", "colored"):
        path = ROOT / provenance[f"{prefix}_source"]
        assert file_sha256(path) == provenance[f"{prefix}_sha256"]
    a6 = json.loads((ROOT / provenance["a6_source"]).read_text())
    colored = json.loads((ROOT / provenance["colored_source"]).read_text())
    states = tuple(map(
        colored_corona_from_json, colored["generated_colored_states"],
    ))
    colored_to_id, language = colored_collar_bijection(states)
    assert len(states) == len(language) == 17

    immediate_templates = parent_templates(a6)
    immediate_rule = CompositionRule(
        immediate_templates[0], immediate_templates[1],
        len(immediate_templates[0]), 0,
    )
    recursive = a6["recursive_hierarchy"]["rules"][0]
    recursive_rule = CompositionRule(
        template(recursive["full"]), template(recursive["missing"]),
        len(recursive["full"]), 0,
    )

    roundtrips = audit_component_state_roundtrips(
        states, immediate_templates,
    )
    assert len(roundtrips) == 17
    assert all(
        row["pairwise_component_disjoint"]
        and row["central_exposed_edges"] == 0
        and row["central_external_edges"] == row["contact_colors"]
        and row["roundtrip_exact"]
        for row in roundtrips
    )

    # Reconstruct the A6 numbering directly from the exact level-four parent
    # collars; no stored D4 relation table is trusted.
    physical4 = tuple(pose for _, pose in exact_leaves(4, "Delta"))
    parents4, adjacency4 = immediate(physical4, immediate_rule)
    signatures4 = oriented_collar_signatures(parents4, adjacency4, 1)
    control_language = tuple(sorted({
        signatures4[index]
        for index, neighbors in enumerate(adjacency4)
        if len(neighbors) == 6
    }))
    assert control_language == language
    occurrences = Counter(
        control_language.index(signatures4[index])
        for index, neighbors in enumerate(adjacency4)
        if len(neighbors) == 6
    )
    stored_bijection = artifact["colored_collar_bijection"]
    assert sum(occurrences.values()) == stored_bijection["complete_occurrences"] == 310
    assert {str(key): value for key, value in sorted(occurrences.items())} == (
        stored_bijection["occurrences_by_state"]
    )
    assert stored_bijection["bijective"]

    # Cold level-pair replay of the forward and inverse patch identity.
    replay_rows = []
    upper_five = None
    for lower_level in (2, 3, 4):
        lower_physical = tuple(
            pose for _, pose in exact_leaves(lower_level, "Delta")
        )
        upper_physical = tuple(
            pose for _, pose in exact_leaves(lower_level + 1, "Delta")
        )
        lower_first, lower_adjacency = immediate(
            lower_physical, immediate_rule,
        )
        upper_first, _ = immediate(upper_physical, immediate_rule)
        upper_second = contract_level(
            upper_first, recursive_rule,
            cover_with_rule(
                upper_first.poses,
                recursive_rule.full,
                recursive_rule.missing,
            ),
        )
        if lower_level == 4:
            upper_five = upper_physical, upper_first, upper_second
        ordinary = {normalize_parent_pose(pose) for pose in upper_first.poses}
        companions = {
            compose_pose(normalize_parent_pose(pose), COMPANION_POSE)
            for pose in upper_second.poses
        }
        lower_set = set(lower_physical)
        assert ordinary.isdisjoint(companions)
        assert ordinary | companions == lower_set
        phase = next(iter(ordinary))[1] % 2
        assert {
            denormalize_parent_pose(pose)
            for pose in lower_set if pose[1] % 2 == phase
        } == set(upper_first.poses)
        assert {
            denormalize_parent_pose(pose)
            for pose in ordinary
            if compose_pose(pose, COMPANION_POSE) in lower_set
        } == set(upper_second.poses)

        normalized_second = {
            normalize_parent_pose(pose) for pose in upper_second.poses
        }
        assert normalized_second == set(lower_first.poses)
        upper_adjacency = contracted_adjacency(
            physical_edge_contacts(upper_physical, SPECTRE_TILE_BOUNDARY),
            upper_second,
        )
        li = {pose: index for index, pose in enumerate(lower_first.poses)}
        for index, pose in enumerate(upper_second.poses):
            mapped_index = li[normalize_parent_pose(pose)]
            assert {
                li[normalize_parent_pose(upper_second.poses[neighbor])]
                for neighbor in upper_adjacency[index]
            } == set(lower_adjacency[mapped_index])
            assert (
                upper_second.exceptional[index]
                == lower_first.exceptional[mapped_index]
            )
        replay_rows.append((
            lower_level + 1, lower_level, len(ordinary), len(companions),
        ))
    assert upper_five is not None
    assert replay_rows == [(3, 2, 63, 8), (4, 3, 496, 63), (5, 4, 3905, 496)]

    # In the complete level-five collar control the selected second-parent
    # bases are exactly states 10/11/12.
    upper_physical, upper_first, upper_second = upper_five
    upper_adjacency = contracted_adjacency(
        physical_edge_contacts(upper_physical, SPECTRE_TILE_BOUNDARY),
        upper_first,
    )
    upper_signatures = oriented_collar_signatures(
        upper_first, upper_adjacency, 1,
    )
    second = set(upper_second.poses)
    marker_rows = [
        (control_language.index(upper_signatures[index]), pose in second)
        for index, pose in enumerate(upper_first.poses)
        if len(upper_adjacency[index]) == 6
    ]
    assert len(marker_rows) == 3109
    assert sum(selected for _, selected in marker_rows) == 337
    assert all((state in MARKER_STATE_IDS) == selected
               for state, selected in marker_rows)

    x = symbols("x")
    for chirality in (0, 1):
        assert Matrix(NORMALIZATION_LINEAR[chirality]).det() == 1
        assert Matrix(NORMALIZATION_LINEAR[chirality]).inv() == Matrix(
            NORMALIZATION_INVERSE[chirality]
        )
    assert {
        str(Matrix(matrix).charpoly(x).as_expr().factor())
        for matrix in two_level_translation_matrices().values()
    } == {"(x**2 - 8*x + 1)**2"}

    radius1 = audit_radius_one_next_physical(states, colored_to_id)
    stored_radius1 = artifact["radius1_context_probe"]
    assert radius1["total_stars"] == 3565
    assert radius1["outcomes"] == {
        "central_ordinary_not_buffered": 410,
        "central_ordinary_valid": 2619,
        "output_overlap": 536,
    }
    assert radius1["outcomes"] == stored_radius1["outcomes"]
    assert {
        str(key): value for key, value in radius1["total_by_center"].items()
    } == stored_radius1["total_by_center"]
    assert radius1["central_signature_count_by_state"] == (
        stored_radius1["central_signature_count_by_state"]
    )

    # Independent one-solution SAT replay for every pinned radius-one seed.
    kernel = ParentStateKernel(states, immediate_templates)
    surviving = Counter()
    checked = 0
    for root in range(17):
        for witness in colored_local_overlap_witnesses(
            states, root, limit=1_000_000,
        ):
            checked += 1
            if kernel.enumerate_assignments(
                kernel.build_radius_two(root, witness), limit=1,
            ):
                surviving[root] += 1
    assert checked == 3565
    assert sum(surviving.values()) == 80
    assert {
        str(index): surviving[index] for index in range(17)
    } == artifact["radius2_context_filter"]["surviving_by_center"]
    assert artifact["finite_kernel_verified"]
    assert artifact["d4_assessment"]["status"] == "partial"
    assert not artifact["d4_assessment"]["standalone_d4_verified"]
    assert artifact["status"] == "FAITHFUL_FINITE_KERNEL_CONTEXT_LANGUAGE_OPEN"
    print(
        "PASS D4 finite equivalence kernel: 17<->17 states; "
        "3 exact level-pair round trips; 3565->80 context seeds; "
        "standalone D4 remains partial"
    )


if __name__ == "__main__":
    main()
