"""Blind exact hierarchy mining on rank-4 module tile anchors (A6 v0).

The discovery channel sees only unoracular tile poses.  It proposes repeated
local clusters by exact nearest-anchor distance, canonicalizes them under the
module-preserving dihedral group, and accepts a composition only when exact
template matching gives a unique, disjoint cover of the complete patch.

Known substitution ancestry is deliberately handled by separate validation
functions and is never an input to discovery.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import cmp_to_key
from pathlib import Path
from typing import Iterable, Sequence

from einstein.substrate.module12 import (
    Pose,
    Vec4,
    apply_sr,
    compare_quadratic,
    compose_pose,
    madd,
    norm2_pair,
    relative_pose,
)

Template = tuple[Pose, ...]
Occurrence = frozenset[int]

# Exact Tile(1,1) boundary in the rank-4 module, from the supplied generator.
SPECTRE_TILE_BOUNDARY: tuple[Vec4, ...] = (
    (0, 0, 0, 0),
    (1, 0, 0, 0),
    (2, 0, -1, 0),
    (2, 1, -1, 0),
    (2, 1, -1, 1),
    (3, 1, -1, 1),
    (3, 1, 0, 1),
    (3, 0, 0, 2),
    (3, -1, 0, 2),
    (2, -1, 1, 2),
    (1, -1, 1, 2),
    (0, -1, 1, 2),
    (0, -1, 0, 2),
    (0, 0, 0, 1),
)


@dataclass(frozen=True)
class CompositionRule:
    full: Template
    missing: Template
    full_size: int
    proposal_frequency: int


@dataclass(frozen=True)
class CoverResult:
    groups: tuple[Occurrence, ...]
    n_full: int
    n_missing: int
    n_solutions: int


def read_anchor_poses(path: str | Path) -> list[Pose]:
    """Read the ordinary Spectre anchor format, intentionally ignoring kind."""
    with open(path, newline="") as f:
        rows = csv.DictReader(f)
        return [
            (
                int(row["s"]),
                int(row["r"]),
                (
                    int(row["t0"]),
                    int(row["t1"]),
                    int(row["t2"]),
                    int(row["t3"]),
                ),
            )
            for row in rows
        ]


def canonical_cluster(poses: Sequence[Pose]) -> Template:
    """Canonical exact relative-pose description of an unlabelled cluster."""
    if not poses:
        return ()
    candidates = []
    for root in poses:
        candidates.append(tuple(sorted(relative_pose(root, pose) for pose in poses)))
    return min(candidates)


def _distance_cmp(origin: Vec4, a: Pose, b: Pose) -> int:
    da = norm2_pair((
        a[2][0] - origin[0],
        a[2][1] - origin[1],
        a[2][2] - origin[2],
        a[2][3] - origin[3],
    ))
    db = norm2_pair((
        b[2][0] - origin[0],
        b[2][1] - origin[1],
        b[2][2] - origin[2],
        b[2][3] - origin[3],
    ))
    c = compare_quadratic(da, db)
    return c if c else ((a > b) - (a < b))


def frequent_nearest_templates(
    poses: Sequence[Pose], size: int, top: int = 3
) -> list[tuple[Template, int]]:
    """Return frequent exact canonical clusters among each anchor's neighbors."""
    if size < 2 or size > len(poses):
        return []
    counts: Counter[Template] = Counter()
    for i, root in enumerate(poses):
        others = [pose for j, pose in enumerate(poses) if j != i]
        others.sort(key=cmp_to_key(lambda a, b: _distance_cmp(root[2], a, b)))
        counts[canonical_cluster([root, *others[: size - 1]])] += 1
    return counts.most_common(top)


def _frequent_templates_by_size(
    poses: Sequence[Pose], min_size: int, max_size: int
) -> dict[int, Counter[Template]]:
    """Compute several neighborhood-size histograms with one exact sort/root."""
    counts = {size: Counter() for size in range(min_size, max_size + 1)}
    for i, root in enumerate(poses):
        others = [pose for j, pose in enumerate(poses) if j != i]
        others.sort(key=cmp_to_key(lambda a, b: _distance_cmp(root[2], a, b)))
        for size in counts:
            counts[size][canonical_cluster([root, *others[: size - 1]])] += 1
    return counts


def deletion_variants(template: Template) -> tuple[Template, ...]:
    """All distinct canonical one-element deletions of a template."""
    return tuple(sorted({
        canonical_cluster(template[:i] + template[i + 1 :])
        for i in range(len(template))
    }))


