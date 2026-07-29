"""Exact finite compilers, germ languages and local obstructions."""

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
    EXAMPLE1_SHA256,
    LONG_DIAGONALS,
    SOURCE_ARCHIVE_SHA256,
    _edge,
    _linear_isometry,
    _triangle_vertices,
    extract_sab_polylines,
    sha256_path,
    triangle_cells,
    verify_atlas,
)

from .sturmian_contacts import (
    _component_axis,
    _corridor_germ_embeddings,
)

from .sturmian_geometry import (
    _component_rhombi,
    _transform_cell_set,
    _transform_rhombi,
    verify_common_support_kernel,
)

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


def _rhombus_long_diagonal(rhombus):
    candidates = []
    points = tuple(rhombus)
    for first_index in range(len(points)):
        for second_index in range(first_index + 1, len(points)):
            first, second = points[first_index], points[second_index]
            delta = (second[0] - first[0], second[1] - first[1])
            if any(
                delta == direction or delta == (-direction[0], -direction[1])
                for direction in LONG_DIAGONALS
            ):
                candidates.append(_edge(first, second))
    if len(candidates) != 1:
        raise ValueError("common rhombus has no unique long diagonal")
    return candidates[0]


def _rhombus_contact_signature(rhombi):
    contacts = []
    for first_index, first in enumerate(rhombi):
        for second_index in range(first_index):
            second = rhombi[second_index]
            shared = first & second
            if len(shared) != 2:
                continue
            edge = _edge(*shared)
            delta = (
                edge[1][0] - edge[0][0], edge[1][1] - edge[0][1]
            )
            if not any(
                delta == direction or delta == (-direction[0], -direction[1])
                for direction in DIRECTIONS
            ):
                continue
            first_endpoint = next(
                point for point in edge if point in _rhombus_long_diagonal(first)
            )
            second_endpoint = next(
                point for point in edge if point in _rhombus_long_diagonal(second)
            )
            contacts.append({
                "edge_uv": [list(point) for point in edge],
                "sab_endpoint_uv": list(first_endpoint),
                "continues": first_endpoint == second_endpoint,
            })
    return sorted(
        contacts,
        key=lambda item: (item["edge_uv"], item["sab_endpoint_uv"]),
    )


def _outer_sab_signature(rhombi):
    edge_owners = {}
    for rhombus in rhombi:
        points = tuple(rhombus)
        diagonal = _rhombus_long_diagonal(rhombus)
        for first_index in range(len(points)):
            for second_index in range(first_index + 1, len(points)):
                edge = _edge(points[first_index], points[second_index])
                delta = (
                    edge[1][0] - edge[0][0], edge[1][1] - edge[0][1]
                )
                if not any(
                    delta == direction
                    or delta == (-direction[0], -direction[1])
                    for direction in DIRECTIONS
                ):
                    continue
                # The other unit segment in a 60/120 rhombus is its short
                # internal diagonal.  A boundary side has exactly one long-
                # diagonal endpoint.
                if sum(point in diagonal for point in edge) != 1:
                    continue
                edge_owners.setdefault(edge, []).append(rhombus)
    signature = []
    for edge, owners in edge_owners.items():
        if len(owners) != 1:
            continue
        endpoint = next(
            point for point in edge
            if point in _rhombus_long_diagonal(owners[0])
        )
        signature.append({
            "edge_uv": [list(point) for point in edge],
            "sab_endpoint_uv": list(endpoint),
        })
    return sorted(signature, key=lambda item: item["edge_uv"])


def _grouping_isometries(common_rhombi, first_macro, second_macro):
    common_vertices = set().union(*common_rhombi)
    anchor = min(common_vertices)
    witnesses = []
    for reflected in (False, True):
        for rotation in range(6):
            transformed_anchor = _linear_isometry(anchor, rotation, reflected)
            for target in common_vertices:
                translation = (
                    target[0] - transformed_anchor[0],
                    target[1] - transformed_anchor[1],
                )
                transformed_common = _transform_rhombi(
                    common_rhombi, rotation, reflected, translation
                )
                if transformed_common != common_rhombi:
                    continue
                transformed_macro = _transform_rhombi(
                    first_macro, rotation, reflected, translation
                )
                if transformed_macro != second_macro:
                    continue
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


