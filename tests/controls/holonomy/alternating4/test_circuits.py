"""Exact controls for affine V4 circuit extraction."""

import json
import random
from pathlib import Path

from einstein.repository import repository_root

from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.circuits import (
    affine_compatible,
    build_v4_equation_system,
    canonical_translation_circuit,
    minimal_affine_circuit,
    translation_orbit,
)
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.local_system import build_v4_coverability_cnf


ROOT = repository_root(Path(__file__))
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _fixture():
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = dict(payload["base_witnesses"][0])
    hnf = (4, 0, 4)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    return shape, hnf, row


def test_known_minimal_triple_and_translation_orbit():
    shape, hnf, row = _fixture()
    system = build_v4_equation_system(shape, hnf, row)
    lookup = {placement: variable for variable, placement in enumerate(
        system.placements, 1
    )}
    triple = tuple(lookup[placement] for placement in (
        (4, 0, 0), (11, 1, 3), (11, 3, 3)
    ))
    assert not affine_compatible(system, triple)
    assert minimal_affine_circuit(system, triple) == tuple(sorted(triple))
    assert all(affine_compatible(system, (
        triple[index], triple[(index + 1) % 3]
    )) for index in range(3))
    orbit = translation_orbit(system, triple)
    assert len(orbit) == 16
    assert canonical_translation_circuit(system, triple) == min(orbit)
    assert all(not affine_compatible(system, translate) for translate in orbit)


def test_union_find_matches_cnf_on_deterministic_subsets():
    shape, hnf, row = _fixture()
    system = build_v4_equation_system(shape, hnf, row)
    cnf, metadata = build_v4_coverability_cnf(
        shape, hnf, tuple(row["images"]), twists=tuple(row["twists"])
    )
    implications = cnf.clauses[metadata["cover_clauses"]:]
    rng = random.Random(0)
    with Cadical195(bootstrap_with=implications) as solver:
        for size in range(1, 9):
            for _ in range(12):
                selected = rng.sample(range(1, len(system.placements) + 1), size)
                assert affine_compatible(system, selected) == solver.solve(
                    assumptions=selected
                )
