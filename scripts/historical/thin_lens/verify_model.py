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

from einstein.repository import repository_root
import sys


ROOT = repository_root(Path(__file__))
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

    def __pow__(self, exponent: int):
        if exponent < 0:
            return Q2(1) / (self ** (-exponent))
        out = Q2(1)
        base = self
        while exponent:
            if exponent & 1:
                out *= base
            base *= base
            exponent //= 2
        return out

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


def tangent(t: Fraction | Q2) -> Point:
    t = as_q2(t)
    den = 1 + t * t
    return (1 - t * t) / den, 2 * t / den


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


def q2_entry(entry, name: str) -> tuple[Q2 | None, str | None]:
    if not entry:
        return None, f"{name}: model value is missing"
    if entry.get("kind") == "rational":
        return Q2(Fraction(entry["numerator"], entry["denominator"])), None
    if entry.get("kind") == "q_sqrt2":
        value = Q2(
            Fraction(entry["rational_numerator"], entry["rational_denominator"]),
            Fraction(entry["sqrt2_numerator"], entry["sqrt2_denominator"]),
        )
        polynomial = {
            int(power): Fraction(coefficient["numerator"], coefficient["denominator"])
            for power, coefficient in entry.get("defining_polynomial", {}).items()
        }
        total = Q2(0)
        for power, coefficient in polynomial.items():
            total += coefficient * (value ** power)
        if not polynomial or not total.is_zero():
            return None, f"{name}: Q(sqrt(2)) value fails its defining polynomial"
        isolation = entry.get("isolation", {})
        try:
            lower_entry = isolation["lower"]
            upper_entry = isolation["upper"]
            lower = Fraction(lower_entry["numerator"], lower_entry["denominator"])
            upper = Fraction(upper_entry["numerator"], upper_entry["denominator"])
        except (KeyError, TypeError, ZeroDivisionError):
            return None, f"{name}: malformed algebraic isolation interval"
        if (value - lower).sign() <= 0 or (upper - value).sign() <= 0:
            return None, f"{name}: Q(sqrt(2)) value lies outside its isolation interval"
        return value, None
    return None, f"{name}: model value is outside the admitted Q(sqrt(2)) field"


def tangent_q2_model(payload) -> tuple[dict[str, Q2] | None, list[str]]:
    failures = []
    values = {}
    for name in ("a", "b", "c", "v", "t1", "t2", "sqrt_half"):
        value, failure = q2_entry(payload["model"].get(name), name)
        if failure:
            failures.append(failure)
        else:
            values[name] = value
    return (values if not failures else None), failures


HC34_CELLS = tuple(
    f"s{strand}-minus-{second}"
    for strand in (1, 2, 3)
    for second in ("minus", "plus")
)


def verify(values: dict[str, Fraction | Q2], cell: str | None = None,
           hc34_cell: str | None = None) -> dict:
    a, b, c, v = (as_q2(values[name]) for name in ("a", "b", "c", "v"))
    t0, t1, t2 = (as_q2(values[name]) for name in ("t0", "t1", "t2"))
    h = a + b + c
    failures = []

    def require(condition: bool, label: str):
        if not condition:
            failures.append(label)

    require(a.sign() > 0 and b.sign() > 0 and c.sign() > 0 and v.sign() > 0, "positive weights")
    require((v - 1).sign() != 0, "unequal guard legs")
    require(t0.sign() > 0 and (1 - t0).sign() > 0,
            "terminal first-quadrant chart")
    require(t1.sign() != 0 and t2.sign() != 0, "bridge irredundancy")

    z = tangent(t0)
    if hc34_cell is None:
        z1, z2 = tangent(t1), tangent(t2)
    else:
        require(hc34_cell in HC34_CELLS, "recognized HC34 cell")
        require((t1 + 1).sign() >= 0 and (1 - t1).sign() >= 0,
                "bounded first bridge chart")
        require((t2 + 1).sign() >= 0 and (1 - t2).sign() >= 0,
                "bounded second bridge chart")
        raw1, raw2 = tangent(t1), tangent(t2)
        z1 = (-raw1[0], -raw1[1])
        second_sign = -1 if hc34_cell.endswith("-minus") else 1
        z2 = (second_sign * raw2[0], second_sign * raw2[1])
        require(z1[0].sign() < 0, "K33C first bridge sign")
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
    if cell is not None:
        require(cell in ("plus-minus", "minus-plus"), "recognized HC31 cell")
        r_b = cmul(z, cmul(q, z1))
        r_c = cmul(z, cmul(q3, z12))
        rel_x = dot(r_b, r_c)
        rel_y = orient(zero, r_b, r_c)
        aa = v - b * Q2(0, Fraction(1, 2))
        bb = b * Q2(0, Fraction(1, 2)) - 1
        require((2 * v * v - 23).sign() > 0, "N38 aspect")
        require((b - Q2(0, 1)).sign() > 0, "N38 b bound")
        require((c - Q2(0, 1)).sign() > 0, "N38 c bound")
        if cell == "plus-minus":
            require(r_b[0].sign() > 0 and r_b[1].sign() > 0,
                    "P_+- B polarity")
            require(r_c[0].sign() < 0 and r_c[1].sign() < 0,
                    "P_+- C polarity")
        elif cell == "minus-plus":
            require(r_b[0].sign() < 0 and r_b[1].sign() < 0,
                    "P_-+ B polarity")
            require(r_c[0].sign() > 0 and r_c[1].sign() > 0,
                    "P_-+ C polarity")
        require((aa * rel_y - bb * rel_x).sign() > 0, "K29O safe cell")
    if hc34_cell is not None:
        r_b = cmul(z, cmul(q, z1))
        r_c = cmul(z, cmul(q3, cmul(z1, z2)))
        rel_x = dot(r_b, r_c)
        rel_y = orient(zero, r_b, r_c)
        aa = v - b * Q2(0, Fraction(1, 2))
        bb = b * Q2(0, Fraction(1, 2)) - 1
        require((2 * v * v - 23).sign() > 0, "N38 aspect")
        require((b - Q2(0, 1)).sign() > 0, "N38 b bound")
        require((c - Q2(0, 1)).sign() > 0, "N38 c bound")
        require(r_b[0].sign() > 0 and r_b[1].sign() > 0,
                "P_+- B polarity")
        require(r_c[0].sign() < 0 and r_c[1].sign() < 0,
                "P_+- C polarity")
        require((aa * rel_y - bb * rel_x).sign() > 0, "K29O safe cell")
        require((13 - v).sign() > 0, "K31C v bound")
        require((Q2(Fraction(3, 2)) - a).sign() > 0, "K31C a bound")
        require((Q2(Fraction(98, 43)) - b).sign() > 0, "K31C b bound")
        require((Q2(Fraction(98, 43)) - c).sign() > 0, "K31C c bound")
        require(central[0].sign() > 0, "corrected N42 H-east")

        half = Q2(Fraction(1, 2))
        n_b = 2 * r_b[0] * (first[2][1] - half) + (v - 2 * first[2][0]) * r_b[1]
        n_c = 2 * r_c[0] * (first[5][1] - half) + (v - 2 * first[5][0]) * r_c[1]
        diff_num = n_c * r_b[0] - n_b * r_c[0]
        sum_num = n_b * r_c[0] + n_c * r_b[0]
        strand = hc34_cell[1]
        if strand == "1":
            require(n_b.sign() > 0 and n_c.sign() < 0 and diff_num.sign() < 0,
                    "K32S S1 signs")
        elif strand == "2":
            require(n_b.sign() < 0 and n_c.sign() > 0 and diff_num.sign() < 0,
                    "K32S S2 signs")
        else:
            require(n_b.sign() < 0 and n_c.sign() < 0 and sum_num.sign() > 0,
                    "K32S S3 signs")
    return {
        "verified": not failures,
        "failures": failures,
        "nonadjacent_segment_intersections": intersections,
        "nonadjacent_pairs_checked": 120,
        "field": "Q(sqrt(2))",
        "cell": cell,
        "hc34_cell": hc34_cell,
    }


