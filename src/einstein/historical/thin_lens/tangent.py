"""Polynomial seven-variable presentation of the K35T tangent stratum.

The HC-38 experiment is admitted only after session 162's preregistration.
This builder removes the terminal chart variable exactly.  Rather than place
``A/T`` and ``B/T`` in rational functions, it multiplies every physical point
by the common positive denominator ``T``.  Rectangle containment, strand
signs and closed-segment incidence are invariant under that positive
homothety, so the resulting QF_NRA formula is polynomial and exactly
equisatisfiable with K35T.
"""

from __future__ import annotations

from dataclasses import dataclass

import z3

from einstein.historical.thin_lens.exact import (
    HC34_CELLS,
    Point,
    cadd,
    cmul,
    cscale,
    csub,
    dot,
    orient,
    segments_intersect,
    tangent_unit,
)


@dataclass(frozen=True)
class K16WTangentProblem:
    solver: z3.Solver
    variables: dict[str, z3.ArithRef]
    relative_first_half: tuple[Point, ...]
    scaled_first_half: tuple[Point, ...]
    scaled_points: tuple[Point, ...]
    nonadjacent_pairs: tuple[tuple[int, int], ...]
    constraint_counts: dict[str, int]
    hc38_cell: str


def build_tangent_problem(cell: str) -> K16WTangentProblem:
    """Build one complete HC-38 tangent cell over seven real variables."""

    if cell not in HC34_CELLS:
        raise ValueError(f"unknown HC-38 tangent cell: {cell}")

    solver = z3.SolverFor("QF_NRA")
    a, b, c, v = z3.Reals("a b c v")
    t1, t2 = z3.Reals("t1 t2")
    k = z3.Real("sqrt_half")
    variables = {
        "a": a,
        "b": b,
        "c": c,
        "v": v,
        "t1": t1,
        "t2": t2,
        "sqrt_half": k,
    }

    h = a + b + c
    base = [
        a > 0,
        b > 0,
        c > 0,
        v > 0,
        (v - 1) * (v - 1) > 0,
        k > 0,
        2 * k * k == 1,
        t1 * t1 > 0,
        t2 * t2 > 0,
        h * h < v * v + 1,
        a > k,
    ]

    second_sign = -1 if cell.endswith("-minus") else 1
    z1 = cscale(z3.RealVal(-1), tangent_unit(t1))
    z2 = cscale(z3.RealVal(second_sign), tangent_unit(t2))
    q = (-k, k)
    q2 = (z3.RealVal(0), z3.RealVal(-1))
    q3 = (k, k)
    q4 = (z3.RealVal(-1), z3.RealVal(0))
    q5 = (k, -k)

    zero = (z3.RealVal(0), z3.RealVal(0))
    w: list[Point] = [zero]
    w.append((a, z3.RealVal(0)))
    w.append(cadd(w[-1], q))
    qz1 = cmul(q, z1)
    w.append(cadd(w[-1], cscale(v, qz1)))
    w.append(cadd(w[-1], cscale(b, cmul(q2, z1))))
    w.append(cadd(w[-1], cmul(q3, z1)))
    z12 = cmul(z1, z2)
    w.append(cadd(w[-1], cscale(v, cmul(q3, z12))))
    w.append(cadd(w[-1], cscale(c, cmul(q4, z12))))
    w.append(cadd(w[-1], cmul(q5, z12)))

    x8, y8 = w[8]
    d2 = v * v + 1
    r2 = x8 * x8 + y8 * y8
    aa_terminal = v * x8 + y8
    bb_terminal = x8 - v * y8
    tangent_t = (d2 + 4 * r2 - h * h) / 4
    tangent_r = aa_terminal * aa_terminal + bb_terminal * bb_terminal
    delta = tangent_r - tangent_t * tangent_t
    tangent = [
        delta == 0,
        tangent_t > 0,
        aa_terminal > 0,
        bb_terminal > 0,
        2 * tangent_t < d2,
    ]

    # T*p_i=(A+iB)*w_i.  T>0 makes this a common positive
    # homothety, so all strict rectangle and incidence predicates below are
    # exactly equivalent to their unscaled K34Q versions.
    terminal_numerator = (aa_terminal, bb_terminal)
    scaled_first = tuple(cmul(terminal_numerator, item) for item in w)
    containment: list[z3.BoolRef] = []
    for x, y in scaled_first[1:]:
        containment.extend((x > 0, x < v * tangent_t, y > 0, y < tangent_t))

    scaled_diagonal = (v * tangent_t, tangent_t)
    scaled_points = list(scaled_first)
    scaled_points.extend(
        csub(scaled_diagonal, scaled_first[index])
        for index in range(8, -1, -1)
    )
    assert len(scaled_points) == 18

    scaled_central = csub(scaled_points[9], scaled_points[8])
    closure = (
        dot(scaled_central, scaled_central)
        == h * h * tangent_t * tangent_t
    )

    # The complete corrected HC-34 decomposition, rewritten homogeneously.
    r_b_numerator = cmul(terminal_numerator, qz1)
    r_c_numerator = cmul(terminal_numerator, cmul(q3, z12))
    rel_x = dot(r_b_numerator, r_c_numerator)
    rel_y = orient(zero, r_b_numerator, r_c_numerator)
    safe_a = v - b * k
    safe_b = b * k - 1
    decomposition: list[z3.BoolRef] = [
        t1 >= -1,
        t1 <= 1,
        t2 >= -1,
        t2 <= 1,
        z1[0] < 0,
        2 * v * v > 23,
        b > 2 * k,
        c > 2 * k,
        r_b_numerator[0] > 0,
        r_b_numerator[1] > 0,
        r_c_numerator[0] < 0,
        r_c_numerator[1] < 0,
        safe_a * rel_y - safe_b * rel_x > 0,
        v < 13,
        2 * a < 3,
        43 * b < 98,
        43 * c < 98,
        scaled_central[0] > 0,
    ]

    # Multiply the HC-34 midline numerators by T^2.  Since T>0, their
    # signs and all subsequent cross-products are unchanged.
    n_b = r_b_numerator[0] * (2 * scaled_first[2][1] - tangent_t) + (
        v * tangent_t - 2 * scaled_first[2][0]
    ) * r_b_numerator[1]
    n_c = r_c_numerator[0] * (2 * scaled_first[5][1] - tangent_t) + (
        v * tangent_t - 2 * scaled_first[5][0]
    ) * r_c_numerator[1]
    diff_num = n_c * r_b_numerator[0] - n_b * r_c_numerator[0]
    sum_num = n_b * r_c_numerator[0] + n_c * r_b_numerator[0]
    strand = cell[1]
    if strand == "1":
        decomposition.extend((n_b > 0, n_c < 0, diff_num < 0))
    elif strand == "2":
        decomposition.extend((n_b < 0, n_c > 0, diff_num < 0))
    else:
        decomposition.extend((n_b < 0, n_c < 0, sum_num > 0))

    nonadjacent_pairs: list[tuple[int, int]] = []
    simplicity: list[z3.BoolRef] = []
    for i in range(17):
        for j in range(i + 2, 17):
            nonadjacent_pairs.append((i, j))
            simplicity.append(z3.Not(segments_intersect(
                scaled_points[i], scaled_points[i + 1],
                scaled_points[j], scaled_points[j + 1],
            )))
    assert len(nonadjacent_pairs) == 120

    solver.add(*(
        base + tangent + containment + [closure] + simplicity + decomposition
    ))
    counts = {
        "base": len(base),
        "tangent_substitution": len(tangent),
        "containment_scalar": len(containment),
        "closure": 1,
        "nonadjacent_segment_pairs": len(simplicity),
        "decomposition": len(decomposition),
        "total_top_level": (
            len(base) + len(tangent) + len(containment) + 1
            + len(simplicity) + len(decomposition)
        ),
    }
    return K16WTangentProblem(
        solver=solver,
        variables=variables,
        relative_first_half=tuple(w),
        scaled_first_half=scaled_first,
        scaled_points=tuple(scaled_points),
        nonadjacent_pairs=tuple(nonadjacent_pairs),
        constraint_counts=counts,
        hc38_cell=cell,
    )
