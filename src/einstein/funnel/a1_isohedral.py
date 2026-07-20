"""Grid-aligned isohedral-surround SAT control.

Kaplan's Proposition 1 (EPTCS 403, 2024) says that a shape admits an
isohedral tiling iff it has a simply connected first surround in which every
neighbour is extendable by the same surround.  This module implements that
finite criterion for the kite grid.

The base CNF is an exact cover of the edge halo.  Inverse clauses and direct
composition-conflict clauses enforce extendability.  Hole-bearing models are
cut lazily.  Positive certificates are independently checked geometrically;
an UNSAT result is exact for grid-aligned surrounds.

This is an early periodicity filter.  It cannot detect k-anisohedral tilings
for k >= 2 and a negative result is not evidence of aperiodicity.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from einstein.funnel.a2_heesch import has_hole, ring
from einstein.funnel.a6_polykite import hex_to_module, kite_op_sr
from einstein.substrate.kitegrid import (
    N_OPS,
    is_center,
    transform_cell,
    translate_cell,
)
from einstein.substrate.module12 import compose_pose, inverse_pose


Cell = tuple[int, int, int]
GridPose = tuple[int, int, int]
IDENTITY: GridPose = (0, 0, 0)


@dataclass(frozen=True)
class Neighbor:
    pose: GridPose
    cells: frozenset[Cell]


def apply_grid_pose(pose: GridPose, cell: Cell) -> Cell:
    """Apply ``(D6 operation, hex-x translation, hex-y translation)``."""

    operation, tx, ty = pose
    if not 0 <= operation < N_OPS or not is_center((tx, ty)):
        raise ValueError(f"invalid kite-grid pose: {pose}")
    return translate_cell(transform_cell(cell, operation), (tx, ty))


def _to_module_pose(pose: GridPose):
    operation, tx, ty = pose
    reflection, rotation = kite_op_sr(operation)
    return reflection, rotation, hex_to_module((tx, ty))


def _from_module_pose(pose) -> GridPose:
    reflection, rotation, translation = pose
    if rotation % 2 or translation[1] or translation[3]:
        raise AssertionError("pose left the kite-grid p6m subgroup")
    if reflection:
        operation = 6 + (((rotation - 6) % 12) // 2)
    else:
        operation = (rotation // 2) % 6
    tx, ty = translation[0], translation[2]
    result = operation, tx, ty
    if not is_center((tx, ty)):
        raise AssertionError("composed pose has a non-lattice translation")
    return result


def compose_grid_poses(left: GridPose, right: GridPose) -> GridPose:
    """Compose grid isometries: apply ``right`` and then ``left``."""

    return _from_module_pose(compose_pose(
        _to_module_pose(left),
        _to_module_pose(right),
    ))


def inverse_grid_pose(pose: GridPose) -> GridPose:
    return _from_module_pose(inverse_pose(_to_module_pose(pose)))


def pose_cells(shape: Iterable[Cell], pose: GridPose) -> frozenset[Cell]:
    return frozenset(apply_grid_pose(pose, cell) for cell in shape)


def surround_halo(shape: Iterable[Cell]) -> frozenset[Cell]:
    """Empty cells sharing any boundary point with the central tile.

    Covering only edge-neighbours can leave an uncovered angular sector at a
    vertex, so it does not guarantee that the centre lies in the topological
    interior of the 1-patch.  This is the same full corona ring used by A2.
    """

    return ring(frozenset(shape))


def neighbor_placements(shape: Iterable[Cell]) -> tuple[Neighbor, ...]:
    """All marked D6 copies that can occupy at least one halo cell."""

    shape = tuple(shape)
    seed = frozenset(shape)
    halo = surround_halo(shape)
    found: dict[GridPose, Neighbor] = {}
    for operation in range(N_OPS):
        image = tuple(transform_cell(cell, operation) for cell in shape)
        for target in halo:
            for source in image:
                if source[2] != target[2]:
                    continue
                tx = target[0] - source[0]
                ty = target[1] - source[1]
                if not is_center((tx, ty)):
                    continue
                pose = operation, tx, ty
                if pose in found:
                    continue
                cells = frozenset(
                    translate_cell(cell, (tx, ty)) for cell in image
                )
                if cells & seed or not cells & halo:
                    continue
                found[pose] = Neighbor(pose, cells)
    return tuple(found[pose] for pose in sorted(found))


def _base_and_extendability_clauses(shape, neighbors):
    """Build the direct finite encoding of Kaplan's extendability criterion."""

    seed = frozenset(shape)
    halo = surround_halo(shape)
    by_halo: dict[Cell, list[int]] = {cell: [] for cell in halo}
    by_cell: dict[Cell, list[int]] = defaultdict(list)
    by_pose = {neighbor.pose: i for i, neighbor in enumerate(neighbors, 1)}
    for variable, neighbor in enumerate(neighbors, 1):
        for cell in neighbor.cells:
            by_cell[cell].append(variable)
            if cell in by_halo:
                by_halo[cell].append(variable)

    clauses: set[tuple[int, ...]] = set()
    for variables in by_halo.values():
        if not variables:
            return (), {"uncovered_halo": 1}
        clauses.add(tuple(sorted(variables)))
    for variables in by_cell.values():
        for offset, left in enumerate(variables):
            for right in variables[offset + 1:]:
                clauses.add((-right, -left) if right > left else (-left, -right))

    inverse_clauses = 0
    for variable, neighbor in enumerate(neighbors, 1):
        inverse = inverse_grid_pose(neighbor.pose)
        inverse_variable = by_pose.get(inverse)
        if inverse_variable is None:
            raise AssertionError(f"inverse neighbour is absent: {neighbor.pose}")
        clause = (-variable, inverse_variable)
        if clause not in clauses:
            clauses.add(clause)
            inverse_clauses += 1

    conflict_clauses = 0
    for left_variable, left in enumerate(neighbors, 1):
        for right_variable, right in enumerate(neighbors, 1):
            composed = compose_grid_poses(left.pose, right.pose)
            transformed = pose_cells(shape, composed)
            if transformed != seed and transformed & seed:
                clause = tuple(sorted((-left_variable, -right_variable)))
                if clause not in clauses:
                    clauses.add(clause)
                    conflict_clauses += 1
            conflicting_variables = {
                variable
                for cell in transformed
                for variable in by_cell.get(cell, ())
                if neighbors[variable - 1].cells != transformed
            }
            for other in conflicting_variables:
                clause = tuple(sorted(
                    (-left_variable, -right_variable, -other)
                ))
                if clause not in clauses:
                    clauses.add(clause)
                    conflict_clauses += 1

    stats = {
        "halo_cells": len(halo),
        "neighbors": len(neighbors),
        "inverse_clauses": inverse_clauses,
        "extendability_conflict_clauses": conflict_clauses,
        "clauses": len(clauses),
    }
    return tuple(sorted(clauses)), stats


