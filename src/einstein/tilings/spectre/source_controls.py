"""Reusable exact controls derived from retained Spectre source artifacts."""

from __future__ import annotations

import ast

from einstein.geometry.cyclotomic import relative_pose
from einstein.tilings.spectre.geometry import exact_leaves
from einstein.tilings.spectre.parent_interfaces import (
    local_overlap_witnesses,
    prune_locally_unsupported,
    reciprocal_domains,
)
from einstein.tilings.spectre.parent_overlaps import parent_templates
from einstein.tilings.spectre.patches import enumerate_first_coronas, pose_json
from einstein.tilings.substitution import (
    CompositionRule,
    SPECTRE_TILE_BOUNDARY,
    contract_level,
    contracted_adjacency,
    cover_with_rule,
    physical_edge_contacts,
    raw_hierarchy_level,
)


def physical_corona_language(physical_artifact):
    """Decode the retained 18-corona language from its exact artifact."""

    analysis = physical_artifact["analysis"]
    coronas = enumerate_first_coronas()
    return tuple(
        coronas[index]
        for index in analysis["substitution_control"]["observed_indices"]
    )


def generated_parent_coronas(a6_result):
    """Reconstruct generated six-neighbor parent coronas at source level 5."""

    full, missing = parent_templates(a6_result)
    rule = CompositionRule(full, missing, len(full), 0)
    poses = tuple(pose for _, pose in exact_leaves(5, "Delta"))
    raw = raw_hierarchy_level(poses)
    cover = cover_with_rule(poses, full, missing)
    parents = contract_level(raw, rule, cover)
    contacts = physical_edge_contacts(poses, SPECTRE_TILE_BOUNDARY)
    adjacency = contracted_adjacency(contacts, parents)
    return tuple(
        sorted(
            {
                tuple(
                    sorted(
                        relative_pose(parents.poses[index], parents.poses[other])
                        for other in neighbors
                    )
                )
                for index, neighbors in enumerate(adjacency)
                if len(neighbors) == 6
            }
        )
    )


def analyze_parent_interfaces(component_artifact, a6_result):
    """Recompute the uncolored contracted parent-corona support audit."""

    generated = generated_parent_coronas(a6_result)
    extras = tuple(
        ast.literal_eval(signature)
        for signature in component_artifact["contraction_audit"][
            "nongenerated_signature_histogram_through_radius7"
        ]
    )
    states = (*generated, *extras)
    if len(states) != len(set(states)):
        raise ValueError("generated and extra parent states overlap")
    rows = []
    for index, state in enumerate(states):
        domains = reciprocal_domains(states, index)
        witnesses = local_overlap_witnesses(states, index, limit=2)
        rows.append(
            {
                "state": index,
                "kind": "generated" if index < len(generated) else "extra",
                "corona": [pose_json(pose) for pose in state],
                "reciprocal_domain_sizes": [len(domain) for domain in domains],
                "triangle_consistent_witnesses_capped_at_2": [
                    list(witness) for witness in witnesses
                ],
            }
        )
    alive, rounds = prune_locally_unsupported(states)
    return {
        "generated_states": len(generated),
        "extra_states": len(extras),
        "total_states": len(states),
        "records": rows,
        "support_pruning_rounds": [list(row) for row in rounds],
        "surviving_states": list(alive),
        "surviving_extra_states": [
            index - len(generated)
            for index in alive
            if index >= len(generated)
        ],
        "verdict": "uncolored-reciprocal-triangle-language-insufficient",
    }
