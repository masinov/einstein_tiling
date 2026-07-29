#!/usr/bin/env python
"""Materialize clause-level SAT witnesses for A4 index-50 pair orbits."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.finite_groups import alternating_group
from einstein.theory.holonomy_csp import _cnf_sha256
from einstein.theory.holonomy_finite_csp import build_finite_boundary_holonomy_cnf


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-sat-index50.json"
VERIFY = ROOT / "scripts/verify_theory_w2_layer_d_a4_sat_index50.py"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _witness(arguments):
    shape, orbit_index, hnf, mapping_index, images, twist_index, twists, group = arguments
    cnf, metadata = build_finite_boundary_holonomy_cnf(
        shape, hnf, images, twists, group
    )
    with Cadical195(bootstrap_with=cnf) as solver:
        if not solver.solve():
            raise AssertionError(f"recorded SAT pair orbit {orbit_index} became UNSAT")
        model = solver.get_model()
    true_variables = sorted(literal for literal in model if literal > 0)
    true_set = set(true_variables)
    if not all(any(
        literal in true_set if literal > 0 else -literal not in true_set
        for literal in clause
    ) for clause in cnf.clauses):
        raise AssertionError(f"solver model failed direct clause check: {orbit_index}")
    return {
        "pair_orbit": orbit_index,
        "hnf": list(hnf),
        "mapping_index": mapping_index,
        "twist_index": twist_index,
        "twists": list(twists),
        "cnf_sha256": _cnf_sha256(cnf),
        "canonical_metadata": metadata,
        "model_true_variables": true_variables,
    }


def main():
    matrix = json.loads(MATRIX.read_text())
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    shape = decode_compiled_key(KEY)
    group = alternating_group(4)
    tasks = []
    for row in matrix["finalist"]["representative_results"]:
        if row["sat_twist_index"] is None:
            continue
        sat_row = next(item for item in row["checks"] if item["sat"])
        representative = row["representative"]
        mapping_index = representative["mapping_index"]
        tasks.append((
            shape, row["pair_orbit"], tuple(representative["hnf"]),
            mapping_index, mappings[mapping_index], sat_row["twist_index"],
            tuple(sat_row["twists"]), group,
        ))
    if len(tasks) != 32:
        raise AssertionError(f"expected 32 SAT pair orbits, got {len(tasks)}")

    witnesses = []
    with ProcessPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_witness, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            witnesses.append(future.result())
            if completed % 8 == 0 or completed == len(tasks):
                print(f"[{completed:2d}/{len(tasks)}] SAT witnesses", flush=True)
    witnesses.sort(key=lambda row: row["pair_orbit"])
    sources = (Path(__file__), VERIFY)
    payload = {
        "kind": "theory-w2-layer-d-a4-index50-sat-witnesses",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "non_obstructed_pair_orbits": len(witnesses),
            "witness_semantics": (
                "listed variables are true and every other canonical CNF "
                "variable is false; the verifier checks every clause"
            ),
            "logical_limit": (
                "these are relaxed at-least-cover/holonomy models, not exact "
                "covers or tilings"
            ),
        },
        "provenance": {
            "matrix": {
                "path": str(MATRIX.relative_to(ROOT)),
                "sha256": sha256(MATRIX.read_bytes()).hexdigest(),
            },
            "sources": [
                {"path": str(path.relative_to(ROOT)),
                 "sha256": sha256(path.read_bytes()).hexdigest()}
                for path in sources
            ],
        },
        "witnesses": witnesses,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
