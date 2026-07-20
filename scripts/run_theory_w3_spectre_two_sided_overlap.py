#!/usr/bin/env python
"""Extend the saved L18 frontier and test exact two-sided parent colors."""

from __future__ import annotations

import gzip
import json
import multiprocessing
import os
import pickle
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from pathlib import Path

try:
    import scripts.probe_theory_w3_spectre_component_language as probe
except ModuleNotFoundError:
    import probe_theory_w3_spectre_component_language as probe
from einstein.theory.spectre_colored_interface import (
    colored_corona_from_json,
    colored_corona_json,
    colored_parent_corona,
    colored_transition_graph,
    prune_colored_unsupported,
    strongly_connected_components,
    uncolored_projection,
)
from einstein.theory.spectre_component_language import extend_language_ring
from einstein.theory.spectre_parent_overlap import parent_templates
from einstein.theory.spectre_patch_language import patch_edge_incidence
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "data/w3-frontiers/spectre-l18-radius7.pkl.gz"
CHECKPOINT8 = ROOT / "data/w3-frontiers/spectre-l18-radius8.pkl.gz"
COMPONENT = ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
CONTROL = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-two-sided-overlap.json"
_ALLOWED = ()
_LOOKUP = {}
_TEMPLATES = ()


def state_id(state):
    return sha256(repr(state).encode()).hexdigest()[:16]


def color_next_ring(item):
    corona_index, patch = item
    extension = extend_language_ring(patch, _ALLOWED)
    rows = []
    for ring in extension.solutions:
        candidate = (*patch, *ring)
        incidence, _ = patch_edge_incidence(candidate)
        adjacency, complete = probe.adjacency_graph(
            candidate, incidence=incidence,
        )
        mapping = probe.transducer_map(
            candidate, _LOOKUP, adjacency=adjacency, complete=complete,
        )
        resolved = probe.resolved_parent_corona(
            candidate, mapping, _TEMPLATES, incidence=incidence,
        )
        state = None
        if resolved is not None:
            state = colored_parent_corona(
                mapping[probe.IDENTITY], candidate, mapping, _TEMPLATES,
                incidence=incidence, complete=complete,
                require_neighbor_kinds=True,
            )
        rows.append((resolved, state, corona_index, candidate))
    return not extension.solutions, rows


