"""W2 Layer A exact area and sector-coloring invariants."""

import json
from pathlib import Path

import pytest

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.polykites.periodic_quotients import sublattices
from einstein.periodicity.binary_families import (
    finalist_thin_family_orbit,
    quotient_period_obstruction,
    verify_finalist_thin_family_orbit,
    verify_quotient_period_obstruction,
)
from einstein.periodicity.invariants import (
    area_allows_index,
    area_obstruction,
    gf2_cokernel_obstruction,
    integer_cokernel_snf,
    integer_cokernel_hnf,
    integer_lattice_membership,
    integer_lattice_membership_hnf,
    nonnegative_cokernel_relaxation,
    finalist_thin_gf2_support,
    prime_sector_obstruction,
    required_index_modulus,
    verify_area_obstruction,
    verify_gf2_cokernel_obstruction,
    verify_integer_cokernel_snf,
    verify_nonnegative_cokernel_relaxation,
    verify_prime_sector_obstruction,
)


FINALIST = decode_compiled_key("010001010104010502f002f1030b030c04fa04fb")


def test_area_modulus_and_tamper_resistance():
    assert required_index_modulus(10) == 5
    assert required_index_modulus(8) == 4
    assert area_allows_index(10, 5)
    assert not area_allows_index(10, 4)
    certificate = area_obstruction(10, 4)
    assert verify_area_obstruction(certificate)
    bad = dict(certificate, remainder=0)
    assert not verify_area_obstruction(bad)


def test_finalist_sector_coloring_witness_matches_area_class():
    certificate = prime_sector_obstruction(FINALIST, 1)
    assert certificate is not None
    assert certificate["modulus"] == 5
    assert verify_prime_sector_obstruction(FINALIST, certificate)
    assert prime_sector_obstruction(FINALIST, 5) is None
    bad = dict(certificate, target_residue=0)
    assert not verify_prime_sector_obstruction(FINALIST, bad)


def test_finalist_full_quotient_gf2_cokernel_witness():
    certificate = gf2_cokernel_obstruction(FINALIST, (1, 0, 5))
    assert certificate is not None
    assert verify_gf2_cokernel_obstruction(FINALIST, certificate)
    # Same admissible index, but this less degenerate quotient is not killed by
    # the mod-2 relaxation; absence is not a SAT claim.
    assert gf2_cokernel_obstruction(FINALIST, (5, 1, 1)) is None
    bad = dict(certificate, weight_support=certificate["weight_support"][:-1])
    assert not verify_gf2_cokernel_obstruction(FINALIST, bad)


def test_gf2_cokernel_does_not_exclude_periodic_controls():
    assert gf2_cokernel_obstruction(((0, 0, 0),), (1, 0, 1)) is None
    assert gf2_cokernel_obstruction(((0, 0, 0), (0, 0, 1)), (1, 0, 1)) is None


def test_integer_lattice_membership_smith_criterion():
    compatible = integer_lattice_membership([[2]], [2])
    assert compatible["verdict"] == "integer-compatible"
    assert compatible["lattice_index"] == 1

    torsion = integer_lattice_membership([[2]], [1])
    assert torsion["verdict"] == "obstructed-index"
    assert torsion["lattice_index"] == 2

    rational = integer_lattice_membership([[1], [0]], [0, 1])
    assert rational["verdict"] == "obstructed-rank"
    assert rational["lattice_index"] is None

    # Independent exact libraries must agree on the complete compact result.
    for rows, target in (
        ([[2]], [1]),
        ([[1], [0]], [0, 1]),
        ([[2, 0], [0, 3]], [2, 3]),
    ):
        assert integer_lattice_membership(rows, target, backend="flint") == (
            integer_lattice_membership(rows, target, backend="sympy")
        )
        assert integer_lattice_membership_hnf(rows, target)["verdict"] == (
            integer_lattice_membership(rows, target)["verdict"]
        )


