"""Controls for the candidate V4 packing-density inequality."""

import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.density import build_signature_density_bound_cnf


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def test_small_density_bound_control_is_unsat():
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    cnf, metadata = build_signature_density_bound_cnf(
        shape, (2, 0, 2), payload["base_witnesses"][0]
    )
    assert metadata["candidate_upper_bound"] == 2
    assert metadata["asserted_minimum"] == 3
    assert metadata["packing_clauses"] == 48
    assert metadata["exact_cover_placements"] is None
    assert metadata["exact_cover_placement_ratio"] == [24, 10]
    with Cadical195(bootstrap_with=cnf) as solver:
        assert not solver.solve()
