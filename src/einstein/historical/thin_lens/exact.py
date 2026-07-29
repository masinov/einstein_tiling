"""Exact QF_NRA formulation of the frozen K16W carrier obligation.

This module constructs one normalized existential formula.  It performs no
search by itself; the gated runner in ``scripts/run_k16w_exact.py`` owns the
single HC-27 solver invocation.
"""

from __future__ import annotations

from dataclasses import dataclass

import z3


Point = tuple[z3.ArithRef, z3.ArithRef]


def cadd(a: Point, b: Point) -> Point:
    return a[0] + b[0], a[1] + b[1]


def csub(a: Point, b: Point) -> Point:
    return a[0] - b[0], a[1] - b[1]


def cmul(a: Point, b: Point) -> Point:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def cscale(s: z3.ArithRef, a: Point) -> Point:
    return s * a[0], s * a[1]


def tangent_unit(t: z3.ArithRef) -> Point:
    """Unit-circle chart omitting only (-1,0), already a forbidden bridge."""

    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


def orient(a: Point, b: Point, c: Point) -> z3.ArithRef:
    ab = csub(b, a)
    ac = csub(c, a)
    return ab[0] * ac[1] - ab[1] * ac[0]


def dot(a: Point, b: Point) -> z3.ArithRef:
    return a[0] * b[0] + a[1] * b[1]


def point_on_segment(a: Point, b: Point, p: Point) -> z3.BoolRef:
    """Closed-segment membership as an exact polynomial predicate."""

    return z3.And(
        orient(a, b, p) == 0,
        dot(csub(p, a), csub(p, b)) <= 0,
    )


def segments_intersect(a: Point, b: Point, c: Point, d: Point) -> z3.BoolRef:
    """Exact closed-segment intersection, including every collinear case."""

    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)
    return z3.Or(
        z3.And(o1 * o2 < 0, o3 * o4 < 0),
        point_on_segment(a, b, c),
        point_on_segment(a, b, d),
        point_on_segment(c, d, a),
        point_on_segment(c, d, b),
    )


@dataclass(frozen=True)
class K16WProblem:
    solver: z3.Solver
    variables: dict[str, z3.ArithRef]
    first_half: tuple[Point, ...]
    points: tuple[Point, ...]
    nonadjacent_pairs: tuple[tuple[int, int], ...]
    constraint_counts: dict[str, int]
    hc34_cell: str | None = None


CELLS = ("plus-minus", "minus-plus")
HC34_CELLS = tuple(
    f"s{strand}-minus-{second}"
    for strand in (1, 2, 3)
    for second in ("minus", "plus")
)


