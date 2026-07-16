"""Exact adapter from kite-grid patch certificates to the A6 module."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Sequence

from einstein.funnel.a6_hierarchy import (
    CompositionRule,
    CoverResult,
    Occurrence,
    canonical_cluster,
    deletion_variants,
    template_occurrences,
)
from einstein.substrate.kitegrid import boundary_cycle
from einstein.substrate.module12 import Pose, Vec4


def hex_to_module(point: tuple[int, int]) -> Vec4:
    """Embed the exact hex basis (0°, 60°) into the 12-fold module."""
    x, y = point
    return (x, 0, y, 0)


def kite_op_sr(op: int) -> tuple[int, int]:
    """Translate kite-grid D6 operation numbering to module (s, r)."""
    if not 0 <= op < 12:
        raise ValueError(f"kite operation out of range: {op}")
    if op < 6:
        return 0, 2 * op
    return 1, (6 + 2 * (op - 6)) % 12


def placement_poses(placements: Sequence[Sequence[int]]) -> tuple[Pose, ...]:
    """Convert A3 ``(op, tx, ty)`` placements to exact A6 poses."""
    return tuple(
        (*kite_op_sr(int(op)), hex_to_module((int(tx), int(ty))))
        for op, tx, ty in placements
    )


def polykite_boundary(shape) -> tuple[Vec4, ...]:
    """Exact simple boundary of one candidate tile in module coordinates."""
    return tuple(hex_to_module(point) for point in boundary_cycle(shape))


def frequent_hex_nearest_templates(
    poses: Sequence[Pose],
    min_size: int = 6,
    max_size: int = 12,
    top: int = 3,
) -> dict[int, list[tuple[tuple[Pose, ...], int]]]:
    """Exact nearest-anchor mining accelerated by the hex translation lattice.

    An expanding integer box is complete once the farthest retained neighbor
    has hex norm strictly below ``3(R+1)^2/4``, the lower bound for any point
    outside the box. No floating-point preselection enters the result.
    """
    if any(t[1] or t[3] for _, _, t in poses):
        raise ValueError("poses are not on the embedded hex translation lattice")
    by_xy: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, (_, _, t) in enumerate(poses):
        by_xy[(t[0], t[2])].append(i)
    counts = {size: Counter() for size in range(min_size, max_size + 1)}
    for root_i, root in enumerate(poses):
        x, y = root[2][0], root[2][2]
        radius = 4
        while True:
            nearby = [
                i
                for xx in range(x - radius, x + radius + 1)
                for yy in range(y - radius, y + radius + 1)
                for i in by_xy.get((xx, yy), ())
                if i != root_i
            ]
            nearby.sort(key=lambda i: (
                (poses[i][2][0] - x) ** 2
                + (poses[i][2][0] - x) * (poses[i][2][2] - y)
                + (poses[i][2][2] - y) ** 2,
                poses[i],
            ))
            if len(nearby) >= max_size - 1:
                dx = poses[nearby[max_size - 2]][2][0] - x
                dy = poses[nearby[max_size - 2]][2][2] - y
                farthest4 = 4 * (dx * dx + dx * dy + dy * dy)
                if farthest4 < 3 * (radius + 1) ** 2:
                    break
            radius *= 2
        for size in counts:
            cluster = [root, *(poses[i] for i in nearby[:size - 1])]
            counts[size][canonical_cluster(cluster)] += 1
    return {
        size: counts[size].most_common(top) for size in counts
    }


def cover_core_with_rule(
    poses: Sequence[Pose],
    core: Sequence[int],
    full: tuple[Pose, ...],
    missing: tuple[Pose, ...],
) -> CoverResult:
    """Exact-cover an interior core; halo tiles may be used but need not cover."""
    from pysat.solvers import Cadical195

    core_set = set(core)
    occurrences = tuple(sorted({
        group
        for template in (full, missing)
        for group in template_occurrences(template, poses)
        if group & core_set
    }, key=lambda group: tuple(sorted(group))))
    by_item: dict[int, list[int]] = defaultdict(list)
    for variable, group in enumerate(occurrences, 1):
        for item in group:
            by_item[item].append(variable)
    if any(not by_item[item] for item in core_set):
        return CoverResult((), 0, 0, 0)
    clauses: list[list[int]] = []
    for item, variables in by_item.items():
        if item in core_set:
            clauses.append(variables)
        for i, a in enumerate(variables):
            for b in variables[i + 1:]:
                clauses.append([-a, -b])
    solutions = []
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < 2 and solver.solve():
            model = {value for value in solver.get_model() if value > 0}
            chosen_variables = [
                variable for variable in range(1, len(occurrences) + 1)
                if variable in model
            ]
            chosen = tuple(
                occurrences[variable - 1] for variable in chosen_variables
            )
            solutions.append(chosen)
            solver.add_clause([-variable for variable in chosen_variables])
    if not solutions:
        return CoverResult((), 0, 0, 0)
    chosen = tuple(sorted(
        solutions[0], key=lambda group: tuple(sorted(group))
    ))
    return CoverResult(
        chosen,
        sum(len(group) == len(full) for group in chosen),
        sum(len(group) == len(missing) for group in chosen),
        len(solutions),
    )


def candidate_rules_from_histogram(
    histogram: Sequence[tuple[tuple[Pose, ...], int]],
) -> tuple[CompositionRule, ...]:
    """Expand frequent full scaffolds into all one-child exceptions."""
    return tuple(
        CompositionRule(full, missing, len(full), frequency)
        for full, frequency in histogram
        for missing in deletion_variants(full)
    )
