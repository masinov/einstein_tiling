#!/usr/bin/env python
"""Cold-check the full 16-map V4 product countermodel and its lifts."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.lifts import BASE_HNF, unsatisfied_clauses
from einstein.holonomy.alternating4.products import (
    build_v4_product_coverability_cnf,
    lift_product_witness,
)
from einstein.holonomy.constraints import _cnf_sha256


ROOT = repository_root(Path(__file__))
ARTIFACT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-product.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    payload = json.loads(ARTIFACT.read_text())
    if payload["kind"] != "theory-w2-layer-d-full-v4-product-countermodel":
        raise AssertionError("unexpected artifact kind")
    for section in ("dependencies", "sources"):
        for row in payload["provenance"][section]:
            path = ROOT / row["path"]
            if sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise AssertionError(f"provenance mismatch: {row['path']}")
    shape = decode_compiled_key(KEY)
    witness = payload["base_witness"]
    images = tuple(tuple(row) for row in witness["images"])
    base_twists = tuple(tuple(row) for row in witness["base_twists"])
    selected = tuple(tuple(row) for row in witness["selected_placements"])
    colors = tuple(tuple(
        (tuple(row["vertex"]), row["color"]) for row in layer
    ) for layer in witness["layer_vertex_colors"])
    layers = tuple(zip(images, base_twists))
    cnf, metadata = build_v4_product_coverability_cnf(shape, BASE_HNF, layers)
    induced, values = lift_product_witness(
        shape, BASE_HNF, base_twists, selected, colors
    )
    if (induced != base_twists
            or metadata != witness["metadata"]
            or _cnf_sha256(cnf) != witness["canonical_cnf_sha256"]
            or unsatisfied_clauses(cnf, values)):
        raise AssertionError("base full-product witness replay failed")
    for row in payload["index60_lifts"]:
        hnf = tuple(row["hnf"])
        induced, values = lift_product_witness(
            shape, hnf, base_twists, selected, colors
        )
        lifted_cnf, lifted_metadata = build_v4_product_coverability_cnf(
            shape, hnf, tuple(zip(images, induced))
        )
        if (lifted_metadata != row["metadata"]
                or _cnf_sha256(lifted_cnf) != row["canonical_cnf_sha256"]
                or unsatisfied_clauses(lifted_cnf, values)):
            raise AssertionError(f"full-product lift replay failed: {hnf}")
    print(
        f"full V4 product countermodel VERIFIED: {len(images)} layers; "
        f"{len(payload['index60_lifts'])} index-60 lifts"
    )


if __name__ == "__main__":
    main()
