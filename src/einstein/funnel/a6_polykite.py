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
    _canonical_colored_cluster,
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


def forced_typed_core_options(
    poses: Sequence[Pose],
    core: Sequence[int],
    templates: Sequence[tuple[Pose, ...]],
    base_r2: int,
) -> dict[Pose, tuple[int, ...]]:
    """Allowed types at every parent anchor forced to exist in all covers."""
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
        return {}
    clauses: list[list[int]] = []
    for item, variables in by_item.items():
        if item in core_set:
            clauses.append(variables)
        for i, a in enumerate(variables):
            for b in variables[i + 1:]:
                clauses.append([-a, -b])
    options = {}
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return {}
        for base, variables in by_base.items():
            x, y = base[2][0], base[2][2]
            if x * x + x * y + y * y > base_r2:
                continue
            if solver.solve(assumptions=[
                -variable for variable in variables
            ]):
                continue
            allowed = tuple(sorted({
                candidates[variable - 1][0]
                for variable in variables
                if solver.solve(assumptions=[variable])
            }))
            if allowed:
                options[base] = allowed
    return options


def _hex_nearest_groups(
    poses: Sequence[Pose],
    sizes: Sequence[int],
) -> set[Occurrence]:
    """One exact nearest-anchor group of each requested size per root."""
    if any(t[1] or t[3] for _, _, t in poses):
        raise ValueError("poses are not on the embedded hex translation lattice")
    largest = max(sizes)
    by_xy: dict[tuple[int, int], list[int]] = defaultdict(list)
    for i, (_, _, t) in enumerate(poses):
        by_xy[(t[0], t[2])].append(i)
    groups = set()
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
            if len(nearby) >= largest - 1:
                dx = poses[nearby[largest - 2]][2][0] - x
                dy = poses[nearby[largest - 2]][2][2] - y
                if 4 * (dx * dx + dx * dy + dy * dy) < (
                    3 * (radius + 1) ** 2
                ):
                    break
            radius *= 2
        for size in sizes:
            groups.add(frozenset((root_i, *nearby[:size - 1])))
    return groups


