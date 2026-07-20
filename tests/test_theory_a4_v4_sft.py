"""Controls for the two-bit local-SFT factor of the map-7 A4 obstruction."""

import itertools

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_semidirect import c3_action, canonical_a4_semidirect
from einstein.theory.a4_v4_sft import (
    MAP7,
    V4_TWIST_PAIRS,
    _append_implied_xor,
    _map7_signed_coordinate,
    build_map7_v4_coverability_cnf,
    build_v4_coverability_cnf,
)
from einstein.theory.a4_v4_twist_union import build_v4_coverability_union_cnf
from einstein.theory.holonomy import polykite_boundary_relators


KEY = "010001010104010502f002f1030b030c04fa04fb"


def test_implied_xor_truth_table():
    for constant, enabled, left, right in itertools.product(range(2), repeat=4):
        from pysat.formula import CNF

        cnf = CNF()
        _append_implied_xor(cnf, 1, 2, 3, constant)
        assumptions = [
            1 if enabled else -1,
            2 if left else -2,
            3 if right else -3,
        ]
        with Cadical195(bootstrap_with=cnf) as solver:
            sat = solver.solve(assumptions=assumptions)
        assert sat == (not enabled or right == (left ^ constant))


def test_map7_phase_normalized_relators_close():
    shape = decode_compiled_key(KEY)
    model = canonical_a4_semidirect()
    assert len(V4_TWIST_PAIRS) == 16
    for relator in polykite_boundary_relators(shape):
        for initial_q in range(3):
            for initial_v in range(4):
                q, v = initial_q, initial_v
                for letter in relator:
                    label = _map7_signed_coordinate(letter)
                    v ^= c3_action(q, label.v)
                    q = (q + label.q) % 3
                assert (v, q) == (initial_v, initial_q)
    assert tuple(model.element(_map7_signed_coordinate(i)) for i in range(1, 7)) == MAP7


def test_reduced_index55_control_is_smaller_and_unsat_for_identity_twist():
    shape = decode_compiled_key(KEY)
    cnf, metadata = build_map7_v4_coverability_cnf(shape, (55, 48, 1))
    assert metadata["potential_bits"] == 2 * metadata["vertices"]
    assert metadata["variables"] == metadata["placements"] + metadata["potential_bits"]
    with Cadical195(bootstrap_with=cnf) as solver:
        assert not solver.solve()


def test_generic_geometric_c3_encoder_agrees_with_map7_wrapper():
    shape = decode_compiled_key(KEY)
    wrapped, wrapped_metadata = build_map7_v4_coverability_cnf(
        shape, (11, 2, 5), twists=(3, 1)
    )
    generic, generic_metadata = build_v4_coverability_cnf(
        shape, (11, 2, 5), MAP7, twists=(3, 1)
    )
    assert generic.clauses == wrapped.clauses
    assert generic_metadata == wrapped_metadata


def test_twist_union_matches_direct_disjunction_on_sat_and_unsat_controls():
    shape = decode_compiled_key(KEY)
    twist_pairs = ((0, 0), (3, 2))
    for hnf in ((2, 0, 2), (55, 48, 1)):
        direct = []
        for twists in twist_pairs:
            cnf, _ = build_v4_coverability_cnf(shape, hnf, MAP7, twists)
            with Cadical195(bootstrap_with=cnf) as solver:
                direct.append(solver.solve())
        union, metadata = build_v4_coverability_union_cnf(
            shape, hnf, MAP7, twist_pairs=twist_pairs
        )
        with Cadical195(bootstrap_with=union) as solver:
            union_sat = solver.solve()
        assert union_sat == any(direct)
        assert metadata["twist_components"] == len(twist_pairs)
        assert metadata["twist_pairs"] == [list(pair) for pair in twist_pairs]