def cluster_adjacency(
    template: Template, tile_boundary: Sequence[Vec4]
) -> tuple[tuple[int, ...], int, int]:
    """Return degrees, internal-edge count and exposed-edge count exactly."""
    edge_tiles: dict[tuple[Vec4, Vec4], list[int]] = defaultdict(list)
    for i, (s, r, t) in enumerate(template):
        vertices = [madd(t, apply_sr(s, r, v)) for v in tile_boundary]
        for j, a in enumerate(vertices):
            b = vertices[(j + 1) % len(vertices)]
            edge_tiles[tuple(sorted((a, b)))].append(i)
    adjacent = [set() for _ in template]
    internal = exposed = 0
    for tiles in edge_tiles.values():
        if len(tiles) == 1:
            exposed += 1
        elif len(tiles) == 2:
            a, b = tiles
            adjacent[a].add(b)
            adjacent[b].add(a)
            internal += 1
        else:
            raise ValueError("non-edge-to-edge cluster: more than two tiles share edge")
    return tuple(sorted(map(len, adjacent))), internal, exposed


def template_occurrences(
    template: Template, poses: Sequence[Pose]
) -> tuple[Occurrence, ...]:
    """Find all exact occurrences of ``template`` in a pose set."""
    index = {pose: i for i, pose in enumerate(poses)}
    if len(index) != len(poses):
        raise ValueError("duplicate tile poses make occurrences ambiguous")
    found: set[Occurrence] = set()
    for base in poses:
        ids = []
        for rel in template:
            target = compose_pose(base, rel)
            j = index.get(target)
            if j is None:
                break
            ids.append(j)
        else:
            found.add(frozenset(ids))
    return tuple(sorted(found, key=lambda group: tuple(sorted(group))))


def _exact_cover_solutions(
    n_items: int, candidates: Iterable[Occurrence], limit: int = 2
) -> list[tuple[Occurrence, ...]]:
    unique = tuple(sorted(
        {group for group in candidates if group},
        key=lambda group: (-len(group), tuple(sorted(group))),
    ))
    by_item: list[list[Occurrence]] = [[] for _ in range(n_items)]
    for group in unique:
        for item in group:
            by_item[item].append(group)
    if any(not choices for choices in by_item):
        return []

    solutions: list[tuple[Occurrence, ...]] = []

    def search(covered: set[int], chosen: list[Occurrence]) -> None:
        if len(solutions) >= limit:
            return
        if len(covered) == n_items:
            solutions.append(tuple(chosen))
            return
        remaining = [i for i in range(n_items) if i not in covered]
        item = min(
            remaining,
            key=lambda i: sum(group.isdisjoint(covered) for group in by_item[i]),
        )
        for group in by_item[item]:
            if group.isdisjoint(covered):
                search(covered | set(group), [*chosen, group])

    search(set(), [])
    return solutions


def cover_with_rule(
    poses: Sequence[Pose], full: Template, missing: Template
) -> CoverResult:
    """Apply a proposed two-scaffold rule and require an exact patch cover."""
    full_occ = template_occurrences(full, poses)
    missing_occ = template_occurrences(missing, poses)
    solutions = _exact_cover_solutions(
        len(poses), (*full_occ, *missing_occ), limit=2
    )
    if not solutions:
        return CoverResult((), 0, 0, 0)
    chosen = solutions[0]
    n_full = sum(len(group) == len(full) for group in chosen)
    n_missing = sum(len(group) == len(missing) for group in chosen)
    return CoverResult(
        tuple(sorted(chosen, key=lambda group: tuple(sorted(group)))),
        n_full,
        n_missing,
        len(solutions),
    )


