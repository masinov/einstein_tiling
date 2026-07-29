"""Architecture-independent exact finite-obstruction primitives.

Several historical tiling searches used the same mathematical pattern:

1. select a finite set of proposed objects;
2. ask an exact compatibility or matching oracle for an obstruction; and
3. deletion-minimize the obstruction before learning or recording it.

This module retains the reusable mathematics without retaining any particular
tile, quotient, SAT encoding or experiment schedule.  It is deliberately
small: solver orchestration and symmetry actions remain with their owning
problem until a second independent consumer justifies a broader interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, Hashable, Iterable, Sequence, TypeVar


Resource = TypeVar("Resource", bound=Hashable)
Item = TypeVar("Item", bound=Hashable)


def deletion_minimal_obstruction(
    items: Iterable[Item],
    obstructed: Callable[[tuple[Item, ...]], bool],
) -> tuple[Item, ...]:
    """Return a deterministic deletion-minimal obstructed subset.

    ``obstructed`` is normally a monotone exact predicate: once a set is
    obstructed, adding more items cannot repair it.  The implementation
    restarts after every deletion, so the returned set is deletion-minimal
    even if the caller supplies a non-monotone predicate.  The empty tuple
    means that the original collection was not obstructed.

    Input order is retained and duplicate items are removed.  This makes the
    result stable without requiring the item type to be orderable.
    """
    core = tuple(dict.fromkeys(items))
    if not obstructed(core):
        return ()
    while True:
        for item in core:
            trial = tuple(candidate for candidate in core if candidate != item)
            if obstructed(trial):
                core = trial
                break
        else:
            return core


def _stable_order(values: Iterable[Resource]) -> tuple[Resource, ...]:
    """Order exact resources reproducibly, including heterogeneous labels."""
    values = tuple(values)
    try:
        return tuple(sorted(values))
    except TypeError:
        return tuple(sorted(
            values,
            key=lambda value: (
                type(value).__module__, type(value).__qualname__, repr(value),
            ),
        ))


@dataclass(frozen=True)
class UniformDemandMatchingResult(Generic[Resource]):
    """A saturated uniform-demand matching or an exact Hall witness."""

    selected: tuple[int, ...]
    demand: int
    matched: int
    assignment: tuple[tuple[int, tuple[Resource, ...]], ...]
    deficient_items: tuple[int, ...]
    deficient_resources: tuple[Resource, ...]

    @property
    def saturated(self) -> bool:
        return self.matched == self.demand * len(self.selected)


def uniform_demand_matching(
    supports: Sequence[frozenset[Resource]],
    selected: Iterable[int],
    *,
    demand: int,
) -> UniformDemandMatchingResult[Resource]:
    """Match ``demand`` distinct resources to every selected item.

    Items are one-based indices into ``supports``.  The routine clones every
    selected left vertex ``demand`` times and runs an exact augmenting-path
    matching.  On failure, alternating reachability from the unmatched clones
    returns a Hall-deficient set of whole items and its complete resource
    neighborhood.  No graph or optimization dependency is required.
    """
    if demand < 1:
        raise ValueError("matching demand must be positive")
    chosen = tuple(sorted(set(selected)))
    for item in chosen:
        if not 1 <= item <= len(supports):
            raise ValueError("selected item out of range")

    left = tuple(
        (item, copy) for item in chosen for copy in range(demand)
    )
    right_match: dict[Resource, tuple[int, int]] = {}
    left_match: dict[tuple[int, int], Resource] = {}

    def augment(node: tuple[int, int], visited: set[Resource]) -> bool:
        item, _copy = node
        for resource in _stable_order(supports[item - 1]):
            if resource in visited:
                continue
            visited.add(resource)
            incumbent = right_match.get(resource)
            if incumbent is None or augment(incumbent, visited):
                right_match[resource] = node
                left_match[node] = resource
                return True
        return False

    for node in left:
        augment(node, set())

    by_item: dict[int, list[Resource]] = {item: [] for item in chosen}
    for (item, _copy), resource in left_match.items():
        by_item[item].append(resource)
    assignment = tuple(
        (item, _stable_order(resources))
        for item, resources in sorted(by_item.items())
        if len(resources) == demand
    )

    if len(left_match) == len(left):
        return UniformDemandMatchingResult(
            selected=chosen,
            demand=demand,
            matched=len(left_match),
            assignment=assignment,
            deficient_items=(),
            deficient_resources=(),
        )

    reachable_left = {node for node in left if node not in left_match}
    reachable_right: set[Resource] = set()
    queue = list(sorted(reachable_left))
    while queue:
        node = queue.pop()
        item, _copy = node
        matched_resource = left_match.get(node)
        for resource in supports[item - 1]:
            if resource == matched_resource or resource in reachable_right:
                continue
            reachable_right.add(resource)
            incumbent = right_match.get(resource)
            if incumbent is not None and incumbent not in reachable_left:
                reachable_left.add(incumbent)
                queue.append(incumbent)

    deficient_items = tuple(sorted({item for item, _ in reachable_left}))
    deficient_resources = _stable_order(set().union(*(
        supports[item - 1] for item in deficient_items
    )))
    if not len(deficient_resources) < demand * len(deficient_items):
        raise AssertionError("alternating search did not yield a Hall witness")
    return UniformDemandMatchingResult(
        selected=chosen,
        demand=demand,
        matched=len(left_match),
        assignment=assignment,
        deficient_items=deficient_items,
        deficient_resources=deficient_resources,
    )


def verify_uniform_demand_matching(
    supports: Sequence[frozenset[Resource]],
    result: UniformDemandMatchingResult[Resource],
) -> bool:
    """Cold-check either side of a uniform-demand matching result."""
    if result.demand < 1:
        return False
    if any(not 1 <= item <= len(supports) for item in result.selected):
        return False
    if result.saturated:
        if len(result.assignment) != len(result.selected):
            return False
        assigned_items = set()
        used_resources = set()
        for item, resources in result.assignment:
            if item in assigned_items or item not in result.selected:
                return False
            if len(resources) != result.demand or len(set(resources)) != result.demand:
                return False
            if any(resource not in supports[item - 1] for resource in resources):
                return False
            if used_resources.intersection(resources):
                return False
            assigned_items.add(item)
            used_resources.update(resources)
        return assigned_items == set(result.selected)

    items = set(result.deficient_items)
    resources = set(result.deficient_resources)
    if not items or not items <= set(result.selected):
        return False
    actual = set().union(*(supports[item - 1] for item in items))
    return resources == actual and len(resources) < result.demand * len(items)
