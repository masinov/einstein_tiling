#!/usr/bin/env python
"""Cold exact verifier for rational K16W solver models.

The verifier does not import the Z3 formula builder.  It reconstructs the
original geometry over Q(sqrt(2)) and checks every predicate directly.
Algebraic model coordinates outside this exact field are rejected rather than
approximated.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/notebook/assets/k16w-exact-verification.json"


@dataclass(frozen=True)
class Q2:
    a: Fraction = Fraction(0)
    b: Fraction = Fraction(0)

    def __add__(self, other):
        other = as_q2(other)
        return Q2(self.a + other.a, self.b + other.b)

    __radd__ = __add__

    def __neg__(self):
        return Q2(-self.a, -self.b)

    def __sub__(self, other):
        return self + (-as_q2(other))

    def __rsub__(self, other):
        return as_q2(other) - self

    def __mul__(self, other):
        other = as_q2(other)
        return Q2(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = as_q2(other)
        norm = other.a * other.a - 2 * other.b * other.b
        if norm == 0:
            raise ZeroDivisionError
        return self * Q2(other.a / norm, -other.b / norm)

    def sign(self) -> int:
        if self.a == 0:
            return (self.b > 0) - (self.b < 0)
        if self.b == 0:
            return (self.a > 0) - (self.a < 0)
        if self.a > 0 and self.b > 0:
            return 1
        if self.a < 0 and self.b < 0:
            return -1
        lhs = self.a * self.a
        rhs = 2 * self.b * self.b
        if lhs == rhs:
            return 0
        if self.a > 0:
            return 1 if lhs > rhs else -1
        return 1 if rhs > lhs else -1

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0


def as_q2(value) -> Q2:
    if isinstance(value, Q2):
        return value
    return Q2(Fraction(value), Fraction(0))


Point = tuple[Q2, Q2]


def cadd(x: Point, y: Point) -> Point:
    return x[0] + y[0], x[1] + y[1]


def csub(x: Point, y: Point) -> Point:
    return x[0] - y[0], x[1] - y[1]


def cmul(x: Point, y: Point) -> Point:
    return x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]


def cscale(s: Q2, x: Point) -> Point:
    return s * x[0], s * x[1]


def tangent(t: Fraction) -> Point:
    den = 1 + t * t
    return Q2((1 - t * t) / den), Q2(2 * t / den)


def orient(a: Point, b: Point, c: Point) -> Q2:
    ab = csub(b, a)
    ac = csub(c, a)
    return ab[0] * ac[1] - ab[1] * ac[0]


def dot(a: Point, b: Point) -> Q2:
    return a[0] * b[0] + a[1] * b[1]


def on_segment(a: Point, b: Point, p: Point) -> bool:
    return orient(a, b, p).is_zero() and dot(csub(p, a), csub(p, b)).sign() <= 0


def intersects(a: Point, b: Point, c: Point, d: Point) -> bool:
    o1, o2 = orient(a, b, c), orient(a, b, d)
    o3, o4 = orient(c, d, a), orient(c, d, b)
    return (
        (o1.sign() * o2.sign() < 0 and o3.sign() * o4.sign() < 0)
        or on_segment(a, b, c)
        or on_segment(a, b, d)
        or on_segment(c, d, a)
        or on_segment(c, d, b)
    )


def rational_model(payload) -> tuple[dict[str, Fraction] | None, list[str]]:
    failures = []
    values = {}
    for name in ("a", "b", "c", "v", "t0", "t1", "t2"):
        entry = payload["model"].get(name)
        if not entry or entry.get("kind") != "rational":
            failures.append(f"{name}: model value is not rational")
            continue
        values[name] = Fraction(entry["numerator"], entry["denominator"])
    return (values if not failures else None), failures


def verify(values: dict[str, Fraction]) -> dict:
    a, b, c, v = (Q2(values[name]) for name in ("a", "b", "c", "v"))
    t0, t1, t2 = (values[name] for name in ("t0", "t1", "t2"))
    h = a + b + c
    failures = []

    def require(condition: bool, label: str):
        if not condition:
            failures.append(label)

    require(a.sign() > 0 and b.sign() > 0 and c.sign() > 0 and v.sign() > 0, "positive weights")
    require((v - 1).sign() != 0, "unequal guard legs")
    require(Fraction(0) < t0 < Fraction(1), "terminal first-quadrant chart")
    require(t1 != 0 and t2 != 0, "bridge irredundancy")

    z, z1, z2 = tangent(t0), tangent(t1), tangent(t2)
    q = (Q2(0, Fraction(-1, 2)), Q2(0, Fraction(1, 2)))
    q2 = (Q2(0), Q2(-1))
    q3 = (Q2(0, Fraction(1, 2)), Q2(0, Fraction(1, 2)))
    q4 = (Q2(-1), Q2(0))
    q5 = (Q2(0, Fraction(1, 2)), Q2(0, Fraction(-1, 2)))
    zero = (Q2(0), Q2(0))
    w = [zero, (a, Q2(0))]
    w.append(cadd(w[-1], q))
    w.append(cadd(w[-1], cscale(v, cmul(q, z1))))
    w.append(cadd(w[-1], cscale(b, cmul(q2, z1))))
    w.append(cadd(w[-1], cmul(q3, z1)))
    z12 = cmul(z1, z2)
    w.append(cadd(w[-1], cscale(v, cmul(q3, z12))))
    w.append(cadd(w[-1], cscale(c, cmul(q4, z12))))
    w.append(cadd(w[-1], cmul(q5, z12)))
    first = [cmul(z, item) for item in w]

    for index, (x, y) in enumerate(first[1:], 1):
        require(x.sign() > 0 and (v - x).sign() > 0, f"p{index} horizontal containment")
        require(y.sign() > 0 and (1 - y).sign() > 0, f"p{index} vertical containment")

    diagonal = (v, Q2(1))
    points = first + [csub(diagonal, first[index]) for index in range(8, -1, -1)]
    central = csub(points[9], points[8])
    require((dot(central, central) - h * h).is_zero(), "central host closure")

    intersections = []
    for i in range(17):
        for j in range(i + 2, 17):
            if intersects(points[i], points[i + 1], points[j], points[j + 1]):
                intersections.append([i, j])
    require(not intersections, "nonadjacent spine intersections")
    return {
        "verified": not failures,
        "failures": failures,
        "nonadjacent_segment_intersections": intersections,
        "nonadjacent_pairs_checked": 120,
        "field": "Q(sqrt(2))",
    }


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    if len(argv) != 2:
        print("usage: verify_k16w_exact.py <k16w-result.json>", file=sys.stderr)
        return 2
    source = Path(argv[1])
    payload = json.loads(source.read_text())
    result = {
        "kind": "k16w-exact-cold-verification",
        "schema_version": 1,
        "source": str(source.resolve().relative_to(ROOT)),
        "solver_status": payload.get("status"),
        "verified": False,
        "failures": [],
    }
    if payload.get("status") != "sat" or not payload.get("model"):
        result["failures"].append("source does not contain a SAT model")
    else:
        values, failures = rational_model(payload)
        result["failures"].extend(failures)
        if values is not None:
            result.update(verify(values))
    OUT.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

