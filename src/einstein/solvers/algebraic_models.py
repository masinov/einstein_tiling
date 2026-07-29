"""Conservative exact extraction of cvc5 real model values.

HC-38 accepts only rationals and values structurally recognized in
``Q(sqrt(2))``.  A general real algebraic number is preserved with its
defining data but is never promoted to that field.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt

import cvc5


Polynomial = dict[int, Fraction]


def _add(left: Polynomial, right: Polynomial) -> Polynomial:
    out = dict(left)
    for power, coefficient in right.items():
        out[power] = out.get(power, Fraction(0)) + coefficient
    return {power: value for power, value in out.items() if value}


def _multiply(left: Polynomial, right: Polynomial) -> Polynomial:
    out: Polynomial = {}
    for p_left, c_left in left.items():
        for p_right, c_right in right.items():
            power = p_left + p_right
            out[power] = out.get(power, Fraction(0)) + c_left * c_right
    return {power: value for power, value in out.items() if value}


def _polynomial(term: cvc5.Term, variable: cvc5.Term) -> Polynomial:
    if term == variable:
        return {1: Fraction(1)}
    if term.isRealValue():
        return {0: Fraction(term.getRealValue())}
    kind = term.getKind()
    children = list(term)
    if kind == cvc5.Kind.ADD:
        out: Polynomial = {}
        for child in children:
            out = _add(out, _polynomial(child, variable))
        return out
    if kind == cvc5.Kind.SUB:
        if len(children) == 1:
            return {p: -c for p, c in _polynomial(children[0], variable).items()}
        out = _polynomial(children[0], variable)
        for child in children[1:]:
            out = _add(out, {
                p: -c for p, c in _polynomial(child, variable).items()
            })
        return out
    if kind == cvc5.Kind.NEG:
        return {p: -c for p, c in _polynomial(children[0], variable).items()}
    if kind == cvc5.Kind.MULT:
        out = {0: Fraction(1)}
        for child in children:
            out = _multiply(out, _polynomial(child, variable))
        return out
    if kind == cvc5.Kind.POW and len(children) == 2 and children[1].isIntegerValue():
        exponent = children[1].getIntegerValue()
        if exponent < 0:
            raise ValueError("negative exponent in algebraic defining polynomial")
        base = _polynomial(children[0], variable)
        out = {0: Fraction(1)}
        for _ in range(exponent):
            out = _multiply(out, base)
        return out
    raise ValueError(f"unsupported defining-polynomial term: {term}")


def _rational_square_root(value: Fraction) -> Fraction | None:
    if value < 0:
        return None
    numerator = isqrt(value.numerator)
    denominator = isqrt(value.denominator)
    if numerator * numerator != value.numerator:
        return None
    if denominator * denominator != value.denominator:
        return None
    return Fraction(numerator, denominator)


def _q2_sign(a: Fraction, b: Fraction) -> int:
    """Sign of ``a+b*sqrt(2)`` using rational comparisons only."""

    if a == 0:
        return (b > 0) - (b < 0)
    if b == 0:
        return (a > 0) - (a < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    lhs = a * a
    rhs = 2 * b * b
    if lhs == rhs:
        return 0
    if a > 0:
        return 1 if lhs > rhs else -1
    return 1 if rhs > lhs else -1


def _in_interval(candidate: tuple[Fraction, Fraction], lower: Fraction,
                 upper: Fraction) -> bool:
    a, b = candidate
    return _q2_sign(a - lower, b) > 0 and _q2_sign(upper - a, -b) > 0


def _fraction_payload(value: Fraction) -> dict:
    return {
        "kind": "rational",
        "numerator": value.numerator,
        "denominator": value.denominator,
    }


def _q2_payload(a: Fraction, b: Fraction, polynomial: Polynomial,
                lower: Fraction, upper: Fraction) -> dict:
    return {
        "kind": "q_sqrt2",
        "rational_numerator": a.numerator,
        "rational_denominator": a.denominator,
        "sqrt2_numerator": b.numerator,
        "sqrt2_denominator": b.denominator,
        "defining_polynomial": {
            str(power): {
                "numerator": coefficient.numerator,
                "denominator": coefficient.denominator,
            }
            for power, coefficient in sorted(polynomial.items())
        },
        "isolation": {
            "lower": _fraction_payload(lower),
            "upper": _fraction_payload(upper),
        },
    }


def exact_real_payload(solver: cvc5.Solver, value: cvc5.Term) -> dict:
    """Serialize one cvc5 real value under HC-38's fail-closed boundary."""

    if value.isRealValue():
        return _fraction_payload(Fraction(value.getRealValue()))
    if not value.isRealAlgebraicNumber():
        return {"kind": "unsupported", "term": str(value)}

    variable = solver.mkVar(solver.getRealSort(), "model_value")
    polynomial_term = value.getRealAlgebraicNumberDefiningPolynomial(variable)
    lower = Fraction(value.getRealAlgebraicNumberLowerBound().getRealValue())
    upper = Fraction(value.getRealAlgebraicNumberUpperBound().getRealValue())
    try:
        polynomial = _polynomial(polynomial_term, variable)
    except ValueError as error:
        return {
            "kind": "unsupported_algebraic",
            "term": str(value),
            "reason": str(error),
            "lower": str(lower),
            "upper": str(upper),
        }

    degree = max(polynomial, default=-1)
    candidates: list[tuple[Fraction, Fraction]] = []
    if degree == 1:
        candidates.append((-polynomial.get(0, Fraction(0)) / polynomial[1], Fraction(0)))
    elif degree == 2:
        qa = polynomial[2]
        qb = polynomial.get(1, Fraction(0))
        qc = polynomial.get(0, Fraction(0))
        discriminant = qb * qb - 4 * qa * qc
        rational_root = _rational_square_root(discriminant)
        sqrt2_root = _rational_square_root(discriminant / 2)
        if rational_root is not None:
            candidates.extend(((-qb + sign * rational_root) / (2 * qa), Fraction(0))
                              for sign in (-1, 1))
        elif sqrt2_root is not None:
            candidates.extend((-qb / (2 * qa), sign * sqrt2_root / (2 * qa))
                              for sign in (-1, 1))

    selected = [candidate for candidate in candidates
                if _in_interval(candidate, lower, upper)]
    if len(selected) == 1:
        a, b = selected[0]
        if b == 0:
            return _fraction_payload(a)
        return _q2_payload(a, b, polynomial, lower, upper)
    return {
        "kind": "unsupported_algebraic",
        "term": str(value),
        "degree": degree,
        "defining_polynomial": {
            str(power): str(coefficient)
            for power, coefficient in sorted(polynomial.items())
        },
        "lower": str(lower),
        "upper": str(upper),
    }
