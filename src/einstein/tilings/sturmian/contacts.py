"""Exact contact languages and local quotients for the reconstructed AHI source."""

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
    _edge,
    _linear_isometry,
    _sab_corridor_bits,
    _sab_screen_direction,
    _source_sab_graph,
    _triangle_vertices,
    extract_sab_polylines,
    sha256_path,
    verify_atlas,
)

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


def _corridor_germ_embeddings(paths, cells, serialized_components):
    """Lift source paths to endpoint-specific bent-SAB direction germs.

    The two germs are stored at the lexicographically ordered endpoints of
    the limiting long diagonal.  A germ direction points from the collapsed
    boundary endpoint into the marked SAB path.  Unlike the corridor quotient,
    this record retains exactly the boundary data needed to test continuation
    across an edge of two source cells.
    """

    graph_points, graph_edges, roles = _source_sab_graph(paths)
    bits = tuple(_sab_corridor_bits(path) for path in paths)
    source_germs = tuple(
        (
            _sab_screen_direction(
                path[1][0] - path[0][0], path[1][1] - path[0][1]
            ),
            (
                _sab_screen_direction(
                    path[3][0] - path[2][0], path[3][1] - path[2][1]
                )
                + 3
            )
            % 6,
        )
        for path in paths
    )
    support_vertices = set().union(
        *(set(_triangle_vertices(cell)) for cell in cells)
    )
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
            transform_direction = lambda index: (
                (rotation - index) % 6
                if reflected
                else (index + rotation) % 6
            )
            adjacency = {index: [] for index in range(len(graph_points))}
            for first, second in graph_edges:
                delta = (
                    graph_points[second][0] - graph_points[first][0],
                    graph_points[second][1] - graph_points[first][1],
                )
                step = LONG_DIAGONALS[transform_direction(DIRECTIONS.index(delta))]
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
                    (point[0] + translation[0], point[1] + translation[1])
                    for point in points
                )
                selected = tuple(
                    _edge(placed[first], placed[second])
                    for first, second in graph_edges
                )
                if frozenset(zip(roles, selected)) != target:
                    continue
                records = []
                for index, (first, second) in enumerate(graph_edges):
                    start, end = placed[first], placed[second]
                    start_germ, end_germ = (
                        transform_direction(source_germs[index][0]),
                        transform_direction(source_germs[index][1]),
                    )
                    if start > end:
                        start_germ, end_germ = end_germ, start_germ
                    records.append(
                        (
                            selected[index],
                            tuple(reversed(bits[index])) if reflected else bits[index],
                            (start_germ, end_germ),
                            roles[index],
                        )
                    )
                solutions.add(frozenset(records))
    if not solutions:
        raise ValueError("the fixed source atlas has no endpoint-germ lift")
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
