"""Adaptive two-center certificates for the Layer-D density bound.

Every placement of the ten-kite candidate meets four centers of the underlying
hexagonal substrate.  If a compatible packing of placements admits two
*distinct* centers per placement, with no center assigned twice, then

``2 * number_of_placements <= number_of_quotient_centers``.

This module implements that certificate as an ordinary bipartite matching.
It deliberately contains no LP or graph-library dependency: the returned
matching and, on failure, the Hall-deficient tile set are independently
checkable finite objects.
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import Counter

from einstein.theory.a4_v4_packing import placement_lattice_cells


Center = tuple[int, int]


@dataclass(frozen=True)
class TwoMatchingResult:
    """A saturated two-matching or an exact Hall-deficiency witness."""

    selected: tuple[int, ...]
    matched: int
    assignment: tuple[tuple[int, Center, Center], ...]
    deficient_tiles: tuple[int, ...]
    deficient_centers: tuple[Center, ...]

    @property
    def saturated(self) -> bool:
        return self.matched == 2 * len(self.selected)


def reduce_center(center: Center, hnf: tuple[int, int, int]) -> Center:
    """Reduce an infinite lattice center through column HNF ``(a,b,d)``."""
    u, v = center
    a, b, d = hnf
    quotient_v, reduced_v = divmod(v, d)
    return (u - quotient_v * b) % a, reduced_v


def placement_center_supports(shape, system):
    """Four-center quotient support of every placement variable."""
    supports = []
    for placement in system.placements:
        centers = frozenset(
            reduce_center((u, v), system.hnf)
            for u, v, _sector in placement_lattice_cells(shape, placement)
        )
        if len(centers) != 4:
            raise ValueError(
                f"placement {placement!r} has {len(centers)} quotient centers; "
                "the four-center Hall certificate is not applicable"
            )
        supports.append(centers)
    return tuple(supports)


def hall_neighborhood(supports, selected) -> frozenset[Center]:
    """Return the exact center neighborhood of one-based tile variables."""
    chosen = tuple(sorted(set(selected)))
    for variable in chosen:
        if not 1 <= variable <= len(supports):
            raise ValueError("placement variable out of range")
    if not chosen:
        return frozenset()
    return frozenset().union(*(supports[variable - 1] for variable in chosen))


def hall_deficiency(supports, selected) -> int:
    """The Hall surplus ``2|S|-|N(S)|`` (positive exactly when deficient)."""
    chosen = tuple(sorted(set(selected)))
    return 2 * len(chosen) - len(hall_neighborhood(supports, chosen))


def two_center_matching(supports, selected) -> TwoMatchingResult:
    """Match two copies of each selected one-based placement to its centers.

    A simple augmenting-path implementation suffices here because every left
    vertex has degree four.  If saturation fails, alternating reachability
    from all unmatched left copies gives a strict Hall witness.  The two
    copies of a tile have identical neighborhoods, hence either both copies
    are reachable or neither is; the witness therefore descends from copies
    to whole tiles and satisfies ``|N(S)| < 2|S|``.
    """
    chosen = tuple(sorted(set(selected)))
    for variable in chosen:
        if not 1 <= variable <= len(supports):
            raise ValueError("placement variable out of range")

    left = tuple((variable, copy) for variable in chosen for copy in (0, 1))
    right_match: dict[Center, tuple[int, int]] = {}
    left_match: dict[tuple[int, int], Center] = {}

    def augment(node, visited: set[Center]) -> bool:
        variable, _copy = node
        for center in sorted(supports[variable - 1]):
            if center in visited:
                continue
            visited.add(center)
            incumbent = right_match.get(center)
            if incumbent is None or augment(incumbent, visited):
                right_match[center] = node
                left_match[node] = center
                return True
        return False

    for node in left:
        augment(node, set())

    by_tile: dict[int, list[Center]] = {variable: [] for variable in chosen}
    for (variable, _copy), center in left_match.items():
        by_tile[variable].append(center)
    assignment = tuple(
        (variable, *sorted(centers))
        for variable, centers in sorted(by_tile.items())
        if len(centers) == 2
    )

    if len(left_match) == len(left):
        return TwoMatchingResult(
            selected=chosen,
            matched=len(left_match),
            assignment=assignment,
            deficient_tiles=(),
            deficient_centers=(),
        )

    # Alternating reachability: unmatched edges left->right, matched edges
    # right->left.  Starting at every unmatched copy produces the min-cut
    # side and thus an explicit Hall-deficient set.
    reachable_left = {node for node in left if node not in left_match}
    reachable_right: set[Center] = set()
    queue = list(sorted(reachable_left))
    while queue:
        node = queue.pop()
        variable, _copy = node
        matched_center = left_match.get(node)
        for center in supports[variable - 1]:
            if center == matched_center or center in reachable_right:
                continue
            reachable_right.add(center)
            incumbent = right_match.get(center)
            if incumbent is not None and incumbent not in reachable_left:
                reachable_left.add(incumbent)
                queue.append(incumbent)

    deficient_tiles = tuple(sorted({variable for variable, _ in reachable_left}))
    deficient_centers = tuple(sorted(set().union(*(
        supports[variable - 1] for variable in deficient_tiles
    ))))
    if not len(deficient_centers) < 2 * len(deficient_tiles):
        raise AssertionError("alternating search did not yield a Hall witness")
    return TwoMatchingResult(
        selected=chosen,
        matched=len(left_match),
        assignment=assignment,
        deficient_tiles=deficient_tiles,
        deficient_centers=deficient_centers,
    )


def minimal_hall_witness(supports, selected) -> TwoMatchingResult:
    """Deletion-minimize an exact Hall-deficient subset of ``selected``.

    The matching oracle may expose a deficient subset even when the full
    selection has at least twice as many neighboring centers as tiles.  We
    first descend to that alternating-path witness, then repeatedly delete a
    tile whenever the remainder still contains *some* Hall obstruction.  At
    termination every proper subset is matchable: if a smaller deficient set
    existed, deleting any tile outside it would still leave that obstruction.
    """
    result = two_center_matching(supports, selected)
    if result.saturated:
        raise ValueError("selection has no Hall-deficient subset")
    core = result.deficient_tiles
    while True:
        reduced = False
        for variable in core:
            trial = tuple(item for item in core if item != variable)
            candidate = two_center_matching(supports, trial)
            if candidate.saturated:
                continue
            core = candidate.deficient_tiles
            reduced = True
            break
        if not reduced:
            break
    result = two_center_matching(supports, core)
    if result.saturated or result.deficient_tiles != core:
        raise AssertionError("Hall witness minimization did not reach a core")
    return result


def hall_witness_profile(supports, result: TwoMatchingResult):
    """Exact structural data for a deletion-minimal Hall witness.

    Two elementary proof obligations are checked here rather than merely
    reported: a minimal witness is connected in the tile-intersection graph,
    and a tile has at most ``2-deficiency`` private centers.  These reductions
    are the starting point for the planar sparsity proof.
    """
    if result.saturated:
        raise ValueError("a saturated matching is not a Hall witness")
    tiles = result.deficient_tiles
    centers = hall_neighborhood(supports, tiles)
    deficiency = 2 * len(tiles) - len(centers)
    if deficiency <= 0 or centers != frozenset(result.deficient_centers):
        raise ValueError("invalid Hall-deficiency witness")
    if any(not two_center_matching(
            supports, tuple(item for item in tiles if item != variable)
    ).saturated for variable in tiles):
        raise ValueError("Hall witness is not deletion-minimal")
    if deficiency not in (1, 2):
        raise AssertionError("a minimal four-center Hall witness has deficit 1 or 2")

    center_degrees = Counter(
        center
        for variable in tiles
        for center in supports[variable - 1]
    )
    private_counts = tuple(
        sum(center_degrees[center] == 1 for center in supports[variable - 1])
        for variable in tiles
    )
    if any(count > 2 - deficiency for count in private_counts):
        raise AssertionError("minimal-witness private-center bound failed")

    adjacency = {variable: set() for variable in tiles}
    for left_index, left in enumerate(tiles):
        for right in tiles[left_index + 1:]:
            if supports[left - 1] & supports[right - 1]:
                adjacency[left].add(right)
                adjacency[right].add(left)
    reached = set()
    stack = [tiles[0]]
    while stack:
        variable = stack.pop()
        if variable in reached:
            continue
        reached.add(variable)
        stack.extend(adjacency[variable] - reached)
    if reached != set(tiles):
        raise AssertionError("minimal Hall witness is disconnected")

    degree_histogram = Counter(center_degrees.values())
    signed_curvature = sum(
        (degree - 2) * count for degree, count in degree_histogram.items()
    )
    if signed_curvature != 2 * deficiency:
        raise AssertionError("four-center incidence curvature identity failed")

    return {
        "tile_count": len(tiles),
        "center_count": len(centers),
        "deficiency": deficiency,
        "private_center_histogram": dict(sorted(Counter(private_counts).items())),
        "center_degree_histogram": dict(sorted(degree_histogram.items())),
        "signed_curvature": signed_curvature,
        "intersection_edges": sum(map(len, adjacency.values())) // 2,
    }


def verify_two_matching(supports, result: TwoMatchingResult) -> bool:
    """Independently check either side of a :class:`TwoMatchingResult`."""
    if result.saturated:
        if len(result.assignment) != len(result.selected):
            return False
        used = set()
        assigned = set()
        for variable, first, second in result.assignment:
            if variable in assigned or variable not in result.selected:
                return False
            if first == second:
                return False
            if first not in supports[variable - 1] or second not in supports[variable - 1]:
                return False
            if first in used or second in used:
                return False
            assigned.add(variable)
            used.update((first, second))
        return assigned == set(result.selected)
    tiles = set(result.deficient_tiles)
    centers = set(result.deficient_centers)
    if not tiles or not tiles <= set(result.selected):
        return False
    actual = set().union(*(supports[variable - 1] for variable in tiles))
    return centers == actual and len(centers) < 2 * len(tiles)
