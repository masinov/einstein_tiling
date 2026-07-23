from fractions import Fraction

from einstein.theory.k16w_exact import build_problem


def test_complete_k16w_formula_has_every_segment_pair():
    problem = build_problem(timeout_ms=1000)
    assert len(problem.first_half) == 9
    assert len(problem.points) == 18
    assert len(problem.nonadjacent_pairs) == 120
    assert problem.constraint_counts == {
        "base": 13,
        "containment_scalar": 32,
        "closure": 1,
        "nonadjacent_segment_pairs": 120,
        "decomposition": 0,
        "total_top_level": 166,
    }


def test_hc31_cells_are_the_exact_two_fixed_decomposition_instances():
    for cell in ("plus-minus", "minus-plus"):
        problem = build_problem(timeout_ms=1000, cell=cell)
        assert problem.constraint_counts["decomposition"] == 8
        assert problem.constraint_counts["total_top_level"] == 174
        assert len(problem.nonadjacent_pairs) == 120


def test_unknown_hc31_cell_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        build_problem(cell="same-polarity")


def test_err010_replacement_is_an_exact_unit_direction():
    x = Fraction(544, 545)
    y = Fraction(33, 545)
    assert x * x + y * y == 1
    assert 2 * x < 2
    assert x < 1


def test_n42_exact_reset_budget_comparisons():
    # sqrt(23/2) > 10/3.
    assert Fraction(23, 2) > Fraction(100, 9)
    # sqrt(42) < 13/2 makes
    # [13(sqrt(21)-sqrt(2))]^2 > 1690 > (6sqrt(46))^2,
    # hence U_0 < 13/6.
    assert Fraction(42) < Fraction(169, 4)
    assert 3887 - 338 * Fraction(13, 2) == 1690
    assert 1690 > 36 * 46
    # sqrt(46)+sqrt(42)>12 makes delta_0<1/6.
    assert 46 > 36 and 42 > 36
