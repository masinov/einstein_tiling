#!/usr/bin/env python
"""Certify the 2-Lambda pullback countermodel family for the V4 local SFT."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_lift import (
    BASE_HNF,
    lift_2lambda_witness,
    semantic_base_witness,
    unsatisfied_clauses,
)
from einstein.theory.a4_v4_sft import V4_TWIST_PAIRS, build_v4_coverability_cnf
from einstein.theory.holonomy_csp import _cnf_sha256


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
SIGNATURE = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature.json"
RESIDUAL = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-signature-index60.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def _even_hnfs(maximum_index):
    return tuple(
        (a, b, d)
        for a in range(2, maximum_index + 1, 2)
        for d in range(2, maximum_index // a + 1, 2)
        for b in range(0, a, 2)
    )


def _aggregate(rows):
    digest = sha256()
    for row in rows:
        digest.update(json.dumps(row, sort_keys=True, separators=(",", ":")).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def _verify_finite_lift(arguments):
    shape, hnf, mapping_index, images, base_twists, selected, colors = arguments
    twists, values = lift_2lambda_witness(
        shape, hnf, base_twists, selected, colors
    )
    cnf, _ = build_v4_coverability_cnf(shape, hnf, images, twists)
    if unsatisfied_clauses(cnf, values):
        raise AssertionError(f"finite pullback failed: {hnf}")
    return {
        "hnf": list(hnf),
        "mapping_index": mapping_index,
        "twists": list(twists),
        "cnf_sha256": _cnf_sha256(cnf),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=24)
    args = parser.parse_args()
    matrix = json.loads(MATRIX.read_text())
    signature = json.loads(SIGNATURE.read_text())
    residual = json.loads(RESIDUAL.read_text())
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    signature_maps = tuple(signature["finite_signature"]["killing_mapping_indices"])
    shape = decode_compiled_key(KEY)
    witnesses = []
    for mapping_index in signature_maps:
        images = mappings[mapping_index]
        sat = []
        for twist_index, twists in enumerate(V4_TWIST_PAIRS):
            cnf, metadata = build_v4_coverability_cnf(
                shape, BASE_HNF, images, twists
            )
            with Cadical195(bootstrap_with=cnf) as solver:
                if solver.solve():
                    sat.append((twist_index, twists, cnf, metadata, solver.get_model()))
        if len(sat) != 1:
            raise AssertionError(f"map {mapping_index} has {len(sat)} base models")
        twist_index, twists, cnf, metadata, model = sat[0]
        selected, colors = semantic_base_witness(shape, model)
        induced, values = lift_2lambda_witness(
            shape, BASE_HNF, twists, selected, colors
        )
        if induced != twists or unsatisfied_clauses(cnf, values):
            raise AssertionError("semantic base witness failed clause replay")
        witnesses.append({
            "mapping_index": mapping_index,
            "images": list(images),
            "base_hnf": list(BASE_HNF),
            "base_twist_index": twist_index,
            "base_twists": list(twists),
            "canonical_cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "selected_placements": [list(row) for row in selected],
            "vertex_colors": [
                {"vertex": list(vertex), "color": color}
                for vertex, color in colors
            ],
            "selected_placement_count": len(selected),
            "coverage_surplus": 10 * len(selected) - metadata["cells"],
            "assignment_verified": True,
        })

    escape_hnfs = tuple(
        tuple(row["hnf"]) for row in residual["by_hnf"]
    )
    expected = {
        (tuple(row["hnf"]), row["mapping_index"]): tuple(row["sat_twist_indices"])
        for row in residual["pair_results"]
    }
    lifted_rows = []
    for witness in witnesses:
        selected = tuple(tuple(row) for row in witness["selected_placements"])
        colors = tuple(
            (tuple(row["vertex"]), row["color"])
            for row in witness["vertex_colors"]
        )
        images = tuple(witness["images"])
        base_twists = tuple(witness["base_twists"])
        for hnf in escape_hnfs:
            twists, values = lift_2lambda_witness(
                shape, hnf, base_twists, selected, colors
            )
            cnf, _ = build_v4_coverability_cnf(shape, hnf, images, twists)
            if unsatisfied_clauses(cnf, values):
                raise AssertionError("index-60 pullback failed clause replay")
            twist_index = V4_TWIST_PAIRS.index(twists)
            if expected[(hnf, witness["mapping_index"])] != (twist_index,):
                raise AssertionError("pullback does not explain unique residual twist")
            lifted_rows.append({
                "hnf": list(hnf),
                "mapping_index": witness["mapping_index"],
                "induced_twist_index": twist_index,
                "induced_twists": list(twists),
                "canonical_cnf_sha256": _cnf_sha256(cnf),
                "assignment_verified": True,
            })

    finite_hnfs = _even_hnfs(60)
    finite_tasks = []
    for witness in witnesses:
        selected = tuple(tuple(row) for row in witness["selected_placements"])
        colors = tuple(
            (tuple(row["vertex"]), row["color"])
            for row in witness["vertex_colors"]
        )
        images = tuple(witness["images"])
        base_twists = tuple(witness["base_twists"])
        for hnf in finite_hnfs:
            finite_tasks.append((
                shape, hnf, witness["mapping_index"], images, base_twists,
                selected, colors,
            ))
    print(
        f"finite pullback tasks: {len(finite_tasks)}; jobs={args.jobs}",
        flush=True,
    )
    finite_rows = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(_verify_finite_lift, task) for task in finite_tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            finite_rows.append(future.result())
            if completed % 192 == 0 or completed == len(finite_tasks):
                print(f"[{completed:4d}/{len(finite_tasks)}] pullbacks", flush=True)
    finite_rows.sort(key=lambda row: (row["mapping_index"], row["hnf"]))

    dependencies = (MATRIX, SIGNATURE, RESIDUAL)
    sources = (
        ROOT / "src/einstein/theory/a4_semidirect.py",
        ROOT / "src/einstein/theory/a4_v4_sft.py",
        ROOT / "src/einstein/theory/a4_v4_lift.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-v4-2lambda-pullback-family",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "statement_type": "explicit SAT countermodel family for a relaxation",
            "base_hnf": list(BASE_HNF),
            "signature_maps": len(signature_maps),
            "proof_status": "proof draft plus explicit base and finite pullback witnesses",
        },
        "provenance": {
            "dependencies": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in dependencies
            ],
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in sources
            ],
        },
        "family": {
            "condition": "HNF (a,b,d) has a,b,d even, equivalently L <= 2 Lambda",
            "construction": (
                "pull back the selected placements and V4 vertex colors along "
                "Lambda/L -> Lambda/(2 Lambda); restrict the base V4 holonomy"
            ),
            "consequence": (
                "no distinct-tail signature map can obstruct any HNF sublattice "
                "of 2 Lambda in the at-least-coverability relaxation"
            ),
            "logical_limit": "countermodels are overlapping covers, not tilings",
        },
        "summary": {
            "base_witnesses": len(witnesses),
            "base_witnesses_verified": sum(row["assignment_verified"] for row in witnesses),
            "index60_lifts_verified": len(lifted_rows),
            "finite_gate_maximum_index": 60,
            "finite_gate_even_hnfs": len(finite_hnfs),
            "finite_gate_map_hnf_lifts": len(finite_rows),
            "finite_gate_aggregate_sha256": _aggregate(finite_rows),
        },
        "base_witnesses": witnesses,
        "index60_lifts": lifted_rows,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))


if __name__ == "__main__":
    main()
