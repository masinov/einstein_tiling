"""Exact carrier classifications and periodicity certificates."""

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

from .sturmian_source_core import (
    DIRECTIONS,
    _edge,
    _linear_isometry,
    _triangle_vertices,
    boundary_vertices,
    triangle_cells,
    verify_atlas,
)

from .sturmian_geometry import (
    _canonical_triangle_support,
    _transform_cell_set,
    _triangle_union_boundary,
    _two_triangles_form_rhombus,
    verify_common_support_kernel,
)

from .sturmian_compiler import (
    _hnf_residue,
    _hnf_sublattices,
    _odd_cycle,
    _rhombus_long_diagonal,
    _serialized_assembly_cells,
)

def _attached_singleton_extensions(triangles, native_small_cells):
    """All common rhombi attached edge-to-edge outside a triangle disk.

    The singleton is moved by every full lattice isometry.  Aligning every
    transformed singleton vertex with every current boundary vertex is a
    finite exhaustive way to find every placement sharing a boundary edge.
    Candidate interiors are primitive lattice triangles, so disjoint cell
    sets are exactly the required interior-disjointness test.
    """

    triangles = frozenset(triangles)
    disk, _, boundary = _triangle_union_boundary(triangles)
    if not disk:
        raise ValueError("attachment base is not a triangle disk")
    boundary_vertices = sorted(set().union(*boundary))
    extensions = {}
    for reflected in (False, True):
        for rotation in range(6):
            rotated = _transform_cell_set(
                native_small_cells, rotation, reflected, (0, 0)
            )
            rotated_vertices = sorted(set().union(*rotated))
            for source_vertex in rotated_vertices:
                for target_vertex in boundary_vertices:
                    translation = (
                        target_vertex[0] - source_vertex[0],
                        target_vertex[1] - source_vertex[1],
                    )
                    candidate = frozenset(
                        frozenset(
                            (
                                point[0] + translation[0],
                                point[1] + translation[1],
                            )
                            for point in cell
                        )
                        for cell in rotated
                    )
                    if candidate & triangles:
                        continue
                    candidate_disk, _, candidate_boundary = (
                        _triangle_union_boundary(candidate)
                    )
                    if not candidate_disk or not (boundary & candidate_boundary):
                        continue
                    union = triangles | candidate
                    union_disk, _, _ = _triangle_union_boundary(union)
                    if not union_disk:
                        continue
                    key = tuple(sorted(
                        _cell_from_triangle_vertices(cell) for cell in candidate
                    ))
                    extensions[key] = candidate
    return tuple(extensions[key] for key in sorted(extensions))


def _all_singleton_subdivisions(triangles):
    """Exhaust the lozenge perfect matchings of one primitive-triangle disk."""

    triangles = tuple(sorted(triangles, key=lambda item: tuple(sorted(item))))
    adjacency = {index: [] for index in range(len(triangles))}
    for first_index, first in enumerate(triangles):
        for second_index in range(first_index):
            second = triangles[second_index]
            if len(first & second) != 2:
                continue
            if not _two_triangles_form_rhombus((first, second)):
                continue
            adjacency[first_index].append(second_index)
            adjacency[second_index].append(first_index)

    matching_count = 0
    bipartite = []
    shortest_cycle = None

    def visit(unmatched, pairs):
        nonlocal matching_count, shortest_cycle
        if not unmatched:
            matching_count += 1
            rhombi = tuple(
                frozenset(triangles[first] | triangles[second])
                for first, second in pairs
            )
            diagonals = tuple(sorted(
                _rhombus_long_diagonal(rhombus) for rhombus in rhombi
            ))
            cycle = _odd_cycle(diagonals)
            if cycle is None:
                bipartite.append(diagonals)
            elif shortest_cycle is None or len(cycle) < len(shortest_cycle):
                shortest_cycle = cycle
            return

        first = min(
            unmatched,
            key=lambda index: sum(
                neighbor in unmatched for neighbor in adjacency[index]
            ),
        )
        for second in sorted(
            neighbor for neighbor in adjacency[first] if neighbor in unmatched
        ):
            visit(
                unmatched - {first, second},
                pairs + ((min(first, second), max(first, second)),),
            )

    visit(frozenset(range(len(triangles))), tuple())
    return matching_count, tuple(bipartite), shortest_cycle


