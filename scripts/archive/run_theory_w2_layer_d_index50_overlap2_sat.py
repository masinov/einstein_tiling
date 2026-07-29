#!/usr/bin/env python
"""Materialize SAT witnesses for the 77 overlap-at-most-two pair orbits."""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy_overlap import build_bounded_overlap_holonomy_cnf
from einstein.theory.holonomy_csp import _cnf_sha256


ROOT = Path(__file__).resolve().parents[2]
SEARCH = ROOT / "docs/notebook/assets/theory-w2-layer-d-overlap2-index50.json"
BASE = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index50.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-overlap2-sat-index50.json"
VERIFY = ROOT / "scripts/verify_theory_w2_layer_d_index50_overlap2_sat.py"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _solve(arguments):
    shape, orbit_index, hnf, mapping_index, images, twists = arguments
    cnf, metadata = build_bounded_overlap_holonomy_cnf(
        shape, hnf, images, twists, maximum_coverage=2
    )
    with Cadical195(bootstrap_with=cnf) as solver:
        if not solver.solve():
            raise AssertionError(f"SAT orbit changed polarity: {orbit_index}")
        model = solver.get_model()
    true_variables = sorted(literal for literal in model if literal > 0)
    true_set = set(true_variables)
    if not all(any(
        literal in true_set if literal > 0 else -literal not in true_set
        for literal in clause
    ) for clause in cnf.clauses):
        raise AssertionError(f"bad solver model: {orbit_index}")
    return {
        "pair_orbit": orbit_index,
        "hnf": list(hnf),
        "mapping_index": mapping_index,
        "twists": [list(twists[0]), list(twists[1])],
        "cnf_sha256": _cnf_sha256(cnf),
        "canonical_metadata": metadata,
        "model_true_variables": true_variables,
    }


def main():
    search = json.loads(SEARCH.read_text())
    base = json.loads(BASE.read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in base["finalist"]["mapping_representatives"]
    )
    shape = decode_compiled_key(KEY)
    tasks = []
    for row in search["finalist"]["representative_results"]:
        if row["scan"]["verdict"] != "not-obstructed":
            continue
        sat = next(item for item in row["scan"]["results"] if item["sat"])
        rep = row["representative"]
        tasks.append((
            shape, row["pair_orbit"], tuple(rep["hnf"]), rep["mapping_index"],
            mappings[rep["mapping_index"]],
            tuple(tuple(value) for value in sat["twists"]),
        ))
    if len(tasks) != 77:
        raise AssertionError(f"expected 77 tasks, got {len(tasks)}")
    witnesses = []
    with ProcessPoolExecutor(max_workers=16) as executor:
        futures = [executor.submit(_solve, task) for task in tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            witnesses.append(future.result())
            if completed % 10 == 0 or completed == len(tasks):
                print(f"[{completed:2d}/{len(tasks)}] overlap-2 witnesses", flush=True)
    witnesses.sort(key=lambda row: row["pair_orbit"])
    sources = (Path(__file__), VERIFY)
    payload = {
        "kind": "theory-w2-layer-d-index50-overlap2-sat-witnesses",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "maximum_coverage": 2,
            "non_obstructed_pair_orbits": len(witnesses),
            "logical_limit": "relaxed models, not exact covers or tilings",
        },
        "provenance": {
            "dependencies": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in (SEARCH, BASE)
            ],
            "sources": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in sources
            ],
        },
        "witnesses": witnesses,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
