#!/usr/bin/env python
"""Extract exact colored interfaces from controls and a radius-nine branch."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from einstein.funnel.a6_hierarchy import (
    CompositionRule, contract_level, cover_with_rule, raw_hierarchy_level,
)
from einstein.substrate.module12 import compose_pose
from einstein.theory.spectre_colored_interface import (
    colored_edges_are_reciprocal, colored_parent_corona,
    one_sided_projection, uncolored_projection,
)
from einstein.theory.spectre_geometry import exact_leaves
from einstein.theory.spectre_parent_overlap import parent_templates
from einstein.theory.spectre_patch_language import pose_json
from einstein.theory.spectre_patch_language import patch_edge_incidence
from einstein.theory.substitution_certificate import file_sha256

try:
    from scripts.probe_theory_w3_spectre_component_language import (
        all_radius3_states, language, source, transducer_map,
        unique_safe_base_map,
    )
except ModuleNotFoundError:
    from probe_theory_w3_spectre_component_language import (
        all_radius3_states, language, source, transducer_map,
        unique_safe_base_map,
    )


ROOT = Path(__file__).resolve().parents[2]
COMPONENT = ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"


def state_json(state):
    kind, neighbors = state
    return {
        "kind": kind,
        "neighbors": [{
            "relative_anchor": pose_json(relative),
            "kind": neighbor_kind,
            "contacts": [list(contact) for contact in contacts],
        } for relative, neighbor_kind, contacts in neighbors],
    }


def generated_states(a6, templates):
    full, missing = templates
    rule = CompositionRule(full, missing, len(full), 0)
    poses = tuple(pose for _, pose in exact_leaves(5, "Delta"))
    raw = raw_hierarchy_level(poses)
    cover = cover_with_rule(poses, full, missing)
    parents = contract_level(raw, rule, cover)
    mapping = {
        poses[leaf]: parents.poses[index]
        for index, leaves in enumerate(parents.leaves)
        for leaf in leaves
    }
    incidence, _ = patch_edge_incidence(poses)
    fibers = defaultdict(set)
    edges_by_tile = defaultdict(list)
    for key, owners in incidence.items():
        for tile in owners:
            edges_by_tile[tile].append((key, owners))
    for tile, base in mapping.items():
        fibers[base].add(tile)
    state_by_base = {}
    for center in parents.poses:
        state = colored_parent_corona(
            center, poses, mapping, templates,
            incidence=incidence, fibers=fibers, edges_by_tile=edges_by_tile,
            trust_mapping_absence=True,
        )
        if state is not None:
            state_by_base[center] = state
    if not all(
        colored_edges_are_reciprocal(center, state, state_by_base)
        for center, state in state_by_base.items()
        if all(
            # Only require the check where all six neighbor states are interior.
            compose_pose(center, neighbor[0]) in state_by_base
            for neighbor in state[1]
        )
    ):
        raise ValueError("generated colored interfaces fail reciprocity")
    return tuple(sorted(set(state_by_base.values())))


def build_transducer(a6, allowed, templates):
    from einstein.theory.spectre_parent_overlap import centered_parent_templates
    centered = centered_parent_templates(a6)
    lookup = {}
    for _, patch in all_radius3_states(allowed):
        _, mapping, _ = unique_safe_base_map(patch, centered, templates)
        lookup[tuple(sorted(patch))] = mapping[(0, 0, (0, 0, 0, 0))]
    return lookup


def main():
    a6 = source()
    templates = parent_templates(a6)
    generated = generated_states(a6, templates)
    generated_one_sided = tuple(sorted(set(map(
        one_sided_projection, generated,
    ))))
    component = json.loads(COMPONENT.read_text())
    witness = component["representative_radius9_frontier"]
    patch = tuple(
        (row[0], row[1], tuple(row[2])) for row in witness["patch"]
    )
    lookup = build_transducer(a6, language(), templates)
    mapping = transducer_map(patch, lookup)
    center = mapping[(0, 0, (0, 0, 0, 0))]
    extra = colored_parent_corona(
        center, patch, mapping, templates, require_neighbor_kinds=False,
    )
    if extra is None:
        raise ValueError("radius-nine witness does not buffer a colored interface")
    artifact = {
        "schema": "einstein.w3.spectre-colored-interface",
        "version": 1,
        "status": "FIRST_COLORED_EXTRA_EXTRACTED",
        "provenance": {
            "component_source": str(COMPONENT.relative_to(ROOT)),
            "component_sha256": file_sha256(COMPONENT),
        },
        "generated_colored_states": [state_json(state) for state in generated],
        "generated_colored_state_count": len(generated),
        "generated_one_sided_states": [
            state_json(state) for state in generated_one_sided
        ],
        "generated_one_sided_state_count": len(generated_one_sided),
        "generated_uncolored_projection_count": len({
            uncolored_projection(state) for state in generated
        }),
        "representative_extra": state_json(extra),
        "extra_matches_generated_colored_state": extra in generated_one_sided,
        "extra_uncolored_projection_matches_generated": (
            uncolored_projection(extra)
            in {uncolored_projection(state) for state in generated_one_sided}
        ),
        "claim_boundary": (
            "one persistent extra branch is colored; complete radius-seven "
            "colored-state census remains the next experiment"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        f"generated colored states={len(generated)} "
        f"one-sided={len(generated_one_sided)}; extra kind={extra[0]}; "
        f"colored match={extra in generated_one_sided}"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
