#!/usr/bin/env python
"""Run and archive the W1.a exact transfer reference controls.

The control matrix covers every free polykite through n=3, primitive and
nonprimitive vectors, independent small transverse torus checks, a four-kite
torsion trap, and four small hat vectors.  This is a validation artifact, not a
claim about the finalist or all period vectors.
"""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from einstein.db import code_version, deserialize_cells, serialize_cells
from einstein.enumeration.polyform import enumerate_free_polykites
from einstein.funnel.a1_torus import solve_torus_sat, verify_certificate
from einstein.theory.transfer import (
    cylinder_basis,
    decide_period_vector,
    lattice_hnf,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "notebook" / "assets" / "theory-w1-phase0-controls.json"
VECTORS = ((1, 0), (0, 1), (1, 1), (2, 0))
TRANSVERSE_WIDTHS = (1, 2, 3)
TORSION_SHAPE = ((0, 0, 0), (0, 0, 1), (0, 0, 2), (2, 2, 3))


def hat_shape() -> tuple:
    fixture = ROOT / "tests" / "fixtures" / "polykites-n8.sqlite"
    conn = sqlite3.connect(f"{fixture.resolve().as_uri()}?mode=ro", uri=True)
    row = conn.execute("SELECT key FROM shapes WHERE id=635").fetchone()
    conn.close()
    if row is None:
        raise RuntimeError("hat anchor shape 635 is absent from shapes.sqlite")
    shape = deserialize_cells(row[0])
    if len(shape) != 8:
        raise RuntimeError("shape 635 is not the expected eight-kite hat anchor")
    return shape


def run_one(shape, vector, *, torus_widths=TRANSVERSE_WIDTHS) -> dict:
    result = decide_period_vector(shape, vector)
    row = result.summary()
    row["shape"] = serialize_cells(shape)
    if result.verdict == "resource-exhausted":
        raise RuntimeError(f"unexpected reference limit for {vector}: {result.limit}")
    if result.verdict == "cycle":
        if not verify_certificate(shape, result.certificate):
            raise AssertionError("positive control failed independent A1 verification")

    p, _, u = cylinder_basis(vector)
    torus = []
    for width in torus_widths:
        second = (width * u[0], width * u[1])
        hnf = lattice_hnf(vector, second)
        certificate, exhausted = solve_torus_sat(shape, hnf)
        if exhausted:
            raise RuntimeError(f"unbudgeted torus control exhausted for {hnf}")
        verdict = "sat" if certificate else "unsat"
        if certificate and not verify_certificate(shape, certificate):
            raise AssertionError("torus control certificate did not verify")
        if verdict == "sat" and result.verdict != "cycle":
            raise AssertionError(
                f"transfer/torus disagreement for vector={vector}, width={width}"
            )
        torus.append({"width": width, "hnf": list(hnf), "verdict": verdict})
    row["bounded_torus_crosscheck"] = torus
    row.pop("certificate", None)
    if result.certificate:
        row["a1_certificate"] = result.certificate
    return row


def main() -> None:
    census = []
    for n, forms in enumerate_free_polykites(3):
        for index, shape in enumerate(forms):
            for vector in VECTORS:
                row = run_one(shape, vector)
                row.update({"n": n, "shape_index": index})
                census.append(row)

    primitive = run_one(TORSION_SHAPE, (1, 0))
    nonprimitive = run_one(TORSION_SHAPE, (2, 0))
    if primitive["verdict"] != "cycle-free" or nonprimitive["verdict"] != "cycle":
        raise AssertionError("nonprimitive torsion trap did not separate (1,0)/(2,0)")

    hat = hat_shape()
    hat_rows = [run_one(hat, vector) for vector in VECTORS]
    if any(row["verdict"] != "cycle-free" for row in hat_rows):
        raise AssertionError("known aperiodic hat produced a transfer cycle")

    source = ROOT / "src" / "einstein" / "theory" / "transfer.py"
    data = {
        "kind": "theory-w1-phase0-controls",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "small_census": "all free polykites n<=3",
            "vectors": [list(vector) for vector in VECTORS],
            "bounded_torus_transverse_widths": list(TRANSVERSE_WIDTHS),
            "hat_vectors": [list(vector) for vector in VECTORS],
            "claim": (
                "reference validation only; bounded torus comparisons and four "
                "hat vectors do not establish a universal period exclusion"
            ),
        },
        "provenance": {
            "code_version": code_version(),
            "transfer_source": str(source.relative_to(ROOT)),
            "transfer_source_sha256": sha256(source.read_bytes()).hexdigest(),
            "hat_source": "tests/fixtures/polykites-n8.sqlite shape id 635",
        },
        "small_census": census,
        "torsion_control": {
            "shape": serialize_cells(TORSION_SHAPE),
            "primitive": primitive,
            "nonprimitive": nonprimitive,
            "expected": "(1,0) cycle-free; (2,0) cycle",
        },
        "hat": hat_rows,
        "summary": {
            "small_census_cases": len(census),
            "small_census_resource_exhaustions": sum(
                row["verdict"] == "resource-exhausted" for row in census
            ),
            "bounded_torus_checks": sum(
                len(row["bounded_torus_crosscheck"])
                for row in census + [primitive, nonprimitive] + hat_rows
            ),
            "verified_transfer_cycles": sum(
                row["verdict"] == "cycle"
                for row in census + [primitive, nonprimitive] + hat_rows
            ),
            "hat_cycle_free_vectors": sum(
                row["verdict"] == "cycle-free" for row in hat_rows
            ),
            "disagreements": 0,
        },
    }
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(data["summary"], indent=1))


if __name__ == "__main__":
    main()
