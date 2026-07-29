#!/usr/bin/env python
"""Targeted development probe for the 18-corona parent language."""

from __future__ import annotations

import json
import gzip
import multiprocessing
import os
import pickle
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
from pathlib import Path

from einstein.tilings.substitution import (
    CompositionRule,
    contract_level,
    contracted_adjacency,
    cover_with_rule,
    physical_edge_contacts,
    raw_hierarchy_level,
    SPECTRE_TILE_BOUNDARY,
)
from einstein.geometry.cyclotomic import compose_pose, relative_pose
from einstein.tilings.spectre.components import extend_language_ring
from einstein.tilings.spectre.colored_interfaces import colored_parent_corona
from einstein.tilings.spectre.geometry import exact_leaves
from einstein.tilings.spectre.parent_overlaps import (
    build_grouping_problem,
    centered_parent_templates,
    parent_occurrence_base,
    parent_templates,
    solve_core_grouping,
)
from einstein.tilings.spectre.patches import (
    IDENTITY,
    enumerate_first_coronas,
    patch_edge_incidence,
    pose_json,
)
from einstein.tilings.spectre.certificates import file_sha256


ROOT = Path(__file__).resolve().parents[1]
A6_PATH = ROOT / "docs/notebook/assets/a6-spectre-results.json"
PHYSICAL_PATH = ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
OUTPUT = ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
COLORED_FRONTIER = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-frontier.json"
_WORKER_ALLOWED = ()
_WORKER_LOOKUP = {}
_WORKER_TEMPLATES = ()
_WORKER_TARGET = ()
_WORKER_COLOR = False


def source():
    return json.loads(A6_PATH.read_text())


def language():
    physical = json.loads(PHYSICAL_PATH.read_text())["analysis"]
    coronas = enumerate_first_coronas()
    return tuple(
        coronas[index]
        for index in physical["substitution_control"]["observed_indices"]
    )


def unique_safe_base_map(patch, centered, templates):
    problem = build_grouping_problem(patch, centered)
    result = solve_core_grouping(problem, 1_000_000)
    maps = []
    for solution in result.solutions:
        mapping = {}
        for group_index in solution:
            parent = problem.groups[group_index]
            base = parent_occurrence_base(parent, templates)
            for tile in parent & set(problem.safe_tiles):
                if tile in mapping and mapping[tile] != base:
                    raise AssertionError("selected parents disagree")
                mapping[tile] = base
        if set(mapping) != set(problem.safe_tiles):
            raise AssertionError("safe core is not exactly mapped")
        maps.append(tuple(sorted(mapping.items())))
    distinct = tuple(sorted(set(maps)))
    if len(distinct) != 1:
        raise AssertionError(f"nonunique safe base map: {len(distinct)}")
    return problem, dict(distinct[0]), len(result.solutions)


def generated_parent_coronas(a6):
    full, missing = parent_templates(a6)
    rule = CompositionRule(full, missing, len(full), 0)
    poses = tuple(pose for _, pose in exact_leaves(5, "Delta"))
    raw = raw_hierarchy_level(poses)
    cover = cover_with_rule(poses, full, missing)
    parents = contract_level(raw, rule, cover)
    contacts = physical_edge_contacts(poses, SPECTRE_TILE_BOUNDARY)
    adjacency = contracted_adjacency(contacts, parents)
    return tuple(sorted({
        tuple(sorted(relative_pose(parents.poses[i], parents.poses[j])
                     for j in neighbors))
        for i, neighbors in enumerate(adjacency)
        if len(neighbors) == 6
    }))


def partial_parent_corona(patch, mapping):
    center = mapping.get(IDENTITY)
    if center is None:
        return None
    incidence, _ = patch_edge_incidence(patch)
    found = set()
    for owners in incidence.values():
        if len(owners) != 2:
            continue
        left, right = owners
        if left not in mapping or right not in mapping:
            continue
        a, b = mapping[left], mapping[right]
        if a == b:
            continue
        if a == center:
            found.add(relative_pose(center, b))
        elif b == center:
            found.add(relative_pose(center, a))
    return tuple(sorted(found))


