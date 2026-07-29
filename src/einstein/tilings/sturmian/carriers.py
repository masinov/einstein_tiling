"""Exact support geometry and interchangeable-assembly constructions."""

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

from .atlas import (
    DIRECTIONS,
    EXAMPLE1_SHA256,
    LONG_DIAGONALS,
    SOURCE_ARCHIVE_SHA256,
    _direction_index,
    _edge,
    _first_closed_polyline,
    _linear_isometry,
    _matrix,
    _matrix_product,
    _squared,
    _transform_point,
    _triangle_vertices,
    doubled_uv_area,
    sha256_path,
    triangle_cells,
    verify_atlas,
)

from .contacts import (
    _component_geometry,
)

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
