"""Exact normalized supports for the AHI Section 10.1 source system.

The source Illustrator figure is used only to transcribe a finite boundary
word.  Coordinates emitted by this module are integer coordinates in the
triangular-lattice basis

    e_u = direction 30 degrees,  e_v = direction 150 degrees.

All certificate checks after transcription are exact integer arithmetic.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import xml.etree.ElementTree as ET


SOURCE_ARCHIVE_SHA256 = (
    "de757bfc8e3fe174fc04dd19101f30e13dc6776d245f573ff9554f23a60bad28"
)
EXAMPLE1_SHA256 = (
    "88c0e3a3b0cc7dd8c773a69da79c1b8047789d80c34a71f42432edc6b7d2cb53"
)

# Six unit directions in cyclic order in the (u,v) basis.
DIRECTIONS = ((1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1))

# Long diagonals of two adjacent unit triangles, in the same cyclic screen
# direction order as DIRECTIONS.  These are the limiting supports of the
# bent SAB components in the source figure.
LONG_DIAGONALS = ((1, -1), (2, 1), (1, 2), (-1, 1), (-2, -1), (-1, -2))


@dataclass(frozen=True)
class RawOutline:
    points: tuple[tuple[Fraction, Fraction], ...]

    @property
    def edge_count(self) -> int:
        return len(self.points)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _fraction(token: str) -> Fraction:
    return Fraction(token)


def _first_closed_polyline(path_data: str) -> RawOutline:
    """Read the first absolute M/L subpath before Z from pdftocairo SVG."""

    prefix = path_data.split("Z", 1)[0]
    tokens = re.findall(
        r"[ML]|[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", prefix
    )
    points: list[tuple[Fraction, Fraction]] = []
    index = 0
    command = None
    while index < len(tokens):
        token = tokens[index]
        if token in {"M", "L"}:
            command = token
            index += 1
            continue
        if command not in {"M", "L"} or index + 1 >= len(tokens):
            raise ValueError(f"unsupported SVG path near token {index}")
        points.append((_fraction(tokens[index]), _fraction(tokens[index + 1])))
        index += 2
        command = "L"
    if len(points) < 4:
        raise ValueError("outline has fewer than four vertices")
    return RawOutline(tuple(points))


def extract_raw_outlines(svg_path: Path) -> dict[str, RawOutline]:
    root = ET.parse(svg_path).getroot()
    outlines: list[RawOutline] = []
    for element in root.iter():
        if not element.tag.endswith("path"):
            continue
        style = element.attrib.get("style", "")
        if "stroke-width:1;" not in style:
            continue
        if "stroke:rgb(0%,0%,0%)" not in style or "fill:none" not in style:
            continue
        outlines.append(_first_closed_polyline(element.attrib["d"]))

    by_edges = {outline.edge_count: outline for outline in outlines}
    if sorted(by_edges) != [4, 13, 14] or len(outlines) != 3:
        raise ValueError(
            f"expected exactly the 4/13/14-edge source outlines, got "
            f"{sorted(outline.edge_count for outline in outlines)}"
        )
    return {
        "large_A": by_edges[14],
        "large_B": by_edges[13],
        "small_M": by_edges[4],
    }


def _matrix(transform: str | None) -> tuple[Fraction, ...]:
    if transform is None:
        return (Fraction(1), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0))
    if not transform.startswith("matrix("):
        raise ValueError(f"unsupported SVG transform: {transform}")
    values = tuple(Fraction(token) for token in re.findall(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", transform
    ))
    if len(values) != 6:
        raise ValueError(f"malformed SVG matrix: {transform}")
    return values


def _matrix_product(first: tuple[Fraction, ...], second: tuple[Fraction, ...]):
    a, b, c, d, e, f = first
    g, h, i, j, k, ell = second
    return (
        a * g + c * h,
        b * g + d * h,
        a * i + c * j,
        b * i + d * j,
        a * k + c * ell + e,
        b * k + d * ell + f,
    )


def _transform_point(matrix: tuple[Fraction, ...], point):
    a, b, c, d, e, f = matrix
    x, y = point
    return (a * x + c * y + e, b * x + d * y + f)


def _polyline(path_data: str) -> tuple[tuple[Fraction, Fraction], ...]:
    tokens = re.findall(
        r"[MLZ]|[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?",
        path_data,
    )
    numbers = [Fraction(token) for token in tokens if token not in {"M", "L", "Z"}]
    if len(numbers) % 2:
        raise ValueError("odd coordinate count in SVG polyline")
    return tuple(zip(numbers[::2], numbers[1::2]))


def extract_sab_polylines(
    svg_path: Path,
) -> dict[str, tuple[tuple[tuple[Fraction, Fraction], ...], ...]]:
    """Resolve the pinned SVG uses and return the 31 magenta SAB paths."""

    root = ET.parse(svg_path).getroot()
    by_id = {element.attrib["id"]: element for element in root.iter() if "id" in element.attrib}
    surface = by_id.get("surface1")
    if surface is None:
        raise ValueError("source SVG has no surface1")
    xlink = "{http://www.w3.org/1999/xlink}href"

    def visit(element, parent_matrix):
        matrix = _matrix_product(parent_matrix, _matrix(element.attrib.get("transform")))
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "use":
            reference = element.attrib[xlink]
            yield from visit(by_id[reference[1:]], matrix)
            return
        if tag == "path":
            yield element, matrix
        for child in element:
            yield from visit(child, matrix)

    groups: dict[str, list] = {"large_A": [], "large_B": [], "small_M": []}
    for element, matrix in visit(surface, _matrix(None)):
        style = element.attrib.get("style", "")
        if "stroke-width:0.5;" not in style or "92.89856%" not in style:
            continue
        points = tuple(_transform_point(matrix, point) for point in _polyline(element.attrib["d"]))
        if len(points) != 4:
            raise ValueError("every source SAB component must have four vector vertices")
        x = points[0][0]
        if x < 150:
            groups["large_A"].append(points)
        elif x < 260:
            groups["large_B"].append(points)
        else:
            groups["small_M"].append(points)
    result = {name: tuple(paths) for name, paths in groups.items()}
    if {name: len(paths) for name, paths in result.items()} != {
        "large_A": 15,
        "large_B": 15,
        "small_M": 1,
    }:
        raise ValueError("source SAB path census differs from 15/15/1")
    return result


def _squared(vector: tuple[Fraction, Fraction]) -> Fraction:
    return vector[0] * vector[0] + vector[1] * vector[1]


def _direction_index(dx: Fraction, dy: Fraction) -> int:
    """Classify one Illustrator segment into the six exact source directions."""

    # Illustrator stores the source figure with rounded decimal coordinates.
    # The vertical and 30-degree direction classes are nevertheless separated
    # by a wide exact rational gap: dx^2 < dy^2 versus
    # 2*dy^2 < dx^2 < 4*dy^2.  We use only that separation here and never
    # propagate the rounded coordinates into the certificate.
    if dx * dx < dy * dy:
        return 1 if dy > 0 else 4
    if not 2 * dy * dy < dx * dx < 4 * dy * dy:
        raise ValueError(f"segment is not in a triangular direction: {(dx, dy)}")
    if dx > 0 and dy > 0:
        return 0
    if dx > 0 and dy < 0:
        return 5
    if dx < 0 and dy > 0:
        return 2
    if dx < 0 and dy < 0:
        return 3
    raise ValueError(f"zero or unclassified segment: {(dx, dy)}")


def normalized_steps(
    outlines: dict[str, RawOutline],
) -> dict[str, tuple[int, ...]]:
    segments: list[tuple[Fraction, Fraction]] = []
    for outline in outlines.values():
        points = outline.points
        for first, second in zip(points, points[1:] + points[:1]):
            segments.append((second[0] - first[0], second[1] - first[1]))
    minimum = min(_squared(segment) for segment in segments)

    result: dict[str, tuple[int, ...]] = {}
    for name, outline in outlines.items():
        word: list[int] = []
        points = outline.points
        for first, second in zip(points, points[1:] + points[:1]):
            vector = (second[0] - first[0], second[1] - first[1])
            length2 = _squared(vector)
            if length2 < 3 * minimum:
                multiplicity = 1  # physical lengths 1 and sqrt(2)
            elif 4 * minimum < length2 < 7 * minimum:
                multiplicity = 2  # one collinear 1 + sqrt(2) maximal segment
            else:
                raise ValueError(
                    f"unrecognized source edge-length class {length2 / minimum}"
                )
            word.extend([_direction_index(*vector)] * multiplicity)
        result[name] = tuple(word)
    return result


def boundary_vertices(word: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    vertices = [(0, 0)]
    for index in word:
        du, dv = DIRECTIONS[index]
        vertices.append((vertices[-1][0] + du, vertices[-1][1] + dv))
    if vertices[-1] != (0, 0):
        raise ValueError(f"boundary does not close: {vertices[-1]}")
    if len(set(vertices[:-1])) != len(vertices) - 1:
        raise ValueError("boundary repeats a vertex")
    return tuple(vertices[:-1])


def doubled_uv_area(vertices: tuple[tuple[int, int], ...]) -> int:
    total = 0
    for first, second in zip(vertices, vertices[1:] + vertices[:1]):
        total += first[0] * second[1] - first[1] * second[0]
    return total


def _cross(
    first: tuple[int, int],
    second: tuple[int, int],
    point3: tuple[int, int],
) -> int:
    # Polygon vertices are scaled by three; point3 already is.
    x1, y1 = 3 * first[0], 3 * first[1]
    x2, y2 = 3 * second[0], 3 * second[1]
    x, y = point3
    return (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)


def _inside(vertices: tuple[tuple[int, int], ...], point3: tuple[int, int]) -> bool:
    winding = 0
    x, y = point3
    for first, second in zip(vertices, vertices[1:] + vertices[:1]):
        y1, y2 = 3 * first[1], 3 * second[1]
        side = _cross(first, second, point3)
        if y1 <= y < y2 and side > 0:
            winding += 1
        elif y2 <= y < y1 and side < 0:
            winding -= 1
    return winding != 0


def triangle_cells(
    vertices: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, int, str], ...]:
    min_u = min(point[0] for point in vertices) - 1
    max_u = max(point[0] for point in vertices) + 1
    min_v = min(point[1] for point in vertices) - 1
    max_v = max(point[1] for point in vertices) + 1
    cells: list[tuple[int, int, str]] = []
    for u in range(min_u, max_u + 1):
        for v in range(min_v, max_v + 1):
            if _inside(vertices, (3 * u + 2, 3 * v + 1)):
                cells.append((u, v, "U"))
            if _inside(vertices, (3 * u + 1, 3 * v + 2)):
                cells.append((u, v, "D"))
    return tuple(sorted(cells))


def _triangle_vertices(cell: tuple[int, int, str]) -> tuple[tuple[int, int], ...]:
    u, v, orientation = cell
    if orientation == "U":
        return ((u, v), (u + 1, v), (u + 1, v + 1))
    if orientation == "D":
        return ((u, v), (u, v + 1), (u + 1, v + 1))
    raise ValueError(f"unknown orientation {orientation}")


def _edge(first: tuple[int, int], second: tuple[int, int]):
    return tuple(sorted((first, second)))


def _sab_role(path: tuple[tuple[Fraction, Fraction], ...]) -> str:
    dx = path[-1][0] - path[0][0]
    dy = path[-1][1] - path[0][1]
    length2 = dx * dx + dy * dy
    if length2 < 750:
        return "S"
    if length2 < 1100:
        return "M"
    return "L"


def _sab_corridor_bits(
    path: tuple[tuple[Fraction, Fraction], ...]
) -> tuple[int, int]:
    """Recover the ordered transverse narrow/wide state of one source SAB."""

    role = _sab_role(path)
    if role == "S":
        return (0, 0)
    if role == "L":
        return (1, 1)
    directions = tuple(
        _sab_screen_direction(
            path[index + 1][0] - path[index][0],
            path[index + 1][1] - path[index][1],
        )
        for index in range(3)
    )
    if directions[0] != directions[2]:
        raise ValueError("an M SAB has unequal endpoint-arm directions")
    turn = (directions[1] - directions[0]) % 6
    if turn == 1:
        return (0, 1)
    if turn == 5:
        return (1, 0)
    raise ValueError("an M SAB does not have one signed 60-degree bend")


def _sab_screen_direction(dx: Fraction, dy: Fraction) -> int:
    # The limiting directions are multiples of 60 degrees.  The finite-kappa
    # bent M paths deviate by less than 30 degrees; this exact cone test
    # assigns them to the same limiting class without using floats.
    if 3 * dy * dy < dx * dx:
        return 0 if dx > 0 else 3
    if dx > 0 and dy > 0:
        return 1
    if dx < 0 and dy > 0:
        return 2
    if dx < 0 and dy < 0:
        return 4
    if dx > 0 and dy < 0:
        return 5
    raise ValueError("degenerate SAB endpoint direction")


def _source_sab_graph(paths):
    """Collapse the bounded bends and recover the limiting directed graph."""

    points = [point for path in paths for point in path]
    parent = list(range(len(points)))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(first, second):
        first, second = find(first), find(second)
        if first != second:
            parent[second] = first

    for first in range(len(points)):
        for second in range(first):
            dx = points[first][0] - points[second][0]
            dy = points[first][1] - points[second][1]
            if dx * dx + dy * dy < 25:
                union(first, second)

    components: dict[int, list[int]] = {}
    for index in range(len(points)):
        components.setdefault(find(index), []).append(index)
    ordered = sorted(components.values(), key=lambda group: min(group))
    vertex_of = {index: vertex for vertex, group in enumerate(ordered) for index in group}
    centers = [
        (
            sum(points[index][0] for index in group) / len(group),
            sum(points[index][1] for index in group) / len(group),
        )
        for group in ordered
    ]

    edges = []
    roles = []
    for index, path in enumerate(paths):
        start = vertex_of[4 * index]
        end = vertex_of[4 * index + 3]
        if vertex_of[4 * index + 1] != start or vertex_of[4 * index + 2] != end:
            raise ValueError("a SAB bend does not collapse at its two endpoints")
        edges.append((start, end))
        roles.append(_sab_role(path))
    if len(set(edges)) != len(edges):
        raise ValueError("source SAB graph contains a duplicate component")

    adjacency = {index: [] for index in range(len(centers))}
    for first, second in edges:
        dx = centers[second][0] - centers[first][0]
        dy = centers[second][1] - centers[first][1]
        direction = _sab_screen_direction(dx, dy)
        step = DIRECTIONS[direction]
        adjacency[first].append((second, step))
        adjacency[second].append((first, (-step[0], -step[1])))
    graph_points = {0: (0, 0)}
    queue = deque([0])
    while queue:
        first = queue.popleft()
        for second, step in adjacency[first]:
            point = (
                graph_points[first][0] + step[0],
                graph_points[first][1] + step[1],
            )
            if second in graph_points and graph_points[second] != point:
                raise ValueError("limiting SAB directions have nonzero graph holonomy")
            if second not in graph_points:
                graph_points[second] = point
                queue.append(second)
    if len(graph_points) != len(centers):
        raise ValueError("source SAB graph is disconnected")
    return tuple(graph_points[index] for index in range(len(centers))), tuple(edges), tuple(roles)


def _linear_isometry(point, rotation: int, reflected: bool):
    direction = lambda index: (rotation - index) % 6 if reflected else (index + rotation) % 6
    image_u = DIRECTIONS[direction(0)]
    image_v = DIRECTIONS[direction(2)]
    u, v = point
    return (
        u * image_u[0] + v * image_v[0],
        u * image_u[1] + v * image_v[1],
    )


def _support_automorphisms(cells):
    triangles = {frozenset(_triangle_vertices(cell)) for cell in cells}
    vertices = set().union(*(set(triangle) for triangle in triangles))
    anchor = min(vertices)
    result = []
    for reflected in (False, True):
        for rotation in range(6):
            image_anchor = _linear_isometry(anchor, rotation, reflected)
            for target in vertices:
                translation = (
                    target[0] - image_anchor[0],
                    target[1] - image_anchor[1],
                )
                mapped = {
                    frozenset(
                        (
                            _linear_isometry(point, rotation, reflected)[0] + translation[0],
                            _linear_isometry(point, rotation, reflected)[1] + translation[1],
                        )
                        for point in triangle
                    )
                    for triangle in triangles
                }
                if mapped == triangles:
                    item = (reflected, rotation, translation)
                    if item not in result:
                        result.append(item)
    return tuple(result)


def _sab_embeddings(paths, cells):
    graph_points, graph_edges, roles = _source_sab_graph(paths)
    owners: dict[tuple, list] = {}
    for cell in cells:
        triangle = _triangle_vertices(cell)
        for first, second in zip(triangle, triangle[1:] + triangle[:1]):
            owners.setdefault(_edge(first, second), []).append(cell)
    diagonals = {}
    for shared, incident in owners.items():
        if len(incident) != 2:
            continue
        vertices = set(_triangle_vertices(incident[0])) | set(_triangle_vertices(incident[1]))
        diagonal = _edge(*(vertices - set(shared)))
        diagonals[diagonal] = tuple(sorted(incident))
    support_vertices = set().union(*(
        set(_triangle_vertices(cell)) for cell in cells
    ))

    labelled_solutions = set()
    for reflected in (False, True):
        for rotation in range(6):
            adjacency = {index: [] for index in range(len(graph_points))}
            for first, second in graph_edges:
                delta = (
                    graph_points[second][0] - graph_points[first][0],
                    graph_points[second][1] - graph_points[first][1],
                )
                screen_direction = DIRECTIONS.index(delta)
                direction = (
                    (rotation - screen_direction) % 6
                    if reflected
                    else (screen_direction + rotation) % 6
                )
                step = LONG_DIAGONALS[direction]
                adjacency[first].append((second, step))
                adjacency[second].append((first, (-step[0], -step[1])))
            embedded = {0: (0, 0)}
            queue = deque([0])
            consistent = True
            while queue and consistent:
                first = queue.popleft()
                for second, step in adjacency[first]:
                    point = (
                        embedded[first][0] + step[0],
                        embedded[first][1] + step[1],
                    )
                    if second in embedded and embedded[second] != point:
                        consistent = False
                        break
                    if second not in embedded:
                        embedded[second] = point
                        queue.append(second)
            if not consistent:
                continue
            points = tuple(embedded[index] for index in range(len(graph_points)))
            for target in support_vertices:
                translation = (target[0] - points[0][0], target[1] - points[0][1])
                placed = tuple((u + translation[0], v + translation[1]) for u, v in points)
                selected = tuple(_edge(placed[first], placed[second]) for first, second in graph_edges)
                if len(set(selected)) != len(graph_edges):
                    continue
                if any(diagonal not in diagonals for diagonal in selected):
                    continue
                covered = [cell for diagonal in selected for cell in diagonals[diagonal]]
                if len(covered) != len(cells) or len(set(covered)) != len(cells):
                    continue
                labelled_solutions.add(frozenset(zip(roles, selected)))

    if not labelled_solutions:
        raise ValueError("source SAB graph has no exact support embedding")
    automorphisms = _support_automorphisms(cells)
    first_solution = next(iter(labelled_solutions))
    orbit = set()
    for reflected, rotation, translation in automorphisms:
        mapped = frozenset(
            (
                role,
                _edge(
                    (
                        _linear_isometry(edge[0], rotation, reflected)[0] + translation[0],
                        _linear_isometry(edge[0], rotation, reflected)[1] + translation[1],
                    ),
                    (
                        _linear_isometry(edge[1], rotation, reflected)[0] + translation[0],
                        _linear_isometry(edge[1], rotation, reflected)[1] + translation[1],
                    ),
                ),
            )
            for role, edge in first_solution
        )
        if mapped in labelled_solutions:
            orbit.add(mapped)
    if orbit != labelled_solutions:
        raise ValueError("source SAB embeddings split into multiple support-isometry orbits")

    canonical = min(
        labelled_solutions,
        key=lambda solution: tuple(sorted((role, edge) for role, edge in solution)),
    )
    components = []
    for role, diagonal in sorted(canonical):
        components.append(
            {
                "role": role,
                "diagonal_uv": [list(diagonal[0]), list(diagonal[1])],
                "primitive_cells": [list(cell) for cell in diagonals[diagonal]],
            }
        )
    return components, len(labelled_solutions), len(automorphisms)


def verify_support(
    word: tuple[int, ...], cells: tuple[tuple[int, int, str], ...], expected: int
) -> None:
    vertices = boundary_vertices(word)
    if abs(doubled_uv_area(vertices)) != expected:
        raise ValueError("shoelace area does not match expected primitive-cell count")
    if len(cells) != expected:
        raise ValueError("enumerated cell count does not match expected count")

    edge_counts: Counter = Counter()
    for cell in cells:
        triangle = _triangle_vertices(cell)
        for first, second in zip(triangle, triangle[1:] + triangle[:1]):
            edge_counts[_edge(first, second)] += 1
    cell_boundary = {edge for edge, count in edge_counts.items() if count == 1}
    polygon_boundary = {
        _edge(first, second)
        for first, second in zip(vertices, vertices[1:] + vertices[:1])
    }
    if cell_boundary != polygon_boundary:
        raise ValueError("cell-union boundary differs from the polygon boundary")

    adjacency: dict[tuple[int, int, str], set] = {cell: set() for cell in cells}
    edge_owner: dict[tuple, tuple[int, int, str]] = {}
    for cell in cells:
        triangle = _triangle_vertices(cell)
        for first, second in zip(triangle, triangle[1:] + triangle[:1]):
            edge = _edge(first, second)
            other = edge_owner.get(edge)
            if other is None:
                edge_owner[edge] = cell
            else:
                adjacency[cell].add(other)
                adjacency[other].add(cell)
    seen = set()
    queue = deque([cells[0]])
    while queue:
        cell = queue.popleft()
        if cell in seen:
            continue
        seen.add(cell)
        queue.extend(adjacency[cell] - seen)
    if len(seen) != len(cells):
        raise ValueError("primitive-cell support is disconnected")


def build_atlas(archive_path: Path) -> dict:
    if sha256_path(archive_path) != SOURCE_ARCHIVE_SHA256:
        raise ValueError("source archive hash mismatch")
    with tempfile.TemporaryDirectory(prefix="ahi-source-") as directory:
        root = Path(directory)
        with tarfile.open(archive_path, "r:gz") as archive:
            member = archive.getmember("Example1.pdf")
            archive.extract(member, root, filter="data")
        pdf_path = root / "Example1.pdf"
        if sha256_path(pdf_path) != EXAMPLE1_SHA256:
            raise ValueError("Example1.pdf member hash mismatch")
        svg_path = root / "example1-page1.svg"
        subprocess.run(
            [
                "pdftocairo",
                "-svg",
                "-f",
                "1",
                "-l",
                "1",
                str(pdf_path),
                str(svg_path),
            ],
            check=True,
        )
        outlines = extract_raw_outlines(svg_path)
        words = normalized_steps(outlines)
        sab_paths = extract_sab_polylines(svg_path)

    expected = {"large_A": 30, "large_B": 30, "small_M": 2}
    supports = {}
    for name in ("large_A", "large_B", "small_M"):
        vertices = boundary_vertices(words[name])
        cells = triangle_cells(vertices)
        verify_support(words[name], cells, expected[name])
        if name == "small_M":
            first, second = cells
            shared = set(_triangle_vertices(first)) & set(_triangle_vertices(second))
            diagonal = _edge(*(
                (set(_triangle_vertices(first)) | set(_triangle_vertices(second))) - shared
            ))
            sab_components = [{
                "role": "M",
                "diagonal_uv": [list(diagonal[0]), list(diagonal[1])],
                "primitive_cells": [list(first), list(second)],
            }]
            embedding_count = 1
            automorphism_count = len(_support_automorphisms(cells))
        else:
            sab_components, embedding_count, automorphism_count = _sab_embeddings(
                sab_paths[name], cells
            )
        supports[name] = {
            "primitive_triangle_count": expected[name],
            "boundary_directions": list(words[name]),
            "boundary_vertices_uv": [list(point) for point in vertices],
            "cells": [[u, v, orientation] for u, v, orientation in cells],
            "sab_components": sab_components,
            "source_embedding_count": embedding_count,
            "support_automorphism_count": automorphism_count,
            "source_embeddings_one_support_isometry_orbit": True,
        }
    return {
        "schema": "ahi-sturmian-source-atlas-v2",
        "source": {
            "arxiv": "2506.19362v3",
            "archive_sha256": SOURCE_ARCHIVE_SHA256,
            "member": "Example1.pdf",
            "member_sha256": EXAMPLE1_SHA256,
            "figure": 37,
        },
        "basis": {
            "u": "unit direction 30 degrees",
            "v": "unit direction 150 degrees",
        },
        "common_cell": {
            "support": "60/120 rhombus formed by two unit equilateral triangles",
            "macro_address_counts": {"large_A": 15, "large_B": 15, "small_M": 1},
            "total_address_count": 31,
        },
        "supports": supports,
    }


def verify_atlas(data: dict) -> None:
    if data.get("schema") != "ahi-sturmian-source-atlas-v2":
        raise ValueError("unsupported atlas schema")
    source = data.get("source", {})
    if source.get("archive_sha256") != SOURCE_ARCHIVE_SHA256:
        raise ValueError("source archive hash is not pinned")
    if source.get("member_sha256") != EXAMPLE1_SHA256:
        raise ValueError("source member hash is not pinned")
    expected = {"large_A": 30, "large_B": 30, "small_M": 2}
    expected_components = {
        "large_A": {"S": 6, "M": 6, "L": 3},
        "large_B": {"S": 6, "M": 6, "L": 3},
        "small_M": {"M": 1},
    }
    # Counts are distinct role-labelled embeddings, before quotienting by the
    # support stabilizer.  In both large cases they form one isometry orbit.
    expected_embeddings = {"large_A": 2, "large_B": 2, "small_M": 1}
    common_cell = data.get("common_cell", {})
    if common_cell.get("macro_address_counts") != {
        "large_A": 15,
        "large_B": 15,
        "small_M": 1,
    } or common_cell.get("total_address_count") != 31:
        raise ValueError("common-rhombus address census mismatch")
    if set(data.get("supports", {})) != set(expected):
        raise ValueError("atlas support names differ from the fixed source set")
    for name, count in expected.items():
        support = data["supports"][name]
        word = tuple(support["boundary_directions"])
        cells = tuple((u, v, orientation) for u, v, orientation in support["cells"])
        verify_support(word, cells, count)
        if support["primitive_triangle_count"] != count:
            raise ValueError("declared primitive count mismatch")
        if [list(point) for point in boundary_vertices(word)] != support[
            "boundary_vertices_uv"
        ]:
            raise ValueError("serialized boundary vertices mismatch")
        diagonal_to_cells = {}
        owners: dict[tuple, list] = {}
        for cell in cells:
            triangle = _triangle_vertices(cell)
            for first, second in zip(triangle, triangle[1:] + triangle[:1]):
                owners.setdefault(_edge(first, second), []).append(cell)
        for shared, incident in owners.items():
            if len(incident) == 2:
                vertices = set(_triangle_vertices(incident[0])) | set(
                    _triangle_vertices(incident[1])
                )
                diagonal_to_cells[_edge(*(vertices - set(shared)))] = tuple(
                    sorted(incident)
                )
        covered = []
        roles = Counter()
        seen_diagonals = set()
        for component in support.get("sab_components", []):
            role = component["role"]
            if role not in {"S", "M", "L"}:
                raise ValueError("unknown SAB role")
            roles[role] += 1
            diagonal = _edge(*(
                tuple(tuple(point) for point in component["diagonal_uv"])
            ))
            if diagonal in seen_diagonals or diagonal not in diagonal_to_cells:
                raise ValueError("SAB component is duplicate or not a two-triangle diagonal")
            seen_diagonals.add(diagonal)
            declared = tuple(
                sorted((u, v, orientation) for u, v, orientation in component["primitive_cells"])
            )
            if declared != diagonal_to_cells[diagonal]:
                raise ValueError("SAB component primitive-cell incidence mismatch")
            covered.extend(declared)
        if roles != Counter(expected_components[name]):
            raise ValueError("SAB role census mismatch")
        if len(covered) != count or set(covered) != set(cells):
            raise ValueError("SAB components do not partition the primitive support")
        component_of = {
            cell: index
            for index, component in enumerate(support["sab_components"])
            for cell in (
                (u, v, orientation)
                for u, v, orientation in component["primitive_cells"]
            )
        }
        component_adjacency = {
            index: set() for index in range(len(support["sab_components"]))
        }
        edge_components: dict[tuple, set[int]] = {}
        for cell in cells:
            triangle = _triangle_vertices(cell)
            for first, second in zip(triangle, triangle[1:] + triangle[:1]):
                edge_components.setdefault(_edge(first, second), set()).add(
                    component_of[cell]
                )
        for incident in edge_components.values():
            if len(incident) == 2:
                first, second = incident
                component_adjacency[first].add(second)
                component_adjacency[second].add(first)
        reached = set()
        queue = deque([0])
        while queue:
            component = queue.popleft()
            if component in reached:
                continue
            reached.add(component)
            queue.extend(component_adjacency[component] - reached)
        if len(reached) != len(support["sab_components"]):
            raise ValueError("common-rhombus macro address graph is disconnected")
        if support.get("source_embedding_count") != expected_embeddings[name]:
            raise ValueError("source embedding count mismatch")
        if support.get("source_embeddings_one_support_isometry_orbit") is not True:
            raise ValueError("source embeddings were not proved isometry-equivalent")


def _component_geometry(component: dict) -> tuple[set[tuple[int, int]], set[tuple]]:
    """Return the vertices and four unit boundary edges of one SAB rhombus."""

    edge_counts: Counter = Counter()
    vertices: set[tuple[int, int]] = set()
    for raw_cell in component["primitive_cells"]:
        cell = (raw_cell[0], raw_cell[1], raw_cell[2])
        triangle = _triangle_vertices(cell)
        vertices.update(triangle)
        for first, second in zip(triangle, triangle[1:] + triangle[:1]):
            edge_counts[_edge(first, second)] += 1
    boundary = {edge for edge, count in edge_counts.items() if count == 1}
    if len(vertices) != 4 or len(boundary) != 4:
        raise ValueError("a source component is not one four-sided rhombus")
    return vertices, boundary


def build_contact_kernel(atlas: dict) -> dict:
    """Build the exact 31-address macro-contact kernel.

    The binary-domain-wall decision is deliberately narrow.  A carrier in
    this family has one handedness bit per occurrence; unlike-handed contacts
    are precisely macro-internal, while like-handed contacts are precisely
    exposed.  Since the source has no exposed edge colors beyond its SAB
    germ, all exposed address occurrences use the same external channel.
    """

    verify_atlas(atlas)
    states: list[dict] = []
    contacts: list[dict] = []
    exposed_ids: list[str] = []

    for macro_name in ("large_A", "large_B", "small_M"):
        support = atlas["supports"][macro_name]
        edge_owners: dict[tuple, list[tuple[int, str]]] = {}
        component_geometry = []
        for address, component in enumerate(support["sab_components"]):
            vertices, boundary = _component_geometry(component)
            diagonal = tuple(
                sorted(tuple(point) for point in component["diagonal_uv"])
            )
            delta = (
                diagonal[1][0] - diagonal[0][0],
                diagonal[1][1] - diagonal[0][1],
            )
            try:
                diagonal_axis = next(
                    index % 3
                    for index, direction in enumerate(LONG_DIAGONALS)
                    if delta == direction or delta == (-direction[0], -direction[1])
                )
            except StopIteration as error:
                raise ValueError("component diagonal has no limiting axis") from error
            side_records = []
            for edge in sorted(boundary):
                marked = set(edge) & set(diagonal)
                if len(marked) != 1:
                    raise ValueError("a rhombus side does not have one SAB endpoint")
                side_records.append(
                    {
                        "edge_uv": [list(edge[0]), list(edge[1])],
                        "sab_endpoint_uv": list(next(iter(marked))),
                    }
                )
                edge_owners.setdefault(edge, []).append((address, component["role"]))
            state_id = f"{macro_name}:{address}"
            states.append(
                {
                    "id": state_id,
                    "macro": macro_name,
                    "address": address,
                    "role": component["role"],
                    "diagonal_axis": diagonal_axis,
                    "diagonal_uv": [list(point) for point in diagonal],
                    "vertices_uv": [list(point) for point in sorted(vertices)],
                    "sides": side_records,
                }
            )
            component_geometry.append(boundary)

        for edge, owners in sorted(edge_owners.items()):
            if len(owners) == 2:
                first, second = sorted(owner[0] for owner in owners)
                if first == second:
                    continue  # the primitive diagonal inside one rhombus
                contacts.append(
                    {
                        "kind": "internal",
                        "macro": macro_name,
                        "edge_uv": [list(edge[0]), list(edge[1])],
                        "states": [f"{macro_name}:{first}", f"{macro_name}:{second}"],
                        "required_xor": 1,
                    }
                )
            elif len(owners) == 1:
                exposed_ids.append(f"{macro_name}:{owners[0][0]}")
            else:
                raise ValueError("a unit edge has more than two component owners")

    # One equality star is equivalent to all pairwise exposed constraints but
    # avoids serializing a quadratic list of redundant equations.
    exposed_ids = sorted(set(exposed_ids))
    constraints = [
        {
            "left": contact["states"][0],
            "right": contact["states"][1],
            "xor": 1,
            "reason": f"internal:{contact['macro']}:{index}",
        }
        for index, contact in enumerate(contacts)
    ]
    if exposed_ids:
        anchor = exposed_ids[0]
        constraints.extend(
            {
                "left": anchor,
                "right": state_id,
                "xor": 0,
                "reason": "common-exposed-channel",
            }
            for state_id in exposed_ids[1:]
        )

    state_ids = [state["id"] for state in states]
    axis_of = {state["id"]: state["diagonal_axis"] for state in states}
    internal_axis_counts = Counter(
        "same" if axis_of[left] == axis_of[right] else "different"
        for left, right in (contact["states"] for contact in contacts)
    )

    def solve_parity(selected_constraints):
        labels: dict[str, int] = {}
        adjacency: dict[str, list[tuple[str, int, dict]]] = {
            state_id: [] for state_id in state_ids
        }
        for constraint in selected_constraints:
            left, right, parity = (
                constraint["left"],
                constraint["right"],
                constraint["xor"],
            )
            adjacency[left].append((right, parity, constraint))
            adjacency[right].append((left, parity, constraint))
        conflict = None
        for root in adjacency:
            if root in labels:
                continue
            labels[root] = 0
            queue = deque([root])
            while queue and conflict is None:
                left = queue.popleft()
                for right, parity, constraint in adjacency[left]:
                    expected = labels[left] ^ parity
                    if right not in labels:
                        labels[right] = expected
                        queue.append(right)
                    elif labels[right] != expected:
                        conflict = {
                            "left": left,
                            "right": right,
                            "required_xor": parity,
                            "observed_xor": labels[left] ^ labels[right],
                            "closing_constraint": constraint,
                        }
                        break
            if conflict is not None:
                break
        return {
            "satisfiable": conflict is None,
            "labels": labels if conflict is None else None,
            "conflict": conflict,
        }

    internal_constraints = [
        constraint for constraint in constraints if constraint["xor"] == 1
    ]
    internal_verdict = solve_parity(internal_constraints)
    domain_verdict = solve_parity(constraints)
    internal_neighbors = {state_id: set() for state_id in state_ids}
    for constraint in internal_constraints:
        internal_neighbors[constraint["left"]].add(constraint["right"])
        internal_neighbors[constraint["right"]].add(constraint["left"])
    odd_triangle = None
    for first in state_ids:
        for second in sorted(internal_neighbors[first]):
            common = internal_neighbors[first] & internal_neighbors[second]
            if common:
                odd_triangle = sorted((first, second, min(common)))
                break
        if odd_triangle is not None:
            break

    return {
        "schema": "ahi-sturmian-contact-kernel-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "states": states,
        "internal_contacts": contacts,
        "internal_axis_relation_counts": dict(sorted(internal_axis_counts.items())),
        "exposed_state_ids": exposed_ids,
        "internal_opposite_handedness": {
            "family": "every macro-internal contact joins opposite handedness bits",
            "odd_triangle_certificate": odd_triangle,
            **internal_verdict,
        },
        "binary_domain_wall": {
            "family": (
                "one handedness bit; internal contacts require unlike bits; "
                "all exposed contacts use one like-bit channel"
            ),
            **domain_verdict,
        },
    }


def verify_contact_kernel(kernel: dict, atlas: dict) -> None:
    expected = build_contact_kernel(atlas)
    if kernel != expected:
        raise ValueError("serialized contact kernel differs from exact reconstruction")


def _component_axis(component: dict) -> int:
    diagonal = tuple(sorted(tuple(point) for point in component["diagonal_uv"]))
    delta = (
        diagonal[1][0] - diagonal[0][0],
        diagonal[1][1] - diagonal[0][1],
    )
    for index, direction in enumerate(LONG_DIAGONALS):
        if delta == direction or delta == (-direction[0], -direction[1]):
            return index % 3
    raise ValueError("component diagonal has no limiting axis")


def _partner_offset(orientation: str, axis: int) -> tuple[int, int, str]:
    origin = (0, 0, orientation)
    origin_vertices = set(_triangle_vertices(origin))
    matches = []
    other_orientation = "D" if orientation == "U" else "U"
    for u in range(-2, 3):
        for v in range(-2, 3):
            other = (u, v, other_orientation)
            other_vertices = set(_triangle_vertices(other))
            shared = origin_vertices & other_vertices
            if len(shared) != 2:
                continue
            outer = (origin_vertices | other_vertices) - shared
            diagonal = tuple(sorted(outer))
            component = {"diagonal_uv": [list(point) for point in diagonal]}
            if _component_axis(component) == axis:
                matches.append(other)
    if len(matches) != 1:
        raise ValueError("axis does not select exactly one adjacent triangle")
    return matches[0]


def build_periodic_scaffold(atlas: dict) -> dict:
    """Find exact affine periodic perfect matchings containing the templates."""

    verify_atlas(atlas)
    offsets = {
        orientation: {
            axis: _partner_offset(orientation, axis) for axis in range(3)
        }
        for orientation in ("U", "D")
    }

    def axis_value(model, cell):
        a, b, c, d = model
        u, v, orientation = cell
        return (a * u + b * v + c * (orientation == "D") + d) % 3

    globally_valid = []
    for a in range(3):
        for b in range(3):
            for c in range(3):
                for d in range(3):
                    model = (a, b, c, d)
                    valid = True
                    for u in range(3):
                        for v in range(3):
                            for orientation in ("U", "D"):
                                cell = (u, v, orientation)
                                axis = axis_value(model, cell)
                                du, dv, partner_orientation = offsets[orientation][axis]
                                partner = (u + du, v + dv, partner_orientation)
                                if axis_value(model, partner) != axis:
                                    valid = False
                    if valid:
                        globally_valid.append(model)

    macro_models = {}
    for macro_name in ("large_A", "large_B", "small_M"):
        support = atlas["supports"][macro_name]
        required = {}
        for component in support["sab_components"]:
            axis = _component_axis(component)
            for raw_cell in component["primitive_cells"]:
                required[(raw_cell[0], raw_cell[1], raw_cell[2])] = axis
        matches = [
            model
            for model in globally_valid
            if all(axis_value(model, cell) == axis for cell, axis in required.items())
        ]
        macro_models[macro_name] = [list(model) for model in matches]

    common_linear_parts = sorted(
        {
            model[:3]
            for model in globally_valid
            if all(
                any(tuple(candidate[:3]) == model[:3] for candidate in macro_models[name])
                for name in macro_models
            )
        }
    )
    witness = None
    if common_linear_parts:
        linear = common_linear_parts[0]
        phases = {
            name: next(
                candidate[3]
                for candidate in macro_models[name]
                if tuple(candidate[:3]) == linear
            )
            for name in macro_models
        }
        witness = {
            "coefficients_mod_3": list(linear),
            "macro_phases": phases,
            "axis_formula": "a*u+b*v+c*[orientation=D]+phase mod 3",
            "period_generators_uv": [[3, 0], [0, 3]],
        }

    return {
        "schema": "ahi-sturmian-periodic-scaffold-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "partner_offsets": {
            orientation: {
                str(axis): [du, dv, partner_orientation]
                for axis, (du, dv, partner_orientation) in by_axis.items()
            }
            for orientation, by_axis in offsets.items()
        },
        "global_affine_perfect_matching_models": [
            list(model) for model in globally_valid
        ],
        "macro_models": macro_models,
        "common_linear_parts": [list(model) for model in common_linear_parts],
        "periodic_witness": witness,
    }


def verify_periodic_scaffold(scaffold: dict, atlas: dict) -> None:
    expected = build_periodic_scaffold(atlas)
    if scaffold != expected:
        raise ValueError("serialized periodic scaffold differs from exact reconstruction")


def _corridor_state_embeddings(paths, cells, serialized_components):
    """Lift the fixed role-labelled atlas to ordered corridor-bit states."""

    graph_points, graph_edges, roles = _source_sab_graph(paths)
    bits = tuple(_sab_corridor_bits(path) for path in paths)
    owners: dict[tuple, list] = {}
    for cell in cells:
        triangle = _triangle_vertices(cell)
        for first, second in zip(triangle, triangle[1:] + triangle[:1]):
            owners.setdefault(_edge(first, second), []).append(cell)
    diagonals = {}
    for shared, incident in owners.items():
        if len(incident) != 2:
            continue
        vertices = set(_triangle_vertices(incident[0])) | set(
            _triangle_vertices(incident[1])
        )
        diagonals[_edge(*(vertices - set(shared)))] = tuple(sorted(incident))
    support_vertices = set().union(*(
        set(_triangle_vertices(cell)) for cell in cells
    ))
    target = frozenset(
        (
            component["role"],
            _edge(*(tuple(tuple(point) for point in component["diagonal_uv"]))),
        )
        for component in serialized_components
    )
    solutions = set()
    for reflected in (False, True):
        for rotation in range(6):
            adjacency = {index: [] for index in range(len(graph_points))}
            for first, second in graph_edges:
                delta = (
                    graph_points[second][0] - graph_points[first][0],
                    graph_points[second][1] - graph_points[first][1],
                )
                source_direction = DIRECTIONS.index(delta)
                direction = (
                    (rotation - source_direction) % 6
                    if reflected
                    else (source_direction + rotation) % 6
                )
                step = LONG_DIAGONALS[direction]
                adjacency[first].append((second, step))
                adjacency[second].append((first, (-step[0], -step[1])))
            embedded = {0: (0, 0)}
            queue = deque([0])
            consistent = True
            while queue and consistent:
                first = queue.popleft()
                for second, step in adjacency[first]:
                    point = (
                        embedded[first][0] + step[0],
                        embedded[first][1] + step[1],
                    )
                    if second in embedded and embedded[second] != point:
                        consistent = False
                        break
                    if second not in embedded:
                        embedded[second] = point
                        queue.append(second)
            if not consistent:
                continue
            points = tuple(embedded[index] for index in range(len(graph_points)))
            for target_vertex in support_vertices:
                translation = (
                    target_vertex[0] - points[0][0],
                    target_vertex[1] - points[0][1],
                )
                placed = tuple(
                    (u + translation[0], v + translation[1]) for u, v in points
                )
                selected = tuple(
                    _edge(placed[first], placed[second])
                    for first, second in graph_edges
                )
                if frozenset(zip(roles, selected)) != target:
                    continue
                state = frozenset(
                    (
                        diagonal,
                        tuple(reversed(bit_pair)) if reflected else bit_pair,
                    )
                    for diagonal, bit_pair in zip(selected, bits)
                )
                solutions.add(state)
    if not solutions:
        raise ValueError("the fixed source atlas has no corridor-state lift")
    return solutions


def build_corridor_quotient(archive_path: Path, atlas: dict) -> dict:
    """Build the 12-state axis/corridor quotient of the exact source atlas."""

    verify_atlas(atlas)
    if sha256_path(archive_path) != SOURCE_ARCHIVE_SHA256:
        raise ValueError("source archive hash mismatch")
    with tempfile.TemporaryDirectory(prefix="ahi-corridor-") as directory:
        root = Path(directory)
        with tarfile.open(archive_path, "r:gz") as archive:
            member = archive.getmember("Example1.pdf")
            archive.extract(member, root, filter="data")
        pdf_path = root / "Example1.pdf"
        if sha256_path(pdf_path) != EXAMPLE1_SHA256:
            raise ValueError("Example1.pdf member hash mismatch")
        svg_path = root / "example1-page1.svg"
        subprocess.run(
            [
                "pdftocairo",
                "-svg",
                "-f",
                "1",
                "-l",
                "1",
                str(pdf_path),
                str(svg_path),
            ],
            check=True,
        )
        paths = extract_sab_polylines(svg_path)

    macros = {}
    for macro_name in ("large_A", "large_B"):
        support = atlas["supports"][macro_name]
        cells = tuple((u, v, orientation) for u, v, orientation in support["cells"])
        solutions = _corridor_state_embeddings(
            paths[macro_name], cells, support["sab_components"]
        )
        serialized = []
        for solution in sorted(
            solutions,
            key=lambda item: tuple(sorted((edge, bit_pair) for edge, bit_pair in item)),
        ):
            by_diagonal = dict(solution)
            states = []
            for address, component in enumerate(support["sab_components"]):
                diagonal = _edge(*(
                    tuple(tuple(point) for point in component["diagonal_uv"])
                ))
                states.append(
                    {
                        "address": address,
                        "axis": _component_axis(component),
                        "role": component["role"],
                        "corridor_bits": list(by_diagonal[diagonal]),
                    }
                )
            serialized.append(states)
        macros[macro_name] = {
            "corridor_embedding_count": len(serialized),
            "embeddings": serialized,
        }

    small_bits = _sab_corridor_bits(paths["small_M"][0])
    small_component = atlas["supports"]["small_M"]["sab_components"][0]
    macros["small_M"] = {
        "corridor_embedding_count": 2,
        "embeddings": [
            [
                {
                    "address": 0,
                    "axis": _component_axis(small_component),
                    "role": "M",
                    "corridor_bits": list(bits),
                }
            ]
            for bits in (small_bits, tuple(reversed(small_bits)))
        ],
    }

    alphabet = [
        {"axis": axis, "corridor_bits": [first, second]}
        for axis in range(3)
        for first in range(2)
        for second in range(2)
    ]
    action = []
    for reflected in (False, True):
        for rotation in range(6):
            images = []
            for state in alphabet:
                axis = state["axis"]
                image_axis = (
                    (rotation - axis) % 3 if reflected else (axis + rotation) % 3
                )
                bit_pair = state["corridor_bits"]
                if reflected:
                    bit_pair = list(reversed(bit_pair))
                images.append(
                    {
                        "from": state,
                        "to": {"axis": image_axis, "corridor_bits": bit_pair},
                    }
                )
            action.append(
                {"reflected": reflected, "rotation": rotation, "images": images}
            )
    return {
        "schema": "ahi-sturmian-corridor-quotient-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "alphabet": alphabet,
        "euclidean_frame_action": action,
        "macros": macros,
    }


def verify_corridor_quotient(quotient: dict, archive_path: Path, atlas: dict) -> None:
    expected = build_corridor_quotient(archive_path, atlas)
    if quotient != expected:
        raise ValueError("serialized corridor quotient differs from exact source lift")


def _role_hexagons(support: dict, role: str) -> list[dict]:
    """Recover regular three-rhombus hexagons of one source role."""

    components = support["sab_components"]
    selected = [
        address for address, component in enumerate(components)
        if component["role"] == role
    ]
    boundaries = {
        address: _component_geometry(components[address])[1]
        for address in selected
    }
    adjacency = {address: set() for address in selected}
    for offset, first in enumerate(selected):
        for second in selected[offset + 1:]:
            if boundaries[first] & boundaries[second]:
                adjacency[first].add(second)
                adjacency[second].add(first)

    groups = []
    unseen = set(selected)
    while unseen:
        root = min(unseen)
        group = set()
        queue = deque([root])
        while queue:
            address = queue.popleft()
            if address in group:
                continue
            group.add(address)
            queue.extend(adjacency[address] - group)
        unseen -= group
        addresses = sorted(group)
        if len(addresses) != 3 or any(
            (group - {address}) != adjacency[address] for address in group
        ):
            raise ValueError(f"{role} components do not form disjoint 3-cliques")

        cells = sorted(
            (u, v, orientation)
            for address in addresses
            for u, v, orientation in components[address]["primitive_cells"]
        )
        if len(cells) != 6 or len(set(cells)) != 6:
            raise ValueError("role hexagon does not contain six primitive triangles")
        edge_counts: Counter = Counter()
        for cell in cells:
            triangle = _triangle_vertices(cell)
            for first, second in zip(triangle, triangle[1:] + triangle[:1]):
                edge_counts[_edge(first, second)] += 1
        boundary = sorted(edge for edge, count in edge_counts.items() if count == 1)
        vertices = sorted(set().union(*(set(edge) for edge in boundary)))
        if len(boundary) != 6 or len(vertices) != 6:
            raise ValueError("role 3-clique is not one unit regular hexagon")
        boundary_steps = {
            (second[0] - first[0], second[1] - first[1])
            for first, second in boundary
        }
        if any(step not in DIRECTIONS for step in boundary_steps):
            raise ValueError("role hexagon has a non-unit boundary edge")

        # For a primitive triangle, (3u+2,3v+1) or (3u+1,3v+2) is
        # three times its centroid.  Summing the six values gives eighteen
        # times the common hexagon center, entirely in integer arithmetic.
        center18 = [
            sum(3 * u + (2 if orientation == "U" else 1) for u, _, orientation in cells),
            sum(3 * v + (1 if orientation == "U" else 2) for _, v, orientation in cells),
        ]
        groups.append(
            {
                "addresses": addresses,
                "primitive_cells": [list(cell) for cell in cells],
                "boundary_edges_uv": [[list(first), list(second)] for first, second in boundary],
                "center18_uv": center18,
            }
        )
    return sorted(groups, key=lambda item: item["addresses"])


def _rooted_pair_canonical(vectors: list[tuple[int, int]]) -> list[list[int]]:
    """Canonicalize an unordered vector pair under the full lattice D6."""

    if len(vectors) != 2:
        raise ValueError("rooted selector must have exactly two target vectors")
    images = []
    for reflected in (False, True):
        for rotation in range(6):
            images.append(
                tuple(sorted(
                    _linear_isometry(vector, rotation, reflected)
                    for vector in vectors
                ))
            )
    return [list(vector) for vector in min(images)]


def build_l_anchor_selector(atlas: dict) -> dict:
    """Reduce each large macro to one rooted L-to-two-S selector state."""

    verify_atlas(atlas)
    macros = {}
    classes = set()
    for macro_name in ("large_A", "large_B"):
        support = atlas["supports"][macro_name]
        large = _role_hexagons(support, "L")
        small = _role_hexagons(support, "S")
        if len(large) != 1 or len(small) != 2:
            raise ValueError("large macro is not one L plus two S hexagons")
        role_addresses = {
            role: [
                address
                for address, component in enumerate(support["sab_components"])
                if component["role"] == role
            ]
            for role in ("S", "M", "L")
        }
        if len(role_addresses["M"]) != 6:
            raise ValueError("large macro does not have six connector M rhombi")
        root = large[0]["center18_uv"]
        vectors = [
            (item["center18_uv"][0] - root[0], item["center18_uv"][1] - root[1])
            for item in small
        ]
        canonical = _rooted_pair_canonical(vectors)
        class_key = tuple(tuple(vector) for vector in canonical)
        classes.add(class_key)
        macros[macro_name] = {
            "role_address_partition": role_addresses,
            "L_hexagon": large[0],
            "S_hexagons": small,
            "L_to_S_center18_vectors": [list(vector) for vector in vectors],
            "full_isometry_class": canonical,
        }

    ordered_classes = sorted(classes)
    if len(ordered_classes) != 2:
        raise ValueError("the two published large macros do not give two selector classes")
    for macro in macros.values():
        key = tuple(tuple(vector) for vector in macro["full_isometry_class"])
        macro["selector_bit"] = ordered_classes.index(key)
    return {
        "schema": "ahi-sturmian-l-anchor-selector-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "selector_alphabet": [
            {
                "bit": index,
                "full_isometry_class": [list(vector) for vector in class_key],
            }
            for index, class_key in enumerate(ordered_classes)
        ],
        "macros": macros,
    }


def verify_l_anchor_selector(selector: dict, atlas: dict) -> None:
    expected = build_l_anchor_selector(atlas)
    if selector != expected:
        raise ValueError("serialized L-anchor selector differs from exact atlas reduction")


def _edge_substitution_cycle(support: dict, signs: tuple[int, ...]):
    vertices = tuple(tuple(point) for point in support["boundary_vertices_uv"])
    if len(signs) != len(vertices):
        raise ValueError("edge-sign word has the wrong length")
    components = support["sab_components"]
    component_boundaries = [
        _component_geometry(component)[1] for component in components
    ]
    cycle = []
    for index, (first, second) in enumerate(
        zip(vertices, vertices[1:] + vertices[:1])
    ):
        boundary_edge = _edge(first, second)
        owners = [
            component_index
            for component_index, boundary in enumerate(component_boundaries)
            if boundary_edge in boundary
        ]
        if len(owners) != 1:
            raise ValueError("macro boundary edge does not have one inside rhombus")
        diagonal = components[owners[0]]["diagonal_uv"]
        inside2 = (
            diagonal[0][0] + diagonal[1][0],
            diagonal[0][1] + diagonal[1][1],
        )
        first2, second2 = (
            (2 * first[0], 2 * first[1]),
            (2 * second[0], 2 * second[1]),
        )
        outside2 = (
            first2[0] + second2[0] - inside2[0],
            first2[1] + second2[1] - inside2[1],
        )
        apex2 = outside2 if signs[index] else inside2
        cycle.extend((first2, apex2))
    return tuple(cycle)


def _simplify_cycle(vertices: tuple[tuple[int, int], ...]):
    result = list(vertices)
    changed = True
    while changed and len(result) >= 3:
        changed = False
        for index in range(len(result)):
            previous = result[index - 1]
            current = result[index]
            following = result[(index + 1) % len(result)]
            first = (current[0] - previous[0], current[1] - previous[1])
            second = (following[0] - current[0], following[1] - current[1])
            if first[0] * second[1] - first[1] * second[0] == 0 and (
                first[0] * second[0] + first[1] * second[1] > 0
            ):
                result.pop(index)
                changed = True
                break
    return tuple(result)


def _canonical_polygon_cycle(vertices: tuple[tuple[int, int], ...]):
    candidates = []
    for reflected in (False, True):
        for rotation in range(6):
            image = tuple(
                _linear_isometry(point, rotation, reflected) for point in vertices
            )
            for traversal in (image, tuple(reversed(image))):
                for start in range(len(traversal)):
                    ordered = traversal[start:] + traversal[:start]
                    anchor = ordered[0]
                    candidates.append(tuple(
                        (point[0] - anchor[0], point[1] - anchor[1])
                        for point in ordered
                    ))
    return min(candidates)


def _closed_segments_intersect(a, b, c, d) -> bool:
    def orientation(first, second, point):
        return (
            (second[0] - first[0]) * (point[1] - first[1])
            - (second[1] - first[1]) * (point[0] - first[0])
        )

    def between(first, second, point):
        return (
            min(first[0], second[0]) <= point[0] <= max(first[0], second[0])
            and min(first[1], second[1]) <= point[1] <= max(first[1], second[1])
        )

    o1, o2 = orientation(a, b, c), orientation(a, b, d)
    o3, o4 = orientation(c, d, a), orientation(c, d, b)
    if (o1 > 0 > o2 or o2 > 0 > o1) and (o3 > 0 > o4 or o4 > 0 > o3):
        return True
    return (
        (o1 == 0 and between(a, b, c))
        or (o2 == 0 and between(a, b, d))
        or (o3 == 0 and between(c, d, a))
        or (o4 == 0 and between(c, d, b))
    )


def _is_simple_cycle(vertices: tuple[tuple[int, int], ...]) -> bool:
    if len(vertices) < 3 or len(set(vertices)) != len(vertices):
        return False
    count = len(vertices)
    segments = [
        (vertices[index], vertices[(index + 1) % count]) for index in range(count)
    ]
    if any(first == second for first, second in segments):
        return False
    for first in range(count):
        for second in range(first + 1, count):
            if second in {first, first + 1} or (first == 0 and second == count - 1):
                continue
            if _closed_segments_intersect(*segments[first], *segments[second]):
                return False
    return doubled_uv_area(vertices) != 0


def build_unit_apex_compiler(atlas: dict) -> dict:
    """Exhaust the direct inward/outward rhomb-center edge substitution."""

    verify_atlas(atlas)
    by_macro = {}
    for macro_name in ("large_A", "large_B"):
        support = atlas["supports"][macro_name]
        edge_count = len(support["boundary_vertices_uv"])
        classes: dict[tuple, list[str]] = {}
        simple_count = 0
        for mask in range(1 << edge_count):
            signs = tuple((mask >> index) & 1 for index in range(edge_count))
            cycle = _edge_substitution_cycle(support, signs)
            if not _is_simple_cycle(cycle):
                continue
            simple_count += 1
            simplified = _simplify_cycle(cycle)
            canonical = _canonical_polygon_cycle(simplified)
            word = "".join(str(bit) for bit in signs)
            classes.setdefault(canonical, []).append(word)
        by_macro[macro_name] = {
            "boundary_edge_count": edge_count,
            "binary_word_count": 1 << edge_count,
            "simple_word_count": simple_count,
            "classes": classes,
        }

    common_keys = sorted(
        set(by_macro["large_A"]["classes"])
        & set(by_macro["large_B"]["classes"])
    )
    common = [
        {
            "canonical_vertices_uv": [list(point) for point in key],
            "large_A_sign_words": sorted(by_macro["large_A"]["classes"][key]),
            "large_B_sign_words": sorted(by_macro["large_B"]["classes"][key]),
        }
        for key in common_keys
    ]
    small = atlas["supports"]["small_M"]
    small_cycle = _edge_substitution_cycle(small, (0, 0, 0, 0))
    return {
        "schema": "ahi-sturmian-unit-apex-compiler-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "substitution": {
            "0": "inward through the center of the incident source rhombus",
            "1": "outward through its reflection across the boundary edge",
            "coordinate_scale": 2,
        },
        "small_M_all_inward": {
            "cycle_uv": [list(point) for point in small_cycle],
            "doubled_area": doubled_uv_area(small_cycle),
            "distinct_vertex_count": len(set(small_cycle)),
        },
        "macros": {
            name: {
                key: value for key, value in data.items() if key != "classes"
            }
            for name, data in by_macro.items()
        },
        "common_simple_support_count": len(common),
        "common_simple_supports": common,
    }


def verify_unit_apex_compiler(compiler: dict, atlas: dict) -> None:
    expected = build_unit_apex_compiler(atlas)
    if compiler != expected:
        raise ValueError("serialized unit-apex compiler differs from exhaustive rebuild")


def _transform_cell_set(cells, rotation, reflected, translation):
    triangles = []
    for raw_cell in cells:
        cell = (raw_cell[0], raw_cell[1], raw_cell[2])
        triangles.append(frozenset(
            (
                _linear_isometry(point, rotation, reflected)[0] + translation[0],
                _linear_isometry(point, rotation, reflected)[1] + translation[1],
            )
            for point in _triangle_vertices(cell)
        ))
    return frozenset(triangles)


def _component_rhombi(support: dict):
    return frozenset(
        frozenset(tuple(point) for point in component["vertices_uv"])
        if "vertices_uv" in component
        else frozenset(_component_geometry(component)[0])
        for component in support["sab_components"]
    )


def _component_rhombus_records(support: dict):
    return {
        frozenset(_component_geometry(component)[0]): {
            "address": address,
            "role": component["role"],
        }
        for address, component in enumerate(support["sab_components"])
    }


def _transform_rhombi(rhombi, rotation, reflected, translation):
    return frozenset(
        frozenset(
            (
                _linear_isometry(point, rotation, reflected)[0] + translation[0],
                _linear_isometry(point, rotation, reflected)[1] + translation[1],
            )
            for point in rhombus
        )
        for rhombus in rhombi
    )


def _triangle_union_boundary(triangles):
    edge_counts: Counter = Counter()
    adjacency = {triangle: set() for triangle in triangles}
    owners = {}
    for triangle in triangles:
        points = tuple(triangle)
        # A triangle arrives as an unordered vertex set.  Its three pairs are
        # exactly its three unit edges.
        edges = [
            _edge(points[first], points[second])
            for first in range(3) for second in range(first + 1, 3)
        ]
        for edge in edges:
            edge_counts[edge] += 1
            if edge in owners:
                adjacency[triangle].add(owners[edge])
                adjacency[owners[edge]].add(triangle)
            else:
                owners[edge] = triangle
    reached = set()
    queue = deque([next(iter(triangles))])
    while queue:
        triangle = queue.popleft()
        if triangle in reached:
            continue
        reached.add(triangle)
        queue.extend(adjacency[triangle] - reached)
    boundary = {edge for edge, count in edge_counts.items() if count == 1}
    vertex_neighbors = {}
    for first, second in boundary:
        vertex_neighbors.setdefault(first, set()).add(second)
        vertex_neighbors.setdefault(second, set()).add(first)
    disk_boundary = (
        len(reached) == len(triangles)
        and vertex_neighbors
        and all(len(neighbors) == 2 for neighbors in vertex_neighbors.values())
    )
    cycle = []
    if disk_boundary:
        start = min(vertex_neighbors)
        previous = None
        current = start
        while True:
            cycle.append(current)
            choices = sorted(vertex_neighbors[current] - ({previous} if previous else set()))
            following = choices[0]
            previous, current = current, following
            if current == start:
                break
            if len(cycle) > len(vertex_neighbors):
                disk_boundary = False
                break
        if len(cycle) != len(vertex_neighbors):
            disk_boundary = False
    return disk_boundary, cycle, boundary


def _two_triangles_form_rhombus(triangles) -> bool:
    if len(triangles) != 2:
        return False
    first, second = tuple(triangles)
    if len(first & second) != 2 or len(first | second) != 4:
        return False
    shared = first & second
    diagonal = (first | second) - shared
    if len(diagonal) != 2:
        return False
    first_point, second_point = tuple(diagonal)
    delta = (
        second_point[0] - first_point[0],
        second_point[1] - first_point[1],
    )
    return any(
        delta == direction or delta == (-direction[0], -direction[1])
        for direction in LONG_DIAGONALS
    )


def build_common_support_kernel(atlas: dict) -> dict:
    """Find the exact closest common support of the two large source patches."""

    verify_atlas(atlas)
    support_a = atlas["supports"]["large_A"]
    support_b = atlas["supports"]["large_B"]
    cells_a = _transform_cell_set(support_a["cells"], 0, False, (0, 0))
    rhombi_a = _component_rhombi(support_a)
    records_a = _component_rhombus_records(support_a)
    vertices_a = set().union(*cells_a)
    best_triangle_overlap = -1
    best_rhombus_overlap = -1
    best = []
    one_rhombus_equalizers = []
    two_rhombus_equalizers = []

    for reflected in (False, True):
        for rotation in range(6):
            cells_b_zero = _transform_cell_set(
                support_b["cells"], rotation, reflected, (0, 0)
            )
            rhombi_b_zero = _transform_rhombi(
                _component_rhombi(support_b), rotation, reflected, (0, 0)
            )
            records_b_zero = {
                next(iter(_transform_rhombi(
                    frozenset({rhombus}), rotation, reflected, (0, 0)
                ))): record
                for rhombus, record in _component_rhombus_records(support_b).items()
            }
            vertices_b = set().union(*cells_b_zero)
            translations = sorted({
                (a[0] - b[0], a[1] - b[1])
                for a in vertices_a for b in vertices_b
            })
            for translation in translations:
                cells_b = frozenset(
                    frozenset(
                        (point[0] + translation[0], point[1] + translation[1])
                        for point in triangle
                    )
                    for triangle in cells_b_zero
                )
                triangle_overlap = len(cells_a & cells_b)
                if triangle_overlap < best_triangle_overlap:
                    continue
                rhombi_b = frozenset(
                    frozenset(
                        (point[0] + translation[0], point[1] + translation[1])
                        for point in rhombus
                    )
                    for rhombus in rhombi_b_zero
                )
                rhombus_overlap = len(rhombi_a & rhombi_b)
                record = {
                    "reflected": reflected,
                    "rotation": rotation,
                    "translation_uv": list(translation),
                    "primitive_triangle_overlap": triangle_overlap,
                    "rhombus_overlap": rhombus_overlap,
                    "A_only_triangle_count": len(cells_a - cells_b),
                    "B_only_triangle_count": len(cells_b - cells_a),
                    "A_only_rhombus_count": len(rhombi_a - rhombi_b),
                    "B_only_rhombus_count": len(rhombi_b - rhombi_a),
                }
                if triangle_overlap > best_triangle_overlap:
                    best_triangle_overlap = triangle_overlap
                    best_rhombus_overlap = rhombus_overlap
                    best = [record]
                elif triangle_overlap == best_triangle_overlap:
                    if rhombus_overlap > best_rhombus_overlap:
                        best_rhombus_overlap = rhombus_overlap
                        best = [record]
                    elif rhombus_overlap == best_rhombus_overlap:
                        best.append(record)

                a_only, b_only = cells_a - cells_b, cells_b - cells_a
                if _two_triangles_form_rhombus(a_only) and _two_triangles_form_rhombus(b_only):
                    equalizer = dict(record)
                    equalizer["add_to_A_vertices_uv"] = [
                        list(point) for point in sorted(set().union(*b_only))
                    ]
                    equalizer["add_to_B_vertices_uv"] = [
                        list(point) for point in sorted(set().union(*a_only))
                    ]
                    one_rhombus_equalizers.append(equalizer)
                if (
                    len(a_only) == len(b_only) == 4
                    and len(rhombi_a - rhombi_b) == len(rhombi_b - rhombi_a) == 2
                ):
                    common_cells = cells_a | cells_b
                    is_disk, boundary_cycle, boundary_edges = _triangle_union_boundary(
                        common_cells
                    )
                    transformed_records_b = {
                        frozenset(
                            (point[0] + translation[0], point[1] + translation[1])
                            for point in rhombus
                        ): record
                        for rhombus, record in records_b_zero.items()
                    }
                    two_rhombus_equalizers.append({
                        **record,
                        "A_only_components": [
                            {
                                **records_a[rhombus],
                                "vertices_uv": [list(point) for point in sorted(rhombus)],
                            }
                            for rhombus in sorted(
                                rhombi_a - rhombi_b,
                                key=lambda item: tuple(sorted(item)),
                            )
                        ],
                        "B_only_components": [
                            {
                                **transformed_records_b[rhombus],
                                "vertices_uv": [list(point) for point in sorted(rhombus)],
                            }
                            for rhombus in sorted(
                                rhombi_b - rhombi_a,
                                key=lambda item: tuple(sorted(item)),
                            )
                        ],
                        "common_support_triangle_count": len(common_cells),
                        "common_support_is_topological_disk": is_disk,
                        "common_support_boundary_edge_count": len(boundary_edges),
                        "common_support_boundary_cycle_uv": [
                            list(point) for point in boundary_cycle
                        ],
                    })

    best = sorted(
        best,
        key=lambda item: (
            item["reflected"], item["rotation"], item["translation_uv"]
        ),
    )
    one_rhombus_equalizers = sorted(
        one_rhombus_equalizers,
        key=lambda item: (
            item["reflected"], item["rotation"], item["translation_uv"]
        ),
    )
    two_rhombus_equalizers = sorted(
        two_rhombus_equalizers,
        key=lambda item: (
            item["reflected"], item["rotation"], item["translation_uv"]
        ),
    )
    return {
        "schema": "ahi-sturmian-common-support-kernel-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "best_primitive_triangle_overlap": best_triangle_overlap,
        "best_rhombus_overlap_at_that_support_overlap": best_rhombus_overlap,
        "best_alignments": best,
        "one_rhombus_equalizer_count": len(one_rhombus_equalizers),
        "one_rhombus_equalizers": one_rhombus_equalizers,
        "two_rhombus_equalizer_count": len(two_rhombus_equalizers),
        "two_rhombus_equalizers": two_rhombus_equalizers,
    }


def verify_common_support_kernel(kernel: dict, atlas: dict) -> None:
    expected = build_common_support_kernel(atlas)
    if kernel != expected:
        raise ValueError("serialized common-support kernel differs from exhaustive rebuild")


def _resolved_svg_paths(svg_path: Path):
    root = ET.parse(svg_path).getroot()
    by_id = {
        element.attrib["id"]: element
        for element in root.iter()
        if "id" in element.attrib
    }
    surface = by_id.get("surface1")
    if surface is None:
        raise ValueError("source SVG has no surface1")
    xlink = "{http://www.w3.org/1999/xlink}href"

    def visit(element, parent_matrix):
        matrix = _matrix_product(
            parent_matrix, _matrix(element.attrib.get("transform"))
        )
        tag = element.tag.rsplit("}", 1)[-1]
        if tag == "use":
            yield from visit(by_id[element.attrib[xlink][1:]], matrix)
            return
        if tag == "path":
            yield element, matrix
        for child in element:
            yield from visit(child, matrix)

    yield from visit(surface, _matrix(None))


def _canonical_triangle_support(triangles):
    keys = []
    for reflected in (False, True):
        for rotation in range(6):
            transformed = [
                frozenset(
                    _linear_isometry(point, rotation, reflected)
                    for point in triangle
                )
                for triangle in triangles
            ]
            minimum_u = min(point[0] for cell in transformed for point in cell)
            minimum_v = min(point[1] for cell in transformed for point in cell)
            keys.append(tuple(sorted(
                tuple(sorted(
                    (point[0] - minimum_u, point[1] - minimum_v)
                    for point in triangle
                ))
                for triangle in transformed
            )))
    return min(keys)


def _canonical_assembly_signatures(tiles):
    """Return one support key and every typed tiling on its canonical support."""

    union = frozenset().union(*(tile["triangles"] for tile in tiles))
    candidates = []
    for reflected in (False, True):
        for rotation in range(6):
            transformed_union = [
                frozenset(
                    _linear_isometry(point, rotation, reflected)
                    for point in triangle
                )
                for triangle in union
            ]
            minimum_u = min(
                point[0] for triangle in transformed_union for point in triangle
            )
            minimum_v = min(
                point[1] for triangle in transformed_union for point in triangle
            )

            def normalized_triangle(triangle):
                return tuple(sorted(
                    (
                        _linear_isometry(point, rotation, reflected)[0] - minimum_u,
                        _linear_isometry(point, rotation, reflected)[1] - minimum_v,
                    )
                    for point in triangle
                ))

            support_key = tuple(sorted(
                normalized_triangle(triangle) for triangle in union
            ))
            tiling_key = tuple(sorted(
                (
                    tile["source_type"],
                    tuple(sorted(
                        normalized_triangle(triangle)
                        for triangle in tile["triangles"]
                    )),
                )
                for tile in tiles
            ))
            candidates.append((support_key, tiling_key))
    support_key = min(item[0] for item in candidates)
    signatures = sorted({
        item[1] for item in candidates if item[0] == support_key
    })
    return support_key, signatures


def _figure45_outlines(svg_path: Path, atlas: dict):
    outlines = []
    for element, matrix in _resolved_svg_paths(svg_path):
        style = element.attrib.get("style", "")
        if (
            "stroke-width:1;" not in style
            or "stroke:rgb(0%,0%,0%)" not in style
        ):
            continue
        try:
            raw = _first_closed_polyline(element.attrib["d"])
        except ValueError:
            continue
        if raw.edge_count not in (4, 13, 14):
            continue
        points = tuple(
            _transform_point(matrix, point) for point in raw.points
        )
        outlines.append({
            "raw_edge_count": raw.edge_count,
            "points": points,
            "center_x": sum(point[0] for point in points) / len(points),
        })
    if len(outlines) != 32:
        raise ValueError(f"expected 32 Figure 45 tile outlines, got {len(outlines)}")

    segments = [
        (second[0] - first[0], second[1] - first[1])
        for outline in outlines
        for first, second in zip(
            outline["points"], outline["points"][1:] + outline["points"][:1]
        )
    ]
    minimum = min(_squared(segment) for segment in segments)
    type_by_edges = {14: "large_A", 13: "large_B", 4: "small_M"}
    atlas_keys = {
        name: _canonical_triangle_support(
            _transform_cell_set(support["cells"], 0, False, (0, 0))
        )
        for name, support in atlas["supports"].items()
    }
    for outline in outlines:
        relative_vertices = [(0, 0)]
        raw_vertices_uv = [(0, 0)]
        word = []
        for first, second in zip(
            outline["points"], outline["points"][1:] + outline["points"][:1]
        ):
            vector = (second[0] - first[0], second[1] - first[1])
            length2 = _squared(vector)
            if length2 < 3 * minimum:
                multiplicity = 1
            elif 4 * minimum < length2 < 7 * minimum:
                multiplicity = 2
            else:
                raise ValueError("unrecognized Figure 45 boundary length")
            direction_index = _direction_index(*vector)
            direction = DIRECTIONS[direction_index]
            word.extend([direction_index] * multiplicity)
            for _ in range(multiplicity):
                last = relative_vertices[-1]
                relative_vertices.append(
                    (last[0] + direction[0], last[1] + direction[1])
                )
            raw_vertices_uv.append(relative_vertices[-1])
        if relative_vertices[-1] != (0, 0):
            raise ValueError("Figure 45 outline does not close on normalized lattice")
        source_type = type_by_edges[outline["raw_edge_count"]]
        cells = triangle_cells(tuple(relative_vertices[:-1]))
        triangles = frozenset(
            frozenset(_triangle_vertices(cell)) for cell in cells
        )
        if _canonical_triangle_support(triangles) != atlas_keys[source_type]:
            raise ValueError("Figure 45 outline does not match pinned source atlas")
        outline.update({
            "source_type": source_type,
            "boundary_directions": tuple(word),
            "raw_vertices_uv": tuple(raw_vertices_uv[:-1]),
            "relative_triangles": triangles,
        })
    return outlines


def build_interchangeable_pairs(archive_path: Path, atlas: dict) -> dict:
    """Transcribe the two source-native local flips in AHI Figure 45."""

    verify_atlas(atlas)
    if sha256_path(archive_path) != SOURCE_ARCHIVE_SHA256:
        raise ValueError("source archive hash mismatch")
    with tempfile.TemporaryDirectory(prefix="ahi-source-pair-") as directory:
        root = Path(directory)
        with tarfile.open(archive_path, "r:gz") as archive:
            member = archive.getmember("Example1.pdf")
            archive.extract(member, root, filter="data")
        pdf_path = root / "Example1.pdf"
        if sha256_path(pdf_path) != EXAMPLE1_SHA256:
            raise ValueError("Example1.pdf member hash mismatch")
        svg_path = root / "example1-page5.svg"
        subprocess.run(
            [
                "pdftocairo", "-svg", "-f", "5", "-l", "5",
                str(pdf_path), str(svg_path),
            ],
            check=True,
        )
        outlines = _figure45_outlines(svg_path, atlas)

    # These are the four separated panels in the fixed vector source.  The
    # cuts lie in blank horizontal gutters and are checked by the tile census.
    intervals = ((0, 220), (220, 450), (450, 680), (680, 900))
    assemblies = []
    threshold2 = Fraction(1, 400)
    for panel, (lower, upper) in enumerate(intervals):
        tiles = [
            outline for outline in outlines
            if lower < outline["center_x"] < upper
        ]
        expected_count = 9 if panel < 2 else 7
        if len(tiles) != expected_count:
            raise ValueError(f"unexpected Figure 45 panel-{panel} tile count")
        adjacency = {index: [] for index in range(len(tiles))}
        contact_count = 0
        for first_index, first in enumerate(tiles):
            for second_index in range(first_index):
                second = tiles[second_index]
                for first_vertex, first_point in enumerate(first["points"]):
                    for second_vertex, second_point in enumerate(second["points"]):
                        delta = (
                            first_point[0] - second_point[0],
                            first_point[1] - second_point[1],
                        )
                        if _squared(delta) >= threshold2:
                            continue
                        first_uv = first["raw_vertices_uv"][first_vertex]
                        second_uv = second["raw_vertices_uv"][second_vertex]
                        displacement = (
                            second_uv[0] - first_uv[0],
                            second_uv[1] - first_uv[1],
                        )
                        adjacency[second_index].append((first_index, displacement))
                        adjacency[first_index].append((
                            second_index, (-displacement[0], -displacement[1])
                        ))
                        contact_count += 1
        translations = {0: (0, 0)}
        queue = deque([0])
        while queue:
            first = queue.popleft()
            for second, displacement in adjacency[first]:
                candidate = (
                    translations[first][0] + displacement[0],
                    translations[first][1] + displacement[1],
                )
                if second in translations:
                    if translations[second] != candidate:
                        raise ValueError("inconsistent Figure 45 vertex transcription")
                    continue
                translations[second] = candidate
                queue.append(second)
        if len(translations) != len(tiles):
            raise ValueError("Figure 45 panel contact graph is disconnected")

        placed = []
        all_triangles = []
        for index, tile in enumerate(tiles):
            translation = translations[index]
            triangles = frozenset(
                frozenset(
                    (point[0] + translation[0], point[1] + translation[1])
                    for point in triangle
                )
                for triangle in tile["relative_triangles"]
            )
            all_triangles.extend(triangles)
            placed.append({
                "source_type": tile["source_type"],
                "translation_uv": list(translation),
                "boundary_directions": list(tile["boundary_directions"]),
                "triangles": triangles,
            })
        if len(set(all_triangles)) != len(all_triangles):
            raise ValueError("Figure 45 physical tiles overlap after normalization")
        union = frozenset(all_triangles)
        is_disk, boundary_cycle, boundary_edges = _triangle_union_boundary(union)
        if not is_disk:
            raise ValueError("Figure 45 assembly is not a topological disk")
        support_key, signatures = _canonical_assembly_signatures(placed)
        assemblies.append({
            "panel": panel,
            "tile_census": dict(sorted(Counter(
                tile["source_type"] for tile in placed
            ).items())),
            "contact_vertex_match_count": contact_count,
            "primitive_triangle_count": len(union),
            "topological_disk": True,
            "boundary_edge_count": len(boundary_edges),
            "boundary_cycle_uv": [list(point) for point in boundary_cycle],
            "canonical_support": support_key,
            "canonical_tiling_signatures": signatures,
            "tiles": placed,
        })

    pairs = []
    for first_panel, second_panel in ((0, 1), (2, 3)):
        first = assemblies[first_panel]
        second = assemblies[second_panel]
        if first["canonical_support"] != second["canonical_support"]:
            raise ValueError("published interchangeable pair supports differ")
        first_signatures = set(first["canonical_tiling_signatures"])
        second_signatures = set(second["canonical_tiling_signatures"])
        pairs.append({
            "panels": [first_panel, second_panel],
            "tile_census": first["tile_census"],
            "primitive_triangle_count": first["primitive_triangle_count"],
            "rhombus_count": first["primitive_triangle_count"] // 2,
            "boundary_edge_count": first["boundary_edge_count"],
            "same_support_under_full_isometry": True,
            "decompositions_distinct_under_full_isometry": not bool(
                first_signatures & second_signatures
            ),
        })

    def serializable_assembly(assembly):
        result = {
            key: value for key, value in assembly.items()
            if key not in {
                "canonical_support", "canonical_tiling_signatures", "tiles"
            }
        }
        result["tiles"] = [
            {
                key: value for key, value in tile.items()
                if key != "triangles"
            }
            for tile in assembly["tiles"]
        ]
        return result

    return {
        "schema": "ahi-sturmian-interchangeable-pairs-v1",
        "source": {
            "arxiv": "2506.19362v3",
            "archive_sha256": SOURCE_ARCHIVE_SHA256,
            "member": "Example1.pdf",
            "member_sha256": EXAMPLE1_SHA256,
            "figure": 45,
            "page": 5,
        },
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "outline_count": len(outlines),
        "assemblies": [serializable_assembly(item) for item in assemblies],
        "pairs": pairs,
    }


def verify_interchangeable_pairs(data: dict, archive_path: Path, atlas: dict) -> None:
    expected = build_interchangeable_pairs(archive_path, atlas)
    if data != expected:
        raise ValueError("serialized interchangeable pairs differ from source rebuild")


def _serialized_assembly_cells(assembly: dict):
    cells = []
    for tile in assembly["tiles"]:
        vertices = [(0, 0)]
        for direction_index in tile["boundary_directions"]:
            direction = DIRECTIONS[direction_index]
            vertices.append((
                vertices[-1][0] + direction[0],
                vertices[-1][1] + direction[1],
            ))
        if vertices[-1] != (0, 0):
            raise ValueError("serialized tile boundary does not close")
        translation = tile["translation_uv"]
        cells.extend(
            (u + translation[0], v + translation[1], orientation)
            for u, v, orientation in triangle_cells(tuple(vertices[:-1]))
        )
    if len(cells) != len(set(cells)):
        raise ValueError("serialized assembly tiles overlap")
    return tuple(sorted(cells))


def _hnf_sublattices(index: int):
    for horizontal in range(1, index + 1):
        if index % horizontal:
            continue
        vertical = index // horizontal
        for shear in range(horizontal):
            yield horizontal, shear, vertical


def _hnf_residue(u: int, v: int, horizontal: int, shear: int, vertical: int):
    quotient, remainder = divmod(v, vertical)
    return ((u - quotient * shear) % horizontal, remainder)


def build_interchangeable_pair_periodicity(pairs: dict) -> dict:
    """Apply the complete one-tile translation-FD test to Figure 45 supports."""

    if pairs.get("schema") != "ahi-sturmian-interchangeable-pairs-v1":
        raise ValueError("unsupported interchangeable-pair schema")
    results = []
    for pair_index, pair in enumerate(pairs["pairs"]):
        assembly = pairs["assemblies"][pair["panels"][0]]
        cells = _serialized_assembly_cells(assembly)
        if len(cells) != pair["primitive_triangle_count"]:
            raise ValueError("serialized assembly count differs from pair summary")
        by_orientation = {
            orientation: [(u, v) for u, v, cell_orientation in cells
                          if cell_orientation == orientation]
            for orientation in ("U", "D")
        }
        if len(by_orientation["U"]) != len(by_orientation["D"]):
            raise ValueError("translation fundamental domain has unequal orientations")
        index = len(by_orientation["U"])
        certificates = []
        tested = 0
        for horizontal, shear, vertical in _hnf_sublattices(index):
            tested += 1
            residues = {
                orientation: {
                    _hnf_residue(u, v, horizontal, shear, vertical)
                    for u, v in points
                }
                for orientation, points in by_orientation.items()
            }
            if any(len(values) != index for values in residues.values()):
                continue
            certificates.append({
                "hnf": {
                    "basis_uv": [[horizontal, 0], [shear, vertical]],
                    "determinant": index,
                },
                "up_residue_count": len(residues["U"]),
                "down_residue_count": len(residues["D"]),
            })
        results.append({
            "pair_index": pair_index,
            "rhombus_count": pair["rhombus_count"],
            "forced_translation_index": index,
            "hnf_count_tested": tested,
            "translation_fundamental_domain_count": len(certificates),
            "translation_fundamental_domains": certificates,
        })
    return {
        "schema": "ahi-sturmian-interchangeable-periodicity-v1",
        "interchangeable_pairs_sha256": hashlib.sha256(
            (json.dumps(pairs, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "results": results,
    }


def verify_interchangeable_pair_periodicity(data: dict, pairs: dict) -> None:
    expected = build_interchangeable_pair_periodicity(pairs)
    if data != expected:
        raise ValueError("serialized local-pair periodicity census differs from rebuild")


def dump_atlas(data: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