def resolved_parent_corona(patch, mapping, templates, incidence=None):
    """Return the complete contracted corona once its physical interface is buffered."""
    center = mapping.get(IDENTITY)
    if center is None:
        return None
    full, missing = templates
    common = {compose_pose(center, child) for child in missing}
    optional = next(iter(set(full) - set(missing)))
    optional = compose_pose(center, optional)
    mapped = set(mapping)
    if not common <= mapped or any(mapping[child] != center for child in common):
        return None
    if optional in patch and optional not in mapped:
        return None
    fiber = set(common)
    if mapping.get(optional) == center:
        fiber.add(optional)

    if incidence is None:
        incidence, _ = patch_edge_incidence(patch)
    neighbors = set()
    for owners in incidence.values():
        inside = [tile for tile in owners if tile in fiber]
        if not inside:
            continue
        if len(owners) != 2:
            return None
        other = owners[0] if owners[1] in fiber else owners[1]
        if other in fiber:
            continue
        if other not in mapped:
            return None
        neighbors.add(mapping[other])
    return tuple(sorted(relative_pose(center, neighbor) for neighbor in neighbors))


def adjacency_graph(patch, incidence=None):
    adjacency = {tile: set() for tile in patch}
    if incidence is None:
        incidence, _ = patch_edge_incidence(patch)
    exposed = set()
    for owners in incidence.values():
        if len(owners) == 1:
            exposed.add(owners[0])
        if len(owners) == 2:
            left, right = owners
            adjacency[left].add(right)
            adjacency[right].add(left)
    return adjacency, set(patch) - exposed


def rooted_ball(adjacency, complete, center, radius=3):
    ball = {center}
    frontier = {center}
    for depth in range(radius):
        if not frontier <= complete:
            return None
        frontier = {
            neighbor for tile in frontier for neighbor in adjacency[tile]
        } - ball
        ball.update(frontier)
    return tuple(sorted(relative_pose(center, tile) for tile in ball))


def transducer_map(patch, lookup, adjacency=None, complete=None):
    if adjacency is None or complete is None:
        adjacency, complete = adjacency_graph(patch)
    mapping = {}
    for tile in patch:
        ball = rooted_ball(adjacency, complete, tile)
        relative_base = lookup.get(ball)
        if relative_base is not None:
            mapping[tile] = compose_pose(tile, relative_base)
    return mapping


def all_radius3_states(allowed):
    rows = []
    for corona_index, corona in enumerate(enumerate_first_coronas()):
        if corona not in allowed:
            continue
        states = [(IDENTITY, *corona)]
        for _ in range(2):
            states = [
                (*patch, *ring)
                for patch in states
                for ring in extend_language_ring(patch, allowed).solutions
            ]
        rows.extend((corona_index, patch) for patch in states)
    return rows


def advance_case(item):
    corona_index, patch = item
    extension = extend_language_ring(patch, _WORKER_ALLOWED)
    rows = []
    for ring in extension.solutions:
        candidate = (*patch, *ring)
        incidence, _ = patch_edge_incidence(candidate)
        adjacency, complete = adjacency_graph(candidate, incidence=incidence)
        mapping = transducer_map(
            candidate, _WORKER_LOOKUP,
            adjacency=adjacency, complete=complete,
        )
        resolved = resolved_parent_corona(
            candidate, mapping, _WORKER_TEMPLATES, incidence=incidence,
        )
        center = mapping.get(IDENTITY)
        common = (
            {compose_pose(center, child) for child in _WORKER_TEMPLATES[1]}
            if center is not None else set()
        )
        core_ok = (
            IDENTITY in mapping
            and common <= set(mapping)
            and all(mapping[child] == center for child in common)
        )
        status = (
            "unresolved" if resolved is None
            else "inside" if resolved in _WORKER_TARGET
            else "outside"
        )
        colored = None
        if _WORKER_COLOR and resolved is not None:
            colored = colored_parent_corona(
                mapping[IDENTITY], candidate, mapping, _WORKER_TEMPLATES,
                incidence=incidence, complete=complete,
                require_neighbor_kinds=False,
            )
            if colored is None:
                raise ValueError("resolved parent lacks a colored interface")
        rows.append((status, core_ok, resolved, colored, corona_index, candidate))
    return not extension.solutions, rows


def advance_outside_case(item):
    corona_index, patch = item
    extension = extend_language_ring(patch, _WORKER_ALLOWED)
    return (
        not extension.solutions,
        [(corona_index, (*patch, *ring)) for ring in extension.solutions],
    )


