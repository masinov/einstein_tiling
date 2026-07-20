#!/usr/bin/env python
"""Record the full 16-map product countermodel on 2 Lambda and its lifts."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_lift import BASE_HNF, unsatisfied_clauses
from einstein.theory.a4_v4_product import (
    build_v4_product_coverability_cnf,
    lift_product_witness,
    semantic_product_witness,
)
from einstein.theory.holonomy_csp import _cnf_sha256, quotient_boundary_data


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
RESIDUAL = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-signature-index60.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-product.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    base = json.loads(BASE.read_text())
    residual = json.loads(RESIDUAL.read_text())
    witnesses = sorted(base["base_witnesses"], key=lambda row: row["mapping_index"])
    shape = decode_compiled_key(KEY)
    layers = tuple(
        (tuple(row["images"]), tuple(row["base_twists"]))
        for row in witnesses
    )
    cnf, metadata = build_v4_product_coverability_cnf(shape, BASE_HNF, layers)
    with Cadical195(bootstrap_with=cnf) as solver:
        if not solver.solve():
            raise AssertionError("full signature product unexpectedly UNSAT")
        stats = solver.accum_stats()
        selected, layer_colors = semantic_product_witness(
            shape, solver.get_model(), len(layers)
        )
    induced, values = lift_product_witness(
        shape, BASE_HNF,
        tuple(tuple(row["base_twists"]) for row in witnesses),
        selected, layer_colors,
    )
    if induced != tuple(twists for _, twists in layers) or unsatisfied_clauses(cnf, values):
        raise AssertionError("semantic full-product witness failed replay")

    instance, _, _ = quotient_boundary_data(shape, BASE_HNF)
    selected_set = set(selected)
    multiplicities = [0] * instance.n_cells
    for (op, tu, tv), mask in instance.placements:
        if (op, tu % 2, tv % 2) not in selected_set:
            continue
        for cell in range(instance.n_cells):
            multiplicities[cell] += (mask >> cell) & 1
    histogram = Counter(multiplicities)
    if min(multiplicities) < 1 or max(multiplicities) > 2:
        raise AssertionError("full-product witness is not an overlap-two cover")

    escape_hnfs = tuple(tuple(row["hnf"]) for row in residual["by_hnf"])
    lifts = []
    for hnf in escape_hnfs:
        induced, values = lift_product_witness(
            shape, hnf,
            tuple(tuple(row["base_twists"]) for row in witnesses),
            selected, layer_colors,
        )
        lifted_layers = tuple(
            (tuple(row["images"]), twists)
            for row, twists in zip(witnesses, induced)
        )
        lifted_cnf, lifted_metadata = build_v4_product_coverability_cnf(
            shape, hnf, lifted_layers
        )
        if unsatisfied_clauses(lifted_cnf, values):
            raise AssertionError("full-product index-60 lift failed")
        lifts.append({
            "hnf": list(hnf),
            "induced_twists": [list(twists) for twists in induced],
            "canonical_cnf_sha256": _cnf_sha256(lifted_cnf),
            "metadata": lifted_metadata,
            "assignment_verified": True,
        })

    dependencies = (BASE, RESIDUAL)
    sources = (
        ROOT / "src/einstein/theory/a4_v4_sft.py",
        ROOT / "src/einstein/theory/a4_v4_lift.py",
        ROOT / "src/einstein/theory/a4_v4_product.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-full-v4-product-countermodel",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "signature_maps_in_product": len(layers),
            "base_hnf": list(BASE_HNF),
            "statement_type": "explicit SAT countermodel for the full product relaxation",
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
        "conclusion": {
            "full_product_sat": True,
            "all_pairs_sat_by_projection": True,
            "overlap_two_sat": True,
            "infinite_pullback_family": "every HNF sublattice of 2 Lambda",
            "missing_axiom": "nonoverlap/packing or an equivalent density constraint",
            "not_a_tiling": True,
        },
        "base_witness": {
            "mapping_indices": [row["mapping_index"] for row in witnesses],
            "images": [row["images"] for row in witnesses],
            "base_twists": [row["base_twists"] for row in witnesses],
            "selected_placements": [list(row) for row in selected],
            "layer_vertex_colors": [
                [
                    {"vertex": list(vertex), "color": color}
                    for vertex, color in colors
                ]
                for colors in layer_colors
            ],
            "coverage_multiplicity_histogram": {
                str(value): count for value, count in sorted(histogram.items())
            },
            "coverage_surplus": sum(multiplicities) - len(multiplicities),
            "canonical_cnf_sha256": _cnf_sha256(cnf),
            "metadata": metadata,
            "solver_conflicts": stats.get("conflicts"),
            "assignment_verified": True,
        },
        "index60_lifts": lifts,
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({
        "full_product_sat": True,
        "selected_placements": len(selected),
        "coverage_histogram": payload["base_witness"]["coverage_multiplicity_histogram"],
        "index60_lifts": len(lifts),
    }, indent=1))


if __name__ == "__main__":
    main()
