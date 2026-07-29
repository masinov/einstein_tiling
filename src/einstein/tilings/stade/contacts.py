"""Exact labelled-stick contacts for Stade's weave construction.

The hexagon grid is represented in axial coordinates.  A length-n stick is
the cell row {(k, 0): 0 <= k < n}.  Sharing two rooted unit edges fixes the
orientation-preserving placement of the second stick uniquely.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass


Axial = tuple[int, int]

# Counterclockwise outward normals: E, NE, NW, W, SW, SE.
DIRECTIONS: tuple[Axial, ...] = (
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, 0),
    (-1, 1),
    (0, 1),
)

# Vertices of the Voronoi hexagon about an axial-lattice point, multiplied by
# three.  This is an exact affine model of a regular hexagon; affine maps
# preserve interior intersection.  The independent polygonal contact check
# below therefore needs integer arithmetic only.
HEX_VERTICES3: tuple[Axial, ...] = (
    (2, -1),
    (1, 1),
    (-1, 2),
    (-2, 1),
    (-1, -1),
    (1, -2),
)


@dataclass(frozen=True, order=True)
class Port:
    label: str
    cell: int
    direction: int


def add(left: Axial, right: Axial) -> Axial:
    return left[0] + right[0], left[1] + right[1]


def scale(factor: int, vector: Axial) -> Axial:
    return factor * vector[0], factor * vector[1]


def rotate(vector: Axial, steps: int) -> Axial:
    """Rotate an axial vector counterclockwise by steps*pi/3."""

    q, r = vector
    for _ in range(steps % 6):
        q, r = q + r, -q
    return q, r


def stick_ports(n: int) -> tuple[Port, ...]:
    """Return the source-labelled ports in counterclockwise boundary order."""

    if n < 2:
        raise ValueError("the labelled stick requires n >= 2")
    ports: list[Port] = [Port("y1", n - 1, 0), Port("z1", n - 1, 1)]
    for index in range(1, n):
        ports.append(Port(f"a{index}", n - index, 2))
        ports.append(Port(f"b{index}", n - 1 - index, 1))
    ports.extend((Port("x2", 0, 2), Port("y2", 0, 3), Port("z2", 0, 4)))
    for index in range(1, n):
        ports.append(Port(f"c{index}", index - 1, 5))
        ports.append(Port(f"d{index}", index, 4))
    ports.append(Port("x1", n - 1, 5))
    assert len(ports) == 4 * n + 2
    assert len({port.label for port in ports}) == len(ports)
    return tuple(ports)


def placed_second_cells(n: int, first: Port, second: Port) -> frozenset[Axial]:
    """Place second's complete port against first's complete port."""

    first_cell = (first.cell, 0)
    base = add(first_cell, DIRECTIONS[first.direction])
    rotation = (first.direction + 3 - second.direction) % 6
    chain_step = rotate((1, 0), rotation)
    return frozenset(
        add(base, scale(index - second.cell, chain_step)) for index in range(n)
    )


def shared_edge_is_exact(first: Port, second: Port, second_cells: frozenset[Axial]) -> bool:
    """Check the two incident cells occupy opposite sides of first's edge."""

    first_cell = (first.cell, 0)
    across = add(first_cell, DIRECTIONS[first.direction])
    if across not in second_cells:
        return False
    rotation = (first.direction + 3 - second.direction) % 6
    return (second.direction + rotation) % 6 == (first.direction + 3) % 6


def physical_contact(n: int, first: Port, second: Port) -> bool:
    """Whether the unique full-edge placement has disjoint stick interiors."""

    second_cells = placed_second_cells(n, first, second)
    if not shared_edge_is_exact(first, second, second_cells):
        raise AssertionError("port placement failed to identify the shared edge")
    first_cells = frozenset((index, 0) for index in range(n))
    return first_cells.isdisjoint(second_cells)


def _hex_polygon3(cell: Axial) -> tuple[Axial, ...]:
    center = scale(3, cell)
    return tuple(add(center, vertex) for vertex in HEX_VERTICES3)


def _strict_convex_overlap(left: tuple[Axial, ...], right: tuple[Axial, ...]) -> bool:
    """Exact separating-axis test for overlap of convex polygon interiors."""

    for polygon in (left, right):
        for start, end in zip(polygon, polygon[1:] + polygon[:1]):
            edge = end[0] - start[0], end[1] - start[1]
            normal = -edge[1], edge[0]
            left_projection = [point[0] * normal[0] + point[1] * normal[1] for point in left]
            right_projection = [
                point[0] * normal[0] + point[1] * normal[1] for point in right
            ]
            if max(left_projection) <= min(right_projection):
                return False
            if max(right_projection) <= min(left_projection):
                return False
    return True


def polygonal_physical_contact(n: int, first: Port, second: Port) -> bool:
    """Independently test contact by exact convex-polygon intersections."""

    first_polygons = [_hex_polygon3((index, 0)) for index in range(n)]
    second_polygons = [
        _hex_polygon3(cell) for cell in placed_second_cells(n, first, second)
    ]
    return not any(
        _strict_convex_overlap(left, right)
        for left in first_polygons
        for right in second_polygons
    )


