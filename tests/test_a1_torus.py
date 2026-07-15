"""A1 torus-test validation.

Anchors: shapes with known behavior. The decisive one is the hat -- it is
PROVEN aperiodic (SMKG 2023), so if our solver ever produces a periodic
certificate for it, the solver is wrong.
"""

import pytest

from einstein.funnel.a1_torus import (
    cell_to_lattice,
    find_periodic_tiling,
    lattice_to_cell,
    sublattices,
    verify_certificate,
)
from tests.test_hat import HAT_OUTLINE
from einstein.substrate.kitegrid import canonical_form, cells_in_polygon


def test_lattice_coordinate_roundtrip():
    for u in range(-3, 4):
        for v in range(-3, 4):
            for d in range(6):
                assert cell_to_lattice(lattice_to_cell((u, v, d))) == (u, v, d)
    with pytest.raises(ValueError):
        cell_to_lattice((2, 0, 0))  # not a hex center


def test_sublattice_count():
    # number of index-k sublattices of Z^2 is sigma(k) = sum of divisors
    sigma = {1: 1, 2: 3, 3: 4, 4: 7, 5: 6, 6: 12, 12: 28}
    for k, s in sigma.items():
        assert len(sublattices(k)) == s


def test_single_kite_tiles_periodically():
    cert, exhausted = find_periodic_tiling(((0, 0, 0),), k_max=2)
    assert cert is not None and not exhausted
    assert cert["index"] == 1  # six kites tile one hexagon, hexagons the plane
    assert verify_certificate(((0, 0, 0),), cert)


def test_same_hex_pair_tiles_periodically():
    shape = ((0, 0, 0), (0, 0, 1))
    cert, _ = find_periodic_tiling(shape, k_max=2)
    assert cert is not None and cert["index"] == 1


def test_tampered_certificate_rejected():
    shape = ((0, 0, 0),)
    cert, _ = find_periodic_tiling(shape, k_max=2)
    bad = dict(cert)
    bad["placements"] = cert["placements"][:-1]  # drop a tile: not a cover
    assert not verify_certificate(shape, bad)
    if len(cert["placements"]) > 1:
        bad2 = dict(cert)
        bad2["placements"] = cert["placements"][:-1] + [cert["placements"][0]]
        assert not verify_certificate(shape, bad2)  # duplicate: overlap


def test_hat_gets_no_periodic_certificate():
    """The hat is proven aperiodic; any certificate here is a solver bug.
    Budget k_max=8 covers tori of up to 48 kite cells (6 hats)."""
    hat = canonical_form(cells_in_polygon(HAT_OUTLINE))
    cert, exhausted = find_periodic_tiling(hat, k_max=8)
    assert cert is None
    assert not exhausted, "budget too small to be meaningful for the hat"
