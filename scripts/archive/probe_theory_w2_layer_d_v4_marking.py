#!/usr/bin/env python
"""Search for a state-dependent two-center injection proving density 1/2."""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
import itertools
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.funnel.a1_torus import lattice_to_cell
from einstein.theory.a4_semidirect import c3_action, canonical_a4_semidirect
from einstein.theory.a4_v4_packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.theory.a4_v4_packing_family import PACKING_COLLISION_SEED
from einstein.theory.a4_v4_sft import _signed_coordinate
from einstein.theory.holonomy import kite_edge_letter
from einstein.theory.holonomy_csp import _placement_boundary, _point_type


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


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


def translated_pattern(pattern, delta, gauge):
    tx, ty, _ = lattice_to_cell((delta[0], delta[1], 0))
    return {(x + tx, y + ty): value ^ gauge
            for (x, y), value in pattern.items()}


def pair_compatible(left_pattern, left_gauge, right_pattern, right_gauge, delta):
    left = translated_pattern(left_pattern, (0, 0), left_gauge)
    right = translated_pattern(right_pattern, delta, right_gauge)
    return all(left[vertex] == right[vertex] for vertex in left.keys() & right.keys())


def target_collision(shape, left_operation, right_operation, delta, target):
    left = placement_lattice_cells(shape, (left_operation, 0, 0))
    right = placement_lattice_cells(
        shape, (right_operation, delta[0], delta[1])
    )
    return bool(left & right) and canonical_collision_type(left, right) == target


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--resource-radius", type=int)
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = payload["base_witnesses"][0]
    images = tuple(row["images"])
    patterns = tuple(
        relative_boundary_pattern(shape, operation, images)
        for operation in range(12)
    )
    occupied_resources = tuple(tuple(sorted({
        (u, v) for u, v, _ in placement_lattice_cells(
            shape, (operation, 0, 0)
        )
    })) for operation in range(12))
    assert all(len(row) == 4 for row in occupied_resources)
    if args.resource_radius is None:
        resources = occupied_resources
    else:
        radius = args.resource_radius
        common = tuple(
            (u, v)
            for u in range(-radius, radius + 1)
            for v in range(-radius, radius + 1)
            if max(abs(u), abs(v), abs(u + v)) <= radius
        )
        resources = (common,) * 12
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )

    # One type is (operation, actual V4 value at its reference vertex).
    types = tuple(itertools.product(range(12), range(4)))
    variables = {}
    next_variable = 1
    for tile_type in types:
        operation, _ = tile_type
        for resource in resources[operation]:
            variables[(tile_type, resource)] = next_variable
            next_variable += 1
    cnf = CNF()
    for tile_type in types:
        operation, _ = tile_type
        cardinality = CardEnc.equals(
            lits=[variables[(tile_type, resource)]
                  for resource in resources[operation]],
            bound=2,
            top_id=max(cnf.nv, next_variable - 1),
            encoding=EncType.seqcounter,
        )
        cnf.extend(cardinality.clauses)

    exclusions = set()
    compatibility_cache = {}
    packing_cache = {}
    compatible_pairs = 0
    packing_pairs = 0
    for left_type_index, left_type in enumerate(types):
        left_operation, left_gauge = left_type
        for right_type in types[left_type_index:]:
            right_operation, right_gauge = right_type
            for left_resource in resources[left_operation]:
                for right_resource in resources[right_operation]:
                    delta = (
                        left_resource[0] - right_resource[0],
                        left_resource[1] - right_resource[1],
                    )
                    if left_type == right_type and delta == (0, 0):
                        continue
                    compatibility_key = (left_type, right_type, delta)
                    compatible = compatibility_cache.get(compatibility_key)
                    if compatible is None:
                        compatible = pair_compatible(
                            patterns[left_operation], left_gauge,
                            patterns[right_operation], right_gauge, delta,
                        )
                        compatibility_cache[compatibility_key] = compatible
                    packing_key = (left_operation, right_operation, delta)
                    forbidden = packing_cache.get(packing_key)
                    if forbidden is None:
                        forbidden = target_collision(
                            shape, left_operation, right_operation, delta, target
                        )
                        packing_cache[packing_key] = forbidden
                    compatible_pairs += compatible
                    packing_pairs += forbidden
                    if compatible and not forbidden:
                        exclusions.add(tuple(sorted((
                            variables[(left_type, left_resource)],
                            variables[(right_type, right_resource)],
                        ))))
    cnf.extend([[-left, -right] for left, right in sorted(exclusions)])
    with Cadical195(bootstrap_with=cnf) as solver:
        sat = solver.solve()
        model = solver.get_model() if sat else None
    print(f"types={len(types)} marker variables={len(variables)}")
    print(f"compatible marker coincidences={compatible_pairs}")
    print(f"packing-forbidden coincidences={packing_pairs}")
    print(f"distinct exclusion clauses={len(exclusions)}")
    print(f"two-center marking SAT={sat}")
    if model is not None:
        truth = {literal for literal in model if literal > 0}
        certificate = {
            str(tile_type): [list(resource) for resource in resources[tile_type[0]]
                             if variables[(tile_type, resource)] in truth]
            for tile_type in types
        }
        print(json.dumps(certificate, indent=1))
    return 0 if sat else 1


if __name__ == "__main__":
    raise SystemExit(main())