def main():
    if not CHECKPOINT.exists():
        raise SystemExit(
            "missing radius-7 checkpoint; run "
            "W3_STOP_RADIUS=7 W3_SAVE_FRONTIER=1 "
            "scripts/probe_theory_w3_spectre_component_language.py"
        )
    component = json.loads(COMPONENT.read_text())
    expected_r7 = next(
        row for row in component["contraction_audit"]["radius_records"]
        if row["radius"] == 7
    )
    with gzip.open(CHECKPOINT, "rb") as stream:
        frontier = pickle.load(stream)
    if len(frontier) != expected_r7["continued_frontier_patches"]:
        raise ValueError("radius-seven checkpoint count mismatch")
    if probe.frontier_digest(frontier) != expected_r7["continued_frontier_sha256"]:
        raise ValueError("radius-seven checkpoint digest mismatch")

    a6 = probe.source()
    allowed = probe.language()
    templates = parent_templates(a6)
    control = json.loads(CONTROL.read_text())
    generated = set(map(
        colored_corona_from_json, control["generated_colored_states"],
    ))
    target = {uncolored_projection(state) for state in generated}
    print("building 418-entry physical transducer", flush=True)
    indexed = probe.all_radius3_states(allowed)
    centered = probe.centered_parent_templates(a6)
    lookup = {}
    for _, patch in indexed:
        _, mapping, _ = probe.unique_safe_base_map(patch, centered, templates)
        lookup[tuple(sorted(patch))] = probe.relative_pose(
            probe.IDENTITY, mapping[probe.IDENTITY],
        )

    print("physical transducer ready; extending radius seven", flush=True)
    probe._WORKER_ALLOWED = allowed
    workers = min(24, os.cpu_count() or 4)
    if CHECKPOINT8.exists():
        with gzip.open(CHECKPOINT8, "rb") as stream:
            checkpoint8 = pickle.load(stream)
        r8 = checkpoint8["frontier"]
        dead8 = checkpoint8["dead_inputs"]
        print("loaded radius-eight checkpoint", flush=True)
    else:
        r8 = []
        dead8 = 0
        with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("fork"),
        ) as executor:
            for dead, rows in executor.map(
                probe.advance_outside_case, frontier, chunksize=4,
            ):
                dead8 += dead
                r8.extend(rows)
        with gzip.open(CHECKPOINT8, "wb", compresslevel=3) as stream:
            pickle.dump(
                {"frontier": r8, "dead_inputs": dead8}, stream,
                protocol=pickle.HIGHEST_PROTOCOL,
            )
    print(f"radius8 frontier={len(r8)} dead-input={dead8}", flush=True)

    global _ALLOWED, _LOOKUP, _TEMPLATES
    _ALLOWED = allowed
    _LOOKUP = lookup
    _TEMPLATES = templates
    r9 = []
    dead9 = 0
    state_counts = Counter()
    unresolved = uncolored_inside = 0
    with ProcessPoolExecutor(
        max_workers=workers,
        mp_context=multiprocessing.get_context("fork"),
    ) as executor:
        for dead, rows in executor.map(color_next_ring, r8, chunksize=2):
            dead9 += dead
            for resolved, state, corona_index, candidate in rows:
                r9.append((corona_index, candidate))
                unresolved += state is None
                uncolored_inside += resolved in target if resolved else False
                if state is not None:
                    state_counts[state] += 1
    print(
        f"radius9 frontier={len(r9)} dead-input={dead9} "
        f"two-sided-unresolved={unresolved} states={len(state_counts)}",
        flush=True,
    )

    extras = set(state_counts)
    states = tuple(sorted(generated | extras, key=repr))
    state_index = {state: index for index, state in enumerate(states)}
    generated_indices = {state_index[state] for state in generated}
    extra_indices = {state_index[state] for state in extras - generated}
    alive, rounds = prune_colored_unsupported(states)
    alive_set = set(alive)
    transition = colored_transition_graph(states, allowed=alive)
    components = strongly_connected_components(transition, allowed=alive)
    surviving_extras = extra_indices & alive_set
    complete = unresolved == 0 and uncolored_inside == 0
    if complete and not surviving_extras and generated_indices <= alive_set:
        status = "TWO_SIDED_OVERLAP_ELIMINATES_ALL_EXTRA_STATES"
    elif complete:
        status = "TWO_SIDED_OVERLAP_LEAVES_A_FRONTIER"
    else:
        status = "TWO_SIDED_ALPHABET_INCOMPLETE_AT_RADIUS9"

    def ids(indices):
        return [state_id(states[index]) for index in sorted(indices)]

    artifact = {
        "schema": "einstein.w3.spectre-two-sided-overlap",
        "version": 1,
        "status": status,
        "provenance": {
            "component_source": str(COMPONENT.relative_to(ROOT)),
            "component_sha256": file_sha256(COMPONENT),
            "control_source": str(CONTROL.relative_to(ROOT)),
            "control_sha256": file_sha256(CONTROL),
            "radius7_checkpoint_sha256": file_sha256(CHECKPOINT),
            "radius7_frontier_digest": probe.frontier_digest(frontier),
        },
        "extension": {
            "radius7_states": len(frontier),
            "radius8_states": len(r8),
            "radius9_states": len(r9),
            "radius8_dead_inputs": dead8,
            "radius9_dead_inputs": dead9,
            "two_sided_unresolved": unresolved,
            "nongenerated_branch_contracts_to_generated": uncolored_inside,
        },
        "alphabet": {
            "generated_states": len(generated),
            "observed_radius9_states": len(extras),
            "new_radius9_states": len(extras - generated),
            "generated_radius9_intersection": len(extras & generated),
            "radius9_occurrences": sum(state_counts.values()),
            "state_occurrences": {
                state_id(state): count
                for state, count in sorted(state_counts.items(), key=lambda row: repr(row[0]))
            },
            "observed_radius9_state_records": [{
                "id": state_id(state),
                "occurrences": state_counts[state],
                "state": colored_corona_json(state),
            } for state in sorted(extras, key=repr)],
        },
        "fixed_point": {
            "combined_states": len(states),
            "rounds": [ids(round_) for round_ in rounds],
            "surviving_states": len(alive),
            "surviving_generated_states": len(generated_indices & alive_set),
            "surviving_extra_states": len(surviving_extras),
            "surviving_extra_state_ids": ids(surviving_extras),
        },
        "transition_sccs": [{
            "size": len(component),
            "generated_states": len(set(component) & generated_indices),
            "extra_states": len(set(component) & extra_indices),
        } for component in components],
        "claim_boundary": (
            "when the radius-nine alphabet is complete, fixed-point deletion "
            "is rigorous nonexistence evidence for removed states; surviving "
            "states still need not possess a whole-plane realization"
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(
        f"{status}: combined={len(states)} fixed={len(alive)} "
        f"extra-fixed={len(surviving_extras)}"
    )
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
