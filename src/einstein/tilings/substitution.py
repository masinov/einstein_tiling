"""Infer finite substitution hierarchies from exact module-valued anchors.

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

from einstein.geometry.cyclotomic import (
    Pose,
    Vec4,
    apply_sr,
    compare_quadratic,
    compose_pose,
    inverse_pose,
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


@dataclass(frozen=True)
class HierarchyLevel:
    """A contracted patch with exact anchors and physical-leaf provenance."""

    poses: tuple[Pose, ...]
    exceptional: tuple[bool, ...]
    leaves: tuple[Occurrence, ...]


@dataclass(frozen=True)
class RecursiveHierarchy:
    """Scale-specific rules and contractions recovered from two patch sizes."""

    levels: tuple[HierarchyLevel, ...]
    rules: tuple[CompositionRule, ...]
    covers: tuple[CoverResult, ...]
    refinement_rounds: tuple[int, ...]


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

    # Split the candidate hypergraph into independent overlap components.
    # Large substitution patches contain thousands of tiny components; solving
    # them separately avoids recursion depth proportional to the whole patch.
    components: list[tuple[set[int], set[Occurrence]]] = []
    unseen = set(range(n_items))
    while unseen:
        seed = unseen.pop()
        items = {seed}
        groups: set[Occurrence] = set()
        frontier = [seed]
        while frontier:
            item = frontier.pop()
            for group in by_item[item]:
                if group in groups:
                    continue
                groups.add(group)
                for other in group:
                    if other not in items:
                        items.add(other)
                        unseen.discard(other)
                        frontier.append(other)
        components.append((items, groups))

    def solve_component(
        items: set[int], groups: set[Occurrence]
    ) -> list[tuple[Occurrence, ...]]:
        solutions: list[tuple[Occurrence, ...]] = []

        def search(covered: set[int], chosen: list[Occurrence]) -> None:
            if len(solutions) >= limit:
                return
            if covered == items:
                solutions.append(tuple(chosen))
                return
            remaining = items - covered
            item = min(
                remaining,
                key=lambda i: sum(group.isdisjoint(covered) for group in by_item[i]),
            )
            for group in by_item[item]:
                if group in groups and group.isdisjoint(covered):
                    search(covered | set(group), [*chosen, group])

        search(set(), [])
        return solutions

    combined: list[tuple[Occurrence, ...]] = [()]
    for items, groups in components:
        local = solve_component(items, groups)
        if not local:
            return []
        next_combined = []
        for prefix in combined:
            for suffix in local:
                next_combined.append((*prefix, *suffix))
                if len(next_combined) >= limit:
                    break
            if len(next_combined) >= limit:
                break
        combined = next_combined
        if not combined:
            return []
    return combined


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


def raw_hierarchy_level(poses: Sequence[Pose]) -> HierarchyLevel:
    """Wrap physical poses as a level with one leaf per node."""
    return HierarchyLevel(
        tuple(poses),
        tuple(False for _ in poses),
        tuple(frozenset((i,)) for i in range(len(poses))),
    )


def occurrence_base(
    group: Occurrence, template: Template, poses: Sequence[Pose]
) -> Pose:
    """Recover the unique exact transform carrying a template onto a group."""
    index = {pose: i for i, pose in enumerate(poses)}
    return _occurrence_base(group, template, poses, index)


def _occurrence_base(
    group: Occurrence,
    template: Template,
    poses: Sequence[Pose],
    index: dict[Pose, int],
) -> Pose:
    found: set[Pose] = set()
    for item in group:
        for rel in template:
            base = compose_pose(poses[item], inverse_pose(rel))
            ids = frozenset(index.get(compose_pose(base, q), -1) for q in template)
            if ids == group:
                found.add(base)
    if len(found) != 1:
        raise ValueError(f"expected one occurrence base, found {len(found)}")
    return found.pop()


def contract_level(
    level: HierarchyLevel,
    rule: CompositionRule,
    cover: CoverResult | None = None,
) -> HierarchyLevel:
    """Contract an exact cover into parent anchors, retaining leaf provenance."""
    if cover is None:
        cover = cover_with_rule(level.poses, rule.full, rule.missing)
    if cover.n_solutions != 1:
        raise ValueError("contraction requires a unique exact cover")
    poses = []
    exceptional = []
    leaves = []
    index = {pose: i for i, pose in enumerate(level.poses)}
    for group in cover.groups:
        template = rule.full if len(group) == len(rule.full) else rule.missing
        poses.append(_occurrence_base(group, template, level.poses, index))
        exceptional.append(len(group) == len(rule.missing))
        leaves.append(frozenset().union(*(level.leaves[i] for i in group)))
    return HierarchyLevel(tuple(poses), tuple(exceptional), tuple(leaves))


def discover_exceptional_composition(
    level: HierarchyLevel, full_size: int = 8
) -> tuple[CompositionRule, CoverResult, dict]:
    """Find the recursive rule requiring one exceptional child per parent."""
    accepted = []
    proposals = frequent_nearest_templates(
        level.poses, full_size, top=len(level.poses)
    )
    for rank, (full, frequency) in enumerate(proposals, 1):
        for missing in deletion_variants(full):
            cover = cover_with_rule(level.poses, full, missing)
            if cover.n_solutions != 1:
                continue
            if all(sum(level.exceptional[i] for i in group) == 1
                   for group in cover.groups):
                accepted.append((
                    rank,
                    CompositionRule(full, missing, full_size, frequency),
                    cover,
                ))
    if len(accepted) != 1:
        raise ValueError(
            f"expected one exceptional-child composition, found {len(accepted)}"
        )
    rank, rule, cover = accepted[0]
    return rule, cover, {
        "proposal_rank": rank,
        "proposal_frequency": rule.proposal_frequency,
        "n_full": cover.n_full,
        "n_missing": cover.n_missing,
    }


def physical_edge_contacts(
    poses: Sequence[Pose], tile_boundary: Sequence[Vec4]
) -> tuple[tuple[int, int], ...]:
    """Physical-tile pairs sharing one or more complete boundary edges."""
    edge_tiles: dict[tuple[Vec4, Vec4], list[int]] = defaultdict(list)
    for i, (s, r, t) in enumerate(poses):
        vertices = [madd(t, apply_sr(s, r, v)) for v in tile_boundary]
        for j, a in enumerate(vertices):
            b = vertices[(j + 1) % len(vertices)]
            edge_tiles[tuple(sorted((a, b)))].append(i)
    contacts = set()
    for tiles in edge_tiles.values():
        if len(tiles) == 2:
            contacts.add(tuple(sorted(tiles)))
        elif len(tiles) > 2:
            raise ValueError("more than two physical tiles share an edge")
    return tuple(sorted(contacts))


def contracted_adjacency(
    contacts: Sequence[tuple[int, int]], level: HierarchyLevel
) -> tuple[frozenset[int], ...]:
    """Adjacency graph induced by physical edge contacts between clusters."""
    owner = {leaf: i for i, leaves in enumerate(level.leaves) for leaf in leaves}
    adjacent = [set() for _ in level.poses]
    for x, y in contacts:
        a, b = owner[x], owner[y]
        if a != b:
            adjacent[a].add(b)
            adjacent[b].add(a)
    return tuple(frozenset(neighbors) for neighbors in adjacent)


def refinement_isomorphism(
    left: Sequence[Occurrence],
    left_colors: Sequence[object],
    right: Sequence[Occurrence],
    right_colors: Sequence[object],
) -> tuple[dict[int, int], int]:
    """Exact joint color refinement; require a discrete graph isomorphism."""
    if len(left) != len(right):
        raise ValueError("graph sizes differ")
    lc = [(left_colors[i], len(left[i])) for i in range(len(left))]
    rc = [(right_colors[i], len(right[i])) for i in range(len(right))]
    rounds = 0
    for rounds in range(len(left) + 1):
        ls = [(lc[i], tuple(sorted(lc[j] for j in left[i])))
              for i in range(len(left))]
        rs = [(rc[i], tuple(sorted(rc[j] for j in right[i])))
              for i in range(len(right))]
        keys = {sig: k for k, sig in enumerate(sorted(set(ls + rs)))}
        nl = [keys[sig] for sig in ls]
        nr = [keys[sig] for sig in rs]
        if Counter(nl) != Counter(nr):
            raise ValueError("colored adjacency graphs are not isomorphic")
        if nl == lc and nr == rc:
            break
        lc, rc = nl, nr
    if len(set(lc)) != len(left):
        raise ValueError("color refinement did not produce a unique bijection")
    inverse = {color: i for i, color in enumerate(rc)}
    mapping = {i: inverse[color] for i, color in enumerate(lc)}
    if not all(
        {mapping[j] for j in left[i]} == set(right[mapping[i]])
        for i in mapping
    ):
        raise ValueError("refinement bijection does not preserve edges")
    return mapping, rounds


def rule_from_partition(
    level: HierarchyLevel, groups: Sequence[Occurrence]
) -> tuple[CompositionRule, CoverResult]:
    """Extract one 8/7 congruence rule from a known exact partition."""
    templates: dict[int, Counter[Template]] = defaultdict(Counter)
    for group in groups:
        templates[len(group)][
            canonical_cluster([level.poses[i] for i in group])
        ] += 1
    if set(templates) != {7, 8}:
        raise ValueError(f"expected group sizes 7 and 8, got {set(templates)}")
    if len(templates[7]) != 1 or len(templates[8]) != 1:
        raise ValueError("partition does not form one congruence class per size")
    full, n_full = templates[8].most_common(1)[0]
    missing, n_missing = templates[7].most_common(1)[0]
    if missing not in deletion_variants(full):
        raise ValueError("seven-child template is not a deletion of the full rule")
    ordered = tuple(sorted(groups, key=lambda group: tuple(sorted(group))))
    rule = CompositionRule(full, missing, 8, n_full)
    return rule, CoverResult(ordered, n_full, n_missing, 1)


def recover_recursive_hierarchy(
    lower_physical: Sequence[Pose],
    upper_physical: Sequence[Pose],
    physical_rule: CompositionRule,
    tile_boundary: Sequence[Vec4],
) -> RecursiveHierarchy:
    """Recover all scale-specific 8/7 rules using adjacent-size graph transfer.

    ``lower_physical`` and ``upper_physical`` must be consecutive substitution
    patches with the same root. No labels or hidden paths are consumed.
    """
    low_raw = raw_hierarchy_level(lower_physical)
    high_raw = raw_hierarchy_level(upper_physical)
    low = contract_level(low_raw, physical_rule)
    high_base = contract_level(high_raw, physical_rule)
    current_rule, low_cover, _ = discover_exceptional_composition(low)
    high_cover = cover_with_rule(
        high_base.poses, current_rule.full, current_rule.missing
    )
    if high_cover.n_solutions != 1 or not all(
        sum(high_base.exceptional[i] for i in group) == 1
        for group in high_cover.groups
    ):
        raise ValueError("first recursive rule does not close on upper patch")
    high = contract_level(high_base, current_rule, high_cover)
    if len(low.poses) != len(high.poses):
        raise ValueError("consecutive patches did not align after contraction")

    low_contacts = physical_edge_contacts(lower_physical, tile_boundary)
    high_contacts = physical_edge_contacts(upper_physical, tile_boundary)
    levels = [low]
    rules = []
    covers = []
    refinement_rounds = []

    while True:
        rules.append(current_rule)
        covers.append(low_cover)
        low_next = contract_level(low, current_rule, low_cover)
        levels.append(low_next)
        if len(low_next.poses) == 1:
            break

        mapping, rounds = refinement_isomorphism(
            contracted_adjacency(low_contacts, low),
            low.exceptional,
            contracted_adjacency(high_contacts, high),
            high.exceptional,
        )
        refinement_rounds.append(rounds)
        transferred = tuple(
            frozenset(mapping[i] for i in group) for group in low_cover.groups
        )
        next_rule, transferred_cover = rule_from_partition(high, transferred)
        high_next = contract_level(high, next_rule, transferred_cover)
        next_cover = cover_with_rule(
            low_next.poses, next_rule.full, next_rule.missing
        )
        if next_cover.n_solutions != 1 or not all(
            sum(low_next.exceptional[i] for i in group) == 1
            for group in next_cover.groups
        ):
            raise ValueError("transferred recursive rule does not close")
        low, high = low_next, high_next
        current_rule, low_cover = next_rule, next_cover

    return RecursiveHierarchy(
        tuple(levels), tuple(rules), tuple(covers), tuple(refinement_rounds)
    )


def oriented_collar_colors(
    level: HierarchyLevel,
    adjacency: Sequence[Occurrence],
    radius: int = 1,
) -> tuple[int, ...]:
    """Exact rooted collar colors using oriented relative neighbor poses."""
    signatures = oriented_collar_signatures(level, adjacency, radius)
    keys = {sig: k for k, sig in enumerate(sorted(set(signatures)))}
    return tuple(keys[sig] for sig in signatures)


def oriented_collar_signatures(
    level: HierarchyLevel,
    adjacency: Sequence[Occurrence],
    radius: int = 1,
) -> tuple[object, ...]:
    """Scale-local exact signatures, before arbitrary integer color naming."""
    colors: list[object] = list(level.exceptional)
    for _ in range(radius):
        colors = [
            (
                colors[i],
                tuple(sorted(
                    (relative_pose(level.poses[i], level.poses[j]), colors[j])
                    for j in adjacency[i]
                )),
            )
            for i in range(len(level.poses))
        ]
    return tuple(colors)


def _strongly_connected(graph: dict[int, set[int]]) -> bool:
    """Whether every state reaches every other state."""
    if not graph:
        return False
    states = set(graph)
    for start in states:
        seen = {start}
        frontier = [start]
        while frontier:
            node = frontier.pop()
            for child in graph[node]:
                if child not in seen:
                    seen.add(child)
                    frontier.append(child)
        if seen != states:
            return False
    return True


def collared_substitution_rules(
    reference_child: HierarchyLevel,
    child: HierarchyLevel,
    parent: HierarchyLevel,
    cover: CoverResult,
    reference_contacts: Sequence[tuple[int, int]],
    contacts: Sequence[tuple[int, int]],
    radius: int = 1,
    interior_degree: int = 6,
) -> dict:
    """Align both sides to one stationary finite collar alphabet.

    Integer collar colors computed independently at adjacent scales are not
    comparable.  The equal-sized ``reference_child`` and ``parent`` graphs
    are therefore aligned by exact colored graph isomorphism.  Child collar
    signatures are matched directly to the reference signatures (the two
    child patches live at the same physical scale).  The returned parent
    keys and child values consequently inhabit one closed state set.
    """
    reference_adjacency = contracted_adjacency(
        reference_contacts, reference_child
    )
    child_adjacency = contracted_adjacency(contacts, child)
    parent_adjacency = contracted_adjacency(contacts, parent)
    mapping, refinement_rounds = refinement_isomorphism(
        reference_adjacency,
        reference_child.exceptional,
        parent_adjacency,
        parent.exceptional,
    )
    parent_to_reference = {parent_i: reference_i
                           for reference_i, parent_i in mapping.items()}
    reference_signatures = oriented_collar_signatures(
        reference_child, reference_adjacency, radius
    )
    child_signatures = oriented_collar_signatures(
        child, child_adjacency, radius
    )
    interior_reference = sorted({
        reference_signatures[i]
        for i, neighbors in enumerate(reference_adjacency)
        if len(neighbors) == interior_degree
    })
    state_for_signature = {
        signature: state for state, signature in enumerate(interior_reference)
    }
    child_interior_signatures = {
        child_signatures[i]
        for i, neighbors in enumerate(child_adjacency)
        if len(neighbors) == interior_degree
    }
    if child_interior_signatures != set(interior_reference):
        raise ValueError("reference and child collar languages differ")

    patterns: dict[int, Counter[tuple]] = defaultdict(Counter)
    for i, group in enumerate(cover.groups):
        if len(parent_adjacency[i]) != interior_degree:
            continue
        if any(len(child_adjacency[j]) != interior_degree for j in group):
            continue
        reference_i = parent_to_reference[i]
        if len(reference_adjacency[reference_i]) != interior_degree:
            raise ValueError("interior parent mapped to boundary reference node")
        parent_state = state_for_signature[reference_signatures[reference_i]]
        pattern = tuple(sorted(
            (
                relative_pose(parent.poses[i], child.poses[j]),
                state_for_signature[child_signatures[j]],
            )
            for j in group
        ))
        patterns[parent_state][pattern] += 1
    ambiguous = {
        state: len(found) for state, found in patterns.items() if len(found) != 1
    }
    rules = {}
    for state, found in patterns.items():
        if len(found) == 1:
            pattern, occurrences = found.most_common(1)[0]
            rules[state] = {
                "occurrences": occurrences,
                "children": pattern,
            }
    parent_states = set(patterns)
    child_states = {
        state
        for rule in rules.values()
        for _, state in rule["children"]
    }
    state_domain = set(range(len(interior_reference)))
    transition_graph = {
        state: {child_state for _, child_state in rules[state]["children"]}
        for state in rules
    }
    return {
        "radius": radius,
        "interior_degree": interior_degree,
        "eligible_parents": sum(sum(found.values()) for found in patterns.values()),
        "state_count": len(state_domain),
        "states": sorted(state_domain),
        "reference_child_collar_classes": len(interior_reference),
        "child_collar_classes": len(child_interior_signatures),
        "parent_collar_classes": len(patterns),
        "parent_states": sorted(parent_states),
        "child_states": sorted(child_states),
        "closed": parent_states == child_states == state_domain,
        "strongly_connected": (
            set(transition_graph) == state_domain
            and _strongly_connected(transition_graph)
        ),
        "alignment_refinement_rounds": refinement_rounds,
        "ambiguous_classes": ambiguous,
        "deterministic": (
            bool(patterns)
            and not ambiguous
            and parent_states == state_domain
        ),
        "rules": rules,
    }


def _canonical_colored_cluster(
    poses: Sequence[Pose], states: Sequence[int]
) -> tuple:
    """Root-independent exact colored cluster signature."""
    return min(
        tuple(sorted(
            (relative_pose(root, pose), state)
            for pose, state in zip(poses, states)
        ))
        for root in poses
    )


def collared_composition_sat_certificate(
    reference_child: HierarchyLevel,
    child: HierarchyLevel,
    parent: HierarchyLevel,
    cover: CoverResult,
    reference_contacts: Sequence[tuple[int, int]],
    contacts: Sequence[tuple[int, int]],
    collared_rules: dict,
    radius: int = 1,
    interior_degree: int = 6,
) -> dict:
    """SAT-check unique parent grouping for every recovered legal collar.

    Every geometric 8/7 occurrence touching a central parent is offered to
    the solver.  Occurrences whose colored child pattern is not one of the
    stationary rules are forbidden.  Exact-one clauses cover the central
    children, overlap clauses keep selected parents disjoint, and a second
    solve forbids the known parent.  UNSAT on that second solve proves that
    the collared local configuration has no alternative composition.
    """
    from pysat.solvers import Cadical195

    reference_adjacency = contracted_adjacency(
        reference_contacts, reference_child
    )
    child_adjacency = contracted_adjacency(contacts, child)
    parent_adjacency = contracted_adjacency(contacts, parent)
    mapping, _ = refinement_isomorphism(
        reference_adjacency,
        reference_child.exceptional,
        parent_adjacency,
        parent.exceptional,
    )
    parent_to_reference = {parent_i: reference_i
                           for reference_i, parent_i in mapping.items()}
    reference_signatures = oriented_collar_signatures(
        reference_child, reference_adjacency, radius
    )
    child_signatures = oriented_collar_signatures(
        child, child_adjacency, radius
    )
    interior_reference = sorted({
        reference_signatures[i]
        for i, neighbors in enumerate(reference_adjacency)
        if len(neighbors) == interior_degree
    })
    state_for_signature = {
        signature: state for state, signature in enumerate(interior_reference)
    }
    child_states = [
        state_for_signature.get(signature) for signature in child_signatures
    ]

    legal_patterns = {
        _canonical_colored_cluster(
            [pose for pose, _ in rule["children"]],
            [state for _, state in rule["children"]],
        )
        for rule in collared_rules["rules"].values()
    }
    templates = {
        canonical_cluster([pose for pose, _ in rule["children"]])
        for rule in collared_rules["rules"].values()
    }
    occurrences = sorted({
        occurrence
        for template in templates
        for occurrence in template_occurrences(template, child.poses)
    }, key=lambda occurrence: tuple(sorted(occurrence)))
    occurrence_index = {
        occurrence: i for i, occurrence in enumerate(occurrences)
    }
    legal = []
    fully_colored = []
    for occurrence in occurrences:
        states = [child_states[i] for i in occurrence]
        complete = all(state is not None for state in states)
        fully_colored.append(complete)
        legal.append(
            complete
            and _canonical_colored_cluster(
                [child.poses[i] for i in occurrence],
                states,
            ) in legal_patterns
        )

    by_state: dict[int, dict[str, int | bool]] = {
        state: {
            "instances": 0,
            "complete_contexts": 0,
            "unique": 0,
            "ambiguous": 0,
        }
        for state in collared_rules["states"]
    }
    eligible = complete_contexts = unique = ambiguous = 0
    known_groups = set(cover.groups)
    for parent_i, group in enumerate(cover.groups):
        if len(parent_adjacency[parent_i]) != interior_degree:
            continue
        if any(len(child_adjacency[i]) != interior_degree for i in group):
            continue
        reference_i = parent_to_reference[parent_i]
        state = state_for_signature[reference_signatures[reference_i]]
        eligible += 1
        by_state[state]["instances"] += 1
        local = [
            i for i, occurrence in enumerate(occurrences)
            if occurrence & group
        ]
        if any(not fully_colored[i] for i in local):
            continue
        complete_contexts += 1
        by_state[state]["complete_contexts"] += 1
        known = occurrence_index[group]
        variables = {candidate: j + 1 for j, candidate in enumerate(local)}
        clauses: list[list[int]] = []
        for child_i in group:
            covering = [
                variables[candidate]
                for candidate in local
                if child_i in occurrences[candidate]
            ]
            clauses.append(covering)
            for a_pos, a in enumerate(covering):
                for b in covering[a_pos + 1:]:
                    clauses.append([-a, -b])
        touching: dict[int, list[int]] = defaultdict(list)
        for candidate in local:
            for child_i in occurrences[candidate]:
                touching[child_i].append(variables[candidate])
            if not legal[candidate]:
                clauses.append([-variables[candidate]])
        for candidates in touching.values():
            for a_pos, a in enumerate(candidates):
                for b in candidates[a_pos + 1:]:
                    clauses.append([-a, -b])
        known_var = variables[known]
        with Cadical195(bootstrap_with=clauses) as solver:
            known_valid = solver.solve(assumptions=[known_var])
            alternative = solver.solve(assumptions=[-known_var])
        if not known_valid:
            raise ValueError("known parent is not admitted by collar rules")
        if alternative:
            ambiguous += 1
            by_state[state]["ambiguous"] += 1
        else:
            unique += 1
            by_state[state]["unique"] += 1

    legal_occurrences = {
        occurrences[i] for i, admitted in enumerate(legal) if admitted
    }
    return {
        "radius": radius,
        "solver": "CaDiCaL 1.9.5",
        "state_count": collared_rules["state_count"],
        "geometric_candidates": len(occurrences),
        "fully_colored_candidates": sum(fully_colored),
        "legal_candidates": sum(legal),
        "rejected_candidates": sum(
            complete and not admitted
            for complete, admitted in zip(fully_colored, legal)
        ),
        "legal_candidates_outside_known_cover": len(
            legal_occurrences - known_groups
        ),
        "eligible_parent_instances": eligible,
        "complete_context_instances": complete_contexts,
        "unique_instances": unique,
        "ambiguous_instances": ambiguous,
        "states_checked": sum(
            bool(record["complete_contexts"]) for record in by_state.values()
        ),
        "all_states_checked": all(
            record["complete_contexts"] for record in by_state.values()
        ),
        "unique_composition": (
            complete_contexts > 0
            and unique == complete_contexts
            and ambiguous == 0
            and all(
                record["complete_contexts"] for record in by_state.values()
            )
        ),
        "by_state": by_state,
    }


def physical_composition_sat_certificate(
    reference_poses: Sequence[Pose],
    poses: Sequence[Pose],
    selected_rule: CompositionRule,
    candidate_rules: Sequence[CompositionRule],
    tile_boundary: Sequence[Vec4],
    radius: int = 1,
) -> dict:
    """Use physical-tile collars to eliminate competing composition phases.

    The recursively closing rule supplies the legal parent patterns, but the
    colors used here are derived only from radius-``radius`` physical edge
    neighborhoods.  Every occurrence from every locally exact phase is then
    offered to SAT.  Thus recursive closure chooses the language once, while
    a finite local rule recognizes it without hidden ancestry.
    """
    from pysat.solvers import Cadical195

    reference = raw_hierarchy_level(reference_poses)
    upper = raw_hierarchy_level(poses)
    reference_adjacency = contracted_adjacency(
        physical_edge_contacts(reference_poses, tile_boundary), reference
    )
    adjacency = contracted_adjacency(
        physical_edge_contacts(poses, tile_boundary), upper
    )
    reference_signatures = oriented_collar_signatures(
        reference, reference_adjacency, radius
    )
    signatures = oriented_collar_signatures(upper, adjacency, radius)
    language = sorted(set(reference_signatures))
    if set(signatures) != set(language):
        raise ValueError("physical collar language changed between patch sizes")
    state_for_signature = {
        signature: state for state, signature in enumerate(language)
    }
    reference_states = [
        state_for_signature[signature] for signature in reference_signatures
    ]
    states = [state_for_signature[signature] for signature in signatures]

    reference_cover = cover_with_rule(
        reference_poses, selected_rule.full, selected_rule.missing
    )
    selected_cover = cover_with_rule(
        poses, selected_rule.full, selected_rule.missing
    )
    if reference_cover.n_solutions != 1 or selected_cover.n_solutions != 1:
        raise ValueError("selected physical rule does not uniquely cover patches")

    def patterns_for(
        patch: Sequence[Pose],
        patch_states: Sequence[int],
        cover: CoverResult,
    ) -> set[tuple]:
        return {
            _canonical_colored_cluster(
                [patch[i] for i in group],
                [patch_states[i] for i in group],
            )
            for group in cover.groups
        }

    reference_patterns = patterns_for(
        reference_poses, reference_states, reference_cover
    )
    legal_patterns = patterns_for(poses, states, selected_cover)
    if reference_patterns != legal_patterns:
        raise ValueError("physical collared parent language did not stabilize")

    occurrences = sorted({
        occurrence
        for rule in candidate_rules
        for template in (rule.full, rule.missing)
        for occurrence in template_occurrences(template, poses)
    }, key=lambda occurrence: tuple(sorted(occurrence)))
    occurrence_index = {
        occurrence: i for i, occurrence in enumerate(occurrences)
    }
    occurrence_patterns = [
        _canonical_colored_cluster(
            [poses[i] for i in occurrence],
            [states[i] for i in occurrence],
        )
        for occurrence in occurrences
    ]
    legal = [
        pattern in legal_patterns for pattern in occurrence_patterns
    ]
    legal_occurrences = {
        occurrences[i] for i, admitted in enumerate(legal) if admitted
    }

    representative: dict[tuple, Occurrence] = {}
    for group in selected_cover.groups:
        representative.setdefault(
            occurrence_patterns[occurrence_index[group]], group
        )
    unique = ambiguous = 0
    for group in representative.values():
        local = [
            i for i, occurrence in enumerate(occurrences)
            if occurrence & group
        ]
        variables = {candidate: j + 1 for j, candidate in enumerate(local)}
        clauses: list[list[int]] = []
        for tile_i in group:
            covering = [
                variables[candidate]
                for candidate in local
                if tile_i in occurrences[candidate]
            ]
            clauses.append(covering)
            for a_pos, a in enumerate(covering):
                for b in covering[a_pos + 1:]:
                    clauses.append([-a, -b])
        touching: dict[int, list[int]] = defaultdict(list)
        for candidate in local:
            for tile_i in occurrences[candidate]:
                touching[tile_i].append(variables[candidate])
            if not legal[candidate]:
                clauses.append([-variables[candidate]])
        for candidates in touching.values():
            for a_pos, a in enumerate(candidates):
                for b in candidates[a_pos + 1:]:
                    clauses.append([-a, -b])
        known_var = variables[occurrence_index[group]]
        with Cadical195(bootstrap_with=clauses) as solver:
            known_valid = solver.solve(assumptions=[known_var])
            alternative = solver.solve(assumptions=[-known_var])
        if not known_valid:
            raise ValueError("known physical parent is not locally admitted")
        if alternative:
            ambiguous += 1
        else:
            unique += 1

    return {
        "radius": radius,
        "solver": "CaDiCaL 1.9.5",
        "physical_collar_states": len(language),
        "legal_parent_patterns": len(legal_patterns),
        "candidate_phases": len(candidate_rules),
        "geometric_candidates": len(occurrences),
        "legal_candidates": sum(legal),
        "rejected_candidates": len(legal) - sum(legal),
        "selected_cover_groups": len(selected_cover.groups),
        "legal_candidates_outside_selected_cover": len(
            legal_occurrences - set(selected_cover.groups)
        ),
        "patterns_sat_checked": len(representative),
        "unique_patterns": unique,
        "ambiguous_patterns": ambiguous,
        "stable_between_patch_sizes": True,
        "unique_composition": (
            legal_occurrences == set(selected_cover.groups)
            and unique == len(representative)
            and ambiguous == 0
        ),
    }


def enumerate_composition_candidates(
    poses: Sequence[Pose],
    confirmation_poses: Sequence[Pose] | None = None,
    min_size: int = 6,
    max_size: int = 12,
    top: int = 3,
) -> tuple[tuple[CompositionRule, CoverResult], ...]:
    """Return every exact-cover hypothesis before heuristic ranking.

    This is the appropriate input to a wider closure gate: a later recursive
    check may reject a locally valid phase without consulting hidden ancestry.
    """
    accepted: dict[
        tuple[Template, Template], tuple[CompositionRule, CoverResult]
    ] = {}
    final_size = min(max_size, len(poses))
    histograms = _frequent_templates_by_size(poses, min_size, final_size)
    for size in range(min_size, final_size + 1):
        for full, frequency in histograms[size].most_common(top):
            for missing in deletion_variants(full):
                cover = cover_with_rule(poses, full, missing)
                if cover.n_solutions == 1:
                    rule = CompositionRule(full, missing, size, frequency)
                    accepted[(full, missing)] = (rule, cover)
    if confirmation_poses is not None:
        accepted = {
            key: pair
            for key, pair in accepted.items()
            if cover_with_rule(
                confirmation_poses, pair[0].full, pair[0].missing
            ).n_solutions == 1
        }
    return tuple(
        accepted[key] for key in sorted(accepted)
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
    path: str | Path, poses: Sequence[Pose], levels_up: int = 1
) -> tuple[Occurrence, ...]:
    """Read validation-only ancestry and group leaves by an ancestor depth."""
    if levels_up < 1:
        raise ValueError("levels_up must be positive")
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
            grouped[slots[:-levels_up]].add(i)
    return tuple(sorted(
        (frozenset(group) for group in grouped.values()),
        key=lambda group: tuple(sorted(group)),
    ))


def read_hidden_node_labels(
    path: str | Path,
    poses: Sequence[Pose],
    level: HierarchyLevel,
    levels_up: int = 1,
) -> tuple[int, ...]:
    """Read withheld ancestor labels for already recovered physical clusters."""
    pose_index = {pose: i for i, pose in enumerate(poses)}
    leaf_labels: dict[int, tuple[int, ...]] = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if "labels" not in row:
                raise ValueError("hierarchy dump lacks validation label ancestry")
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
            leaf_labels[pose_index[pose]] = tuple(
                int(label) for label in row["labels"].split(".")
            )
    result = []
    for leaves in level.leaves:
        labels = {leaf_labels[leaf][-(levels_up + 1)] for leaf in leaves}
        if len(labels) != 1:
            raise ValueError("recovered cluster crosses hidden label ancestors")
        result.append(labels.pop())
    return tuple(result)


def collar_label_validation(
    colors: Sequence[int],
    labels: Sequence[int],
    indices: Iterable[int] | None = None,
) -> dict:
    """Post-hoc purity of blind collar colors against withheld labels."""
    selected = range(len(colors)) if indices is None else tuple(indices)
    by_color: dict[int, set[int]] = defaultdict(set)
    for i in selected:
        by_color[colors[i]].add(labels[i])
    mixed = {color: sorted(values) for color, values in by_color.items()
             if len(values) > 1}
    return {
        "nodes": sum(1 for _ in selected),
        "collar_classes": len(by_color),
        "labels": len({labels[i] for i in selected}),
        "mixed_classes": mixed,
        "pure": not mixed,
    }


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
