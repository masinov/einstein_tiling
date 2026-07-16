"""Exact adapter from kite-grid patch certificates to the A6 module."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Sequence

from einstein.funnel.a6_hierarchy import (
    CompositionRule,
    CoverResult,
    HierarchyLevel,
    Occurrence,
    canonical_cluster,
    deletion_variants,
    occurrence_base,
    template_occurrences,
)
from einstein.substrate.kitegrid import boundary_cycle
from einstein.substrate.module12 import Pose, Vec4


@dataclass(frozen=True)
class TypedCoreCover:
    """One core composition with the selected template type per parent."""

    groups: tuple[tuple[int, Occurrence], ...]


@dataclass(frozen=True)
class TypedContraction:
    """Contracted parent patch plus its finite parent-type alphabet."""

    level: HierarchyLevel
    types: tuple[int, ...]


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
    """Return the first core cover and multiplicity capped at two."""
    solutions = enumerate_core_covers(
        poses, core, full, missing, limit=2
    )
    if not solutions:
        return CoverResult((), 0, 0, 0)
    first = solutions[0]
    return CoverResult(
        first.groups,
        first.n_full,
        first.n_missing,
        len(solutions),
    )


def enumerate_core_covers(
    poses: Sequence[Pose],
    core: Sequence[int],
    full: tuple[Pose, ...],
    missing: tuple[Pose, ...],
    limit: int = 2,
) -> tuple[CoverResult, ...]:
    """Enumerate exact core covers, using surrounding tiles as optional halo."""
    from pysat.solvers import Cadical195

    if limit < 1:
        return ()
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
        return ()
    clauses: list[list[int]] = []
    for item, variables in by_item.items():
        if item in core_set:
            clauses.append(variables)
        for i, a in enumerate(variables):
            for b in variables[i + 1:]:
                clauses.append([-a, -b])
    solutions = []
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < limit and solver.solve():
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
    return tuple(
        CoverResult(
            tuple(sorted(chosen, key=lambda group: tuple(sorted(group)))),
            sum(len(group) == len(full) for group in chosen),
            sum(len(group) == len(missing) for group in chosen),
            1,
        )
        for chosen in solutions
    )


def enumerate_typed_core_covers(
    poses: Sequence[Pose],
    core: Sequence[int],
    templates: Sequence[tuple[Pose, ...]],
    limit: int = 2,
) -> tuple[TypedCoreCover, ...]:
    """Enumerate core covers from an arbitrary finite template library."""
    from pysat.solvers import Cadical195

    if limit < 1:
        return ()
    core_set = set(core)
    candidates = tuple(sorted({
        (template_type, group)
        for template_type, template in enumerate(templates)
        for group in template_occurrences(template, poses)
        if group & core_set
    }, key=lambda item: (item[0], tuple(sorted(item[1])))))
    by_item: dict[int, list[int]] = defaultdict(list)
    for variable, (_, group) in enumerate(candidates, 1):
        for item in group:
            by_item[item].append(variable)
    if any(not by_item[item] for item in core_set):
        return ()
    clauses: list[list[int]] = []
    for item, variables in by_item.items():
        if item in core_set:
            clauses.append(variables)
        for i, a in enumerate(variables):
            for b in variables[i + 1:]:
                clauses.append([-a, -b])
    solutions = []
    with Cadical195(bootstrap_with=clauses) as solver:
        while len(solutions) < limit and solver.solve():
            model = {value for value in solver.get_model() if value > 0}
            selected = tuple(
                candidates[variable - 1]
                for variable in range(1, len(candidates) + 1)
                if variable in model
            )
            solutions.append(TypedCoreCover(selected))
            solver.add_clause([
                -variable
                for variable in range(1, len(candidates) + 1)
                if variable in model
            ])
    return tuple(solutions)


def contract_typed_core_cover(
    level: HierarchyLevel,
    templates: Sequence[tuple[Pose, ...]],
    cover: TypedCoreCover,
) -> TypedContraction:
    """Contract a typed partial cover, preserving physical-leaf provenance."""
    records = []
    for template_type, group in cover.groups:
        base = occurrence_base(group, templates[template_type], level.poses)
        leaves = frozenset().union(*(level.leaves[i] for i in group))
        records.append((base, template_type, leaves))
    records.sort(key=lambda record: record[0])
    return TypedContraction(
        HierarchyLevel(
            tuple(record[0] for record in records),
            tuple(record[1] != 0 for record in records),
            tuple(record[2] for record in records),
        ),
        tuple(record[1] for record in records),
    )


def typed_core_backbone(
    poses: Sequence[Pose],
    core: Sequence[int],
    templates: Sequence[tuple[Pose, ...]],
    base_r2: int,
) -> dict:
    """Classify which interior parent anchors/types are forced by all covers."""
    from pysat.solvers import Cadical195

    core_set = set(core)
    candidates = tuple(sorted({
        (template_type, group, occurrence_base(group, template, poses))
        for template_type, template in enumerate(templates)
        for group in template_occurrences(template, poses)
        if group & core_set
    }, key=lambda item: (
        item[2], item[0], tuple(sorted(item[1]))
    )))
    by_item: dict[int, list[int]] = defaultdict(list)
    by_base: dict[Pose, list[int]] = defaultdict(list)
    for variable, (_, group, base) in enumerate(candidates, 1):
        for item in group:
            by_item[item].append(variable)
        by_base[base].append(variable)
    if any(not by_item[item] for item in core_set):
        return {
            "satisfiable": False,
            "candidate_occurrences": len(candidates),
            "candidate_bases": len(by_base),
        }
    clauses: list[list[int]] = []
    for item, variables in by_item.items():
        if item in core_set:
            clauses.append(variables)
        for i, a in enumerate(variables):
            for b in variables[i + 1:]:
                clauses.append([-a, -b])
    profiles: Counter[tuple[int, ...]] = Counter()
    forced = optional = impossible = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return {
                "satisfiable": False,
                "candidate_occurrences": len(candidates),
                "candidate_bases": len(by_base),
            }
        for base, variables in by_base.items():
            x, y = base[2][0], base[2][2]
            if x * x + x * y + y * y > base_r2:
                continue
            is_forced = not solver.solve(
                assumptions=[-variable for variable in variables]
            )
            allowed = tuple(sorted({
                candidates[variable - 1][0]
                for variable in variables
                if solver.solve(assumptions=[variable])
            }))
            profiles[allowed] += 1
            if not allowed:
                impossible += 1
            elif is_forced:
                forced += 1
            else:
                optional += 1
    return {
        "satisfiable": True,
        "candidate_occurrences": len(candidates),
        "candidate_bases": len(by_base),
        "analyzed_bases": forced + optional + impossible,
        "forced_bases": forced,
        "optional_bases": optional,
        "impossible_bases": impossible,
        "all_analyzed_bases_forced": optional == 0,
        "allowed_type_profiles": {
            ",".join(map(str, profile)): count
            for profile, count in sorted(profiles.items())
        },
    }


def candidate_rules_from_histogram(
    histogram: Sequence[tuple[tuple[Pose, ...], int]],
) -> tuple[CompositionRule, ...]:
    """Expand frequent full scaffolds into all one-child exceptions."""
    return tuple(
        CompositionRule(full, missing, len(full), frequency)
        for full, frequency in histogram
        for missing in deletion_variants(full)
    )