def test_finalist_integer_cokernel_smith_controls():
    killed = integer_cokernel_snf(FINALIST, (1, 0, 5))
    assert killed["verdict"] == "obstructed-rank"
    assert verify_integer_cokernel_snf(FINALIST, killed)
    assert verify_gf2_cokernel_obstruction(FINALIST, killed["modular_witness"])

    compatible = integer_cokernel_snf(FINALIST, (5, 1, 1))
    assert compatible["verdict"] == "integer-compatible"
    assert compatible["matrix"]["determinantal_divisor"] == 25
    assert compatible["augmented"]["determinantal_divisor"] == 25
    assert verify_integer_cokernel_snf(FINALIST, compatible)

    periodic = integer_cokernel_snf(((0, 0, 0),), (1, 0, 1))
    assert periodic["verdict"] == "integer-compatible"
    bad = dict(killed, verdict="integer-compatible")
    assert not verify_integer_cokernel_snf(FINALIST, bad)
    assert integer_cokernel_hnf(FINALIST, (1, 0, 5))["verdict"] == (
        killed["verdict"]
    )
    assert integer_cokernel_hnf(FINALIST, (5, 1, 1))["verdict"] == (
        compatible["verdict"]
    )


def test_nonnegative_rational_relaxation_full_incidence_witness():
    result = nonnegative_cokernel_relaxation(FINALIST, (5, 1, 1))
    assert result["verdict"] == "fractional-compatible"
    assert len(result["profile_coefficients"]) <= 6
    assert verify_nonnegative_cokernel_relaxation(FINALIST, result)
    bad = json.loads(json.dumps(result))
    bad["profile_coefficients"][0]["numerator"] += 1
    assert not verify_nonnegative_cokernel_relaxation(FINALIST, bad)

    killed = nonnegative_cokernel_relaxation(FINALIST, (1, 0, 5))
    assert killed["verdict"] == "fractional-obstructed"
    assert verify_gf2_cokernel_obstruction(FINALIST, killed["modular_witness"])


def test_binary_period_family_composition_and_hnf_horizon():
    vectors = [
        (x, y)
        for x in range(-7, 8)
        for y in range(-7, 8)
        if (x or y) and x * x + x * y + y * y <= 36
    ]
    for index in range(1, 37):
        for hnf in sublattices(index):
            certificate = quotient_period_obstruction(hnf, vectors)
            assert certificate is not None
            assert verify_quotient_period_obstruction(certificate)
    survivors_37 = [
        hnf for hnf in sublattices(37)
        if quotient_period_obstruction(hnf, vectors) is None
    ]
    assert len(survivors_37) == 2


def test_three_thin_hnf_families_are_one_exact_d6_orbit():
    for index in range(4, 101):
        certificate = finalist_thin_family_orbit(index)
        assert [tuple(row["hnf"]) for row in certificate] == [
            (1, 0, index),
            (index, 0, 1),
            (index, index - 1, 1),
        ]
        assert verify_finalist_thin_family_orbit(index, certificate)


def test_finalist_thin_infinite_family_formula():
    for index in range(4, 101):
        certificate = gf2_cokernel_obstruction(FINALIST, (1, 0, index))
        assert certificate is not None
        assert certificate["weight_support"] == finalist_thin_gf2_support(index)
        assert verify_gf2_cokernel_obstruction(FINALIST, certificate)


def test_all_available_compiled_periodic_certificates_pass_layer_a():
    paths = sorted(Path("data/a1-compiled").glob("periodic-*.jsonl"))
    if not paths:
        pytest.skip("compiled E1 periodic corpus is not materialized")
    checked = 0
    for path in paths:
        for line in path.read_text().splitlines():
            if not line:
                continue
            row = json.loads(line)
            shape = decode_compiled_key(row["shape"])
            index = row["hnf"][0] * row["hnf"][2]
            assert area_allows_index(len(shape), index)
            assert prime_sector_obstruction(shape, index) is None
            checked += 1
    assert checked == 60_477