def _serialized_diagonals(diagonals):
    if diagonals is None:
        return None
    return [
        [list(first), list(second)] for first, second in diagonals
    ]


def build_sub30_carrier_classification(atlas: dict) -> dict:
    """Classify the K64A area-15/16/17 carrier-local support superset."""

    verify_atlas(atlas)
    native_small_cells = tuple(
        tuple(cell) for cell in atlas["supports"]["small_M"]["cells"]
    )
    classes = []
    total_supports = 0
    total_matchings = 0
    total_bipartite = 0

    for macro_name in ("large_A", "large_B"):
        macro = _transform_cell_set(
            atlas["supports"][macro_name]["cells"], 0, False, (0, 0)
        )
        support_level = {tuple(sorted(
            _cell_from_triangle_vertices(cell) for cell in macro
        )): macro}
        for attachment_count in range(3):
            support_records = []
            for support_key in sorted(support_level):
                support = support_level[support_key]
                disk, boundary_cycle, _ = _triangle_union_boundary(support)
                if not disk:
                    raise ValueError("generated carrier support is not a disk")
                matching_count, bipartite, shortest_cycle = (
                    _all_singleton_subdivisions(support)
                )
                support_records.append({
                    "primitive_cells": [list(cell) for cell in support_key],
                    "boundary_vertices_uv": [list(point) for point in boundary_cycle],
                    "perfect_matching_count": matching_count,
                    "bipartite_matching_count": len(bipartite),
                    "bipartite_subdivisions_diagonals_uv": [
                        _serialized_diagonals(item) for item in bipartite
                    ],
                    "shortest_odd_cycle_edges_uv": _serialized_diagonals(
                        tuple(
                            (
                                shortest_cycle[index],
                                shortest_cycle[(index + 1) % len(shortest_cycle)],
                            )
                            for index in range(len(shortest_cycle))
                        )
                        if shortest_cycle is not None
                        else None
                    ),
                })
                total_matchings += matching_count
                total_bipartite += len(bipartite)

            classes.append({
                "macro": macro_name,
                "attachment_count": attachment_count,
                "carrier_area_rhombi": 15 + attachment_count,
                "support_count": len(support_records),
                "supports": support_records,
            })
            total_supports += len(support_records)

            if attachment_count == 2:
                continue
            next_level = {}
            for support in support_level.values():
                for extension in _attached_singleton_extensions(
                    support, native_small_cells
                ):
                    union = support | extension
                    key = tuple(sorted(
                        _cell_from_triangle_vertices(cell) for cell in union
                    ))
                    next_level[key] = union
            support_level = next_level

    return {
        "schema": "ahi-sturmian-sub30-carrier-classification-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "scope": {
            "macro_supports": ["large_A", "large_B"],
            "attachment_counts": [0, 1, 2],
            "carrier_areas_rhombi": [15, 16, 17],
            "attachment_rule": (
                "every full-isometry singleton placement with disjoint "
                "primitive-triangle interior sharing a unit boundary edge; "
                "retain connected topological disks"
            ),
            "source_rule_filter": (
                "none: this is a geometric superset, so zero parity "
                "survivors is a valid source-language obstruction"
            ),
        },
        "class_count": len(classes),
        "support_count": total_supports,
        "perfect_matching_count": total_matchings,
        "bipartite_matching_count": total_bipartite,
        "all_sub30_supports_fail_parity": total_bipartite == 0,
        "classes": classes,
    }


def verify_sub30_carrier_classification(data: dict, atlas: dict) -> None:
    expected = build_sub30_carrier_classification(atlas)
    if data != expected:
        raise ValueError(
            "serialized sub-30 carrier classification differs from exact rebuild"
        )