def reconstruct_tangent(values: dict[str, Q2], cell: str) -> tuple[dict[str, Q2], list[str]]:
    """Coldly reconstruct K35T's eliminated terminal chart and Delta."""

    failures = []
    a, b, c, v = (values[name] for name in ("a", "b", "c", "v"))
    t1, t2 = values["t1"], values["t2"]
    k = values["sqrt_half"]
    if k != Q2(Fraction(0), Fraction(1, 2)):
        failures.append("sqrt_half is not the positive sqrt(2)/2 root")

    raw1, raw2 = tangent(t1), tangent(t2)
    z1 = (-raw1[0], -raw1[1])
    second_sign = -1 if cell.endswith("-minus") else 1
    z2 = (second_sign * raw2[0], second_sign * raw2[1])
    q = (-k, k)
    q2 = (Q2(0), Q2(-1))
    q3 = (k, k)
    q4 = (Q2(-1), Q2(0))
    q5 = (k, -k)
    zero = (Q2(0), Q2(0))
    w = [zero, (a, Q2(0))]
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
    h = a + b + c
    d2 = v * v + 1
    r2 = x8 * x8 + y8 * y8
    aa = v * x8 + y8
    bb = x8 - v * y8
    tangent_t = (d2 + 4 * r2 - h * h) / 4
    delta = aa * aa + bb * bb - tangent_t * tangent_t
    if not delta.is_zero():
        failures.append("K35T Delta is not zero")
    if tangent_t.sign() <= 0:
        failures.append("K35T T is not positive")
    if aa.sign() <= 0 or bb.sign() <= 0:
        failures.append("K35T terminal numerator is not first-quadrant")
    if (d2 - 2 * tangent_t).sign() <= 0:
        failures.append("K35T H-east inequality fails")
    if (tangent_t + aa).is_zero():
        failures.append("K35T terminal chart denominator is zero")
        return values, failures
    out = dict(values)
    out["t0"] = bb / (tangent_t + aa)
    return out, failures


def main(argv=None) -> int:
    argv = sys.argv if argv is None else argv
    if len(argv) not in (2, 3):
        print("usage: verify_k16w_exact.py <k16w-result.json> [cell]", file=sys.stderr)
        return 2
    source = Path(argv[1])
    token = argv[2] if len(argv) == 3 else None
    hc34_cell = token if token in HC34_CELLS else None
    cell = token if token is not None and hc34_cell is None else None
    out = OUT if cell is None and hc34_cell is None else source.with_name(source.stem + "-verification.json")
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
    elif payload.get("kind") == "k16w-hc38-tangent-cell-result":
        values, failures = tangent_q2_model(payload)
        result["failures"].extend(failures)
        if values is not None:
            values, failures = reconstruct_tangent(values, hc34_cell)
            result["failures"].extend(failures)
            if not failures:
                checked = verify(values, hc34_cell=hc34_cell)
                checked["tangent_reconstructed"] = True
                result.update(checked)
    else:
        values, failures = rational_model(payload)
        result["failures"].extend(failures)
        if values is not None:
            result.update(verify(values, cell=cell, hc34_cell=hc34_cell))
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
