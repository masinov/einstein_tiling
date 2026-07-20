"""Local V4 states for packing-density marking and discharging searches."""

from __future__ import annotations

from collections import defaultdict, deque
import itertools

from einstein.funnel.a1_torus import lattice_to_cell
from einstein.theory.a4_semidirect import c3_action, canonical_a4_semidirect
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.theory.a4_v4_packing_family import PACKING_COLLISION_SEED
from einstein.theory.a4_v4_sft import _signed_coordinate
from einstein.theory.holonomy import kite_edge_letter
from einstein.theory.holonomy_csp import (
    _placement_boundary,
    _point_type,
    quotient_boundary_data,
)


def equation_relative_patterns(system):
    """Per-placement quotient-vertex colors, normalized to one vertex."""
    patterns = []
    for equations in system.equations:
        graph = defaultdict(list)
        for left, right, value in equations:
            graph[left].append((right, value))
            graph[right].append((left, value))
        reference = min(graph)
        values = {reference: 0}
        queue = deque([reference])
        while queue:
            left = queue.popleft()
            for right, value in graph[left]:
                candidate = values[left] ^ value
                if right in values:
                    if values[right] != candidate:
                        raise AssertionError("placement equation pattern is inconsistent")
                else:
                    values[right] = candidate
                    queue.append(right)
        if len(values) != len(graph):
            raise AssertionError("placement boundary equation graph is disconnected")
        patterns.append(values)
    return tuple(patterns)


