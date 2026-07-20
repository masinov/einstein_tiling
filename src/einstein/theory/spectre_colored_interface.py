"""Colored parent/component interfaces derived from physical Spectre edges."""

from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import Iterable, Mapping, Sequence

from einstein.substrate.module12 import (
    Pose, compose_pose, inverse_pose, relative_pose,
)
from einstein.theory.spectre_patch_language import (
    edge_key,
    patch_edge_incidence,
    polygon_edges,
    transformed_polygon,
)


Contact = tuple[int, int, int, int]
ANY_KIND = "*"
ColoredNeighbor = tuple[Pose, str, tuple[Contact, ...]]
ColoredCorona = tuple[str, tuple[ColoredNeighbor, ...]]


def component_kind(
    base: Pose, mapping: Mapping[Pose, Pose], templates, *,
    patch: Iterable[Pose] | None = None,
    complete: Iterable[Pose] | None = None,
) -> str | None:
    """Return full/missing once the canonical eight-child core is mapped.

    With a finite ``patch``, absence of the optional child is not enough to
    call a component missing.  At least one core child which would touch that
    optional child must have its entire physical corona present (belong to
    ``complete``).  This turns absence into an observed alternative contact,
    rather than an artifact of the finite patch boundary.
    """
    full, missing = templates
    common = {compose_pose(base, child) for child in missing}
    if any(child not in mapping for child in common):
        return None
    if any(mapping[child] != base for child in common):
        return None
    optional_relative = next(iter(set(full) - set(missing)))
    optional = compose_pose(base, optional_relative)
    if optional in mapping:
        # The physical tile at the optional pose may instead belong to an
        # adjacent component; that is an observed missing-parent interface.
        return "full" if mapping[optional] == base else "missing"
    if patch is None:
        return "missing"
    patch_set = patch if isinstance(patch, (set, frozenset)) else set(patch)
    if optional in patch_set or complete is None:
        return None
    complete_set = (
        complete if isinstance(complete, (set, frozenset)) else set(complete)
    )
    observed_contacts = {
        compose_pose(base, child)
        for child in _optional_adjacent_core(tuple(full), tuple(missing))
    }
    return "missing" if observed_contacts & complete_set else None


@lru_cache(maxsize=None)
def _optional_adjacent_core(full, missing):
    """Canonical core children sharing a physical edge with child nine."""
    optional = next(iter(set(full) - set(missing)))
    optional_edges = {
        edge_key(edge) for edge in polygon_edges(transformed_polygon(optional))
    }
    return tuple(
        child for child in missing
        if optional_edges & {
            edge_key(edge)
            for edge in polygon_edges(transformed_polygon(child))
        }
    )


def _edge_index(tile: Pose, key) -> int:
    for index, edge in enumerate(polygon_edges(transformed_polygon(tile))):
        if edge_key(edge) == key:
            return index
    raise ValueError("incidence edge is absent from its owner tile")