def mine_option_state_recursive_library(
    options: dict[Pose, tuple[int, ...]],
    training_r2: int,
    forcing_r2: int,
    group_sizes: Sequence[int] = (7, 8),
) -> dict:
    """Mine a minimum typed next-level library from cover-invariant states."""
    from pysat.card import CardEnc, EncType
    from pysat.examples.rc2 import RC2
    from pysat.formula import IDPool, WCNF
    from pysat.solvers import Cadical195

    poses = tuple(sorted(options))
    option_states = {
        option: state
        for state, option in enumerate(sorted(set(options.values())))
    }
    states = tuple(option_states[options[pose]] for pose in poses)
    training = {
        i for i, pose in enumerate(poses)
        if (
            pose[2][0] ** 2
            + pose[2][0] * pose[2][2]
            + pose[2][2] ** 2
        ) <= training_r2
    }
    forcing = {
        i for i, pose in enumerate(poses)
        if (
            pose[2][0] ** 2
            + pose[2][0] * pose[2][2]
            + pose[2][2] ** 2
        ) <= forcing_r2
    }
    groups = [
        group for group in _hex_nearest_groups(poses, group_sizes)
        if group & training
    ]
    typed = [
        (
            _canonical_colored_cluster(
                [poses[i] for i in group],
                [states[i] for i in group],
            ),
            group,
        )
        for group in groups
    ]
    pattern_ids = {
        pattern: i for i, pattern in enumerate(sorted({
            pattern for pattern, _ in typed
        }))
    }
    items = [(pattern_ids[pattern], group) for pattern, group in typed]
    by_item: dict[int, list[int]] = defaultdict(list)
    for variable, (_, group) in enumerate(items, 1):
        for item in group:
            by_item[item].append(variable)

    formula = WCNF()
    pool = IDPool(start_from=len(items) + 1)
    for item, variables in by_item.items():
        if item in training:
            formula.append(variables)
        formula.extend(CardEnc.atmost(
            variables, 1, vpool=pool, encoding=EncType.seqcounter
        ).clauses)
    for pattern_id in range(len(pattern_ids)):
        formula.append([-pool.id(("pattern", pattern_id))], weight=1)
    for variable, (pattern_id, _) in enumerate(items, 1):
        formula.append([
            -variable, pool.id(("pattern", pattern_id))
        ])
    with RC2(formula) as optimizer:
        model = optimizer.compute()
        minimum_patterns = optimizer.cost if model is not None else None
    if model is None:
        return {
            "satisfiable": False,
            "option_states": len(option_states),
            "training_nodes": len(training),
        }
    positive = {value for value in model if value > 0}
    selected_pattern_ids = {
        pattern_id for pattern_id in range(len(pattern_ids))
        if pool.id(("pattern", pattern_id)) in positive
    }
    selected_state = {
        pattern_id: state
        for state, pattern_id in enumerate(sorted(selected_pattern_ids))
    }
    allowed = [
        (pattern_id, group)
        for pattern_id, group in items
        if pattern_id in selected_pattern_ids
    ]
    allowed_by_item: dict[int, list[int]] = defaultdict(list)
    for variable, (_, group) in enumerate(allowed, 1):
        for item in group:
            allowed_by_item[item].append(variable)
    clauses: list[list[int]] = []
    pool2 = IDPool(start_from=len(allowed) + 1)
    for item, variables in allowed_by_item.items():
        if item in training:
            clauses.append(variables)
        clauses.extend(CardEnc.atmost(
            variables, 1, vpool=pool2, encoding=EncType.seqcounter
        ).clauses)
    forced = optional = impossible = 0
    forced_groups = []
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            raise ValueError("optimized pattern library lost its own cover")
        for variable, (_, group) in enumerate(allowed, 1):
            if not group & forcing:
                continue
            if not solver.solve(assumptions=[variable]):
                impossible += 1
            elif solver.solve(assumptions=[-variable]):
                optional += 1
            else:
                forced += 1
                pattern_id, group = allowed[variable - 1]
                template = canonical_cluster([poses[i] for i in group])
                base = occurrence_base(group, template, poses)
                forced_groups.append({
                    "pattern": selected_state[pattern_id],
                    "base": [base[0], base[1], list(base[2])],
                    "members": sorted(group),
                })
    inverse_patterns = {
        pattern_id: pattern for pattern, pattern_id in pattern_ids.items()
    }
    selected_patterns = [
        [
            {
                "pose": [s, r, list(t)],
                "state": state,
            }
            for (s, r, t), state in inverse_patterns[pattern_id]
        ]
        for pattern_id in sorted(selected_pattern_ids)
    ]
    return {
        "satisfiable": True,
        "option_states": len(option_states),
        "option_state_values": [
            list(option) for option in sorted(option_states)
        ],
        "available_parent_anchors": len(poses),
        "training_r2": training_r2,
        "training_nodes": len(training),
        "forcing_r2": forcing_r2,
        "forcing_nodes": len(forcing),
        "candidate_groups": len(groups),
        "observed_typed_patterns": len(pattern_ids),
        "minimum_patterns": minimum_patterns,
        "selected_pattern_arities": dict(Counter(
            len(inverse_patterns[pattern_id])
            for pattern_id in selected_pattern_ids
        )),
        "selected_patterns": selected_patterns,
        "allowed_group_occurrences": len(allowed),
        "forced_inner_groups": forced,
        "optional_inner_groups": optional,
        "impossible_inner_groups": impossible,
        "inner_grouping_forced": forced > 0 and optional == 0,
        "forced_groups": sorted(
            forced_groups, key=lambda group: (
                group["base"], group["pattern"], group["members"]
            )
        ),
    }


