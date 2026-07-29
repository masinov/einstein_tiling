"""Pull back a V4 coverability-SFT witness from ``2 Lambda``.

The quotient HNF ``(2,0,2)`` represents the sublattice ``2 Lambda``.  Every
HNF ``(a,b,d)`` with a, b and d even is a sublattice of it, so the associated
torus covers the four-cell center quotient.  A semantic local-SFT assignment
therefore pulls back without another SAT solve.
"""

from __future__ import annotations

from einstein.holonomy.constraints import quotient_boundary_data


BASE_HNF = (2, 0, 2)


def lies_in_2lambda(hnf) -> bool:
    """Whether both HNF period generators lie in ``2 Lambda``."""
    a, b, d = hnf
    return a > 0 and d > 0 and 0 <= b < a and all(value % 2 == 0 for value in hnf)


def induced_v4_twists(base_twists, hnf) -> tuple[int, int]:
    """Restrict a ``2 Lambda`` V4 holonomy to an even HNF sublattice."""
    if not lies_in_2lambda(hnf):
        raise ValueError("HNF is not a sublattice of 2 Lambda")
    left, right = base_twists
    a, b, d = hnf
    return (
        left if (a // 2) % 2 else 0,
        (left if (b // 2) % 2 else 0) ^ (right if (d // 2) % 2 else 0),
    )


def semantic_base_witness(shape, model):
    """Decode a SAT assignment on HNF (2,0,2) into local geometric data."""
    instance, vertices, _ = quotient_boundary_data(shape, BASE_HNF)
    truth = {abs(literal): literal > 0 for literal in model}
    n_placements = len(instance.placements)
    selected = tuple(sorted(
        (op, tu % 2, tv % 2)
        for variable, ((op, tu, tv), _) in enumerate(instance.placements, 1)
        if truth[variable]
    ))
    colors = tuple(
        (vertex, int(truth[n_placements + 2 * index + 1])
         | (int(truth[n_placements + 2 * index + 2]) << 1))
        for index, vertex in enumerate(vertices)
    )
    return selected, colors


def lift_2lambda_witness(shape, hnf, base_twists, selected, colors):
    """Return induced twists and a complete Boolean assignment by variable."""
    twists = induced_v4_twists(base_twists, hnf)
    selected = set(tuple(row) for row in selected)
    colors = {tuple(vertex): color for vertex, color in colors}
    instance, vertices, _ = quotient_boundary_data(shape, tuple(hnf))
    values = {}
    for variable, ((op, tu, tv), _) in enumerate(instance.placements, 1):
        values[variable] = (op, tu % 2, tv % 2) in selected
    n_placements = len(instance.placements)
    for index, vertex in enumerate(vertices):
        kind0, kind1, u, v = vertex
        base_vertex = (kind0, kind1, u % 2, v % 2)
        color = colors[base_vertex]
        if (u // 2) % 2:
            color ^= base_twists[0]
        if (v // 2) % 2:
            color ^= base_twists[1]
        values[n_placements + 2 * index + 1] = bool(color & 1)
        values[n_placements + 2 * index + 2] = bool(color & 2)
    return twists, values


def unsatisfied_clauses(cnf, values):
    """Indices of clauses false under a complete Boolean assignment."""
    return tuple(
        index for index, clause in enumerate(cnf.clauses)
        if not any(values[abs(literal)] == (literal > 0) for literal in clause)
    )