def _attached_support_extensions(triangles, native_cells):
    """Every disk attachment of one fixed lattice-cell support."""

    triangles = frozenset(triangles)
    disk, _, boundary = _triangle_union_boundary(triangles)
    if not disk:
        raise ValueError("attachment base is not a triangle disk")
    boundary_vertices = sorted(set().union(*boundary))
    extensions = {}
    for reflected in (False, True):
        for rotation in range(6):
            rotated = _transform_cell_set(native_cells, rotation, reflected, (0, 0))
            rotated_vertices = sorted(set().union(*rotated))
            for source_vertex in rotated_vertices:
                for target_vertex in boundary_vertices:
                    translation = (
                        target_vertex[0] - source_vertex[0],
                        target_vertex[1] - source_vertex[1],
                    )
                    candidate = frozenset(
                        frozenset(
                            (
                                point[0] + translation[0],
                                point[1] + translation[1],
                            )
                            for point in cell
                        )
                        for cell in rotated
                    )
                    if candidate & triangles:
                        continue
                    candidate_disk, _, candidate_boundary = (
                        _triangle_union_boundary(candidate)
                    )
                    if not candidate_disk or not (boundary & candidate_boundary):
                        continue
                    union = triangles | candidate
                    union_disk, _, _ = _triangle_union_boundary(union)
                    if not union_disk:
                        continue
                    key = tuple(sorted(
                        _cell_from_triangle_vertices(cell) for cell in candidate
                    ))
                    extensions[key] = candidate
    return tuple(extensions[key] for key in sorted(extensions))


def _contained_support_embeddings(container, native_cells):
    """Every full-isometry image of native_cells contained in container."""

    container = frozenset(container)
    container_vertices = sorted(set().union(*container))
    embeddings = {}
    for reflected in (False, True):
        for rotation in range(6):
            rotated = _transform_cell_set(native_cells, rotation, reflected, (0, 0))
            rotated_vertices = sorted(set().union(*rotated))
            for source_vertex in rotated_vertices:
                for target_vertex in container_vertices:
                    translation = (
                        target_vertex[0] - source_vertex[0],
                        target_vertex[1] - source_vertex[1],
                    )
                    candidate = frozenset(
                        frozenset(
                            (
                                point[0] + translation[0],
                                point[1] + translation[1],
                            )
                            for point in cell
                        )
                        for cell in rotated
                    )
                    if not candidate <= container:
                        continue
                    key = tuple(sorted(
                        _cell_from_triangle_vertices(cell) for cell in candidate
                    ))
                    embeddings[key] = candidate
    return tuple(embeddings[key] for key in sorted(embeddings))


