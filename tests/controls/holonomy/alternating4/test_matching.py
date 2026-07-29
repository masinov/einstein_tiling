"""Exact controls for the adaptive two-center Hall certificate."""

import json
import itertools
import random
from pathlib import Path

from einstein.repository import repository_root

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.circuits import build_v4_equation_system
from einstein.holonomy.alternating4.matching import (
    hall_deficiency,
    hall_neighborhood,
    hall_witness_profile,
    minimal_hall_witness,
    placement_center_supports,
    two_center_matching,
    verify_two_matching,
)
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import placement_lattice_cells


ROOT = repository_root(Path(__file__))
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _fixture(hnf=(4, 0, 10)):
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = dict(payload["base_witnesses"][0])
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    return shape, system


def test_known_density_half_extremizer_has_a_perfect_two_matching():
    shape, system = _fixture()
    lookup = {placement: variable for variable, placement in enumerate(
        system.placements, 1
    )}
    placements = (
        (5, 2, 4), (6, 3, 2), (8, 0, 0), (9, 0, 9), (8, 1, 6),
        (8, 3, 4), (8, 0, 7), (3, 2, 2), (0, 1, 2), (5, 3, 2),
        (3, 0, 5), (11, 0, 8), (1, 3, 4), (9, 1, 1), (8, 1, 4),
        (10, 2, 7), (2, 1, 9), (7, 1, 8), (0, 2, 0), (1, 1, 6),
    )
    supports = placement_center_supports(shape, system)
    result = two_center_matching(supports, tuple(lookup[p] for p in placements))
    assert result.saturated
    assert result.matched == 40
    assert verify_two_matching(supports, result)


def test_hall_deficiency_witness_is_exact():
    supports = (
        frozenset(((0, 0), (1, 0))),
        frozenset(((0, 0), (1, 0))),
    )
    result = two_center_matching(supports, (1, 2))
    assert not result.saturated
    assert result.deficient_tiles == (1, 2)
    assert result.deficient_centers == ((0, 0), (1, 0))
    assert verify_two_matching(supports, result)


def test_minimal_hall_witness_discards_irrelevant_tiles():
    core_centers = tuple((index, 0) for index in range(5))
    supports = (
        frozenset(core_centers[index] for index in (0, 1, 2, 3)),
        frozenset(core_centers[index] for index in (0, 1, 2, 4)),
        frozenset(core_centers[index] for index in (0, 1, 3, 4)),
        frozenset((index, 1) for index in range(4)),
    )
    assert hall_neighborhood(supports, (1, 2, 3)) == frozenset(core_centers)
    assert hall_deficiency(supports, (1, 2, 3)) == 1
    # The full set has nine centers for eight requested matches, but still
    # fails Hall because its first three tiles contain a deficient subset.
    result = minimal_hall_witness(supports, (1, 2, 3, 4))
    assert result.deficient_tiles == (1, 2, 3)
    assert verify_two_matching(supports, result)
    assert hall_witness_profile(supports, result) == {
        "tile_count": 3,
        "center_count": 5,
        "deficiency": 1,
        "private_center_histogram": {0: 3},
        "center_degree_histogram": {2: 3, 3: 2},
        "signed_curvature": 2,
        "intersection_edges": 3,
    }


def test_minimal_hall_witness_can_have_deficiency_two():
    centers = frozenset((index, 0) for index in range(4))
    supports = (centers, centers, centers)
    result = minimal_hall_witness(supports, (1, 2, 3))
    profile = hall_witness_profile(supports, result)
    assert profile["deficiency"] == 2
    assert profile["private_center_histogram"] == {0: 3}


def test_duplicate_cardinality_wires_encode_weight_two_exactly():
    # Discovery uses this dependency-free reduction instead of PyPBLib.
    for bound in range(6):
        cnf = CardEnc.atleast(
            lits=[1, 1, 2, 2, -3], bound=bound, top_id=3,
            encoding=EncType.cardnetwrk,
        )
        with Cadical195(bootstrap_with=cnf) as solver:
            for first, second, center in itertools.product((False, True), repeat=3):
                assumptions = [
                    1 if first else -1,
                    2 if second else -2,
                    3 if center else -3,
                ]
                expected = 2 * first + 2 * second + (not center) >= bound
                assert solver.solve(assumptions=assumptions) == expected


def test_small_torus_hall_obstruction_disappears_on_the_plane():
    # This compatible 4x4-torus configuration is deliberately retained as a
    # guard against confusing quotient-center identifications with a planar
    # Hall obstruction.  Its deficient seven-tile torus subset has 17, not
    # 13, distinct centers after lifting to the infinite substrate.
    shape = decode_compiled_key(KEY)
    placements = (
        (2, 2, 1), (3, 0, 2), (5, 1, 2), (5, 1, 3),
        (6, 1, 3), (6, 2, 3), (8, 2, 0),
    )
    supports = tuple(frozenset(
        (u, v) for u, v, _sector in placement_lattice_cells(shape, placement)
    ) for placement in placements)
    assert len(set().union(*supports)) == 17
    result = two_center_matching(supports, range(1, 8))
    assert result.saturated
    assert verify_two_matching(supports, result)


def test_two_matching_agrees_with_exhaustive_hall_condition():
    rng = random.Random(0)
    centers = tuple((index, 0) for index in range(7))
    for _ in range(40):
        supports = tuple(
            frozenset(rng.sample(centers, 4)) for _ in range(5)
        )
        expected = all(
            len(set().union(*(supports[index] for index in subset)))
            >= 2 * len(subset)
            for size in range(1, 6)
            for subset in itertools.combinations(range(5), size)
        )
        result = two_center_matching(supports, range(1, 6))
        assert result.saturated == expected
        assert verify_two_matching(supports, result)
