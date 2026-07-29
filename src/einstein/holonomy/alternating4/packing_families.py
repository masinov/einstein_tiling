"""Finite controls for a packing-aware V4 invariant on ``2 Lambda``."""

from __future__ import annotations

from collections import Counter

from einstein.holonomy.alternating4.lifts import induced_v4_twists, lies_in_2lambda
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    collision_overlap,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.products import build_v4_product_coverability_cnf
from einstein.holonomy.constraints import quotient_boundary_data


PACKING_COLLISION_SEED = ((3, 0, 0), (5, 0, 1))


def area_admissible_2lambda_hnfs(maximum_index: int, minimum_index: int = 1):
    """All HNFs ``L <= 2 Lambda`` whose six-sector area is tile-divisible."""
    if maximum_index < minimum_index:
        return ()
    return tuple(
        (a, b, d)
        for a in range(2, maximum_index + 1, 2)
        for d in range(2, maximum_index // a + 1, 2)
        if minimum_index <= a * d <= maximum_index and (6 * a * d) % 10 == 0
        for b in range(0, a, 2)
    )


def induced_signature_layers(signature_rows, hnf):
    """Restrict all base ``2 Lambda`` signature holonomies to one HNF."""
    if not lies_in_2lambda(hnf):
        raise ValueError("HNF is not a sublattice of 2 Lambda")
    return tuple(
        (tuple(row["images"]), induced_v4_twists(tuple(row["base_twists"]), hnf))
        for row in signature_rows
    )


def build_signature_packing_cnf(shape, hnf, signature_rows):
    """Full signature product plus the single six-kite collision orbit."""
    hnf = tuple(hnf)
    layers = induced_signature_layers(signature_rows, hnf)
    cnf, product_metadata = build_v4_product_coverability_cnf(shape, hnf, layers)
    instance, _, _ = quotient_boundary_data(shape, hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    clauses = collision_orbit_clauses(shape, hnf, instance, target)
    if any(not (instance.placements[-left - 1][1]
                & instance.placements[-right - 1][1]) for left, right in clauses):
        raise AssertionError("packing orbit contains a non-collision")
    cnf.extend(clauses)
    metadata = {
        "kind": "full-v4-signature-single-orbit-packing-family-control",
        "hnf": list(hnf),
        "layers": len(layers),
        "product": product_metadata,
        "packing": {
            "seed_placements": [list(row) for row in PACKING_COLLISION_SEED],
            "overlap_cells": collision_overlap(target),
            "orbit_clauses": len(clauses),
            "is_subset_of_exact_nonoverlap": True,
        },
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
    }
    return cnf, metadata


def coverage_summary(shape, hnf, true_variables):
    """Selected-placement count and cell multiplicities of a SAT assignment."""
    instance, _, _ = quotient_boundary_data(shape, tuple(hnf))
    truth = set(true_variables)
    multiplicities = [0] * instance.n_cells
    selected = []
    for variable, (placement, mask) in enumerate(instance.placements, 1):
        if variable not in truth:
            continue
        selected.append(placement)
        while mask:
            low = mask & -mask
            multiplicities[low.bit_length() - 1] += 1
            mask ^= low
    return {
        "selected_placements": len(selected),
        "exact_cover_placement_count": instance.n_cells // len(shape),
        "coverage_surplus": sum(multiplicities) - instance.n_cells,
        "maximum_multiplicity": max(multiplicities),
        "multiplicity_histogram": {
            str(value): count
            for value, count in sorted(Counter(multiplicities).items())
        },
    }