def colored_parent_corona(
    center: Pose,
    patch: Sequence[Pose],
    mapping: Mapping[Pose, Pose],
    templates,
    *,
    incidence=None,
    fibers=None,
    edges_by_tile=None,
    complete=None,
    require_neighbor_kinds: bool = True,
    trust_mapping_absence: bool = False,
) -> ColoredCorona | None:
    """Return a complete parent corona with exact child-edge interface colors.

    A contact color records ``(center child slot, center physical edge,
    neighbor child slot, neighbor physical edge)``. Parent type and neighbor
    type are explicit. ``None`` means that the finite physical patch does not
    yet buffer all required data.
    """
    full, _ = templates
    slot = {relative: index for index, relative in enumerate(full)}
    if incidence is None:
        incidence, _ = patch_edge_incidence(patch)
    if complete is None:
        exposed = {
            owners[0] for owners in incidence.values() if len(owners) == 1
        }
        complete = set(patch) - exposed
    patch_set = set(patch)
    kind_context = (
        {} if trust_mapping_absence
        else {"patch": patch_set, "complete": complete}
    )
    center_kind = component_kind(
        center, mapping, templates, **kind_context,
    )
    if center_kind is None:
        return None
    fiber = (
        set(fibers.get(center, ()))
        if fibers is not None
        else {tile for tile, base in mapping.items() if base == center}
    )
    expected = {compose_pose(center, child) for child in full}
    if not fiber <= expected or len(fiber) not in (len(full) - 1, len(full)):
        return None

    incidence_items = (
        {
            key: owners
            for tile in fiber
            for key, owners in edges_by_tile.get(tile, ())
        }.items()
        if edges_by_tile is not None else incidence.items()
    )
    contacts = defaultdict(list)
    for key, owners in incidence_items:
        center_owners = [tile for tile in owners if tile in fiber]
        if not center_owners:
            continue
        if len(owners) != 2:
            return None
        left, right = owners
        if left in fiber and right in fiber:
            continue
        own = left if left in fiber else right
        other = right if own == left else left
        neighbor = mapping.get(other)
        if neighbor is None:
            return None
        if require_neighbor_kinds:
            neighbor_kind = component_kind(
                neighbor, mapping, templates, **kind_context,
            )
            if neighbor_kind is None:
                return None
        own_relative = relative_pose(center, own)
        other_relative = relative_pose(neighbor, other)
        if own_relative not in slot or other_relative not in slot:
            raise ValueError("mapped tile is outside canonical parent support")
        contacts[neighbor].append((
            slot[own_relative], _edge_index(own, key),
            slot[other_relative], _edge_index(other, key),
        ))

    if len(contacts) != 6:
        return None
    neighbors = []
    for neighbor in sorted(contacts):
        kind = ANY_KIND
        if require_neighbor_kinds:
            kind = component_kind(
                neighbor, mapping, templates, **kind_context,
            )
            if kind is None:
                return None
        neighbors.append((
            relative_pose(center, neighbor), kind,
            tuple(sorted(contacts[neighbor])),
        ))
    return center_kind, tuple(sorted(neighbors))


def uncolored_projection(state: ColoredCorona):
    return tuple(sorted(neighbor[0] for neighbor in state[1]))


def one_sided_projection(state: ColoredCorona) -> ColoredCorona:
    """Forget neighbor types while retaining the observed center type/color."""
    return state[0], tuple(
        (relative, ANY_KIND, contacts)
        for relative, _, contacts in state[1]
    )


def reciprocal_color(color: Contact) -> Contact:
    return color[2], color[3], color[0], color[1]


def colored_corona_from_json(row) -> ColoredCorona:
    """Parse the stable JSON representation used by W3 artifacts."""
    return (
        str(row["kind"]),
        tuple(sorted(
            (
                (
                    int(neighbor["relative_anchor"][0]),
                    int(neighbor["relative_anchor"][1]),
                    tuple(map(int, neighbor["relative_anchor"][2])),
                ),
                str(neighbor["kind"]),
                tuple(sorted(tuple(map(int, contact))
                             for contact in neighbor["contacts"])),
            )
            for neighbor in row["neighbors"]
        )),
    )


def colored_corona_json(state: ColoredCorona):
    """Stable JSON representation of an exact colored parent corona."""
    kind, neighbors = state
    return {
        "kind": kind,
        "neighbors": [{
            "relative_anchor": [
                relative[0], relative[1], list(relative[2]),
            ],
            "kind": neighbor_kind,
            "contacts": [list(contact) for contact in contacts],
        } for relative, neighbor_kind, contacts in neighbors],
    }


def colored_reciprocal_domains(
    states: Sequence[ColoredCorona], state_index: int,
    allowed: Iterable[int] | None = None,
    edge_index=None,
):
    """Allowed state indices across each exact colored directed edge."""
    center_kind, neighbors = states[state_index]
    if edge_index is None:
        edge_index = colored_edge_index(states, allowed=allowed)
    domains = []
    for relative, neighbor_kind, contacts in neighbors:
        candidate_kinds = (
            ("full", "missing") if neighbor_kind == ANY_KIND
            else (neighbor_kind,)
        )
        back_kinds = (center_kind, ANY_KIND)
        reversed_contacts = tuple(sorted(map(reciprocal_color, contacts)))
        domain = {
            index
            for candidate_kind in candidate_kinds
            for back_kind in back_kinds
            for index in edge_index.get((
                candidate_kind, inverse_pose(relative), back_kind,
                reversed_contacts,
            ), ())
        }
        domains.append(tuple(sorted(domain)))
    return tuple(domains)


