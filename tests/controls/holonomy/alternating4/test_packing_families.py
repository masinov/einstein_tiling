"""Controls for the candidate infinite packing-family invariant."""

import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.packing_families import (
    area_admissible_2lambda_hnfs,
    build_signature_packing_cnf,
)


ROOT = repository_root(Path(__file__))
KEY = "010001010104010502f002f1030b030c04fa04fb"


def test_area_admissible_2lambda_hnf_counts():
    hnfs = area_admissible_2lambda_hnfs(60)
    assert len(hnfs) == 48
    assert {a * d for a, _, d in hnfs} == {20, 40, 60}
    assert all(a % 2 == b % 2 == d % 2 == 0 for a, b, d in hnfs)


def test_base_packing_family_builder_reproduces_full_signature_product():
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    cnf, metadata = build_signature_packing_cnf(
        shape, (2, 0, 2), payload["base_witnesses"]
    )
    assert metadata["layers"] == 16
    assert metadata["packing"]["orbit_clauses"] == 48
    assert metadata["packing"]["overlap_cells"] == 6
    assert metadata["clauses"] == len(cnf.clauses)
