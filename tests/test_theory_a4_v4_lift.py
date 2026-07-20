"""Controls for the infinite 2-Lambda pullback family."""

from pysat.solvers import Cadical195

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_lift import (
    BASE_HNF,
    induced_v4_twists,
    lies_in_2lambda,
    lift_2lambda_witness,
    semantic_base_witness,
    unsatisfied_clauses,
)
from einstein.theory.a4_v4_sft import MAP7, build_v4_coverability_cnf


KEY = "010001010104010502f002f1030b030c04fa04fb"


def test_even_hnf_predicate_and_induced_twists():
    assert lies_in_2lambda(BASE_HNF)
    assert lies_in_2lambda((10, 2, 6))
    assert not lies_in_2lambda((10, 1, 6))
    assert induced_v4_twists((3, 2), (10, 2, 6)) == (3, 1)
    assert induced_v4_twists((3, 2), (30, 6, 2)) == (3, 1)
    assert induced_v4_twists((3, 2), (30, 22, 2)) == (3, 1)


def test_base_witness_pulls_back_clausewise_to_index60_escape():
    shape = decode_compiled_key(KEY)
    base_cnf, _ = build_v4_coverability_cnf(shape, BASE_HNF, MAP7, (3, 2))
    with Cadical195(bootstrap_with=base_cnf) as solver:
        assert solver.solve()
        selected, colors = semantic_base_witness(shape, solver.get_model())
    assert not unsatisfied_clauses(
        base_cnf,
        lift_2lambda_witness(
            shape, BASE_HNF, (3, 2), selected, colors
        )[1],
    )
    hnf = (10, 2, 6)
    twists, values = lift_2lambda_witness(shape, hnf, (3, 2), selected, colors)
    assert twists == (3, 1)
    lifted_cnf, _ = build_v4_coverability_cnf(shape, hnf, MAP7, twists)
    assert not unsatisfied_clauses(lifted_cnf, values)