def colored_edge_index(
    states: Sequence[ColoredCorona], allowed: Iterable[int] | None = None,
):
    """Index exact directed edge signatures by owning state."""
    candidates = range(len(states)) if allowed is None else tuple(allowed)
    index = defaultdict(list)
    for state_index in candidates:
        kind, neighbors = states[state_index]
        for relative, neighbor_kind, contacts in neighbors:
            index[(kind, relative, neighbor_kind, contacts)].append(state_index)
    return {signature: tuple(indices) for signature, indices in index.items()}


def _pair_agrees(
    states: Sequence[ColoredCorona], left_index: int, right_index: int,
    left_to_right: Pose, right_to_left: Pose,
) -> bool:
    """Whether two assigned neighbor states agree on their shared edge."""
    left_kind, left_neighbors = states[left_index]
    right_kind, right_neighbors = states[right_index]
    left = [entry for entry in left_neighbors if entry[0] == left_to_right]
    right = [entry for entry in right_neighbors if entry[0] == right_to_left]
    if bool(left) != bool(right):
        return False
    if not left:
        return True
    if len(left) != 1 or len(right) != 1:
        return False
    return (
        left[0][1] in (ANY_KIND, right_kind)
        and right[0][1] in (ANY_KIND, left_kind)
        and left[0][2]
        == tuple(sorted(map(reciprocal_color, right[0][2])))
    )


def colored_states_agree_at_relative(
    states: Sequence[ColoredCorona], left_index: int, right_index: int,
    left_to_right: Pose,
) -> bool:
    """Exact two-state agreement at a prescribed relative anchor pose."""
    return _pair_agrees(
        states, left_index, right_index,
        left_to_right, inverse_pose(left_to_right),
    )


def colored_local_overlap_witnesses(
    states: Sequence[ColoredCorona], state_index: int, limit: int = 2,
    allowed: Iterable[int] | None = None,
    edge_index=None,
):
    """Assign all six neighboring states with exact overlap agreement.

    Besides reversing the center interface, assigned neighbors must agree on
    whether each pair is adjacent and, when it is, on parent type and every
    oriented physical child-edge contact.  This is the complete constraint
    visible in a colored radius-one parent-corona star.
    """
    if limit < 1:
        raise ValueError("limit must be positive")
    neighbors = states[state_index][1]
    domains = colored_reciprocal_domains(
        states, state_index, allowed=allowed, edge_index=edge_index,
    )
    if any(not domain for domain in domains):
        return ()
    compatibility = {}
    for left in range(len(neighbors)):
        for right in range(left):
            lr = relative_pose(neighbors[left][0], neighbors[right][0])
            rl = relative_pose(neighbors[right][0], neighbors[left][0])
            compatibility[left, right] = {
                (a, b)
                for a in domains[left]
                for b in domains[right]
                if _pair_agrees(states, a, b, lr, rl)
            }

    order = tuple(sorted(range(len(neighbors)), key=lambda i: len(domains[i])))
    assignment = {}
    witnesses = []

    def search(depth):
        if len(witnesses) >= limit:
            return
        if depth == len(order):
            witnesses.append(tuple(
                assignment[index] for index in range(len(neighbors))
            ))
            return
        current = order[depth]
        for candidate in domains[current]:
            if all(
                (
                    (candidate, selected)
                    if current > other else (selected, candidate)
                ) in compatibility[
                    (current, other) if current > other else (other, current)
                ]
                for other, selected in assignment.items()
            ):
                assignment[current] = candidate
                search(depth + 1)
                del assignment[current]

    search(0)
    return tuple(witnesses)