def discover_composition(
    poses: Sequence[Pose],
    confirmation_poses: Sequence[Pose] | None = None,
    tile_boundary: Sequence[Vec4] | None = None,
    min_size: int = 6,
    max_size: int = 12,
    top: int = 3,
) -> tuple[CompositionRule, CoverResult, dict]:
    """Blindly rank full-plus-one-deletion exact composition hypotheses."""
    diagnostics = {"sizes": {}}
    accepted: dict[tuple[Template, Template], tuple[CompositionRule, CoverResult]] = {}
    final_size = min(max_size, len(poses))
    histograms = _frequent_templates_by_size(poses, min_size, final_size)
    for size in range(min_size, final_size + 1):
        proposals = histograms[size].most_common(top)
        diagnostics["sizes"][str(size)] = {
            "top_frequency": proposals[0][1] if proposals else 0,
            "accepted": 0,
        }
        for full, frequency in proposals:
            for missing in deletion_variants(full):
                cover = cover_with_rule(poses, full, missing)
                if cover.n_solutions == 1:
                    rule = CompositionRule(full, missing, size, frequency)
                    accepted[(full, missing)] = (rule, cover)
        diagnostics["sizes"][str(size)]["accepted"] = sum(
            rule.full_size == size for rule, _ in accepted.values()
        )
    if not accepted:
        raise ValueError("no unique exact composition found")
    diagnostics["training_candidates"] = len(accepted)
    if confirmation_poses is not None:
        confirmed = {}
        for key, (rule, cover) in accepted.items():
            check = cover_with_rule(confirmation_poses, rule.full, rule.missing)
            if check.n_solutions == 1:
                confirmed[key] = (rule, cover)
        diagnostics["confirmation_candidates"] = len(confirmed)
        accepted = confirmed
        if not accepted:
            raise ValueError("no training rule exactly composes confirmation patch")

    def score(rule: CompositionRule) -> tuple[int, ...]:
        base = (rule.proposal_frequency, rule.full_size)
        if tile_boundary is None:
            return base
        # A one-child exception should disturb the frequent scaffold as little
        # as possible: maximize exact shared-edge cohesion, then minimize its
        # exposed boundary. This is an adjacency-graph criterion, not ancestry.
        _, internal, exposed = cluster_adjacency(rule.missing, tile_boundary)
        return (*base, internal, -exposed)

    if tile_boundary is not None:
        diagnostics["candidate_scores"] = sorted(
            [
                {
                    "full_size": rule.full_size,
                    "proposal_frequency": rule.proposal_frequency,
                    "missing_internal_edges": cluster_adjacency(
                        rule.missing, tile_boundary
                    )[1],
                    "missing_exposed_edges": cluster_adjacency(
                        rule.missing, tile_boundary
                    )[2],
                }
                for rule, _ in accepted.values()
            ],
            key=lambda item: (
                -item["proposal_frequency"],
                -item["full_size"],
                -item["missing_internal_edges"],
                item["missing_exposed_edges"],
            ),
        )
    best_score = max(score(rule) for rule, _ in accepted.values())
    best = [
        pair for pair in accepted.values()
        if score(pair[0]) == best_score
    ]
    distinct_covers = {pair[1].groups for pair in best}
    if len(distinct_covers) != 1:
        raise ValueError(f"ambiguous exact compositions at score {best_score}")
    rule, cover = best[0]
    diagnostics["selected"] = {
        "full_size": rule.full_size,
        "proposal_frequency": rule.proposal_frequency,
        "n_full": cover.n_full,
        "n_missing": cover.n_missing,
    }
    if tile_boundary is not None:
        degrees, internal, exposed = cluster_adjacency(rule.missing, tile_boundary)
        diagnostics["selected"]["missing_adjacency"] = {
            "degrees": list(degrees),
            "internal_edges": internal,
            "exposed_edges": exposed,
        }
    return rule, cover, diagnostics


def read_hidden_parent_groups(
    path: str | Path, poses: Sequence[Pose]
) -> tuple[Occurrence, ...]:
    """Read validation-only ancestry and group leaves by immediate parent."""
    pose_index = {pose: i for i, pose in enumerate(poses)}
    grouped: dict[tuple[int, ...], set[int]] = defaultdict(set)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            pose = (
                int(row["s"]),
                int(row["r"]),
                (
                    int(row["t0"]),
                    int(row["t1"]),
                    int(row["t2"]),
                    int(row["t3"]),
                ),
            )
            i = pose_index[pose]
            raw = row["path"]
            if raw.endswith(("a", "b")):
                raw = raw[:-1]
            slots = tuple(int(part) for part in raw.split(".") if part)
            grouped[slots[:-1]].add(i)
    return tuple(sorted(
        (frozenset(group) for group in grouped.values()),
        key=lambda group: tuple(sorted(group)),
    ))


def validate_against_hidden(
    predicted: Sequence[Occurrence], hidden: Sequence[Occurrence]
) -> dict:
    """Score a blind partition after discovery against withheld ancestry."""
    p, h = set(predicted), set(hidden)
    matched = len(p & h)
    return {
        "predicted": len(p),
        "hidden": len(h),
        "matched": matched,
        "precision": matched / len(p) if p else 0.0,
        "recall": matched / len(h) if h else 0.0,
        "exact": p == h,
    }


def recover_order2_recurrence(values: Sequence[int]) -> dict:
    """Recover ``T[n+1] = a*T[n] + b*T[n-1]`` from four exact counts."""
    if len(values) < 4:
        raise ValueError("four counts are required")
    t0, t1, t2, t3 = values[:4]
    det = t1 * t1 - t0 * t2
    if det == 0:
        raise ValueError("singular recurrence system")
    anum = t2 * t1 - t0 * t3
    bnum = t1 * t3 - t2 * t2
    if anum % det or bnum % det:
        raise ValueError("counts do not have an integer order-2 recurrence")
    a, b = anum // det, bnum // det
    if any(values[i + 1] != a * values[i] + b * values[i - 1]
           for i in range(1, len(values) - 1)):
        raise ValueError("recurrence does not verify on all supplied counts")
    return {
        "a": a,
        "b": b,
        "characteristic": [1, -a, -b],
    }