def build_area30_carrier_classification(atlas: dict) -> dict:
    """Classify the exact K65A two-large area-30 carrier superset."""

    verify_atlas(atlas)
    macro_cells = {
        name: tuple(tuple(cell) for cell in atlas["supports"][name]["cells"])
        for name in ("large_A", "large_B")
    }

    support_sources = {}
    for first_name in ("large_A", "large_B"):
        first = _transform_cell_set(
            macro_cells[first_name], 0, False, (0, 0)
        )
        for second_name in ("large_A", "large_B"):
            for second in _attached_support_extensions(
                first, macro_cells[second_name]
            ):
                union = first | second
                canonical = _canonical_triangle_support(union)
                support_sources.setdefault(canonical, set()).add(
                    (first_name, second_name)
                )

    supports = []
    matching_cache = {}
    total_z_matchings = 0
    total_z_bipartite = 0
    total_g_embeddings = 0
    total_g_matchings = 0
    total_g_bipartite = 0

    def matching_data(triangles):
        canonical = _canonical_triangle_support(triangles)
        if canonical not in matching_cache:
            representative = frozenset(
                frozenset(point for point in triangle) for triangle in canonical
            )
            matching_cache[canonical] = _all_singleton_subdivisions(representative)
        return matching_cache[canonical]

    for canonical in sorted(support_sources):
        support = frozenset(
            frozenset(point for point in triangle) for triangle in canonical
        )
        disk, boundary_cycle, _ = _triangle_union_boundary(support)
        if not disk or len(support) != 60:
            raise ValueError("area-30 two-large support is not a 60-triangle disk")

        z_count, z_bipartite, z_cycle = matching_data(support)
        total_z_matchings += z_count
        total_z_bipartite += len(z_bipartite)

        g_records = []
        for macro_name in ("large_A", "large_B"):
            for embedding in _contained_support_embeddings(
                support, macro_cells[macro_name]
            ):
                residual = support - embedding
                if len(residual) != 30:
                    raise ValueError("area-30 G residual is not 30 triangles")
                residual_disk, _, _ = _triangle_union_boundary(residual)
                count, bipartite, cycle = matching_data(residual)
                total_g_embeddings += 1
                total_g_matchings += count
                total_g_bipartite += len(bipartite)
                g_records.append({
                    "macro": macro_name,
                    "macro_primitive_cells": [
                        list(cell) for cell in sorted(
                            _cell_from_triangle_vertices(item)
                            for item in embedding
                        )
                    ],
                    "residual_is_disk": residual_disk,
                    "perfect_matching_count": count,
                    "bipartite_matching_count": len(bipartite),
                    "bipartite_subdivisions_diagonals_uv": [
                        _serialized_diagonals(item) for item in bipartite
                    ],
                    "shortest_odd_cycle_edges_uv": _serialized_diagonals(
                        tuple(
                            (cycle[index], cycle[(index + 1) % len(cycle)])
                            for index in range(len(cycle))
                        )
                        if cycle is not None
                        else None
                    ),
                })

        supports.append({
            "source_macro_type_pairs": [
                list(item) for item in sorted(support_sources[canonical])
            ],
            "primitive_cells": [
                list(_cell_from_triangle_vertices(item))
                for item in sorted(support, key=lambda cell: tuple(sorted(cell)))
            ],
            "boundary_vertices_uv": [list(point) for point in boundary_cycle],
            "Z": {
                "perfect_matching_count": z_count,
                "bipartite_matching_count": len(z_bipartite),
                "bipartite_subdivisions_diagonals_uv": [
                    _serialized_diagonals(item) for item in z_bipartite
                ],
                "shortest_odd_cycle_edges_uv": _serialized_diagonals(
                    tuple(
                        (z_cycle[index], z_cycle[(index + 1) % len(z_cycle)])
                        for index in range(len(z_cycle))
                    )
                    if z_cycle is not None
                    else None
                ),
            },
            "G_embedding_count": len(g_records),
            "G": g_records,
        })

    return {
        "schema": "ahi-sturmian-area30-carrier-classification-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "scope": {
            "H_state": "two exact published large macros in a disk union",
            "G_state": "one contained exact large macro plus 15 singleton rhombi",
            "Z_state": "30 singleton rhombi",
            "source_rule_filter": (
                "singleton long-diagonal bipartiteness only; all supports "
                "and embeddings form a geometric superset"
            ),
        },
        "support_count": len(supports),
        "matching_cache_class_count": len(matching_cache),
        "Z_perfect_matching_count": total_z_matchings,
        "Z_bipartite_matching_count": total_z_bipartite,
        "G_embedding_count": total_g_embeddings,
        "G_perfect_matching_count": total_g_matchings,
        "G_bipartite_matching_count": total_g_bipartite,
        "area30_parity_survivor_count": (
            total_z_bipartite + total_g_bipartite
        ),
        "area30_fails_parity": (
            total_z_bipartite + total_g_bipartite == 0
        ),
        "supports": supports,
    }


def verify_area30_carrier_classification(data: dict, atlas: dict) -> None:
    expected = build_area30_carrier_classification(atlas)
    if data != expected:
        raise ValueError(
            "serialized area-30 carrier classification differs from exact rebuild"
        )