def build_problem(*, timeout_ms: int | None = None,
                  cell: str | None = None,
                  hc34_cell: str | None = None) -> K16WProblem:
    """Build the complete normalized K16W QF_NRA sentence.

    Scale is fixed by ``u=1``.  Tangent-half-angle charts make the three unit
    directions rational functions.  Because bridge directions ``+1`` and
    ``-1`` are both forbidden, the bridge chart loses no admitted point.
    """

    if cell is not None and cell not in CELLS:
        raise ValueError(f"unknown K16W cell: {cell}")
    if hc34_cell is not None and hc34_cell not in HC34_CELLS:
        raise ValueError(f"unknown HC34 K16W cell: {hc34_cell}")
    if cell is not None and hc34_cell is not None:
        raise ValueError("choose either an HC31 cell or an HC34 cell")

    solver = z3.SolverFor("QF_NRA")
    if timeout_ms is not None:
        solver.set(timeout=timeout_ms)

    a, b, c, v = z3.Reals("a b c v")
    t0, t1, t2 = z3.Reals("t0 t1 t2")
    k = z3.Real("sqrt_half")
    variables = {
        "a": a,
        "b": b,
        "c": c,
        "v": v,
        "t0": t0,
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
        t0 > 0,
        t0 < 1,
        t1 * t1 > 0,
        t2 * t2 > 0,
        h * h < v * v + 1,
        a > k,
    ]

    z = tangent_unit(t0)
    if hc34_cell is None:
        z1 = tangent_unit(t1)
        z2 = tangent_unit(t2)
    else:
        second_sign = -1 if hc34_cell.endswith("-minus") else 1
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

    first_half = tuple(cmul(z, item) for item in w)
    containment: list[z3.BoolRef] = []
    for x, y in first_half[1:]:
        containment.extend((x > 0, x < v, y > 0, y < 1))

    diagonal = (v, z3.RealVal(1))
    points = list(first_half)
    points.extend(csub(diagonal, first_half[index]) for index in range(8, -1, -1))
    assert len(points) == 18

    central = csub(points[9], points[8])
    closure = central[0] * central[0] + central[1] * central[1] == h * h

    decomposition: list[z3.BoolRef] = []
    if cell is not None:
        # N38 and K29O: the two cells left after the theorem-only HC-31 pass.
        r_b = cmul(z, qz1)
        r_c = cmul(z, cmul(q3, z12))
        rel_x = dot(r_b, r_c)
        rel_y = orient(zero, r_b, r_c)
        aa = v - b * k
        bb = b * k - 1
        decomposition.extend((
            2 * v * v > 23,
            b > 2 * k,
            c > 2 * k,
        ))
        if cell == "plus-minus":
            decomposition.extend((
                r_b[0] > 0, r_b[1] > 0,
                r_c[0] < 0, r_c[1] < 0,
            ))
        else:
            decomposition.extend((
                r_b[0] < 0, r_b[1] < 0,
                r_c[0] > 0, r_c[1] > 0,
            ))
        decomposition.append(aa * rel_y - bb * rel_x > 0)
    elif hc34_cell is not None:
        # Corrected HC-33: one surviving polarity, three strand orders and
        # two bounded second-bridge charts.  Every original K21Q predicate
        # remains conjunctive below.
        r_b = cmul(z, qz1)
        r_c = cmul(z, cmul(q3, z12))
        rel_x = dot(r_b, r_c)
        rel_y = orient(zero, r_b, r_c)
        aa = v - b * k
        bb = b * k - 1
        decomposition.extend((
            t1 >= -1, t1 <= 1,
            t2 >= -1, t2 <= 1,
            z1[0] < 0,
            2 * v * v > 23,
            b > 2 * k,
            c > 2 * k,
            r_b[0] > 0, r_b[1] > 0,
            r_c[0] < 0, r_c[1] < 0,
            aa * rel_y - bb * rel_x > 0,
            v < 13,
            2 * a < 3,
            43 * b < 98,
            43 * c < 98,
            central[0] > 0,
        ))

        # Twice x_direction times the signed height above y=1/2.
        n_b = 2 * r_b[0] * (first_half[2][1] - z3.RealVal(1) / 2) + (
            v - 2 * first_half[2][0]
        ) * r_b[1]
        n_c = 2 * r_c[0] * (first_half[5][1] - z3.RealVal(1) / 2) + (
            v - 2 * first_half[5][0]
        ) * r_c[1]
        diff_num = n_c * r_b[0] - n_b * r_c[0]
        sum_num = n_b * r_c[0] + n_c * r_b[0]
        strand = hc34_cell[1]
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
            simplicity.append(
                z3.Not(segments_intersect(points[i], points[i + 1], points[j], points[j + 1]))
            )
    assert len(nonadjacent_pairs) == 120

    solver.add(*(base + containment + [closure] + simplicity + decomposition))
    return K16WProblem(
        solver=solver,
        variables=variables,
        first_half=tuple(first_half),
        points=tuple(points),
        nonadjacent_pairs=tuple(nonadjacent_pairs),
        constraint_counts={
            "base": len(base),
            "containment_scalar": len(containment),
            "closure": 1,
            "nonadjacent_segment_pairs": len(simplicity),
            "decomposition": len(decomposition),
            "total_top_level": (
                len(base) + len(containment) + 1 + len(simplicity)
                + len(decomposition)
            ),
        },
        hc34_cell=hc34_cell,
    )
