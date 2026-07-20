"""Packing-sensitive refinements of the geometric-C3 A4/V4 SFT.

The local coverability encoders deliberately omit nonoverlap.  This module
adds a weaker, global packing condition: at most ``budget`` tile placements
may be selected.  Since every placement of a fixed polyform has the same
area, an exact cover of ``n`` quotient cells by an area-``q`` tile uses
exactly ``n/q`` placements.  Budgets above that value measure how much
overlap the holonomy relaxation intrinsically requires before restoring the
full cellwise packing clauses.
"""

from __future__ import annotations

import itertools

from pysat.card import CardEnc, EncType
from pysat.formula import CNF

from einstein.funnel.a1_torus import cell_to_lattice, lattice_to_cell
from einstein.substrate.kitegrid import N_OPS, transform_cell


def add_placement_budget(cnf: CNF, placement_count: int, budget: int):
    """Return a copy of ``cnf`` with ``sum(placements) <= budget``.

    Placement variables are the initial consecutive block used by every
    Layer-D encoder.  A sequential counter is deterministic and keeps the
    extension variables disjoint from the potential variables already in the
    formula.
    """
    if placement_count < 1:
        raise ValueError("placement_count must be positive")
    if not 0 <= budget <= placement_count:
        raise ValueError("budget must lie between zero and placement_count")
    bounded = CNF(from_clauses=cnf.clauses)
    cardinality = CardEnc.atmost(
        lits=list(range(1, placement_count + 1)),
        bound=budget,
        top_id=bounded.nv,
        encoding=EncType.seqcounter,
    )
    bounded.extend(cardinality.clauses)
    return bounded, {
        "placement_budget": budget,
        "placement_variables": placement_count,
        "budget_variables": bounded.nv - cnf.nv,
        "budget_clauses": len(cardinality.clauses),
        "variables": bounded.nv,
        "clauses": len(bounded.clauses),
    }


def selected_placements(model, placement_count: int):
    """Return the selected initial placement variables in a SAT model."""
    truth = {literal for literal in model if literal > 0}
    return tuple(variable for variable in range(1, placement_count + 1)
                 if variable in truth)


def placement_lattice_cells(shape, placement):
    """Exact infinite-grid cells of one ``(operation, u, v)`` placement."""
    operation, translate_u, translate_v = placement
    return frozenset(
        (u + translate_u, v + translate_v, sector)
        for u, v, sector in (
            cell_to_lattice(transform_cell(cell, operation)) for cell in shape
        )
    )


def canonical_collision_type(left_cells, right_cells):
    """Canonical D6-and-translation orbit key for two overlapping tiles.

    The two components are unordered.  Unlike canonicalizing their union,
    retaining both component cell sets distinguishes different decompositions
    of the same occupied region.
    """
    left_cells, right_cells = frozenset(left_cells), frozenset(right_cells)
    if not left_cells & right_cells:
        raise ValueError("collision components must overlap")
    best = None
    for operation in range(N_OPS):
        components = []
        for cells in (left_cells, right_cells):
            components.append(tuple(sorted(
                cell_to_lattice(transform_cell(lattice_to_cell(cell), operation))
                for cell in cells
            )))
        origin_u, origin_v = min(
            cell for component in components for cell in component
        )[:2]
        key = tuple(sorted(
            tuple((u - origin_u, v - origin_v, sector)
                  for u, v, sector in component)
            for component in components
        ))
        if best is None or key < best:
            best = key
    return best


def collision_overlap(collision_type) -> int:
    """Number of kite cells shared by a canonical collision type."""
    return len(set(collision_type[0]) & set(collision_type[1]))


def _ceil_div(numerator, denominator):
    return -((-numerator) // denominator)


def _deck_collision_types(shape, hnf, left, right):
    """Local collision types represented by one torus-placement pair."""
    a, b, d = hnf
    left_op, left_u, left_v = left
    right_op, right_u, right_v = right
    left_cells = placement_lattice_cells(shape, (left_op, 0, 0))
    right_zero = placement_lattice_cells(shape, (right_op, 0, 0))
    delta_u, delta_v = right_u - left_u, right_v - left_v
    left_us = [cell[0] for cell in left_cells]
    left_vs = [cell[1] for cell in left_cells]
    right_us = [cell[0] for cell in right_zero]
    right_vs = [cell[1] for cell in right_zero]
    n_min = _ceil_div(min(left_vs) - max(right_vs) - delta_v, d)
    n_max = (max(left_vs) - min(right_vs) - delta_v) // d
    out = set()
    for n in range(n_min, n_max + 1):
        shifted_u = delta_u + n * b
        m_min = _ceil_div(min(left_us) - max(right_us) - shifted_u, a)
        m_max = (max(left_us) - min(right_us) - shifted_u) // a
        for m in range(m_min, m_max + 1):
            right_cells = frozenset(
                (u + delta_u + m * a + n * b,
                 v + delta_v + n * d, sector)
                for u, v, sector in right_zero
            )
            if left_cells & right_cells:
                out.add(canonical_collision_type(left_cells, right_cells))
    return tuple(sorted(out))


def torus_conflicting_pairs(instance):
    """All placement-variable pairs that overlap on a torus quotient."""
    by_cell = [[] for _ in range(instance.n_cells)]
    for variable, (_, mask) in enumerate(instance.placements, 1):
        while mask:
            low = mask & -mask
            by_cell[low.bit_length() - 1].append(variable)
            mask ^= low
    pairs = set()
    for variables in by_cell:
        pairs.update(itertools.combinations(variables, 2))
    return tuple(sorted(pairs))


def collision_orbit_clauses(shape, hnf, instance, target_type):
    """Nonoverlap clauses for one exact local D6 collision orbit.

    A quotient pair is included when any of its deck translates realizes the
    target local collision.  Every returned clause is consequently a subset
    of the ordinary exact-cover nonoverlap clauses.
    """
    target_type = tuple(tuple(tuple(cell) for cell in component)
                        for component in target_type)
    cache = {}
    clauses = []
    for left_var, right_var in torus_conflicting_pairs(instance):
        left = instance.placements[left_var - 1][0]
        right = instance.placements[right_var - 1][0]
        relative = (
            left[0], right[0], right[1] - left[1], right[2] - left[2]
        )
        types = cache.get(relative)
        if types is None:
            types = _deck_collision_types(shape, hnf, left, right)
            cache[relative] = types
        if target_type in types:
            clauses.append([-left_var, -right_var])
    return tuple(clauses)