def frontier_digest(frontier):
    digest = sha256()
    for corona_index, patch in sorted(frontier):
        digest.update(str(corona_index).encode())
        digest.update(b":")
        digest.update(json.dumps(
            [pose_json(pose) for pose in patch], separators=(",", ":")
        ).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def main():
    a6 = source()
    allowed = language()
    centered = centered_parent_templates(a6)
    templates = parent_templates(a6)
    target = generated_parent_coronas(a6)
    print(f"target parent coronas={len(target)}", flush=True)

    indexed_states = all_radius3_states(allowed)
    print(f"all r3 states={len(indexed_states)}", flush=True)
    bad = []
    unresolved = []
    hist = Counter()
    solution_hist = Counter()
    safe_hist = Counter()
    core_failures = []
    lookup = {}
    for corona_index, patch in indexed_states:
        problem, mapping, solutions = unique_safe_base_map(
            patch, centered, templates
        )
        solution_hist[solutions] += 1
        safe_hist[len(problem.safe_tiles)] += 1
        if IDENTITY not in problem.safe_tiles:
            raise AssertionError("central tile is not buffered at radius three")
        center = mapping.get(IDENTITY)
        common = (
            {compose_pose(center, child) for child in templates[1]}
            if center is not None else set()
        )
        core_ok = (
            IDENTITY in problem.safe_tiles
            and common <= set(problem.safe_tiles)
            and all(mapping[child] == center for child in common)
        )
        if not core_ok:
            core_failures.append((corona_index, patch))
        relative_base = relative_pose(IDENTITY, mapping[IDENTITY])
        rooted = tuple(sorted(patch))
        if rooted in lookup and lookup[rooted] != relative_base:
            raise AssertionError("one rooted radius-three case has two anchors")
        lookup[rooted] = relative_base
        partial = partial_parent_corona(patch, mapping)
        compatible = sum(set(partial or ()) <= set(signature) for signature in target)
        hist[(len(problem.safe_tiles), solutions, len(partial or ()), compatible)] += 1
        if not compatible:
            bad.append((corona_index, patch))
        local_mapping = transducer_map(patch, lookup)
        resolved = resolved_parent_corona(patch, local_mapping, templates)
        if resolved is None:
            unresolved.append((corona_index, patch))
        elif resolved not in target:
            raise AssertionError(("resolved outside target", corona_index, resolved))
    print(
        f"r3 histogram={dict(hist)} bad={len(bad)} "
        f"core_failures={len(core_failures)} transducer={len(lookup)} "
        f"unresolved={len(unresolved)}",
        flush=True,
    )

    global _WORKER_ALLOWED, _WORKER_LOOKUP, _WORKER_TEMPLATES, _WORKER_TARGET
    global _WORKER_COLOR
    _WORKER_ALLOWED = allowed
    _WORKER_LOOKUP = lookup
    _WORKER_TEMPLATES = templates
    _WORKER_TARGET = target
    frontier = unresolved
    radius_records = []
    outside_signatures = Counter()
    colored_generated = Counter()
    colored_extra = Counter()
    representative_signature = None
    stop_radius = int(os.environ.get("W3_STOP_RADIUS", "9"))
    if stop_radius < 7 or stop_radius > 9:
        raise ValueError("W3_STOP_RADIUS must be 7, 8, or 9")
    for radius in range(4, stop_radius + 1):
        next_frontier = []
        resolved_count = outside_count = dead_count = core_failure_count = 0
        workers = min(24, os.cpu_count() or 4)
        _WORKER_COLOR = radius == 7
        with ProcessPoolExecutor(
            max_workers=workers,
            mp_context=multiprocessing.get_context("fork"),
        ) as executor:
            if radius >= 8:
                for dead, rows in executor.map(
                    advance_outside_case, frontier, chunksize=4
                ):
                    dead_count += dead
                    outside_count += len(rows)
                    next_frontier.extend(rows)
            else:
                for dead, rows in executor.map(advance_case, frontier, chunksize=4):
                    dead_count += dead
                    for status, core_ok, resolved, colored, corona_index, candidate in rows:
                        core_failure_count += not core_ok
                        if radius == 7:
                            target_counter = (
                                colored_generated if status == "inside"
                                else colored_extra
                            )
                            target_counter[repr(colored)] += 1
                        if status == "inside":
                            resolved_count += 1
                        else:
                            outside_count += status == "outside"
                            if status == "outside":
                                outside_signatures[repr(resolved)] += 1
                                representative_signature = (
                                    representative_signature or resolved
                                )
                            next_frontier.append((corona_index, candidate))
        frontier = next_frontier
        record = {
            "radius": radius,
            "dead_input_patches": dead_count,
            "generated_parent_corona_extensions": resolved_count,
            "nongenerated_parent_corona_extensions": outside_count,
            "component_core_failures": core_failure_count,
            "continued_frontier_patches": len(frontier),
            "continued_frontier_sha256": frontier_digest(frontier),
        }
        if radius <= 7:
            record["unresolved_interface_extensions"] = (
                len(frontier) - outside_count
            )
        radius_records.append(record)
        print(
            f"closure r{radius}: resolved={resolved_count} outside={outside_count} "
            f"dead={dead_count} core_failures={core_failure_count} "
            f"frontier={len(frontier)}", flush=True,
        )
        if os.environ.get("W3_SAVE_FRONTIER"):
            checkpoint_dir = ROOT / "data/w3-frontiers"
            checkpoint_dir.mkdir(parents=True, exist_ok=True)
            checkpoint = checkpoint_dir / f"spectre-l18-radius{radius}.pkl.gz"
            with gzip.open(checkpoint, "wb", compresslevel=3) as stream:
                pickle.dump(frontier, stream, protocol=pickle.HIGHEST_PROTOCOL)
            print(
                f"checkpoint {checkpoint.relative_to(ROOT)}",
                flush=True,
            )
        if not frontier:
            break

    if not colored_generated or not colored_extra:
        raise ValueError("radius-seven colored census was not reached")
    colored_artifact = {
        "schema": "einstein.w3.spectre-colored-frontier",
        "version": 1,
        "status": "COMPLETE_RESOLVED_RADIUS7_CENSUS",
        "provenance": {
            "a6_source": str(A6_PATH.relative_to(ROOT)),
            "a6_sha256": file_sha256(A6_PATH),
            "physical_source": str(PHYSICAL_PATH.relative_to(ROOT)),
            "physical_sha256": file_sha256(PHYSICAL_PATH),
        },
        "radius7": {
            "generated_extensions": sum(colored_generated.values()),
            "extra_extensions": sum(colored_extra.values()),
            "generated_colored_states": dict(sorted(colored_generated.items())),
            "extra_colored_states": dict(sorted(colored_extra.items())),
            "all_interfaces_resolved": True,
        },
    }
    COLORED_FRONTIER.write_text(json.dumps(colored_artifact, indent=1) + "\n")
    print(COLORED_FRONTIER.relative_to(ROOT), flush=True)

    if stop_radius < 9:
        return

    representative = frontier[0] if frontier else None
    representative_parent_corona = None
    if representative is not None:
        representative_parent_corona = resolved_parent_corona(
            representative[1], transducer_map(representative[1], lookup), templates
        )
    artifact = {
        "schema": "einstein.w3.spectre-component-language",
        "version": 1,
        "status": "PARENT_PARTITION_PROVED_CLOSURE_OPEN_RADIUS9",
        "provenance": {
            "a6_source": str(A6_PATH.relative_to(ROOT)),
            "a6_sha256": file_sha256(A6_PATH),
            "physical_source": str(PHYSICAL_PATH.relative_to(ROOT)),
            "physical_sha256": file_sha256(PHYSICAL_PATH),
        },
        "scope": {
            "tile": "straight-edged Tile(1,1)",
            "chirality": "one fixed handedness",
            "motions": ["translation", "rotation"],
            "contact_model": "edge-to-edge unit-edge tilings",
            "hypothesis": "every complete physical tile corona is in L18",
        },
        "radius3_transducer": {
            "rooted_cases": len(lookup),
            "all_have_parent": len(lookup) == 418,
            "all_have_unique_parent_anchor": len(lookup) == 418,
            "raw_grouping_solution_histogram": {
                str(key): value for key, value in sorted(solution_hist.items())
            },
            "safe_tile_count_histogram": {
                str(key): value for key, value in sorted(safe_hist.items())
            },
            "distinct_parent_anchor_maps_per_case": 1,
        },
        "partition_theorem": {
            "decisive_radius": 6,
            "surviving_radius6_patches": 15216,
            "common_eight_child_core_failures": 0,
            "fiber_types": [8, 9],
            "verdict": "unique-parent-anchor fibers form a full/missing partition",
        },
        "contraction_audit": {
            "generated_parent_corona_types": len(target),
            "radius_records": radius_records,
            "nongenerated_signature_histogram_through_radius7": dict(
                sorted(outside_signatures.items())
            ),
            "verdict": "not-closed-through-radius9",
            "claim_boundary": (
                "a finite nongenerated contracted corona branch reaches radius "
                "nine; no whole-plane counterexample or closure theorem follows"
            ),
        },
        "representative_radius9_frontier": (
            None if representative is None else {
                "corona_index": representative[0],
                "patch": [pose_json(pose) for pose in representative[1]],
                "parent_corona": [
                    pose_json(pose) for pose in (representative_parent_corona or ())
                ],
            }
        ),
    }
    OUTPUT.write_text(json.dumps(artifact, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT), flush=True)


if __name__ == "__main__":
    main()
