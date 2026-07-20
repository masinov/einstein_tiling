"""Exact representation maps for the W3 Spectre D4 obligation.

The immediate 9/8-component tiling has two independent finite descriptions:
physical child-edge colors and the radius-one A6 collar.  This module makes
their bijection explicit and records the exact scale-normalization which turns
successive component layers back into a physical Spectre patch.

The normalization is phase-sensitive.  All component anchors in one phase
have one chirality and one rotation parity.  It toggles chirality uniformly,
maps translations through a unimodular integer matrix, and is equivariant
under a global 30-degree rotation.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Mapping, Sequence

from pysat.solvers import Cadical195

from einstein.substrate.module12 import (
    Pose,
    Vec4,
    apply_sr,
    compose_pose,
    relative_pose,
)
from einstein.theory.spectre_colored_interface import (
    ColoredCorona,
    colored_local_overlap_witnesses,
    colored_parent_corona,
)
from einstein.theory.spectre_component_language import completed_coronas
from einstein.theory.spectre_patch_language import (
    IDENTITY,
    edge_key,
    patch_edge_incidence,
    polygon_edges,
    poses_overlap,
    transformed_polygon,
)


ZERO: Vec4 = (0, 0, 0, 0)

# If p is a component anchor, NORMALIZE(p) is the anchor of its ordinary
# Spectre in the reflected next physical patch.  The matrices were recovered
# from the exact level-pair correspondence and then checked on every anchor of
# the level 3->2, 4->3 and 5->4 controls.  Both have determinant one.
NORMALIZATION_LINEAR = {
    0: (
        (0, 1, 1, -1),
        (1, 0, 2, -2),
        (-1, 1, -1, 2),
        (-2, 2, -1, 2),
    ),
    1: (
        (-1, 1, -1, -1),
        (1, 2, -1, 2),
        (1, 1, 0, 2),
        (1, -2, 2, 0),
    ),
}

NORMALIZATION_INVERSE = {
    0: (
        (2, -1, 2, -2),
        (2, -1, 1, -1),
        (-2, 2, 0, 1),
        (-1, 1, 1, 0),
    ),
    1: (
        (0, 2, -2, 1),
        (2, 0, 1, 1),
        (2, -1, 2, 1),
        (-1, -1, 1, -1),
    ),
}

# Offsets for even anchor rotations.  Odd phases are obtained by conjugating
# the complete formula by one global 30-degree rotation.
NORMALIZATION_OFFSET = {
    0: {
        0: (-2, -1, -2, 2),
        2: (2, 2, -4, -1),
        4: (4, 5, -2, -1),
        6: (2, 5, 2, 2),
        8: (-2, 2, 4, 5),
        10: (-4, -1, 2, 5),
    },
    1: {
        0: (4, 1, -2, 1),
        2: (2, 1, 2, 4),
        4: (-2, -2, 4, 7),
        6: (-4, -5, 2, 7),
        8: (-2, -5, -2, 4),
        10: (2, -2, -4, 1),
    },
}

NORMALIZATION_ROTATION_SHIFT = {0: 8, 1: 4}

# Every current component contributes its normalized ordinary Spectre.  Every
# second-parent marker contributes one additional Spectre at this relative
# pose.  The two sets are disjoint in the exact controls.
COMPANION_POSE: Pose = (0, 1, (1, -3, -2, 0))
MARKER_STATE_IDS = frozenset((10, 11, 12))


def _add(left: Vec4, right: Vec4) -> Vec4:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def _sub(left: Vec4, right: Vec4) -> Vec4:
    return tuple(a - b for a, b in zip(left, right))  # type: ignore[return-value]


def _matvec(matrix, vector: Vec4) -> Vec4:
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        for row in matrix
    )  # type: ignore[return-value]


def normalize_parent_pose(pose: Pose) -> Pose:
    """Normalize one component anchor to the next reflected physical phase."""
    chirality, rotation, translation = pose
    parity = rotation % 2
    even_rotation = (rotation - parity) % 12
    local_translation = apply_sr(0, -parity, translation)
    normalized_local = _add(
        _matvec(NORMALIZATION_LINEAR[chirality], local_translation),
        NORMALIZATION_OFFSET[chirality][even_rotation],
    )
    return (
        1 - chirality,
        (rotation + NORMALIZATION_ROTATION_SHIFT[chirality]) % 12,
        apply_sr(0, parity, normalized_local),
    )


def denormalize_parent_pose(pose: Pose) -> Pose:
    """The exact inverse of :func:`normalize_parent_pose`."""
    output_chirality, output_rotation, output_translation = pose
    chirality = 1 - output_chirality
    rotation = (
        output_rotation - NORMALIZATION_ROTATION_SHIFT[chirality]
    ) % 12
    parity = rotation % 2
    even_rotation = (rotation - parity) % 12
    normalized_local = apply_sr(0, -parity, output_translation)
    local_translation = _matvec(
        NORMALIZATION_INVERSE[chirality],
        _sub(
            normalized_local,
            NORMALIZATION_OFFSET[chirality][even_rotation],
        ),
    )
    return chirality, rotation, apply_sr(0, parity, local_translation)


def collar_signature(state: ColoredCorona):
    """Forget interface colors, retaining precisely the A6 radius-one collar."""
    kind, neighbors = state
    return (
        kind == "missing",
        tuple(sorted(
            (relative, neighbor_kind == "missing")
            for relative, neighbor_kind, _ in neighbors
        )),
    )


def colored_collar_bijection(states: Sequence[ColoredCorona]):
    """Return the canonical A6 state number for every colored state.

    A6 numbers states by sorting the exact oriented collar signatures.  A
    bijection therefore means that the child-edge colors add no hidden choice
    and, conversely, that no two colored interfaces collapse to one collar.
    """
    signatures = tuple(map(collar_signature, states))
    language = tuple(sorted(set(signatures)))
    if len(language) != len(states):
        raise ValueError("colored interfaces do not map injectively to collars")
    state_id = {signature: index for index, signature in enumerate(language)}
    colored_to_id = tuple(state_id[signature] for signature in signatures)
    if set(colored_to_id) != set(range(len(states))):
        raise ValueError("colored/collar correspondence is not surjective")
    return colored_to_id, language


def _component_support(base: Pose, kind: str, templates):
    full, missing = templates
    template = full if kind == "full" else missing
    return tuple(compose_pose(base, child) for child in template)


def audit_component_state_roundtrips(
    states: Sequence[ColoredCorona], templates,
):
    """Expand and re-encode each of the 17 component-interface states."""
    records = []
    for state_index, state in enumerate(states):
        bases = (IDENTITY, *(neighbor[0] for neighbor in state[1]))
        kinds = (state[0], *(neighbor[1] for neighbor in state[1]))
        fibers = {
            base: set(_component_support(base, kind, templates))
            for base, kind in zip(bases, kinds)
        }
        pairwise_disjoint = all(
            fibers[left].isdisjoint(fibers[right])
            and not any(
                poses_overlap(a, b)
                for a in fibers[left] for b in fibers[right]
            )
            for position, left in enumerate(bases)
            for right in bases[:position]
        )
        patch = tuple(sorted(set().union(*fibers.values())))
        mapping = {
            child: base for base, fiber in fibers.items() for child in fiber
        }
        incidence, _ = patch_edge_incidence(patch)
        edges_by_tile = defaultdict(list)
        for key, owners in incidence.items():
            for tile in owners:
                edges_by_tile[tile].append((key, owners))
        recovered = colored_parent_corona(
            IDENTITY,
            patch,
            mapping,
            templates,
            incidence=incidence,
            fibers=fibers,
            edges_by_tile=edges_by_tile,
            trust_mapping_absence=True,
        )
        center = fibers[IDENTITY]
        central_external_edges = sum(
            bool(set(owners) & center) and not set(owners) <= center
            for owners in incidence.values()
        )
        central_exposed_edges = sum(
            len(owners) == 1 and owners[0] in center
            for owners in incidence.values()
        )
        contact_colors = sum(len(neighbor[2]) for neighbor in state[1])
        records.append({
            "state_index": state_index,
            "kind": state[0],
            "component_tiles": len(center),
            "star_tiles": len(patch),
            "central_external_edges": central_external_edges,
            "contact_colors": contact_colors,
            "central_exposed_edges": central_exposed_edges,
            "pairwise_component_disjoint": pairwise_disjoint,
            "roundtrip_exact": recovered == state,
        })
    return tuple(records)


def next_physical_patch(
    parent_states: Mapping[Pose, int], colored_to_state_id: Sequence[int],
):
    """Map a finite colored component patch to its reflected physical patch.

    The caller supplies colored-state indices at exact component anchors.
    Boundary completeness is a separate question; the map itself is total and
    injective once the global phase is fixed.
    """
    ordinary = {
        normalize_parent_pose(parent) for parent in parent_states
    }
    companion = {
        compose_pose(normalize_parent_pose(parent), COMPANION_POSE)
        for parent, colored_state in parent_states.items()
        if colored_to_state_id[colored_state] in MARKER_STATE_IDS
    }
    return tuple(sorted(ordinary | companion)), ordinary, companion


def faithful_radius_two_assignment(
    problem, kernel, colored_to_state_id: Sequence[int],
):
    """Find a radius-two state assignment with a valid central D4 image.

    Each parent anchor always emits its normalized ordinary Spectre and emits
    the companion precisely in marker states 10--12.  In addition to the
    exact parent-state constraints, this SAT encoding forbids duplicate or
    interior-overlapping output tiles and requires every primitive edge of
    the central ordinary tile (and of its companion, when the root is a
    marker) to have exactly one other owner in the finite image.

    This is a local faithful-map filter.  Satisfiability does not assert that
    the assignment extends to the plane or was induced by a physical L18
    tiling.
    """
    positions = problem.positions
    domains = problem.domains
    variables = {}
    clauses = []
    next_variable = 1
    for position, domain in enumerate(domains):
        row = []
        for state in domain:
            variables[position, state] = next_variable
            row.append(next_variable)
            next_variable += 1
        clauses.append(row)
        for offset, variable in enumerate(row):
            for other in row[:offset]:
                clauses.append([-variable, -other])

    for left in range(len(positions)):
        for right in range(left):
            relative = relative_pose(positions[left], positions[right])
            for a in domains[left]:
                for b in domains[right]:
                    if not kernel.compatible(relative, a, b):
                        clauses.append([
                            -variables[left, a], -variables[right, b],
                        ])

    marker_states = {
        state for state, collar in enumerate(colored_to_state_id)
        if collar in MARKER_STATE_IDS
    }
    ordinary = tuple(map(normalize_parent_pose, positions))
    companion = tuple(
        compose_pose(pose, COMPANION_POSE) for pose in ordinary
    )
    if len(set(ordinary)) != len(ordinary) or any(
        poses_overlap(left, right)
        for offset, left in enumerate(ordinary)
        for right in ordinary[:offset]
    ):
        return None

    marker_variables = {
        position: tuple(
            variables[position, state]
            for state in domains[position] if state in marker_states
        )
        for position in range(len(positions))
    }

    # A selected companion must be distinct and interior-disjoint from every
    # unconditional ordinary output tile.
    for position, candidate in enumerate(companion):
        if any(
            candidate == fixed or poses_overlap(candidate, fixed)
            for fixed in ordinary
        ):
            clauses.extend(
                [-variable] for variable in marker_variables[position]
            )

    # Likewise, two selected companions may not coincide or overlap.
    for left, left_pose in enumerate(companion):
        for right in range(left):
            right_pose = companion[right]
            if left_pose != right_pose and not poses_overlap(
                left_pose, right_pose,
            ):
                continue
            for left_variable in marker_variables[left]:
                for right_variable in marker_variables[right]:
                    clauses.append([-left_variable, -right_variable])

    edge_sets = {
        pose: {
            edge_key(edge)
            for edge in polygon_edges(transformed_polygon(pose))
        }
        for pose in set(ordinary) | set(companion)
    }

    def require_complete(center):
        for edge in edge_sets[center]:
            fixed_owners = [
                index for index, pose in enumerate(ordinary)
                if pose != center and edge in edge_sets[pose]
            ]
            conditional = [
                variable
                for index, pose in enumerate(companion)
                if pose != center and edge in edge_sets[pose]
                for variable in marker_variables[index]
            ]
            if len(fixed_owners) > 1:
                return False
            if fixed_owners:
                clauses.extend([-variable] for variable in conditional)
                continue
            if not conditional:
                return False
            clauses.append(conditional)
            for offset, variable in enumerate(conditional):
                for other in conditional[:offset]:
                    clauses.append([-variable, -other])
        return True

    root_position = positions.index(IDENTITY)
    if not require_complete(ordinary[root_position]):
        return None
    if problem.root_state in marker_states:
        if not require_complete(companion[root_position]):
            return None

    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        positive = {
            literal for literal in solver.get_model() if literal > 0
        }
    return tuple(
        next(
            state for state in domains[position]
            if variables[position, state] in positive
        )
        for position in range(len(positions))
    )


def audit_radius_one_next_physical(
    states: Sequence[ColoredCorona], colored_to_state_id: Sequence[int],
):
    """Classify every exact colored radius-one star under the D4 map.

    This is deliberately a diagnostic, not a closure assertion.  A colored
    radius-one overlap witness need not extend to the physical-derived hull.
    Overlap witnesses here identify the precise extra context D4 must exclude.
    """
    base: Pose = (1, 0, ZERO)
    counts = Counter()
    signatures_by_center = defaultdict(set)
    total_by_center = Counter()
    for center_index, state in enumerate(states):
        for witness in colored_local_overlap_witnesses(
            states, center_index, limit=1_000_000,
        ):
            total_by_center[center_index] += 1
            bases = (
                base,
                *(compose_pose(base, neighbor[0]) for neighbor in state[1]),
            )
            assignment = dict(zip(bases, (center_index, *witness)))
            patch, ordinary, _ = next_physical_patch(
                assignment, colored_to_state_id,
            )
            if len(patch) != len(set(patch)):
                counts["duplicate_output_tiles"] += 1
                continue
            if any(
                poses_overlap(left, right)
                for position, left in enumerate(patch)
                for right in patch[:position]
            ):
                counts["output_overlap"] += 1
                continue
            center = normalize_parent_pose(base)
            completed = dict(completed_coronas(patch))
            if center not in completed:
                counts["central_ordinary_not_buffered"] += 1
                continue
            counts["central_ordinary_valid"] += 1
            signatures_by_center[center_index].add(completed[center])
            if center not in ordinary:
                raise AssertionError("central ordinary tile disappeared")
    return {
        "total_stars": sum(total_by_center.values()),
        "total_by_center": dict(sorted(total_by_center.items())),
        "outcomes": dict(sorted(counts.items())),
        "central_signature_count_by_state": {
            str(index): len(signatures_by_center[index])
            for index in range(len(states))
        },
        "distinct_buffered_central_signatures": len({
            signature
            for signatures in signatures_by_center.values()
            for signature in signatures
        }),
        "buffered_signature_owner_sets_are_disjoint": all(
            not signatures_by_center[left] & signatures_by_center[right]
            for left in range(len(states))
            for right in range(left)
        ),
    }


def matrix_product(left, right):
    columns = tuple(zip(*right))
    return tuple(
        tuple(sum(a * b for a, b in zip(row, column)) for column in columns)
        for row in left
    )


def two_level_translation_matrices():
    """Translation maps after both chirality phases."""
    return {
        "0_then_1": matrix_product(
            NORMALIZATION_LINEAR[1], NORMALIZATION_LINEAR[0]
        ),
        "1_then_0": matrix_product(
            NORMALIZATION_LINEAR[0], NORMALIZATION_LINEAR[1]
        ),
    }