def minimum_colored_neighbor_cost(
    states: Sequence[ColoredCorona], state_index: int,
    costs: Mapping[int, int], allowed: Iterable[int] | None = None,
):
    """Minimum additive neighbor cost over exact colored star witnesses."""
    neighbors = states[state_index][1]
    edge_index = colored_edge_index(states, allowed=allowed)
    domains = colored_reciprocal_domains(
        states, state_index, allowed=allowed, edge_index=edge_index,
    )
    if any(not domain for domain in domains):
        return None, None
    compatibility = {}
    for left in range(len(neighbors)):
        for right in range(left):
            lr = relative_pose(neighbors[left][0], neighbors[right][0])
            rl = relative_pose(neighbors[right][0], neighbors[left][0])
            compatibility[left, right] = {
                (a, b)
                for a in domains[left]
                for b in domains[right]
                if _pair_agrees(states, a, b, lr, rl)
            }
    order = tuple(sorted(
        range(len(neighbors)),
        key=lambda index: (
            min(costs.get(candidate, 0) for candidate in domains[index]),
            len(domains[index]),
        ),
    ))
    assignment = {}
    best_cost = None
    best_witness = None

    def search(depth, cost):
        nonlocal best_cost, best_witness
        if best_cost is not None and cost >= best_cost:
            return
        if depth == len(order):
            best_cost = cost
            best_witness = tuple(
                assignment[index] for index in range(len(neighbors))
            )
            return
        current = order[depth]
        for candidate in sorted(
            domains[current], key=lambda index: costs.get(index, 0),
        ):
            if all(
                (
                    (candidate, selected)
                    if current > other else (selected, candidate)
                ) in compatibility[
                    (current, other) if current > other else (other, current)
                ]
                for other, selected in assignment.items()
            ):
                assignment[current] = candidate
                search(depth + 1, cost + costs.get(candidate, 0))
                del assignment[current]

    search(0, 0)
    return best_cost, best_witness


def prune_colored_unsupported(states: Sequence[ColoredCorona]):
    """Delete states without a colored local star, to an exact fixed point."""
    alive = set(range(len(states)))
    rounds = []
    while True:
        edge_index = colored_edge_index(states, allowed=alive)
        removed = tuple(
            index for index in sorted(alive)
            if not colored_local_overlap_witnesses(
                states, index, limit=1, allowed=alive,
                edge_index=edge_index,
            )
        )
        if not removed:
            break
        alive.difference_update(removed)
        rounds.append(removed)
    return tuple(sorted(alive)), tuple(rounds)


def colored_transition_graph(
    states: Sequence[ColoredCorona], allowed: Iterable[int] | None = None,
):
    """Directed state graph induced by exact reciprocal edge domains."""
    alive = set(range(len(states))) if allowed is None else set(allowed)
    edge_index = colored_edge_index(states, allowed=alive)
    return tuple(
        tuple(sorted({
            neighbor
            for domain in colored_reciprocal_domains(
                states, index, allowed=alive, edge_index=edge_index,
            )
            for neighbor in domain
        })) if index in alive else ()
        for index in range(len(states))
    )


def strongly_connected_components(adjacency, allowed=None):
    """Deterministic Tarjan decomposition of a finite directed graph."""
    vertices = (
        set(range(len(adjacency))) if allowed is None else set(allowed)
    )
    counter = 0
    indices = {}
    low = {}
    stack = []
    on_stack = set()
    components = []

    def visit(vertex):
        nonlocal counter
        indices[vertex] = low[vertex] = counter
        counter += 1
        stack.append(vertex)
        on_stack.add(vertex)
        for neighbor in adjacency[vertex]:
            if neighbor not in vertices:
                continue
            if neighbor not in indices:
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
            elif neighbor in on_stack:
                low[vertex] = min(low[vertex], indices[neighbor])
        if low[vertex] == indices[vertex]:
            component = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == vertex:
                    break
            components.append(tuple(sorted(component)))

    for vertex in sorted(vertices):
        if vertex not in indices:
            visit(vertex)
    return tuple(sorted(components, key=lambda component: component[0]))


def colored_edges_are_reciprocal(
    center: Pose, state: ColoredCorona,
    neighbor_states: Mapping[Pose, ColoredCorona],
) -> bool:
    """Check exact type/contact reversal against supplied neighbor states."""
    center_kind, neighbors = state
    for relative, neighbor_kind, contacts in neighbors:
        neighbor = compose_pose(center, relative)
        other = neighbor_states.get(neighbor)
        if other is None or other[0] != neighbor_kind:
            return False
        back = relative_pose(neighbor, center)
        matches = [entry for entry in other[1] if entry[0] == back]
        if len(matches) != 1 or matches[0][1] != center_kind:
            return False
        if tuple(sorted(map(reciprocal_color, contacts))) != matches[0][2]:
            return False
    return True
