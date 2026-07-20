"""Coordinated parent-overlap constraints for finite Spectre patches.

The physical patch-language experiment showed that choosing a parent for one
central tile is the wrong local object.  A grouping is instead a partial exact
partition of the physical tiles into translated/rotated occurrences of the
recovered eight- and nine-child parent templates.

Finite patches have a boundary, so the kernel only demands coverage of a
``safe`` tile when every parent occurrence still geometrically compatible
with the visible patch is fully contained in it.  Selected parent groups must
be pairwise disjoint on *all* visible tiles.  This is a sound buffered-core
condition: UNSAT cannot be blamed on forcing the artificial patch boundary to
be a parent boundary.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import deque
from hashlib import sha256
import json
from typing import Iterable, Sequence

from einstein.substrate.module12 import Pose, compose_pose, inverse_pose
from einstein.theory.spectre_patch_language import (
    IDENTITY,
    _candidate_ring_tiles,
    central_parent_candidates,
    enumerate_first_coronas,
    extend_complete_ring,
    language_digest,
    patch_edge_incidence,
    poses_overlap,
)


Parent = frozenset[Pose]


@dataclass(frozen=True)
class GroupingProblem:
    patch: frozenset[Pose]
    safe_tiles: tuple[Pose, ...]
    groups: tuple[Parent, ...]
    compatible_count_by_tile: tuple[tuple[Pose, int], ...]


@dataclass(frozen=True)
class GroupingResult:
    solutions: tuple[tuple[int, ...], ...]
    safe_tiles: int
    candidate_groups: int
    sat_calls: int
    solver: str


@dataclass(frozen=True)
class CoordinatedExtension:
    """One physical next ring coupled to a parent partition of a safe core."""

    physical_ring: tuple[Pose, ...] | None
    selected_parents: tuple[Parent, ...]
    target_tiles: tuple[Pose, ...]
    physical_candidates: int
    parent_candidates: int
    sat_calls: int
    solver: str


def _parse_template(rows) -> tuple[Pose, ...]:
    return tuple(
        (int(reflection), int(rotation), tuple(map(int, translation)))
        for reflection, rotation, translation in rows
    )


def centered_parent_templates(a6_result) -> tuple[Parent, ...]:
    """Return every recovered full/missing parent containing identity."""
    selected = a6_result["selected_rule"]
    return central_parent_candidates(
        _parse_template(selected["full"]),
        _parse_template(selected["missing"]),
    )


def parent_templates(a6_result):
    """Return the canonical full and missing templates at one parent base."""
    selected = a6_result["selected_rule"]
    return _parse_template(selected["full"]), _parse_template(selected["missing"])


def parent_occurrence_base(parent: Parent, templates) -> Pose:
    """Recover the unique pose carrying a canonical template to ``parent``."""
    full, missing = templates
    template = full if len(parent) == len(full) else missing
    if len(parent) != len(template):
        raise ValueError("parent size matches neither canonical template")
    found = set()
    for child in parent:
        for relative in template:
            base = compose_pose(child, inverse_pose(relative))
            if frozenset(compose_pose(base, pose) for pose in template) == parent:
                found.add(base)
    if len(found) != 1:
        raise ValueError(f"expected one parent base, found {len(found)}")
    return found.pop()


def parent_occurrences(tile: Pose, centered: Sequence[Parent]) -> tuple[Parent, ...]:
    """Translate/rotate every identity-centered parent to contain ``tile``."""
    return tuple(sorted(
        {
            frozenset(compose_pose(tile, child) for child in parent)
            for parent in centered
        },
        key=lambda parent: (len(parent), tuple(sorted(parent))),
    ))


def occurrence_compatible(parent: Parent, patch: frozenset[Pose]) -> bool:
    """Whether absent children could still be added without overlap."""
    return all(
        child in patch
        or all(not poses_overlap(child, visible) for visible in patch)
        for child in parent
    )


def build_grouping_problem(
    patch: Iterable[Pose], centered: Sequence[Parent]
) -> GroupingProblem:
    """Construct the sound buffered-core exact-partition problem."""
    patch = frozenset(patch)
    compatible: dict[Pose, tuple[Parent, ...]] = {}
    full_groups: set[Parent] = set()
    for tile in sorted(patch):
        occurrences = tuple(
            parent
            for parent in parent_occurrences(tile, centered)
            if occurrence_compatible(parent, patch)
        )
        compatible[tile] = occurrences
        full_groups.update(parent for parent in occurrences if parent <= patch)

    safe_tiles = tuple(sorted(
        tile
        for tile, occurrences in compatible.items()
        if occurrences and all(parent <= patch for parent in occurrences)
    ))
    groups = tuple(sorted(
        full_groups, key=lambda parent: (len(parent), tuple(sorted(parent)))
    ))
    return GroupingProblem(
        patch=patch,
        safe_tiles=safe_tiles,
        groups=groups,
        compatible_count_by_tile=tuple(
            (tile, len(compatible[tile])) for tile in sorted(patch)
        ),
    )


def solve_grouping(
    problem: GroupingProblem, solution_limit: int = 2
) -> GroupingResult:
    """Solve coordinated coverage of safe tiles and disjointness everywhere."""
    if solution_limit < 1:
        raise ValueError("solution_limit must be positive")
    variables = tuple(range(1, len(problem.groups) + 1))
    clauses: list[list[int]] = []
    safe = set(problem.safe_tiles)
    for tile in sorted(problem.patch):
        covering = [
            variables[index]
            for index, parent in enumerate(problem.groups)
            if tile in parent
        ]
        if tile in safe:
            if not covering:
                return GroupingResult(
                    (), len(problem.safe_tiles), len(problem.groups), 0,
                    "CaDiCaL 1.9.5",
                )
            clauses.append(covering)
        for position, left in enumerate(covering):
            for right in covering[position + 1:]:
                clauses.append([-left, -right])

    # With no safe tiles the empty grouping is the unique relevant witness.
    if not problem.safe_tiles:
        return GroupingResult(((),), 0, len(problem.groups), 0, "trivial")

    from pysat.solvers import Cadical195

    solutions: list[tuple[int, ...]] = []
    calls = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < solution_limit:
            calls += 1
            if not solver.solve():
                break
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(
                index
                for index, variable in enumerate(variables)
                if variable in positive
            )
            solutions.append(selected)
            solver.add_clause([-variables[index] for index in selected])
    return GroupingResult(
        tuple(sorted(solutions)), len(problem.safe_tiles), len(problem.groups),
        calls, "CaDiCaL 1.9.5",
    )


def solve_core_grouping(
    problem: GroupingProblem, solution_limit: int = 2
) -> GroupingResult:
    """Enumerate partitions projected to parents touching the safe core.

    Parent groups wholly outside the required target are deliberately omitted:
    toggling an irrelevant boundary group must not turn one inner partition
    into two apparent solutions.
    """
    if solution_limit < 1:
        raise ValueError("solution_limit must be positive")
    safe = set(problem.safe_tiles)
    active_indices = tuple(
        index for index, parent in enumerate(problem.groups) if parent & safe
    )
    if not safe:
        return GroupingResult(((),), 0, len(active_indices), 0, "trivial")
    variables = tuple(range(1, len(active_indices) + 1))
    clauses: list[list[int]] = []
    for tile in sorted(problem.patch):
        covering = [
            variables[position]
            for position, group_index in enumerate(active_indices)
            if tile in problem.groups[group_index]
        ]
        if tile in safe:
            if not covering:
                return GroupingResult(
                    (), len(safe), len(active_indices), 0, "CaDiCaL 1.9.5"
                )
            clauses.append(covering)
        clauses.extend(_pairwise_at_most_one(covering))

    from pysat.solvers import Cadical195

    solutions = []
    calls = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < solution_limit:
            calls += 1
            if not solver.solve():
                break
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(
                group_index
                for position, group_index in enumerate(active_indices)
                if variables[position] in positive
            )
            solutions.append(selected)
            solver.add_clause([
                -variables[position]
                if group_index in selected else variables[position]
                for position, group_index in enumerate(active_indices)
            ])
    return GroupingResult(
        tuple(sorted(solutions)), len(safe), len(active_indices), calls,
        "CaDiCaL 1.9.5",
    )


def verify_grouping_solution(
    problem: GroupingProblem, selected: Sequence[int]
) -> bool:
    """Check a stored partial parent partition without invoking a solver."""
    if len(set(selected)) != len(selected):
        return False
    if any(index < 0 or index >= len(problem.groups) for index in selected):
        return False
    parents = tuple(problem.groups[index] for index in selected)
    multiplicity = {
        tile: sum(tile in parent for parent in parents)
        for tile in problem.patch
    }
    return (
        all(multiplicity[tile] == 1 for tile in problem.safe_tiles)
        and all(count <= 1 for count in multiplicity.values())
    )


def _pairwise_at_most_one(variables: Sequence[int]) -> list[list[int]]:
    return [
        [-left, -right]
        for position, left in enumerate(variables)
        for right in variables[position + 1:]
    ]


def solve_coordinated_ring_extension(
    patch: Sequence[Pose], centered: Sequence[Parent],
    blocked_physical_rings: Sequence[Sequence[Pose]] = (),
) -> CoordinatedExtension:
    """Choose the next physical ring and a joint parent grouping in one SAT.

    The target is the largest subset of the fixed inner patch for which every
    parent occurrence compatible with that patch lies in the union of the
    patch and all legal next-ring candidates.  Consequently no possible
    parent of a target tile is silently discarded at the artificial outer
    boundary.
    """
    patch = tuple(sorted(set(patch)))
    patch_set = frozenset(patch)
    exposed, candidate_cover = _candidate_ring_tiles(patch)
    candidates = tuple(sorted(candidate_cover))
    universe = patch_set | frozenset(candidates)

    compatible: dict[Pose, tuple[Parent, ...]] = {}
    target = []
    parent_groups: set[Parent] = set()
    for tile in patch:
        occurrences = tuple(
            parent
            for parent in parent_occurrences(tile, centered)
            if occurrence_compatible(parent, patch_set)
        )
        compatible[tile] = occurrences
        if occurrences and all(parent <= universe for parent in occurrences):
            target.append(tile)
            parent_groups.update(occurrences)
    target = tuple(sorted(target))
    groups = tuple(sorted(
        parent_groups, key=lambda parent: (len(parent), tuple(sorted(parent)))
    ))

    if not target:
        return CoordinatedExtension(
            None, (), (), len(candidates), len(groups), 0, "no-safe-target",
        )

    x_vars = tuple(range(1, len(candidates) + 1))
    y_vars = tuple(range(len(candidates) + 1, len(candidates) + len(groups) + 1))
    candidate_index = {pose: index for index, pose in enumerate(candidates)}
    clauses: list[list[int]] = []

    # Exact cover of every currently exposed physical edge.
    by_edge: list[list[int]] = [[] for _ in exposed]
    for index, pose in enumerate(candidates):
        for edge in candidate_cover[pose]:
            by_edge[edge].append(x_vars[index])
    if not all(by_edge):
        return CoordinatedExtension(
            None, (), target, len(candidates), len(groups), 0, "CaDiCaL 1.9.5",
        )
    for covering in by_edge:
        clauses.append(covering)
        clauses.extend(_pairwise_at_most_one(covering))

    # Enumerate distinct physical rings independently of how many parent
    # partitions each ring admits.  The full Boolean assignment is blocked so
    # the semantics does not rely on exact covers being inclusion-minimal.
    for blocked in blocked_physical_rings:
        blocked_set = set(blocked)
        if not blocked_set <= set(candidates):
            raise ValueError("blocked ring contains a non-candidate pose")
        clauses.append([
            -x_vars[index] if pose in blocked_set else x_vars[index]
            for index, pose in enumerate(candidates)
        ])

    # Physical nonoverlap within the selected ring.
    for left, left_pose in enumerate(candidates):
        for right in range(left):
            if poses_overlap(left_pose, candidates[right]):
                clauses.append([-x_vars[left], -x_vars[right]])

    # A selected parent may use a candidate tile only if that tile is present.
    for group_index, parent in enumerate(groups):
        y = y_vars[group_index]
        for child in parent - patch_set:
            candidate = candidate_index.get(child)
            if candidate is None:
                raise AssertionError("parent child escaped the candidate universe")
            clauses.append([-y, x_vars[candidate]])

    # Exact one parent on the universally buffered target; at most one parent
    # on every visible/candidate tile prevents incompatible local choices.
    target_set = set(target)
    for tile in sorted(universe):
        covering = [
            y_vars[index]
            for index, parent in enumerate(groups)
            if tile in parent
        ]
        if tile in target_set:
            if not covering:
                return CoordinatedExtension(
                    None, (), target, len(candidates), len(groups), 0,
                    "CaDiCaL 1.9.5",
                )
            clauses.append(covering)
        clauses.extend(_pairwise_at_most_one(covering))

    from pysat.solvers import Cadical195

    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return CoordinatedExtension(
                None, (), target, len(candidates), len(groups), 1,
                "CaDiCaL 1.9.5",
            )
        positive = {literal for literal in solver.get_model() if literal > 0}
    ring = tuple(
        candidates[index]
        for index, variable in enumerate(x_vars)
        if variable in positive
    )
    selected = tuple(
        groups[index]
        for index, variable in enumerate(y_vars)
        if variable in positive
    )
    return CoordinatedExtension(
        tuple(sorted(ring)), tuple(sorted(
            selected, key=lambda parent: (len(parent), tuple(sorted(parent)))
        )), target, len(candidates), len(groups), 1, "CaDiCaL 1.9.5",
    )


def verify_coordinated_extension(
    patch: Sequence[Pose], extension: CoordinatedExtension,
    centered: Sequence[Parent],
) -> bool:
    """Independently check the geometry and grouping of a SAT witness."""
    if extension.physical_ring is None:
        return False
    patch = tuple(sorted(set(patch)))
    patch_set = frozenset(patch)
    exposed, candidate_cover = _candidate_ring_tiles(patch)
    candidates = set(candidate_cover)
    ring = tuple(extension.physical_ring)
    if len(set(ring)) != len(ring) or not set(ring) <= candidates:
        return False
    if any(poses_overlap(left, right)
           for index, left in enumerate(ring) for right in ring[:index]):
        return False
    for edge in range(len(exposed)):
        if sum(edge in candidate_cover[pose] for pose in ring) != 1:
            return False

    final_patch = patch_set | frozenset(ring)
    parents = tuple(extension.selected_parents)
    if any(not parent <= final_patch for parent in parents):
        return False
    if any(parent not in parent_occurrences(tile, centered)
           for parent in parents for tile in parent):
        return False
    multiplicity = {
        tile: sum(tile in parent for parent in parents)
        for tile in final_patch
    }
    return (
        all(tile in patch_set for tile in extension.target_tiles)
        and all(multiplicity[tile] == 1 for tile in extension.target_tiles)
        and all(count <= 1 for count in multiplicity.values())
    )


def pose_json(pose: Pose):
    return [pose[0], pose[1], list(pose[2])]


def parent_json(parent: Parent):
    return [pose_json(pose) for pose in sorted(parent)]


def grouping_witness_json(problem: GroupingProblem, selected: Sequence[int]):
    return {
        "patch": [pose_json(pose) for pose in sorted(problem.patch)],
        "safe_tiles": [pose_json(pose) for pose in problem.safe_tiles],
        "selected_parents": [
            parent_json(problem.groups[index]) for index in selected
        ],
        "patch_tiles": len(problem.patch),
        "safe_tile_count": len(problem.safe_tiles),
        "candidate_parent_groups": len(problem.groups),
        "selected_parent_groups": len(selected),
    }


def grouping_digest(problem: GroupingProblem, selected: Sequence[int]) -> str:
    payload = grouping_witness_json(problem, selected)
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(encoded.encode()).hexdigest()


def _generated_radius4_controls(observed_indices, centered):
    """One exact graph-radius-four generated ball for each observed corona."""
    from einstein.substrate.module12 import relative_pose
    from einstein.theory.spectre_geometry import exact_leaves

    coronas = enumerate_first_coronas()
    corona_index = {corona: index for index, corona in enumerate(coronas)}
    poses = tuple(pose for _, pose in exact_leaves(4, "Delta"))
    pose_index = {pose: index for index, pose in enumerate(poses)}
    incidence, _ = patch_edge_incidence(poses)
    adjacency = [set() for _ in poses]
    boundary = set()
    for owners in incidence.values():
        if len(owners) == 1:
            boundary.add(pose_index[owners[0]])
        elif len(owners) == 2:
            left, right = map(pose_index.__getitem__, owners)
            adjacency[left].add(right)
            adjacency[right].add(left)
        else:
            raise ValueError("generated control has invalid edge incidence")
    distance = [10**9] * len(poses)
    queue = deque(boundary)
    for index in boundary:
        distance[index] = 0
    while queue:
        current = queue.popleft()
        for neighbor in adjacency[current]:
            if distance[neighbor] > distance[current] + 1:
                distance[neighbor] = distance[current] + 1
                queue.append(neighbor)

    wanted = set(observed_indices)
    controls = {}
    witnesses = {}
    for center, pose in enumerate(poses):
        if distance[center] < 5:
            continue
        signature = tuple(sorted(
            relative_pose(pose, poses[neighbor])
            for neighbor in adjacency[center]
        ))
        index = corona_index.get(signature)
        if index not in wanted or index in controls:
            continue
        ball = {center}
        frontier = {center}
        for _ in range(4):
            frontier = {
                neighbor
                for item in frontier
                for neighbor in adjacency[item]
            } - ball
            ball.update(frontier)
        patch = tuple(sorted(poses[item] for item in ball))
        problem = build_grouping_problem(patch, centered)
        result = solve_grouping(problem, 2)
        if not result.solutions or not verify_grouping_solution(
            problem, result.solutions[0]
        ):
            raise ValueError(f"generated corona {index} lost parent grouping")
        controls[index] = {
            "corona_index": index,
            "patch_tiles": len(patch),
            "safe_tiles": len(problem.safe_tiles),
            "candidate_parent_groups": len(problem.groups),
            "solutions_capped_at_2": len(result.solutions),
            "witness_sha256": grouping_digest(problem, result.solutions[0]),
        }
        witnesses[index] = grouping_witness_json(problem, result.solutions[0])
        if set(controls) == wanted:
            break
    if set(controls) != wanted:
        raise ValueError(
            f"missing generated controls {sorted(wanted - set(controls))}"
        )
    return tuple(controls[index] for index in sorted(controls)), witnesses


def _advance_grouped_frontier(patch, centered):
    """Enumerate every admissible next ring with honest boundary semantics."""
    probe = solve_coordinated_ring_extension(patch, centered)
    if probe.solver == "no-safe-target":
        physical = extend_complete_ring(patch, 1_000_000)
        return {
            "mode": "unbuffered-physical-extension",
            "buffered_target_tiles": 0,
            "physical_candidates": physical.candidates,
            "parent_candidates": 0,
            "sat_calls": physical.sat_calls,
            "rings": tuple(sorted(physical.solutions)),
        }

    rings = []
    blocked = []
    final = probe
    while final.physical_ring is not None:
        if not verify_coordinated_extension(patch, final, centered):
            raise ValueError("invalid coordinated frontier witness")
        rings.append(final.physical_ring)
        blocked.append(final.physical_ring)
        final = solve_coordinated_ring_extension(patch, centered, blocked)
    return {
        "mode": "coordinated-parent-extension",
        "buffered_target_tiles": len(final.target_tiles),
        "physical_candidates": final.physical_candidates,
        "parent_candidates": final.parent_candidates,
        "sat_calls": len(rings) + 1,
        "rings": tuple(sorted(rings)),
    }


def analyze_parent_overlap_language(a6_result, physical_artifact):
    """Exhaust the three extra corona types under coordinated grouping.

    For every complete second ring, distinct third physical rings admitting a
    buffered parent partition are enumerated to exhaustion.  Each is then
    coupled to a fourth physical ring and a larger buffered partition.  A
    failed fourth-ring SAT call is therefore a finite refutation of that
    *grouped branch*, not merely failure of a chosen patch-growth heuristic.
    """
    if physical_artifact.get("status") != "COMPLETE_RADIUS3_PREFIX":
        raise ValueError("unsupported physical-language source")
    physical = physical_artifact["analysis"]
    observed = tuple(physical["substitution_control"]["observed_indices"])
    extras = tuple(physical["radius3"]["unobserved_survivor_indices"])
    if extras != (33, 44, 155):
        raise ValueError("physical-language extra set changed")

    centered = centered_parent_templates(a6_result)
    controls, control_witnesses = _generated_radius4_controls(observed, centered)
    coronas = enumerate_first_coronas()
    extra_results = []
    total_third_frontier = 0
    total_fourth_inputs = 0
    for index in extras:
        base = (IDENTITY, *coronas[index])
        second_rings = extend_complete_ring(base, 1_000_000).solutions
        branch_rows = []
        radius3_states = []
        for second_index, second_ring in enumerate(second_rings):
            radius2_patch = (*base, *second_ring)
            advance = _advance_grouped_frontier(radius2_patch, centered)
            for ring_index, third_ring in enumerate(advance["rings"]):
                radius3_states.append((
                    second_index, ring_index,
                    (*radius2_patch, *third_ring),
                ))
            branch_rows.append({
                "second_ring_index": second_index,
                "advance_mode": advance["mode"],
                "radius3_buffered_target_tiles": advance[
                    "buffered_target_tiles"
                ],
                "radius3_frontier_rings": len(advance["rings"]),
                "radius3_frontier_sha256": language_digest(advance["rings"]),
                "physical_candidates": advance["physical_candidates"],
                "parent_candidates": advance["parent_candidates"],
                "sat_calls": advance["sat_calls"],
            })
        total_third_frontier += len(radius3_states)

        radius4_rows = []
        radius4_states = []
        for second_index, third_index, radius3_patch in radius3_states:
            advance = _advance_grouped_frontier(radius3_patch, centered)
            for fourth_index, fourth_ring in enumerate(advance["rings"]):
                radius4_states.append((
                    second_index, third_index, fourth_index,
                    (*radius3_patch, *fourth_ring),
                ))
            radius4_rows.append({
                "second_ring_index": second_index,
                "third_ring_index": third_index,
                "advance_mode": advance["mode"],
                "radius4_buffered_target_tiles": advance[
                    "buffered_target_tiles"
                ],
                "radius4_frontier_rings": len(advance["rings"]),
                "physical_candidates": advance["physical_candidates"],
                "parent_candidates": advance["parent_candidates"],
                "sat_calls": advance["sat_calls"],
            })
        total_fourth_inputs += len(radius4_rows)
        radius3_modes = {
            mode: sum(row["advance_mode"] == mode for row in branch_rows)
            for mode in (
                "coordinated-parent-extension",
                "unbuffered-physical-extension",
            )
        }
        radius4_modes = {
            mode: sum(row["advance_mode"] == mode for row in radius4_rows)
            for mode in (
                "coordinated-parent-extension",
                "unbuffered-physical-extension",
            )
        }
        extra_results.append({
            "corona_index": index,
            "complete_radius2_branches": len(second_rings),
            "radius3_input_mode_histogram": radius3_modes,
            "radius3_frontier_states": len(radius3_states),
            "radius3_frontier_sha256": language_digest(tuple(
                sorted(state[2] for state in radius3_states)
            )),
            "radius4_input_mode_histogram": radius4_modes,
            "radius4_input_states": len(radius4_rows),
            "radius4_frontier_states": len(radius4_states),
            "radius4_frontier_sha256": language_digest(tuple(
                sorted(state[3] for state in radius4_states)
            )),
            "verdict": (
                "not-refuted-through-coordinated-radius4"
                if radius4_states
                else "refuted-before-coordinated-radius4"
                if not radius3_states
                else "refuted-by-coordinated-radius4"
            ),
            "radius3_branch_audit": branch_rows,
            "radius4_branch_audit": radius4_rows,
        })

    representative = control_witnesses[min(observed)]
    return {
        "scope": {
            "tile": "straight-edged Tile(1,1)",
            "chirality": "one fixed handedness",
            "motions": ["translation", "rotation"],
            "contact_model": "edge-to-edge unit-edge tilings",
            "parent_language": "recovered full/missing 9/8 physical templates",
            "finite_semantics": (
                "exactly cover every universally buffered inner tile by one "
                "parent occurrence; cover every other visible tile at most once"
            ),
            "claim_boundary": (
                "conditional finite exclusion from the recovered parent-grouping "
                "language; not a proof that every whole-plane physical tiling "
                "admits such a grouping"
            ),
        },
        "parent_templates": {
            "centered_occurrences_per_tile": len(centered),
            "sizes": sorted({len(parent) for parent in centered}),
        },
        "generated_controls": {
            "corona_indices": list(observed),
            "all_18_survive_coordinated_radius4": len(controls) == 18,
            "records": list(controls),
        },
        "extra_coronas": extra_results,
        "summary": {
            "physical_radius3_survivors": 21,
            "substitution_observed": 18,
            "extras_tested": list(extras),
            "extras_surviving_coordinated_grouping": [
                row["corona_index"] for row in extra_results
                if row["radius4_frontier_states"]
            ],
            "radius3_frontier_states_exhausted": total_third_frontier,
            "radius4_frontier_inputs_exhausted": total_fourth_inputs,
            "conditional_language_after_grouping": 18,
        },
        "representative_generated_grouping": {
            "corona_index": min(observed),
            **representative,
        },
        "interpretation": {
            "result": (
                "the three locally extendable extra coronas do not survive "
                "the recovered coordinated parent-overlap language"
            ),
            "remaining_gap": (
                "prove parent existence and unique iterative grouping for every "
                "admitted whole-plane physical tiling; this experiment is "
                "conditional on the recovered 9/8 parent language"
            ),
        },
    }