def verify_isohedral_surround(shape, certificate) -> bool:
    """Cold geometric check of one finite Proposition-1 witness."""

    if certificate.get("kind") != "isohedral-surround":
        return False
    shape = tuple(shape)
    seed = frozenset(shape)
    try:
        poses = [tuple(map(int, pose)) for pose in certificate["placements"]]
        cells = [pose_cells(shape, pose) for pose in poses]
    except (KeyError, TypeError, ValueError):
        return False
    if len(poses) != len(set(poses)):
        return False
    allowed = {neighbor.pose for neighbor in neighbor_placements(shape)}
    if any(pose not in allowed for pose in poses):
        return False
    occupied = set(seed)
    for placement in cells:
        if placement & occupied:
            return False
        occupied.update(placement)
    patch = frozenset(occupied)
    if surround_halo(seed) - patch or has_hole(patch):
        return False

    original = [seed, *cells]
    for left_pose in poses:
        for right_pose in poses:
            transformed = pose_cells(
                shape, compose_grid_poses(left_pose, right_pose)
            )
            for placement in original:
                if transformed != placement and transformed & placement:
                    return False
    return True


def find_isohedral_surround(shape, conflict_budget: int | None = None):
    """Return an exact grid-aligned isohedral verdict and finite witness.

    ``isohedral`` is true with a verified surround certificate, false after
    SAT-UNSAT, and ``None`` only if an optional conflict budget is exhausted.
    """

    from pysat.solvers import Cadical195

    shape = tuple(shape)
    neighbors = neighbor_placements(shape)
    clauses, stats = _base_and_extendability_clauses(shape, neighbors)
    if stats.get("uncovered_halo"):
        return {"isohedral": False, "exhausted": False, "certificate": None,
                "stats": stats}

    solver = Cadical195(bootstrap_with=clauses)
    hole_cuts = 0
    models = 0
    while True:
        if conflict_budget is not None:
            solver.conf_budget(conflict_budget)
            satisfiable = solver.solve_limited()
        else:
            satisfiable = solver.solve()
        if satisfiable is None:
            solver.delete()
            return {"isohedral": None, "exhausted": True,
                    "certificate": None,
                    "stats": {**stats, "models": models,
                              "hole_cuts": hole_cuts}}
        if not satisfiable:
            solver.delete()
            return {"isohedral": False, "exhausted": False,
                    "certificate": None,
                    "stats": {**stats, "models": models,
                              "hole_cuts": hole_cuts}}
        model = {literal for literal in solver.get_model() if literal > 0}
        selected = [
            variable for variable in range(1, len(neighbors) + 1)
            if variable in model
        ]
        models += 1
        certificate = {
            "kind": "isohedral-surround",
            "placements": [list(neighbors[v - 1].pose) for v in selected],
        }
        if verify_isohedral_surround(shape, certificate):
            solver.delete()
            return {"isohedral": True, "exhausted": False,
                    "certificate": certificate,
                    "stats": {**stats, "models": models,
                              "hole_cuts": hole_cuts}}
        # The CNF already enforces overlap and extendability, so a rejected
        # model can only violate the simply-connected-patch requirement.
        solver.add_clause([-variable for variable in selected])
        hole_cuts += 1