def lifted_state_conflict_graph(shape, system):
    """Conflict graph on explicit ``(placement, V4 gauge)`` states.

    Pairwise independence is equivalent to a globally shared potential on the
    selected boundary union, because every state assigns explicit values to
    all vertices of its placement boundary.
    """
    patterns = equation_relative_patterns(system)
    nodes = tuple(
        (placement_variable, gauge)
        for placement_variable in range(1, len(system.placements) + 1)
        for gauge in range(4)
    )
    node_index = {node: index for index, node in enumerate(nodes)}
    edges = set()
    for placement in range(1, len(system.placements) + 1):
        gauges = [node_index[(placement, gauge)] for gauge in range(4)]
        edges.update(itertools.combinations(gauges, 2))

    instance, _, _ = quotient_boundary_data(shape, system.hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing = {
        tuple(sorted(-literal for literal in clause))
        for clause in collision_orbit_clauses(shape, system.hnf, instance, target)
    }
    for left in range(1, len(system.placements) + 1):
        left_pattern = patterns[left - 1]
        for right in range(left + 1, len(system.placements) + 1):
            right_pattern = patterns[right - 1]
            shared = left_pattern.keys() & right_pattern.keys()
            packing_forbidden = (left, right) in packing
            if not shared and not packing_forbidden:
                continue
            for left_gauge in range(4):
                for right_gauge in range(4):
                    incompatible = any(
                        (left_pattern[vertex] ^ left_gauge)
                        != (right_pattern[vertex] ^ right_gauge)
                        for vertex in shared
                    )
                    if incompatible or packing_forbidden:
                        edges.add(tuple(sorted((
                            node_index[(left, left_gauge)],
                            node_index[(right, right_gauge)],
                        ))))
    return nodes, tuple(sorted(edges))


def relative_boundary_pattern(shape, operation, images):
    """Boundary V4 values normalized at a translation-covariant vertex."""
    model = canonical_a4_semidirect()
    c3_values = tuple(model.coordinate(element).q for element in images)
    geometric = (1, 2, 1, 0, 0, 0)
    if c3_values == geometric:
        sign = 1
    elif c3_values == tuple((-value) % 3 for value in geometric):
        sign = -1
    else:
        raise ValueError("non-geometric signature")
    graph = defaultdict(list)
    for edge in _placement_boundary(shape, (operation, 0, 0)):
        start, end = sorted(edge)
        letter = kite_edge_letter(start, end)
        label = _signed_coordinate(letter, images)
        constant = c3_action((sign * _point_type(start)[0]) % 3, label.v)
        graph[start].append((end, constant))
        graph[end].append((start, constant))
    reference = min(graph)
    values = {reference: 0}
    queue = deque([reference])
    while queue:
        start = queue.popleft()
        for end, constant in graph[start]:
            value = values[start] ^ constant
            if end in values:
                if values[end] != value:
                    raise AssertionError("one placement has inconsistent V4 boundary")
            else:
                values[end] = value
                queue.append(end)
    return values


def boundary_patterns(shape, images):
    return tuple(
        relative_boundary_pattern(shape, operation, images)
        for operation in range(12)
    )


def translated_pattern(pattern, anchor, gauge):
    tx, ty, _ = lattice_to_cell((anchor[0], anchor[1], 0))
    return {(x + tx, y + ty): value ^ gauge
            for (x, y), value in pattern.items()}


def state_placements_compatible(patterns, left, right):
    """Pairwise consistency of two explicit oriented/gauged tile states."""
    left_operation, left_gauge, left_u, left_v = left
    right_operation, right_gauge, right_u, right_v = right
    left_values = translated_pattern(
        patterns[left_operation], (left_u, left_v), left_gauge
    )
    right_values = translated_pattern(
        patterns[right_operation], (right_u, right_v), right_gauge
    )
    return all(
        left_values[vertex] == right_values[vertex]
        for vertex in left_values.keys() & right_values.keys()
    )


def resource_offsets(radius):
    """Hexagonal center offsets of axial radius ``radius``."""
    return tuple(
        (u, v)
        for u in range(-radius, radius + 1)
        for v in range(-radius, radius + 1)
        if max(abs(u), abs(v), abs(u + v)) <= radius
    )


def resource_incidence_conflict_graph(shape, images, radius):
    """Conflict graph for tiles sending charge to one center.

    A vertex ``(operation, gauge, resource_u, resource_v)`` represents a tile
    anchored at the negative resource offset, so that the distinguished
    resource is the origin.  Independent sets are exactly locally coexistent
    explicit V4 states that avoid the T2.D6 packing collision.
    """
    patterns = boundary_patterns(shape, tuple(images))
    offsets = resource_offsets(radius)
    vertices = tuple(
        (operation, gauge, u, v)
        for operation, gauge, (u, v) in itertools.product(
            range(12), range(4), offsets
        )
    )
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    state_cache = {}
    cell_cache = {}
    for operation, gauge, resource_u, resource_v in vertices:
        anchor = (-resource_u, -resource_v)
        state_cache[(operation, gauge, resource_u, resource_v)] = (
            operation, gauge, *anchor
        )
        cell_cache[(operation, resource_u, resource_v)] = placement_lattice_cells(
            shape, (operation, *anchor)
        )
    edges = []
    for left_index, right_index in itertools.combinations(range(len(vertices)), 2):
        left = vertices[left_index]
        right = vertices[right_index]
        compatible = state_placements_compatible(
            patterns, state_cache[left], state_cache[right]
        )
        left_cells = cell_cache[(left[0], left[2], left[3])]
        right_cells = cell_cache[(right[0], right[2], right[3])]
        packing_forbidden = (
            bool(left_cells & right_cells)
            and canonical_collision_type(left_cells, right_cells) == target
        )
        if not compatible or packing_forbidden:
            edges.append((left_index, right_index))
    return vertices, tuple(edges)


def enhanced_resource_incidence_conflict_graph(
    shape, images, radius, feature_point=None
):
    """Conflict graph with an optional extra local potential value in type.

    ``feature_point`` is relative to the tile anchor.  If it is already a
    boundary vertex its color is forced; otherwise its four possible V4
    values split the oriented/gauged tile type into four local states.
    """
    relative = boundary_patterns(shape, tuple(images))
    tile_types = []
    explicit_patterns = []
    for operation in range(12):
        for gauge in range(4):
            base = {
                point: value ^ gauge
                for point, value in relative[operation].items()
            }
            values = (
                (None,) if feature_point is None
                else ((base[feature_point],) if feature_point in base else range(4))
            )
            for feature_value in values:
                pattern = dict(base)
                if feature_point is not None:
                    pattern[feature_point] = feature_value
                tile_types.append((operation, gauge, feature_value))
                explicit_patterns.append(pattern)

    offsets = resource_offsets(radius)
    vertices = tuple(
        (type_index, u, v)
        for type_index in range(len(tile_types))
        for u, v in offsets
    )
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    translated = {}
    cell_cache = {}
    for type_index, resource_u, resource_v in vertices:
        operation = tile_types[type_index][0]
        anchor = (-resource_u, -resource_v)
        translated[(type_index, resource_u, resource_v)] = translated_pattern(
            explicit_patterns[type_index], anchor, 0
        )
        cell_cache[(operation, resource_u, resource_v)] = placement_lattice_cells(
            shape, (operation, *anchor)
        )
    edges = []
    for left_index, right_index in itertools.combinations(range(len(vertices)), 2):
        left = vertices[left_index]
        right = vertices[right_index]
        left_values = translated[left]
        right_values = translated[right]
        compatible = all(
            left_values[point] == right_values[point]
            for point in left_values.keys() & right_values.keys()
        )
        left_operation = tile_types[left[0]][0]
        right_operation = tile_types[right[0]][0]
        left_cells = cell_cache[(left_operation, left[1], left[2])]
        right_cells = cell_cache[(right_operation, right[1], right[2])]
        packing_forbidden = (
            bool(left_cells & right_cells)
            and canonical_collision_type(left_cells, right_cells) == target
        )
        if not compatible or packing_forbidden:
            edges.append((left_index, right_index))
    return tuple(tile_types), vertices, tuple(edges)