def build_seventeen_rhombus_source_compiler(atlas: dict, kernel: dict) -> dict:
    """Test K54R as the legal source relation A+2M <-> B+2M."""

    verify_atlas(atlas)
    verify_common_support_kernel(kernel, atlas)
    rhombi_a = _component_rhombi(atlas["supports"]["large_A"])
    rhombi_b_zero = _component_rhombi(atlas["supports"]["large_B"])
    records = []
    for equalizer in kernel["two_rhombus_equalizers"]:
        rotation = equalizer["rotation"]
        reflected = equalizer["reflected"]
        translation = tuple(equalizer["translation_uv"])
        rhombi_b = _transform_rhombi(
            rhombi_b_zero, rotation, reflected, translation
        )
        common = rhombi_a | rhombi_b
        added_to_a = rhombi_b - rhombi_a
        added_to_b = rhombi_a - rhombi_b
        if len(common) != 17 or len(added_to_a) != 2 or len(added_to_b) != 2:
            raise ValueError("K54R equalizer no longer has 17/2/2 census")
        decomposition_a = tuple(sorted(
            rhombi_a | added_to_a, key=lambda item: tuple(sorted(item))
        ))
        decomposition_b = tuple(sorted(
            rhombi_b | added_to_b, key=lambda item: tuple(sorted(item))
        ))
        contacts_a = _rhombus_contact_signature(decomposition_a)
        contacts_b = _rhombus_contact_signature(decomposition_b)
        outer_a = _outer_sab_signature(decomposition_a)
        outer_b = _outer_sab_signature(decomposition_b)
        grouping_witnesses = _grouping_isometries(
            common, rhombi_a, rhombi_b
        )
        records.append({
            "rotation": rotation,
            "reflected": reflected,
            "translation_uv": list(translation),
            "common_rhombus_count": len(common),
            "added_singleton_count_per_side": 2,
            "internal_contact_count": len(contacts_a),
            "all_A_plus_2M_contacts_continue": all(
                item["continues"] for item in contacts_a
            ),
            "all_B_plus_2M_contacts_continue": all(
                item["continues"] for item in contacts_b
            ),
            "outer_sab_signatures_equal": outer_a == outer_b,
            "outer_sab_signature": outer_a if outer_a == outer_b else None,
            "groupings_same_full_isometry_orbit": bool(grouping_witnesses),
            "grouping_isometries": grouping_witnesses,
            "failing_A_contacts": [
                item for item in contacts_a if not item["continues"]
            ],
            "failing_B_contacts": [
                item for item in contacts_b if not item["continues"]
            ],
        })
    return {
        "schema": "ahi-sturmian-seventeen-rhombus-compiler-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "common_support_kernel_sha256": hashlib.sha256(
            (json.dumps(kernel, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "equalizer_count": len(records),
        "equalizers": records,
    }


def verify_seventeen_rhombus_source_compiler(
    data: dict, atlas: dict, kernel: dict
) -> None:
    expected = build_seventeen_rhombus_source_compiler(atlas, kernel)
    if data != expected:
        raise ValueError("serialized 17-rhombus source compiler differs from rebuild")


def _component_rhombus(component):
    vertices = set()
    for raw_cell in component["primitive_cells"]:
        vertices.update(_triangle_vertices(tuple(raw_cell)))
    if len(vertices) != 4:
        raise ValueError("a source component does not form one rhombus")
    return frozenset(vertices)


def _germ_solution_by_rhombus(solution, support):
    by_diagonal = {record[0]: record for record in solution}
    result = {}
    for component in support["sab_components"]:
        diagonal = _edge(*(
            tuple(point) for point in component["diagonal_uv"]
        ))
        record = by_diagonal[diagonal]
        rhombus = _component_rhombus(component)
        result[rhombus] = {
            "diagonal": record[0],
            "corridor_bits": record[1],
            "endpoint_germs": record[2],
            "role": record[3],
        }
    return result


def _transform_germ_state(state, rotation, reflected, translation):
    transform_direction = lambda index: (
        (rotation - index) % 6 if reflected else (index + rotation) % 6
    )
    old_diagonal = state["diagonal"]
    mapped_endpoints = tuple(
        (
            _linear_isometry(point, rotation, reflected)[0] + translation[0],
            _linear_isometry(point, rotation, reflected)[1] + translation[1],
        )
        for point in old_diagonal
    )
    mapped_germs = tuple(
        transform_direction(germ) for germ in state["endpoint_germs"]
    )
    if mapped_endpoints[0] > mapped_endpoints[1]:
        mapped_germs = tuple(reversed(mapped_germs))
    return {
        "diagonal": _edge(*mapped_endpoints),
        "corridor_bits": (
            tuple(reversed(state["corridor_bits"]))
            if reflected
            else state["corridor_bits"]
        ),
        "endpoint_germs": mapped_germs,
        "role": state["role"],
    }


def _transform_germ_macro(states, rotation, reflected, translation):
    return {
        frozenset(
            (
                _linear_isometry(point, rotation, reflected)[0] + translation[0],
                _linear_isometry(point, rotation, reflected)[1] + translation[1],
            )
            for point in rhombus
        ): _transform_germ_state(state, rotation, reflected, translation)
        for rhombus, state in states.items()
    }


def _singleton_germ_states_on_rhombus(native_solutions, native_support, target):
    native_rhombus = next(iter(native_support))
    anchor = min(native_rhombus)
    result = {}
    for solution in native_solutions:
        native_state = next(iter(solution.values()))
        for reflected in (False, True):
            for rotation in range(6):
                transformed_anchor = _linear_isometry(anchor, rotation, reflected)
                for target_anchor in target:
                    translation = (
                        target_anchor[0] - transformed_anchor[0],
                        target_anchor[1] - transformed_anchor[1],
                    )
                    transformed_rhombus = frozenset(
                        (
                            _linear_isometry(point, rotation, reflected)[0]
                            + translation[0],
                            _linear_isometry(point, rotation, reflected)[1]
                            + translation[1],
                        )
                        for point in native_rhombus
                    )
                    if transformed_rhombus != target:
                        continue
                    state = _transform_germ_state(
                        native_state, rotation, reflected, translation
                    )
                    key = (
                        state["diagonal"],
                        state["corridor_bits"],
                        state["endpoint_germs"],
                    )
                    result[key] = state
    return tuple(result[key] for key in sorted(result))


def _full_germ_contacts(states):
    contacts = []
    rhombi = tuple(states)
    for first_index, first in enumerate(rhombi):
        for second_index in range(first_index):
            second = rhombi[second_index]
            shared = first & second
            if len(shared) != 2:
                continue
            edge = _edge(*shared)
            delta = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
            if delta not in DIRECTIONS and (-delta[0], -delta[1]) not in DIRECTIONS:
                continue
            first_state, second_state = states[first], states[second]
            first_endpoint = next(
                point for point in edge if point in first_state["diagonal"]
            )
            second_endpoint = next(
                point for point in edge if point in second_state["diagonal"]
            )

            def germ_at(state, endpoint):
                return state["endpoint_germs"][state["diagonal"].index(endpoint)]

            contacts.append({
                "edge_uv": tuple(edge),
                "first_endpoint": first_endpoint,
                "second_endpoint": second_endpoint,
                "first_germ": germ_at(first_state, first_endpoint),
                "second_germ": germ_at(second_state, second_endpoint),
                "germ_difference_mod_6": (
                    germ_at(second_state, second_endpoint)
                    - germ_at(first_state, first_endpoint)
                )
                % 6,
            })
    return tuple(sorted(
        contacts,
        key=lambda item: (
            item["edge_uv"], item["first_endpoint"], item["second_endpoint"]
        ),
    ))


def _full_outer_germ_signature(states):
    edge_owners = {}
    for rhombus, state in states.items():
        points = tuple(rhombus)
        for first_index in range(len(points)):
            for second_index in range(first_index + 1, len(points)):
                edge = _edge(points[first_index], points[second_index])
                delta = (edge[1][0] - edge[0][0], edge[1][1] - edge[0][1])
                if delta not in DIRECTIONS and (-delta[0], -delta[1]) not in DIRECTIONS:
                    continue
                if sum(point in state["diagonal"] for point in edge) != 1:
                    continue
                edge_owners.setdefault(edge, []).append((rhombus, state))
    signature = []
    for edge, owners in edge_owners.items():
        if len(owners) != 1:
            continue
        _, state = owners[0]
        endpoint = next(point for point in edge if point in state["diagonal"])
        germ = state["endpoint_germs"][state["diagonal"].index(endpoint)]
        signature.append((edge, endpoint, germ))
    return tuple(sorted(signature))


def _outer_germ_compatibility_signature(states, allowed_differences):
    """Return the exterior germs compatible with each exposed SAB endpoint."""

    signature = []
    for edge, endpoint, interior_germ in _full_outer_germ_signature(states):
        exterior = tuple(
            direction
            for direction in range(6)
            if (direction - interior_germ) % 6 in allowed_differences
        )
        signature.append((edge, endpoint, exterior))
    return tuple(sorted(signature))


def build_seventeen_rhombus_full_germs(
    archive_path: Path, atlas: dict, kernel: dict
) -> dict:
    """Decide the fixed 17-rhombus relation under full SAB endpoint germs."""

    verify_atlas(atlas)
    verify_common_support_kernel(kernel, atlas)
    if sha256_path(archive_path) != SOURCE_ARCHIVE_SHA256:
        raise ValueError("source archive hash mismatch")
    with tempfile.TemporaryDirectory(prefix="ahi-full-germs-") as directory:
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
                "pdftocairo", "-svg", "-f", "1", "-l", "1",
                str(pdf_path), str(svg_path),
            ],
            check=True,
        )
        paths = extract_sab_polylines(svg_path)

    macro_states = {}
    embedding_counts = {}
    for macro_name in ("large_A", "large_B"):
        support = atlas["supports"][macro_name]
        solutions = _corridor_germ_embeddings(
            paths[macro_name],
            tuple(tuple(cell) for cell in support["cells"]),
            support["sab_components"],
        )
        embedding_counts[macro_name] = len(solutions)
        if len(solutions) != 1:
            raise ValueError("published macro has a non-unique endpoint-germ lift")
        macro_states[macro_name] = _germ_solution_by_rhombus(
            next(iter(solutions)), support
        )

    small_support = atlas["supports"]["small_M"]
    small_solutions_raw = _corridor_germ_embeddings(
        paths["small_M"],
        tuple(tuple(cell) for cell in small_support["cells"]),
        small_support["sab_components"],
    )
    small_solutions = tuple(
        _germ_solution_by_rhombus(solution, small_support)
        for solution in small_solutions_raw
    )
    embedding_counts["small_M"] = len(small_solutions)

    calibration_contacts = {
        name: _full_germ_contacts(states)
        for name, states in macro_states.items()
    }
    calibration_differences = sorted({
        contact["germ_difference_mod_6"]
        for contacts in calibration_contacts.values()
        for contact in contacts
        if contact["first_endpoint"] == contact["second_endpoint"]
    })
    if any(
        contact["first_endpoint"] != contact["second_endpoint"]
        for contacts in calibration_contacts.values()
        for contact in contacts
    ):
        raise ValueError("published macro contains a discontinuous SAB endpoint")
    if not calibration_differences:
        raise ValueError("published macros provide no SAB contact calibration")

    rhombi_a = frozenset(macro_states["large_A"])
    rhombi_b_zero = frozenset(macro_states["large_B"])
    equalizer_results = []
    for equalizer in kernel["two_rhombus_equalizers"]:
        rotation = equalizer["rotation"]
        reflected = equalizer["reflected"]
        translation = tuple(equalizer["translation_uv"])
        states_a = macro_states["large_A"]
        states_b = _transform_germ_macro(
            macro_states["large_B"], rotation, reflected, translation
        )
        rhombi_b = frozenset(states_b)
        added_to_a = tuple(sorted(
            rhombi_b - rhombi_a, key=lambda item: tuple(sorted(item))
        ))
        added_to_b = tuple(sorted(
            rhombi_a - rhombi_b, key=lambda item: tuple(sorted(item))
        ))
        endpoint_signature_a = _outer_sab_signature(
            tuple(rhombi_a | set(added_to_a))
        )
        endpoint_signature_b = _outer_sab_signature(
            tuple(rhombi_b | set(added_to_b))
        )
        choices_a = [
            _singleton_germ_states_on_rhombus(
                small_solutions, frozenset(next(iter(item)) for item in small_solutions),
                rhombus,
            )
            for rhombus in added_to_a
        ]
        choices_b = [
            _singleton_germ_states_on_rhombus(
                small_solutions, frozenset(next(iter(item)) for item in small_solutions),
                rhombus,
            )
            for rhombus in added_to_b
        ]
        if any(not choices for choices in choices_a + choices_b):
            raise ValueError("singleton M has no state on an equalizer rhombus")

        def legal_assignments(base_states, targets, choices):
            assignments = []

            def extend(position, states, selected):
                if position == len(targets):
                    contacts = _full_germ_contacts(states)
                    legal = all(
                        contact["first_endpoint"] == contact["second_endpoint"]
                        and contact["germ_difference_mod_6"]
                        in calibration_differences
                        for contact in contacts
                    )
                    if legal:
                        assignments.append({
                            "states": states,
                            "selected": tuple(selected),
                            "outer_exact": _full_outer_germ_signature(states),
                            "outer_compatibility": (
                                _outer_germ_compatibility_signature(
                                    states, calibration_differences
                                )
                            ),
                        })
                    return
                rhombus = targets[position]
                for state in choices[position]:
                    extend(
                        position + 1,
                        {**states, rhombus: state},
                        selected + [state],
                    )

            extend(0, dict(base_states), [])
            return assignments

        legal_a = legal_assignments(states_a, added_to_a, choices_a)
        legal_b = legal_assignments(states_b, added_to_b, choices_b)
        exact_matching_pairs = []
        compatibility_matching_pairs = []
        for first_index, first in enumerate(legal_a):
            for second_index, second in enumerate(legal_b):
                if first["outer_exact"] == second["outer_exact"]:
                    exact_matching_pairs.append([first_index, second_index])
                if (
                    first["outer_compatibility"]
                    == second["outer_compatibility"]
                ):
                    compatibility_matching_pairs.append(
                        [first_index, second_index]
                    )

        def serialized_assignment(item):
            return [
                {
                    "diagonal_uv": [list(point) for point in state["diagonal"]],
                    "corridor_bits": list(state["corridor_bits"]),
                    "endpoint_germs": list(state["endpoint_germs"]),
                }
                for state in item["selected"]
            ]

        equalizer_results.append({
            "rotation": rotation,
            "reflected": reflected,
            "translation_uv": list(translation),
            "singleton_state_counts_A": [len(item) for item in choices_a],
            "singleton_state_counts_B": [len(item) for item in choices_b],
            "legal_assignment_count_A": len(legal_a),
            "legal_assignment_count_B": len(legal_b),
            "source_endpoint_signature_equal": (
                endpoint_signature_a == endpoint_signature_b
            ),
            "source_endpoint_signature_is_support_determined": True,
            "exact_tangent_signature_pair_count": len(exact_matching_pairs),
            "exact_tangent_signature_pairs": exact_matching_pairs,
            "matching_compatibility_pair_count": len(
                compatibility_matching_pairs
            ),
            "matching_compatibility_pairs": compatibility_matching_pairs,
            "legal_singleton_assignments_A": [
                serialized_assignment(item) for item in legal_a
            ],
            "legal_singleton_assignments_B": [
                serialized_assignment(item) for item in legal_b
            ],
        })

    return {
        "schema": "ahi-sturmian-seventeen-rhombus-full-germs-v1",
        "source_archive_sha256": SOURCE_ARCHIVE_SHA256,
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "common_support_kernel_sha256": hashlib.sha256(
            (json.dumps(kernel, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "embedding_counts": embedding_counts,
        "published_macro_contact_counts": {
            name: len(contacts) for name, contacts in calibration_contacts.items()
        },
        "calibrated_germ_differences_mod_6": calibration_differences,
        "boundary_rule_interpretation": (
            "published contacts realize every odd germ difference; exact "
            "tangent is not a boundary color in the stated AHI matching rule; "
            "the source rule requires edge-to-edge endpoint continuation"
        ),
        "tangent_compatibility_diagnostic_scope": (
            "matching_compatibility_pair_count applies to the stricter "
            "inferred odd-difference relation only; it is not the source rule"
        ),
        "equalizers": equalizer_results,
    }


def verify_seventeen_rhombus_full_germs(
    data: dict, archive_path: Path, atlas: dict, kernel: dict
) -> None:
    expected = build_seventeen_rhombus_full_germs(archive_path, atlas, kernel)
    if data != expected:
        raise ValueError("serialized full SAB-germ test differs from exact rebuild")


def _odd_cycle(edges):
    adjacency = {}
    for first, second in edges:
        adjacency.setdefault(first, []).append(second)
        adjacency.setdefault(second, []).append(first)
    color = {}
    parent = {}
    depth = {}
    for root in sorted(adjacency):
        if root in color:
            continue
        color[root] = 0
        parent[root] = None
        depth[root] = 0
        queue = deque([root])
        while queue:
            first = queue.popleft()
            for second in adjacency[first]:
                if second not in color:
                    color[second] = 1 - color[first]
                    parent[second] = first
                    depth[second] = depth[first] + 1
                    queue.append(second)
                    continue
                if color[second] != color[first]:
                    continue
                left, right = first, second
                left_path, right_path = [left], [right]
                while depth[left] > depth[right]:
                    left = parent[left]
                    left_path.append(left)
                while depth[right] > depth[left]:
                    right = parent[right]
                    right_path.append(right)
                while left != right:
                    left, right = parent[left], parent[right]
                    left_path.append(left)
                    right_path.append(right)
                cycle = left_path + list(reversed(right_path[:-1]))
                return tuple(cycle)
    return None


def build_p17_all_m_obstruction(atlas: dict, kernel: dict) -> dict:
    """Exhaust every lozenge subdivision of P17 and test all-M parity."""

    verify_atlas(atlas)
    verify_common_support_kernel(kernel, atlas)
    equalizer = kernel["two_rhombus_equalizers"][0]
    support = _transform_cell_set(
        atlas["supports"]["large_A"]["cells"], 0, False, (0, 0)
    ) | _transform_cell_set(
        atlas["supports"]["large_B"]["cells"],
        equalizer["rotation"],
        equalizer["reflected"],
        tuple(equalizer["translation_uv"]),
    )
    triangles = tuple(sorted(support, key=lambda item: tuple(sorted(item))))
    adjacency = {index: [] for index in range(len(triangles))}
    for first_index, first in enumerate(triangles):
        for second_index in range(first_index):
            if len(first & triangles[second_index]) == 2:
                adjacency[first_index].append(second_index)
                adjacency[second_index].append(first_index)
    if any(not neighbors for neighbors in adjacency.values()):
        raise ValueError("P17 contains an unmatched primitive triangle")

    matching_count = 0
    bipartite_count = 0
    three_axis_vertex_count = 0
    first_bipartite = None
    shortest_odd_cycle = None

    def visit(unmatched, pairs):
        nonlocal matching_count, bipartite_count, three_axis_vertex_count
        nonlocal first_bipartite, shortest_odd_cycle
        if not unmatched:
            matching_count += 1
            rhombi = tuple(
                frozenset(triangles[first] | triangles[second])
                for first, second in pairs
            )
            diagonals = tuple(_rhombus_long_diagonal(rhombus) for rhombus in rhombi)
            cycle = _odd_cycle(diagonals)
            if cycle is None:
                bipartite_count += 1
                if first_bipartite is None:
                    first_bipartite = tuple(diagonals)
            elif shortest_odd_cycle is None or len(cycle) < len(shortest_odd_cycle):
                shortest_odd_cycle = cycle

            vertices = set().union(*rhombi)
            has_three_axis_vertex = False
            for vertex in vertices:
                incident = [
                    (rhombus, diagonal)
                    for rhombus, diagonal in zip(rhombi, diagonals)
                    if vertex in rhombus
                ]
                if len(incident) != 3:
                    continue
                covered_triangles = [
                    triangle
                    for triangle in triangles
                    if vertex in triangle
                ]
                if len(covered_triangles) != 6:
                    continue
                axes = {
                    _component_axis({
                        "diagonal_uv": [list(point) for point in diagonal]
                    })
                    for _, diagonal in incident
                }
                if axes == {0, 1, 2}:
                    has_three_axis_vertex = True
                    break
            if has_three_axis_vertex:
                three_axis_vertex_count += 1
            return

        first = min(
            unmatched,
            key=lambda index: sum(
                neighbor in unmatched for neighbor in adjacency[index]
            ),
        )
        choices = [
            neighbor for neighbor in adjacency[first] if neighbor in unmatched
        ]
        for second in sorted(choices):
            visit(
                unmatched - {first, second},
                pairs + [(min(first, second), max(first, second))],
            )

    visit(frozenset(range(len(triangles))), [])
    if not matching_count:
        raise ValueError("P17 has no lozenge subdivision")

    def serialize_edges(edges):
        if edges is None:
            return None
        return [
            [list(first), list(second)] for first, second in edges
        ]

    return {
        "schema": "ahi-sturmian-p17-all-m-obstruction-v1",
        "source_atlas_sha256": hashlib.sha256(
            (json.dumps(atlas, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "common_support_kernel_sha256": hashlib.sha256(
            (json.dumps(kernel, indent=2, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "primitive_triangle_count": len(triangles),
        "lozenge_count": len(triangles) // 2,
        "perfect_matching_count": matching_count,
        "matching_count_with_three_axis_vertex": three_axis_vertex_count,
        "nonbipartite_long_diagonal_graph_count": matching_count - bipartite_count,
        "bipartite_long_diagonal_graph_count": bipartite_count,
        "shortest_odd_cycle_edges_uv": serialize_edges(
            tuple(
                (shortest_odd_cycle[index], shortest_odd_cycle[(index + 1) % len(shortest_odd_cycle)])
                for index in range(len(shortest_odd_cycle))
            )
            if shortest_odd_cycle is not None
            else None
        ),
        "first_bipartite_subdivision_diagonals_uv": serialize_edges(first_bipartite),
        "all_m_state_exists": bool(bipartite_count),
    }


def verify_p17_all_m_obstruction(data: dict, atlas: dict, kernel: dict) -> None:
    expected = build_p17_all_m_obstruction(atlas, kernel)
    if data != expected:
        raise ValueError("serialized P17 all-M obstruction differs from exact rebuild")