def _cell_from_triangle_vertices(triangle):
    minimum_u = min(point[0] for point in triangle)
    minimum_v = min(point[1] for point in triangle)
    for u in range(minimum_u - 1, minimum_u + 2):
        for v in range(minimum_v - 1, minimum_v + 2):
            for orientation in ("U", "D"):
                cell = (u, v, orientation)
                if frozenset(_triangle_vertices(cell)) == triangle:
                    return cell
    raise ValueError("triangle vertex set is not a primitive lattice cell")


def _translation_fundamental_domains(cells):
    by_orientation = {
        orientation: [(u, v) for u, v, cell_orientation in cells
                      if cell_orientation == orientation]
        for orientation in ("U", "D")
    }
    if len(by_orientation["U"]) != len(by_orientation["D"]):
        return 0, []
    index = len(by_orientation["U"])
    certificates = []
    tested = 0
    for horizontal, shear, vertical in _hnf_sublattices(index):
        tested += 1
        if all(
            len({
                _hnf_residue(u, v, horizontal, shear, vertical)
                for u, v in by_orientation[orientation]
            }) == index
            for orientation in ("U", "D")
        ):
            certificates.append({
                "basis_uv": [[horizontal, 0], [shear, vertical]],
                "determinant": index,
            })
    return tested, certificates


