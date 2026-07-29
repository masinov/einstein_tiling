"""Exact controls from Akiyama--Araki's alternative Turtle proof."""

from fractions import Fraction

from einstein.tilings.sturmian.turtle import (
    central_word,
    golden_density_root_residual,
    lower_density_side,
    minority_chirality_residual,
    minority_chirality_side,
    standard_word,
    standard_word_stats,
    verify_central_identities,
)


def test_published_standard_and_central_word_prefixes():
    assert [standard_word(n) for n in range(6)] == [
        "0",
        "001",
        "0010",
        "0010001",
        "00100010010",
        "001000100100010001",
    ]
    assert [central_word(n) for n in range(6)] == [
        "",
        "0",
        "00",
        "00100",
        "001000100",
        "0010001001000100",
    ]


def test_central_palindrome_decompositions_hold_exactly():
    assert verify_central_identities(24) == {
        "palindromes": 25,
        "equation_1_instances": 11,
        "equation_2_instances": 11,
    }


def test_standard_word_counts_bracket_the_irrational_slope():
    for n in range(1, 40):
        stats = standard_word_stats(n)
        expected_side = 1 if n % 2 else -1
        assert lower_density_side(stats.one_frequency) == expected_side
        if n <= 18:
            word = standard_word(n)
            assert stats.length == len(word)
            assert stats.zeros == word.count("0")
            assert stats.ones == word.count("1")


def test_density_roots_are_exact_and_match_hat_chirality_polynomial():
    assert golden_density_root_residual(-1) == (0, 0)
    assert golden_density_root_residual(1) == (0, 0)
    assert minority_chirality_residual() == (0, 0)
    # Existing 9,239-tile Turtle patch: minority class 1,181.
    observed = Fraction(1181, 9239)
    assert minority_chirality_side(observed) == 1
    # A coarse rational bracket around (3-sqrt(5))/6.
    assert minority_chirality_side(Fraction(1273, 10000)) == -1
    assert minority_chirality_side(Fraction(1274, 10000)) == 1