def mine_joint_option_state_recursive_library(
    option_samples: Sequence[
        tuple[str, dict[Pose, tuple[int, ...]]]
    ],
    training_r2: int,
    forcing_r2: int,
    group_sizes: Sequence[int] = (7, 8),
) -> dict:
    """Mine one minimum typed library satisfying several independent patches.

    Pattern-presence variables are shared across samples, while every sample
    receives its own exact-cover constraints.  This prevents a minimum library
    from silently specializing to one finite patch.
    """
    from pysat.card import CardEnc, EncType
    from pysat.examples.rc2 import RC2
    from pysat.formula import IDPool, WCNF

    all_option_values = sorted({
        option
        for _, options in option_samples
        for option in options.values()
    })
    option_states = {
        option: state for state, option in enumerate(all_option_values)
    }
    prepared = []
    all_patterns = set()
    for label, options in option_samples:
        poses = tuple(sorted(options))
        states = tuple(option_states[options[pose]] for pose in poses)
        training = {
            i for i, pose in enumerate(poses)
            if (
                pose[2][0] ** 2
                + pose[2][0] * pose[2][2]
                + pose[2][2] ** 2
            ) <= training_r2
        }
        typed = [
            (
                _canonical_colored_cluster(
                    [poses[i] for i in group],
                    [states[i] for i in group],
                ),
                group,
            )
            for group in _hex_nearest_groups(poses, group_sizes)
            if group & training
        ]
        all_patterns.update(pattern for pattern, _ in typed)
        prepared.append((label, options, poses, training, typed))

    patterns = sorted(all_patterns)
    pattern_ids = {
        pattern: pattern_id
        for pattern_id, pattern in enumerate(patterns)
    }
    items = [
        (sample, pattern_ids[pattern], group)
        for sample, (_, _, _, _, typed) in enumerate(prepared)
        for pattern, group in typed
    ]
    formula = WCNF()
    pool = IDPool(start_from=len(items) + 1)
    by_item: dict[tuple[int, int], list[int]] = defaultdict(list)
    for variable, (sample, pattern_id, group) in enumerate(items, 1):
        for item in group:
            by_item[(sample, item)].append(variable)
        formula.append([
            -variable, pool.id(("pattern", pattern_id))
        ])
    for (sample, item), variables in by_item.items():
        if item in prepared[sample][3]:
            formula.append(variables)
        formula.extend(CardEnc.atmost(
            variables, 1, vpool=pool, encoding=EncType.seqcounter
        ).clauses)
    for pattern_id in range(len(patterns)):
        formula.append(
            [-pool.id(("pattern", pattern_id))],
            weight=1,
        )
    with RC2(formula) as optimizer:
        model = optimizer.compute()
        minimum_patterns = optimizer.cost if model is not None else None
    if model is None:
        return {
            "satisfiable": False,
            "samples": len(option_samples),
            "option_states": len(option_states),
        }
    positive = {value for value in model if value > 0}
    selected_pattern_ids = [
        pattern_id for pattern_id in range(len(patterns))
        if pool.id(("pattern", pattern_id)) in positive
    ]
    selected_patterns = [
        [
            {
                "pose": [s, r, list(t)],
                "state": state,
            }
            for (s, r, t), state in patterns[pattern_id]
        ]
        for pattern_id in selected_pattern_ids
    ]
    sample_results = []
    for label, options, _, _, _ in prepared:
        result = verify_option_state_recursive_library(
            options,
            selected_patterns,
            training_r2=training_r2,
            forcing_r2=forcing_r2,
            group_sizes=group_sizes,
            option_state_values=all_option_values,
        )
        result["label"] = label
        sample_results.append(result)
    return {
        "satisfiable": all(
            sample["satisfiable"] for sample in sample_results
        ),
        "samples": len(option_samples),
        "option_states": len(option_states),
        "option_state_values": [
            list(option) for option in all_option_values
        ],
        "training_r2": training_r2,
        "forcing_r2": forcing_r2,
        "observed_typed_patterns": len(patterns),
        "minimum_patterns": minimum_patterns,
        "selected_pattern_arities": dict(Counter(
            len(patterns[pattern_id])
            for pattern_id in selected_pattern_ids
        )),
        "selected_patterns": selected_patterns,
        "sample_results": sample_results,
        "all_samples_forced": all(
            sample.get("inner_grouping_forced", False)
            for sample in sample_results
        ),
    }