def build_seventeen_rhombus_periodicity(atlas: dict, kernel: dict) -> dict:
    """Test one/two-copy translation fundamental domains for K56C."""

    verify_atlas(atlas)
    verify_common_support_kernel(kernel, atlas)
    equalizer = kernel["two_rhombus_equalizers"][0]
    cells_a = _transform_cell_set(
        atlas["supports"]["large_A"]["cells"], 0, False, (0, 0)
    )
    cells_b = _transform_cell_set(
        atlas["supports"]["large_B"]["cells"],
        equalizer["rotation"],
        equalizer["reflected"],
        tuple(equalizer["translation_uv"]),
    )
    support = cells_a | cells_b
    if len(support) != 34:
        raise ValueError("17-rhombus support must have 34 primitive triangles")
    one_cells = tuple(sorted(_cell_from_triangle_vertices(cell) for cell in support))
    one_tested, one_certificates = _translation_fundamental_domains(one_cells)

    _, _, base_boundary = _triangle_union_boundary(support)
    unions = {}
    for reflected in (False, True):
        for rotation in range(6):
            transformed_zero = frozenset(
                frozenset(
                    _linear_isometry(point, rotation, reflected)
                    for point in triangle
                )
                for triangle in support
            )
            _, _, transformed_boundary = _triangle_union_boundary(transformed_zero)
            for base_edge in base_boundary:
                for moving_edge in transformed_boundary:
                    for moving_anchor in moving_edge:
                        translation = (
                            base_edge[0][0] - moving_anchor[0],
                            base_edge[0][1] - moving_anchor[1],
                        )
                        translated_edge = _edge(*(
                            (
                                point[0] + translation[0],
                                point[1] + translation[1],
                            )
                            for point in moving_edge
                        ))
                        if translated_edge != base_edge:
                            continue
                        transformed = frozenset(
                            frozenset(
                                (
                                    point[0] + translation[0],
                                    point[1] + translation[1],
                                )
                                for point in triangle
                            )
                            for triangle in transformed_zero
                        )
                        if support & transformed:
                            continue
                        union = support | transformed
                        key = tuple(sorted(tuple(sorted(cell)) for cell in union))
                        unions.setdefault(key, {
                            "rotation": rotation,
                            "reflected": reflected,
                            "translation_uv": list(translation),
                            "triangles": union,
                        })

    two_certificates = []
    hnf_tests = 0
    for item in unions.values():
        union_cells = tuple(sorted(
            _cell_from_triangle_vertices(cell) for cell in item["triangles"]
        ))
        tested, certificates = _translation_fundamental_domains(union_cells)
        hnf_tests += tested
        for certificate in certificates:
            two_certificates.append({
                "copy_pose": {
                    key: value for key, value in item.items() if key != "triangles"
                },
                "translation_lattice": certificate,
            })
    return {
        "schema": "ahi-sturmian-seventeen-rhombus-periodicity-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "common_support_kernel_sha256": hashlib.sha256(
            (json.dumps(kernel, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "one_copy": {
            "forced_index": 17,
            "hnf_count_tested": one_tested,
            "translation_fundamental_domain_count": len(one_certificates),
            "translation_fundamental_domains": one_certificates,
        },
        "two_copy": {
            "edge_connected_union_count": len(unions),
            "forced_index": 34,
            "hnf_tests_across_unions": hnf_tests,
            "translation_fundamental_domain_count": len(two_certificates),
            "translation_fundamental_domains": sorted(
                two_certificates,
                key=lambda item: (
                    item["copy_pose"]["reflected"],
                    item["copy_pose"]["rotation"],
                    item["copy_pose"]["translation_uv"],
                    item["translation_lattice"]["basis_uv"],
                ),
            ),
        },
    }


def verify_seventeen_rhombus_periodicity(
    data: dict, atlas: dict, kernel: dict
) -> None:
    expected = build_seventeen_rhombus_periodicity(atlas, kernel)
    if data != expected:
        raise ValueError("serialized 17-rhombus periodicity census differs from rebuild")


def _determinant_three_similarity(point):
    """Multiply the Eisenstein coordinate by 1-omega (norm three)."""

    u, v = point
    return (u + v, -u + 2 * v)


def _tile_triangles_from_serialized_assembly(assembly: dict):
    result = []
    for tile_index, tile in enumerate(assembly["tiles"]):
        vertices = [(0, 0)]
        for direction_index in tile["boundary_directions"]:
            direction = DIRECTIONS[direction_index]
            vertices.append((
                vertices[-1][0] + direction[0],
                vertices[-1][1] + direction[1],
            ))
        translation = tile["translation_uv"]
        triangles = frozenset(
            frozenset(
                (point[0] + translation[0], point[1] + translation[1])
                for point in _triangle_vertices(cell)
            )
            for cell in triangle_cells(tuple(vertices[:-1]))
        )
        result.append({
            "tile_index": tile_index,
            "source_type": tile["source_type"],
            "triangles": triangles,
        })
    return result


def _support_mapping_witnesses(first, second):
    first_vertices = set().union(*first)
    second_vertices = set().union(*second)
    anchor = min(first_vertices)
    witnesses = []
    for reflected in (False, True):
        for rotation in range(6):
            transformed_anchor = _linear_isometry(anchor, rotation, reflected)
            for target in second_vertices:
                translation = (
                    target[0] - transformed_anchor[0],
                    target[1] - transformed_anchor[1],
                )
                transformed = frozenset(
                    frozenset(
                        (
                            _linear_isometry(point, rotation, reflected)[0]
                            + translation[0],
                            _linear_isometry(point, rotation, reflected)[1]
                            + translation[1],
                        )
                        for point in triangle
                    )
                    for triangle in first
                )
                if transformed == second:
                    witnesses.append({
                        "rotation": rotation,
                        "reflected": reflected,
                        "translation_uv": list(translation),
                    })
    return sorted(
        witnesses,
        key=lambda item: (
            item["reflected"], item["rotation"], item["translation_uv"]
        ),
    )


def build_seventeen_rhombus_rep3(
    atlas: dict, kernel: dict, pairs: dict
) -> dict:
    """Test whether the 51-rhombus source flip is an inflated K56C tile."""

    verify_atlas(atlas)
    verify_common_support_kernel(kernel, atlas)
    if pairs.get("schema") != "ahi-sturmian-interchangeable-pairs-v1":
        raise ValueError("unsupported interchangeable-pair schema")
    equalizer = kernel["two_rhombus_equalizers"][0]
    small_support = _transform_cell_set(
        atlas["supports"]["large_A"]["cells"], 0, False, (0, 0)
    ) | _transform_cell_set(
        atlas["supports"]["large_B"]["cells"],
        equalizer["rotation"],
        equalizer["reflected"],
        tuple(equalizer["translation_uv"]),
    )
    is_disk, small_boundary_cycle, _ = _triangle_union_boundary(small_support)
    if not is_disk or len(small_support) != 34:
        raise ValueError("K56C support is not the expected 17-rhombus disk")
    scaled_boundary = tuple(
        _determinant_three_similarity(point) for point in small_boundary_cycle
    )
    scaled_cells = triangle_cells(scaled_boundary)
    scaled_support = frozenset(
        frozenset(_triangle_vertices(cell)) for cell in scaled_cells
    )
    if len(scaled_support) != 102:
        raise ValueError("determinant-three image does not have triple area")

    panel_results = []
    for panel in (0, 1):
        assembly = pairs["assemblies"][panel]
        tiles = _tile_triangles_from_serialized_assembly(assembly)
        assembly_support = frozenset().union(
            *(tile["triangles"] for tile in tiles)
        )
        similarity_witnesses = _support_mapping_witnesses(
            scaled_support, assembly_support
        )
        large_tiles = [
            tile for tile in tiles if tile["source_type"] == "large_A"
        ]
        small_tiles = [
            tile for tile in tiles if tile["source_type"] == "small_M"
        ]
        admissible_groups = {tile["tile_index"]: [] for tile in large_tiles}
        for large in large_tiles:
            for first_index in range(len(small_tiles)):
                for second_index in range(first_index + 1, len(small_tiles)):
                    first = small_tiles[first_index]
                    second = small_tiles[second_index]
                    group_support = (
                        large["triangles"] | first["triangles"] | second["triangles"]
                    )
                    if len(group_support) != 34:
                        continue
                    if _canonical_triangle_support(group_support) != (
                        _canonical_triangle_support(small_support)
                    ):
                        continue
                    admissible_groups[large["tile_index"]].append(
                        tuple(sorted((first["tile_index"], second["tile_index"])))
                    )

        partitions = []
        ordered_large = sorted(admissible_groups)

        def extend(position, used_small, selected):
            if position == len(ordered_large):
                if len(used_small) == len(small_tiles):
                    partitions.append([
                        {
                            "large_A_tile_index": large_index,
                            "small_M_tile_indices": list(pair),
                        }
                        for large_index, pair in selected
                    ])
                return
            large_index = ordered_large[position]
            for pair in admissible_groups[large_index]:
                if set(pair) & used_small:
                    continue
                extend(
                    position + 1,
                    used_small | set(pair),
                    selected + [(large_index, pair)],
                )

        extend(0, set(), [])
        panel_results.append({
            "panel": panel,
            "similarity_witness_count": len(similarity_witnesses),
            "similarity_witnesses": similarity_witnesses,
            "admissible_group_counts": {
                str(key): len(value) for key, value in sorted(admissible_groups.items())
            },
            "three_tile_partition_count": len(partitions),
            "three_tile_partitions": sorted(
                partitions,
                key=lambda partition: tuple(
                    (item["large_A_tile_index"], item["small_M_tile_indices"])
                    for item in partition
                ),
            ),
        })
    return {
        "schema": "ahi-sturmian-seventeen-rhombus-rep3-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "common_support_kernel_sha256": hashlib.sha256(
            (json.dumps(kernel, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "interchangeable_pairs_sha256": hashlib.sha256(
            (json.dumps(pairs, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "small_rhombus_count": 17,
        "inflated_rhombus_count": 51,
        "similarity_matrix_uv": [[1, 1], [-1, 2]],
        "similarity_determinant": 3,
        "panels": panel_results,
    }


def verify_seventeen_rhombus_rep3(
    data: dict, atlas: dict, kernel: dict, pairs: dict
) -> None:
    expected = build_seventeen_rhombus_rep3(atlas, kernel, pairs)
    if data != expected:
        raise ValueError("serialized 17-rhombus rep-3 result differs from rebuild")


def _one_two_copy_translation_census(support):
    one_cells = tuple(sorted(_cell_from_triangle_vertices(cell) for cell in support))
    one_tested, one_certificates = _translation_fundamental_domains(one_cells)
    _, _, base_boundary = _triangle_union_boundary(support)
    unions = {}
    for reflected in (False, True):
        for rotation in range(6):
            transformed_zero = frozenset(
                frozenset(
                    _linear_isometry(point, rotation, reflected)
                    for point in triangle
                )
                for triangle in support
            )
            _, _, moving_boundary = _triangle_union_boundary(transformed_zero)
            for base_edge in base_boundary:
                for moving_edge in moving_boundary:
                    for moving_anchor in moving_edge:
                        translation = (
                            base_edge[0][0] - moving_anchor[0],
                            base_edge[0][1] - moving_anchor[1],
                        )
                        translated_edge = _edge(*(
                            (
                                point[0] + translation[0],
                                point[1] + translation[1],
                            )
                            for point in moving_edge
                        ))
                        if translated_edge != base_edge:
                            continue
                        transformed = frozenset(
                            frozenset(
                                (
                                    point[0] + translation[0],
                                    point[1] + translation[1],
                                )
                                for point in triangle
                            )
                            for triangle in transformed_zero
                        )
                        if support & transformed:
                            continue
                        union = support | transformed
                        key = tuple(sorted(tuple(sorted(cell)) for cell in union))
                        unions.setdefault(key, {
                            "rotation": rotation,
                            "reflected": reflected,
                            "translation_uv": list(translation),
                            "triangles": union,
                        })
    two_certificates = []
    two_hnf_tests = 0
    for item in unions.values():
        union_cells = tuple(sorted(
            _cell_from_triangle_vertices(cell) for cell in item["triangles"]
        ))
        tested, certificates = _translation_fundamental_domains(union_cells)
        two_hnf_tests += tested
        for certificate in certificates:
            two_certificates.append({
                "copy_pose": {
                    key: value for key, value in item.items() if key != "triangles"
                },
                "translation_lattice": certificate,
            })
    return {
        "one_copy": {
            "forced_index": len(support) // 2,
            "hnf_count_tested": one_tested,
            "translation_fundamental_domain_count": len(one_certificates),
            "translation_fundamental_domains": one_certificates,
        },
        "two_copy": {
            "edge_connected_union_count": len(unions),
            "forced_index": len(support),
            "hnf_tests_across_unions": two_hnf_tests,
            "translation_fundamental_domain_count": len(two_certificates),
            "translation_fundamental_domains": sorted(
                two_certificates,
                key=lambda item: (
                    item["copy_pose"]["reflected"],
                    item["copy_pose"]["rotation"],
                    item["copy_pose"]["translation_uv"],
                    item["translation_lattice"]["basis_uv"],
                ),
            ),
        },
    }


def build_fiftyone_envelope_periodicity(pairs: dict, rep3: dict) -> dict:
    """Test the Figure 45 51-rhombus envelope as a periodic P macro."""

    if pairs.get("schema") != "ahi-sturmian-interchangeable-pairs-v1":
        raise ValueError("unsupported interchangeable-pair schema")
    if rep3.get("schema") != "ahi-sturmian-seventeen-rhombus-rep3-v1":
        raise ValueError("unsupported 17-rhombus three-tile schema")
    if not all(panel["three_tile_partition_count"] for panel in rep3["panels"]):
        raise ValueError("51-rhombus envelope lacks a proved three-tile partition")
    cells = _serialized_assembly_cells(pairs["assemblies"][0])
    support = frozenset(
        frozenset(_triangle_vertices(cell)) for cell in cells
    )
    result = _one_two_copy_translation_census(support)
    return {
        "schema": "ahi-sturmian-fiftyone-envelope-periodicity-v1",
        "interchangeable_pairs_sha256": hashlib.sha256(
            (json.dumps(pairs, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "rep3_artifact_sha256": hashlib.sha256(
            (json.dumps(rep3, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        **result,
    }


def verify_fiftyone_envelope_periodicity(
    data: dict, pairs: dict, rep3: dict
) -> None:
    expected = build_fiftyone_envelope_periodicity(pairs, rep3)
    if data != expected:
        raise ValueError("serialized 51-rhombus macro periodicity differs from rebuild")
