from __future__ import annotations

import z3

from einstein.solvers.algebraic_models import exact_z3_payload


def test_z3_rational_payload_is_exact():
    payload = exact_z3_payload(z3.RealVal("7/11"))
    assert payload == {
        "kind": "rational",
        "numerator": 7,
        "denominator": 11,
        "smt2": "(/ 7.0 11.0)",
    }


def test_z3_algebraic_payload_preserves_defining_expression():
    value = z3.Sqrt(z3.RealVal(2))
    payload = exact_z3_payload(value)
    assert payload["kind"] == "algebraic"
    assert payload["smt2"]
    assert payload["decimal_80"].endswith("?")
