"""Ancestry-blind finite physical patch language for straight Spectres.

The kernel enumerates same-chirality, edge-to-edge coronas directly from the
exact 14-edge Tile(1,1) polygon.  No substitution labels, child slots or
parent paths enter the enumeration.  Generated substitution patches are a
separate positive-control channel used only after the bare language is fixed.

This is a finite local-language experiment, not a whole-plane extension
theorem.  A first corona may fail at the next ring, and a second-corona witness
may still fail later.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cache
from hashlib import sha256
import json
from typing import Iterable, Sequence

from einstein.tilings.substitution import SPECTRE_TILE_BOUNDARY
from einstein.geometry.cyclotomic import (
    Pose,
    Vec4,
    apply_sr,
    compare_quadratic,
    compose_pose,
    inverse_pose,
    madd,
    mneg,
    relative_pose,
)
from einstein.tilings.spectre.geometry import (
    _coordinate_pairs,
    _polygons_overlap_interior,
    _transformed_polygon,
)


IDENTITY: Pose = (0, 0, (0, 0, 0, 0))


@dataclass(frozen=True)
class RingExtension:
    """Capped exact-cover result for one more complete polygon ring."""

    solutions: tuple[tuple[Pose, ...], ...]
    candidates: int
    sat_calls: int
    solver: str


@cache
def transformed_polygon(pose: Pose):
    return _transformed_polygon(pose)


@cache
def exact_bounding_box(pose: Pose):
    coordinates = tuple(_coordinate_pairs(point) for point in transformed_polygon(pose))

    def extreme(axis: int, want_max: bool):
        value = coordinates[0][axis]
        for coordinate in coordinates[1:]:
            comparison = compare_quadratic(coordinate[axis], value)
            if (comparison > 0) == want_max and comparison != 0:
                value = coordinate[axis]
        return value

    return extreme(0, False), extreme(0, True), extreme(1, False), extreme(1, True)


@cache
def poses_overlap(left: Pose, right: Pose) -> bool:
    if right < left:
        left, right = right, left
    left_box = exact_bounding_box(left)
    right_box = exact_bounding_box(right)
    if (
        compare_quadratic(left_box[1], right_box[0]) <= 0
        or compare_quadratic(right_box[1], left_box[0]) <= 0
        or compare_quadratic(left_box[3], right_box[2]) <= 0
        or compare_quadratic(right_box[3], left_box[2]) <= 0
    ):
        return False
    return _polygons_overlap_interior(
        transformed_polygon(left), transformed_polygon(right)
    )


def _subtract(left: Vec4, right: Vec4) -> Vec4:
    return madd(left, mneg(right))


def polygon_edges(polygon) -> tuple[tuple[Vec4, Vec4], ...]:
    return tuple(zip(polygon, polygon[1:] + polygon[:1]))


def edge_key(edge: tuple[Vec4, Vec4]) -> tuple[Vec4, Vec4]:
    return tuple(sorted(edge))  # type: ignore[return-value]


def patch_edge_incidence(poses: Iterable[Pose]):
    """Map every exact unit edge to its incident tile poses."""
    incidence: dict[tuple[Vec4, Vec4], list[Pose]] = defaultdict(list)
    directed: dict[tuple[Vec4, Vec4], tuple[Vec4, Vec4]] = {}
    for pose in poses:
        polygon = transformed_polygon(pose)
        for edge in polygon_edges(polygon):
            key = edge_key(edge)
            incidence[key].append(pose)
            directed.setdefault(key, edge)
    return incidence, directed


def mates_across_directed_edge(start: Vec4, end: Vec4) -> tuple[Pose, ...]:
    """All rotation/translation copies whose boundary reverses one edge."""
    target_vector = _subtract(start, end)
    found = set()
    for rotation in range(12):
        boundary = tuple(
            apply_sr(0, rotation, point) for point in SPECTRE_TILE_BOUNDARY
        )
        for local_start, local_end in polygon_edges(boundary):
            if _subtract(local_end, local_start) != target_vector:
                continue
            translation = _subtract(end, local_start)
            found.add((0, rotation, translation))
    return tuple(sorted(found))


def _candidate_ring_tiles(patch: Sequence[Pose]):
    patch = tuple(patch)
    patch_set = set(patch)
    incidence, directed = patch_edge_incidence(patch)
    if max(map(len, incidence.values()), default=0) > 2:
        raise ValueError("patch has an edge with more than two incident tiles")
    exposed = tuple(sorted(key for key, owners in incidence.items() if len(owners) == 1))
    exposed_index = {key: i for i, key in enumerate(exposed)}
    internal = {key for key, owners in incidence.items() if len(owners) == 2}
    candidates: dict[Pose, frozenset[int]] = {}
    for key in exposed:
        start, end = directed[key]
        for pose in mates_across_directed_edge(start, end):
            if pose in patch_set:
                continue
            if any(
                poses_overlap(pose, other)
                for other in patch
            ):
                continue
            polygon = transformed_polygon(pose)
            candidate_edges = {edge_key(edge) for edge in polygon_edges(polygon)}
            if candidate_edges & internal:
                continue
            covered = frozenset(
                exposed_index[edge]
                for edge in candidate_edges & set(exposed)
            )
            if covered:
                candidates[pose] = covered
    return exposed, candidates


def extend_complete_ring(
    patch: Sequence[Pose], solution_limit: int = 2
) -> RingExtension:
    """Cover every exposed patch edge by one nonoverlapping new tile.

    The result is complete for existence and uniqueness up to
    ``solution_limit``.  With the default limit, zero means refuted at the
    next ring, one means exactly one extension, and two means at least two.
    """
    if solution_limit < 1:
        raise ValueError("solution_limit must be positive")
    exposed, candidate_cover = _candidate_ring_tiles(patch)
    candidates = tuple(sorted(candidate_cover))
    conflicts = [set() for _ in candidates]
    for i, left in enumerate(candidates):
        for j in range(i):
            if poses_overlap(left, candidates[j]):
                conflicts[i].add(j)
                conflicts[j].add(i)
    by_edge: list[list[int]] = [[] for _ in exposed]
    for i, pose in enumerate(candidates):
        for edge in candidate_cover[pose]:
            by_edge[edge].append(i)
    if not all(by_edge):
        return RingExtension((), len(candidates), 0, "CaDiCaL 1.9.5")

    from pysat.solvers import Cadical195

    variables = tuple(range(1, len(candidates) + 1))
    clauses: list[list[int]] = []
    for covering in by_edge:
        edge_variables = [variables[i] for i in covering]
        clauses.append(edge_variables)
        for position, left in enumerate(edge_variables):
            for right in edge_variables[position + 1:]:
                clauses.append([-left, -right])
    for left, adjacent in enumerate(conflicts):
        for right in adjacent:
            if left < right:
                clauses.append([-variables[left], -variables[right]])

    solutions: list[tuple[Pose, ...]] = []
    calls = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < solution_limit:
            calls += 1
            if not solver.solve():
                break
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(sorted(
                candidates[i] for i, variable in enumerate(variables)
                if variable in positive
            ))
            solutions.append(selected)
            solver.add_clause([
                -variables[i] for i, candidate in enumerate(candidates)
                if candidate in selected
            ])
    return RingExtension(
        tuple(sorted(solutions)), len(candidates), calls, "CaDiCaL 1.9.5"
    )


@cache
def enumerate_first_coronas() -> tuple[tuple[Pose, ...], ...]:
    """Enumerate every exact same-chirality edge-to-edge first corona."""
    extension = extend_complete_ring((IDENTITY,), solution_limit=1_000_000)
    return tuple(sorted(extension.solutions))


def complete_corona_signatures(poses: Sequence[Pose]) -> tuple[tuple[Pose, ...], ...]:
    """Rooted first-corona signatures whose central tile has no exposed edge."""
    poses = tuple(poses)
    incidence, _ = patch_edge_incidence(poses)
    adjacency = [set() for _ in poses]
    exposed = [0 for _ in poses]
    index = {pose: i for i, pose in enumerate(poses)}
    for owners in incidence.values():
        if len(owners) == 1:
            exposed[index[owners[0]]] += 1
        elif len(owners) == 2:
            left, right = map(index.__getitem__, owners)
            adjacency[left].add(right)
            adjacency[right].add(left)
        else:
            raise ValueError("more than two tiles share a physical edge")
    return tuple(sorted({
        tuple(sorted(relative_pose(poses[i], poses[j]) for j in adjacency[i]))
        for i in range(len(poses))
        if exposed[i] == 0
    }))


def central_parent_candidates(
    full_template: Sequence[Pose], missing_template: Sequence[Pose]
) -> tuple[frozenset[Pose], ...]:
    """Every full/missing parent occurrence containing the identity tile."""
    found = set()
    for template in (tuple(full_template), tuple(missing_template)):
        for relative in template:
            base = inverse_pose(relative)
            group = frozenset(compose_pose(base, child) for child in template)
            if IDENTITY not in group:
                raise AssertionError("derived parent does not contain central tile")
            found.add(group)
    return tuple(sorted(found, key=lambda group: (len(group), tuple(sorted(group)))))


def compatible_parents(
    corona: Sequence[Pose], parent_candidates: Sequence[frozenset[Pose]]
) -> tuple[frozenset[Pose], ...]:
    """Parent occurrences not contradicted by a complete first corona."""
    patch = frozenset((IDENTITY, *corona))
    compatible = []
    for parent in parent_candidates:
        if all(
            child in patch
            or all(
                other == child
                or not poses_overlap(child, other)
                for other in patch
            )
            for child in parent
        ):
            compatible.append(parent)
    return tuple(compatible)


def pose_json(pose: Pose):
    return [pose[0], pose[1], list(pose[2])]


def canonical_json(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def language_digest(coronas: Sequence[Sequence[Pose]]) -> str:
    payload = [[pose_json(pose) for pose in corona] for corona in coronas]
    return sha256(canonical_json(payload).encode()).hexdigest()


def histogram(values: Iterable[int]) -> dict[str, int]:
    return {
        str(key): count for key, count in sorted(Counter(values).items())
    }


def _parse_template(rows) -> tuple[Pose, ...]:
    return tuple((int(s), int(r), tuple(map(int, translation)))
                 for s, r, translation in rows)


def analyze_physical_patch_language(a6_result, generated_levels=(3, 4)):
    """Build the exact radius-three prefix and targeted radius-four probe."""
    selected = a6_result["selected_rule"]
    full = _parse_template(selected["full"])
    missing = _parse_template(selected["missing"])
    parents = central_parent_candidates(full, missing)
    coronas = enumerate_first_coronas()

    from einstein.tilings.spectre.geometry import LABELS, exact_leaves

    generated = set()
    generated_checks = []
    for level in generated_levels:
        level_language = set()
        for label in LABELS:
            signatures = complete_corona_signatures(
                [pose for _, pose in exact_leaves(level, label)]
            )
            level_language.update(signatures)
            generated_checks.append({
                "level": level,
                "root_label": label,
                "complete_corona_types": len(signatures),
                "language_sha256": language_digest(signatures),
            })
        generated.update(level_language)

    parent_counts = []
    extension_counts = []
    records = []
    cross = Counter()
    for index, corona in enumerate(coronas):
        compatible = compatible_parents(corona, parents)
        extension = extend_complete_ring((IDENTITY, *corona), 2)
        extension_count = min(len(extension.solutions), 2)
        complete_extension = extension
        third_witness_index = None
        third_witness = None
        if extension.solutions:
            complete_extension = extend_complete_ring(
                (IDENTITY, *corona), 1_000_000
            )
            for solution_index, second_ring in enumerate(
                complete_extension.solutions
            ):
                candidate = extend_complete_ring(
                    (IDENTITY, *corona, *second_ring), 1
                )
                if candidate.solutions:
                    third_witness_index = solution_index
                    third_witness = candidate
                    break
        observed = corona in generated
        parent_counts.append(len(compatible))
        extension_counts.append(extension_count)
        cross[(observed, len(compatible), extension_count)] += 1
        records.append({
            "index": index,
            "neighbors": [pose_json(pose) for pose in corona],
            "neighbor_count": len(corona),
            "substitution_observed": observed,
            "compatible_central_parents": len(compatible),
            "second_ring_status": (
                "refuted" if extension_count == 0
                else "unique" if extension_count == 1
                else "multiple"
            ),
            "second_ring_candidate_tiles": extension.candidates,
            "second_ring_sat_calls": extension.sat_calls,
            "second_ring_total_solutions": len(complete_extension.solutions),
            "second_ring_witness_sha256": language_digest(
                extension.solutions
            ),
            "third_ring_status": (
                "witnessed" if third_witness is not None else "refuted"
            ),
            "third_ring_second_solution_index": third_witness_index,
            "third_ring_candidate_tiles": (
                third_witness.candidates if third_witness is not None else None
            ),
            "third_ring_second_ring_poses": (
                [pose_json(pose) for pose in complete_extension.solutions[
                    third_witness_index
                ]]
                if third_witness_index is not None else None
            ),
            "third_ring_extension_poses": (
                [pose_json(pose) for pose in third_witness.solutions[0]]
                if third_witness is not None else None
            ),
            "third_ring_witness_sha256": (
                language_digest(third_witness.solutions)
                if third_witness is not None else None
            ),
        })

    survivor_indices = [
        record["index"] for record in records
        if record["second_ring_status"] != "refuted"
    ]
    observed_indices = [
        record["index"] for record in records
        if record["substitution_observed"]
    ]
    unique_parent_indices = [
        record["index"] for record in records
        if record["compatible_central_parents"] == 1
    ]
    third_survivor_indices = [
        record["index"] for record in records
        if record["third_ring_status"] == "witnessed"
    ]
    # Discovery locators for one exact fourth-ring witness on each of the
    # three unobserved radius-three branches.  They are not assumptions: the
    # cold verifier reconstructs the indexed SAT models and checks the next
    # exact cover.  This is a targeted existence probe, not a complete r=4
    # language enumeration.
    radius4_locators = {33: (0, 130), 44: (24, 13), 155: (50, 13)}
    radius4_witnesses = []
    for index, (second_index, third_index) in radius4_locators.items():
        corona = coronas[index]
        second_extensions = extend_complete_ring(
            (IDENTITY, *corona), 1_000_000
        ).solutions
        if len(second_extensions) <= second_index:
            raise ValueError("stored radius-four second-ring locator vanished")
        second_ring = second_extensions[second_index]
        third_extensions = extend_complete_ring(
            (IDENTITY, *corona, *second_ring), 1_000_000
        ).solutions
        if len(third_extensions) <= third_index:
            raise ValueError("stored radius-four third-ring locator vanished")
        third_ring = third_extensions[third_index]
        fourth = extend_complete_ring(
            (IDENTITY, *corona, *second_ring, *third_ring), 1
        )
        if not fourth.solutions:
            raise ValueError("stored radius-four witness no longer extends")
        radius4_witnesses.append({
            "corona_index": index,
            "second_ring_solution_index": second_index,
            "third_ring_solution_index": third_index,
            "fourth_ring_candidate_tiles": fourth.candidates,
            "fourth_ring_witness_sha256": language_digest(fourth.solutions),
        })
    return {
        "scope": {
            "tile": "straight-edged Tile(1,1)",
            "chirality": "one fixed handedness",
            "motions": ["translation", "rotation"],
            "reflections_allowed": False,
            "contact_model": "edge-to-edge unit-edge tilings",
            "radius_completed": 3,
            "ancestry_used_in_enumeration": False,
            "claim_boundary": (
                "complete existential central-corona language through three "
                "rings; no claim that every radius-three survivor extends to "
                "a whole-plane tiling"
            ),
        },
        "radius1": {
            "candidate_neighbor_poses": extend_complete_ring(
                (IDENTITY,), 1
            ).candidates,
            "complete_coronas": len(coronas),
            "language_sha256": language_digest(coronas),
            "neighbor_count_histogram": histogram(map(len, coronas)),
            "compatible_parent_count_histogram": histogram(parent_counts),
            "unique_parent_coronas": len(unique_parent_indices),
            "unique_parent_indices": unique_parent_indices,
        },
        "radius2": {
            "refuted_first_coronas": extension_counts.count(0),
            "unique_extensions": extension_counts.count(1),
            "multiple_extensions": extension_counts.count(2),
            "surviving_first_coronas": len(survivor_indices),
            "survivor_indices": survivor_indices,
        },
        "radius3": {
            "refuted_first_coronas": len(coronas) - len(third_survivor_indices),
            "surviving_first_coronas": len(third_survivor_indices),
            "survivor_indices": third_survivor_indices,
            "compatible_parent_count_histogram": histogram(
                records[index]["compatible_central_parents"]
                for index in third_survivor_indices
            ),
            "unique_parent_survivors": sum(
                records[index]["compatible_central_parents"] == 1
                for index in third_survivor_indices
            ),
            "unobserved_survivor_indices": [
                index for index in third_survivor_indices
                if not records[index]["substitution_observed"]
            ],
            "second_ring_solutions_exhausted_for_refutations": True,
        },
        "radius4_targeted_probe": {
            "scope": "existence witnesses for the three unobserved r3 survivors only",
            "complete_language_enumeration": False,
            "all_three_extend": len(radius4_witnesses) == 3,
            "witnesses": radius4_witnesses,
        },
        "substitution_control": {
            "generated_levels": list(generated_levels),
            "root_labels": list(LABELS),
            "checks": generated_checks,
            "observed_first_coronas": len(generated),
            "observed_language_sha256": language_digest(tuple(sorted(generated))),
            "observed_indices": observed_indices,
            "all_observed_are_bare_legal": generated <= set(coronas),
            "all_observed_survive_radius2": all(
                records[index]["second_ring_status"] != "refuted"
                for index in observed_indices
            ),
            "unobserved_radius1_coronas": len(coronas) - len(generated),
            "unobserved_radius2_survivors": sum(
                not records[index]["substitution_observed"]
                for index in survivor_indices
            ),
            "all_observed_survive_radius3": all(
                records[index]["third_ring_status"] == "witnessed"
                for index in observed_indices
            ),
            "unobserved_radius3_survivors": sum(
                not records[index]["substitution_observed"]
                for index in third_survivor_indices
            ),
        },
        "cross_tabulation": [
            {
                "substitution_observed": observed,
                "compatible_central_parents": parents_count,
                "second_ring_solutions_capped_at_2": extensions,
                "coronas": count,
            }
            for (observed, parents_count, extensions), count in sorted(cross.items())
        ],
        "interpretation": {
            "finite_language_contraction": "166 radius-one coronas -> 30 radius-two survivors",
            "radius3_contraction": "30 radius-two survivors -> 21 radius-three survivors",
            "substitution_language": "18 observed coronas, all among the 30 survivors",
            "remaining_gap": (
                "3 radius-three survivors are not observed in the generated "
                "control language and all have targeted radius-four witnesses; "
                "blind radius growth alone has not yet separated them"
            ),
            "ownership_warning": (
                "all eight radius-one coronas that locally force one recovered "
                "parent are refuted at radius two, while none of the 21 "
                "radius-three survivors has a unique central parent; local "
                "parent uniqueness alone is not evidence of membership in the "
                "tiling hull, and valid grouping must coordinate ownership "
                "across multiple centers"
            ),
        },
        "records": records,
    }
