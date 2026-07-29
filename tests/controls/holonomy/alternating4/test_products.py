"""Controls for products of the two-bit A4 local invariant."""

from einstein.polykites.known_shapes import decode_compiled_key
from pysat.solvers import Cadical195

from einstein.holonomy.alternating4.lifts import unsatisfied_clauses
from einstein.holonomy.alternating4.products import (
    build_v4_product_coverability_cnf,
    lift_product_witness,
    semantic_product_witness,
)
from einstein.holonomy.alternating4.local_system import MAP7, build_v4_coverability_cnf


KEY = "010001010104010502f002f1030b030c04fa04fb"


def test_one_layer_product_has_identical_canonical_clauses():
    shape = decode_compiled_key(KEY)
    direct, direct_metadata = build_v4_coverability_cnf(
        shape, (10, 2, 6), MAP7, (3, 1)
    )
    product, product_metadata = build_v4_product_coverability_cnf(
        shape, (10, 2, 6), ((MAP7, (3, 1)),)
    )
    assert product.clauses == direct.clauses
    assert product_metadata["variables"] == direct_metadata["variables"]
    assert product_metadata["clauses"] == direct_metadata["clauses"]


def test_product_semantic_witness_pulls_back():
    shape = decode_compiled_key(KEY)
    layers = ((MAP7, (3, 2)), (MAP7, (3, 2)))
    base_cnf, _ = build_v4_product_coverability_cnf(shape, (2, 0, 2), layers)
    with Cadical195(bootstrap_with=base_cnf) as solver:
        assert solver.solve()
        selected, colors = semantic_product_witness(shape, solver.get_model(), 2)
    induced, values = lift_product_witness(
        shape, (10, 2, 6), ((3, 2), (3, 2)), selected, colors
    )
    assert induced == ((3, 1), (3, 1))
    cnf, _ = build_v4_product_coverability_cnf(
        shape, (10, 2, 6), tuple((MAP7, twists) for twists in induced)
    )
    assert not unsatisfied_clauses(cnf, values)
