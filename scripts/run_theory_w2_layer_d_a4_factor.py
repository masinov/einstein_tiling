#!/usr/bin/env python
"""Record the exact V4 semidirect C3 factorization behind the A4 signature."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from einstein.theory.a4_semidirect import canonical_a4_semidirect
from einstein.theory.holonomy import KITE_EDGE_GENERATORS
from einstein.theory.holonomy_finite_csp import commuting_pairs


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
SIGNATURE = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-factor.json"


def _digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    matrix = json.loads(MATRIX.read_text())
    signature = json.loads(SIGNATURE.read_text())
    model = canonical_a4_semidirect()
    group = model.group
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    killers = frozenset(signature["finite_signature"]["killing_mapping_indices"])

    # Independent exhaustive table check; this is intentionally repeated here
    # rather than trusting the unit-test process.
    for left in range(group.order):
        for right in range(group.order):
            expected = group.multiplication[left][right]
            actual = model.element(model.edge_equation(group.identity, left, right))
            if actual != expected:
                raise AssertionError("semidirect multiplication mismatch")

    mapping_rows = []
    for index, images in enumerate(mappings):
        coordinates = tuple(model.coordinate(value) for value in images)
        predicate = (
            all(value.q == 0 for value in coordinates[3:])
            and len({value.v for value in coordinates[3:]}) == 3
        )
        if predicate != (index in killers):
            raise AssertionError("factorized signature predicate mismatch")
        mapping_rows.append({
            "mapping_index": index,
            "v4_coordinates": [value.v for value in coordinates],
            "c3_coordinates": [value.q for value in coordinates],
            "distinct_v4_tail": predicate,
        })

    map7 = mapping_rows[7]
    geometric_c3 = [
        (2 * x + y) % 3 for x, y in KITE_EDGE_GENERATORS
    ]
    if map7["c3_coordinates"] != geometric_c3:
        raise AssertionError("map 7 C3 projection is not the geometric character")

    twists = commuting_pairs(group)
    twist_rows = []
    for index, (left, right) in enumerate(twists):
        x, y = model.coordinate(left), model.coordinate(right)
        if not model.commute(x, y):
            raise AssertionError("commuting-pair coordinate equation failed")
        twist_rows.append({
            "twist_index": index,
            "elements": [left, right],
            "v4_coordinates": [x.v, y.v],
            "c3_coordinates": [x.q, y.q],
        })
    quotient_pair_counts = Counter(
        tuple(row["c3_coordinates"]) for row in twist_rows
    )
    if quotient_pair_counts[(0, 0)] != 16 or any(
        quotient_pair_counts[pair] != 4
        for pair in quotient_pair_counts if pair != (0, 0)
    ):
        raise AssertionError("unexpected A4 commuting-twist factorization")

    sources = (
        ROOT / "src/einstein/theory/a4_semidirect.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-a4-semidirect-factorization",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "statement_type": "exact group and finite-map classification",
            "target": "A4",
            "mapping_classes": len(mappings),
            "commuting_twists": len(twists),
        },
        "provenance": {
            "dependencies": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in (MATRIX, SIGNATURE)
            ],
            "sources": [
                {"path": str(path.relative_to(ROOT)), "sha256": _digest(path)}
                for path in sources
            ],
        },
        "factorization": {
            "normal_subgroup": "V4 = GF(2)^2",
            "quotient": "C3",
            "coordinate_convention": "element = v * c^q",
            "v4_packed_basis_elements": list(model.v4_elements),
            "c3_section_elements": list(model.c3_elements),
            "action": "M(x,y) = (y,x+y) over GF(2)",
            "multiplication": "(v,q)(w,r) = (v + M^q w, q+r)",
            "edge_equation_c3": "q_y = q_d + q_x + q_label (mod 3)",
            "edge_equation_v4": (
                "v_y = v_d + M^q_d v_x + "
                "M^(q_d+q_x) v_label (over GF(2)^2)"
            ),
        },
        "map7": {
            **map7,
            "edge_vectors": [list(vector) for vector in KITE_EDGE_GENERATORS],
            "geometric_c3_character": "chi(x,y) = 2x+y (mod 3)",
            "geometric_c3_values": geometric_c3,
        },
        "signature": {
            "killing_mapping_indices": sorted(killers),
            "factorized_predicate_exact": True,
            "predicate": (
                "the three tail labels have q=0 and three distinct V4 values"
            ),
            "mappings": mapping_rows,
        },
        "twists": {
            "c3_pair_counts": {
                f"{left},{right}": count
                for (left, right), count in sorted(quotient_pair_counts.items())
            },
            "rows": twist_rows,
        },
        "next_obligation": (
            "derive from exact-cover topology and the factorized edge equations "
            "which HNF congruence classes force the distinct-V4-tail obstruction"
        ),
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({
        "map7_v4": map7["v4_coordinates"],
        "map7_c3": map7["c3_coordinates"],
        "killer_classes": len(killers),
        "twist_c3_pair_counts": payload["twists"]["c3_pair_counts"],
    }, indent=1))


if __name__ == "__main__":
    main()
