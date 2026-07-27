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


def dump_atlas(data: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