def verify_option_state_recursive_library(
    options: dict[Pose, tuple[int, ...]],
    selected_patterns: Sequence[Sequence[dict]],
    training_r2: int,
    forcing_r2: int,
    group_sizes: Sequence[int] = (7, 8),
    option_state_values: Sequence[tuple[int, ...]] | None = None,
) -> dict:
    """Apply a frozen typed library and SAT-check cover/forcing on a patch."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool
    from pysat.solvers import Cadical195

    poses = tuple(sorted(options))
    values = (
        sorted(set(options.values()))
        if option_state_values is None
        else option_state_values
    )
    option_states = {
        option: state for state, option in enumerate(values)
    }
    states = tuple(option_states[options[pose]] for pose in poses)
    frozen = {
        tuple(
            (
                (
                    int(item["pose"][0]),
                    int(item["pose"][1]),
                    tuple(int(x) for x in item["pose"][2]),
                ),
                int(item["state"]),
            )
            for item in pattern
        ): pattern_state
        for pattern_state, pattern in enumerate(selected_patterns)
    }
    training = {
        i for i, pose in enumerate(poses)
        if (
            pose[2][0] ** 2
            + pose[2][0] * pose[2][2]
            + pose[2][2] ** 2
        ) <= training_r2
    }
    forcing = {
        i for i, pose in enumerate(poses)
        if (
            pose[2][0] ** 2
            + pose[2][0] * pose[2][2]
            + pose[2][2] ** 2
        ) <= forcing_r2
    }
    allowed = []
    for group in _hex_nearest_groups(poses, group_sizes):
        if not group & training:
            continue
        pattern = _canonical_colored_cluster(
            [poses[i] for i in group],
            [states[i] for i in group],
        )
        if pattern in frozen:
            allowed.append((frozen[pattern], group))
    by_item: dict[int, list[int]] = defaultdict(list)
    for variable, (_, group) in enumerate(allowed, 1):
        for item in group:
            by_item[item].append(variable)
    if any(not by_item[item] for item in training):
        return {
            "satisfiable": False,
            "training_nodes": len(training),
            "uncovered_training_nodes": sum(
                not by_item[item] for item in training
            ),
            "allowed_group_occurrences": len(allowed),
        }
    clauses: list[list[int]] = []
    pool = IDPool(start_from=len(allowed) + 1)
    for item, variables in by_item.items():
        if item in training:
            clauses.append(variables)
        clauses.extend(CardEnc.atmost(
            variables, 1, vpool=pool, encoding=EncType.seqcounter
        ).clauses)
    forced = optional = impossible = 0
    forced_groups = []
    with Cadical195(bootstrap_with=clauses) as solver:
        if not solver.solve():
            return {
                "satisfiable": False,
                "training_nodes": len(training),
                "uncovered_training_nodes": 0,
                "allowed_group_occurrences": len(allowed),
            }
        for variable, (pattern_state, group) in enumerate(allowed, 1):
            if not group & forcing:
                continue
            if not solver.solve(assumptions=[variable]):
                impossible += 1
            elif solver.solve(assumptions=[-variable]):
                optional += 1
            else:
                forced += 1
                template = canonical_cluster([poses[i] for i in group])
                base = occurrence_base(group, template, poses)
                forced_groups.append({
                    "pattern": pattern_state,
                    "base": [base[0], base[1], list(base[2])],
                    "members": sorted(group),
                })
    return {
        "satisfiable": True,
        "training_nodes": len(training),
        "forcing_nodes": len(forcing),
        "allowed_group_occurrences": len(allowed),
        "forced_inner_groups": forced,
        "optional_inner_groups": optional,
        "impossible_inner_groups": impossible,
        "inner_grouping_forced": forced > 0 and optional == 0,
        "forced_groups": sorted(
            forced_groups, key=lambda group: (
                group["base"], group["pattern"], group["members"]
            )
        ),
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