def _kind(label: str) -> str:
    return label[0]


def _index(label: str) -> int:
    return int(label[1:])


def fixed_forbidden(n: int, left: str, right: str) -> bool:
    """Stade's fixed rules 1--11, treated as unordered edge pairs."""

    a, b = sorted((left, right))
    ka, kb = _kind(a), _kind(b)
    kinds = {ka, kb}

    if ka == kb == "y":  # Rule 1.
        return True
    if ka == kb and ka in {"x", "z"}:  # Rule 2.
        return True
    if kinds == {"x", "y"}:  # Rule 3.
        return True
    if kinds == {"x", "z"}:  # Rule 4.
        return True
    if "y" in kinds:  # Rules 5, 10, 11.
        other = b if ka == "y" else a
        if other in {"a1", "c1", "z2", f"d{n - 1}"}:
            return True
    if "x1" in {left, right}:
        other = right if left == "x1" else left
        if _kind(other) == "c" and 1 <= _index(other) <= n - 1:  # Rule 6.
            return True
    if "z2" in {left, right}:
        other = right if left == "z2" else left
        if _kind(other) == "d" and 1 <= _index(other) <= n - 2:  # Rule 7.
            return True
    if "x2" in {left, right}:
        other = right if left == "x2" else left
        if _kind(other) == "a" and 1 <= _index(other) <= n - 1:  # Rule 8.
            return True
    if "z1" in {left, right}:
        other = right if left == "z1" else left
        if _kind(other) == "b" and 1 <= _index(other) <= n - 1:  # Rule 9.
            return True
    return False


def _node(side: str, label: str) -> str:
    return f"{side}:{label}"


def _split_node(node: str) -> tuple[str, str]:
    side, label = node.split(":", 1)
    return side, label


def _shortest_path(adjacency: dict[str, set[str]], start: str, end: str) -> list[str]:
    queue = deque([start])
    parent: dict[str, str | None] = {start: None}
    while queue:
        current = queue.popleft()
        if current == end:
            break
        for neighbor in sorted(adjacency[current]):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.append(neighbor)
    if end not in parent:
        raise ValueError("nodes are in different allowed-contact components")
    path = []
    current: str | None = end
    while current is not None:
        path.append(current)
        current = parent[current]
    return list(reversed(path))


def analyze_length(n: int) -> dict:
    ports = stick_ports(n)
    labels = [port.label for port in ports]
    by_label = {port.label: port for port in ports}
    physical: set[tuple[str, str]] = set()
    allowed: set[tuple[str, str]] = set()
    forbidden: set[tuple[str, str]] = set()

    for left in labels:
        for right in labels:
            pair = (left, right)
            if physical_contact(n, by_label[left], by_label[right]):
                physical.add(pair)
                (forbidden if fixed_forbidden(n, left, right) else allowed).add(pair)

    adjacency = {_node(side, label): set() for side in ("L", "R") for label in labels}
    for left, right in allowed:
        lnode, rnode = _node("L", left), _node("R", right)
        adjacency[lnode].add(rnode)
        adjacency[rnode].add(lnode)

    component_id: dict[str, int] = {}
    components: list[dict] = []
    for start in sorted(adjacency):
        if start in component_id or not adjacency[start]:
            continue
        cid = len(components)
        queue = deque([start])
        component_id[start] = cid
        nodes: list[str] = []
        while queue:
            current = queue.popleft()
            nodes.append(current)
            for neighbor in sorted(adjacency[current]):
                if neighbor not in component_id:
                    component_id[neighbor] = cid
                    queue.append(neighbor)
        lefts = sorted(_split_node(node)[1] for node in nodes if node.startswith("L:"))
        rights = sorted(_split_node(node)[1] for node in nodes if node.startswith("R:"))
        components.append({"left": lefts, "right": rights})

    hits: list[dict] = []
    for left, right in sorted(forbidden):
        lnode, rnode = _node("L", left), _node("R", right)
        if component_id.get(lnode) == component_id.get(rnode) and lnode in component_id:
            hits.append(
                {
                    "left": left,
                    "right": right,
                    "component": component_id[lnode],
                    "allowed_path": _shortest_path(adjacency, lnode, rnode),
                }
            )

    n61s_pairs = (("z1", "a2"), ("a1", "a2"), ("a1", "b1"), ("z1", "b1"))
    n61s = [
        {
            "pair": list(pair),
            "physical": pair in physical,
            "fixed_allowed": not fixed_forbidden(n, *pair),
            "effective_allowed": pair in allowed,
        }
        for pair in n61s_pairs
    ]

    return {
        "n": n,
        "port_count": len(ports),
        "ports": [
            {"label": port.label, "cell": port.cell, "direction": port.direction}
            for port in ports
        ],
        "physical_pair_count": len(physical),
        "allowed_physical_pair_count": len(allowed),
        "forbidden_physical_pair_count": len(forbidden),
        "physical_pairs": [list(pair) for pair in sorted(physical)],
        "allowed_physical_pairs": [list(pair) for pair in sorted(allowed)],
        "components": components,
        "forced_forbidden_hits": hits,
        "separable_erasure_possible": not hits,
        "n61s_rectangle": n61s,
    }
