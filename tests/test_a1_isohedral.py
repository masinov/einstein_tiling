"""Kaplan Proposition-1 isohedral-surround SAT control."""

import pytest

from einstein.polykites.known_shapes import TURTLE_OUTLINE
from einstein.polykites.enumeration import enumerate_free_polykites
from einstein.polykites.isohedral import (
    apply_grid_pose,
    compose_grid_poses,
    find_isohedral_surround,
    inverse_grid_pose,
    verify_isohedral_surround,
)
from einstein.polykites.periodic_quotients import find_periodic_tiling
from einstein.geometry.kite_grid import canonical_form, cells_in_polygon
from tests.test_hat import HAT_OUTLINE


MYERS_ISOHEDRAL = {1: 1, 2: 1, 3: 4, 4: 4, 5: 0, 6: 70, 7: 52, 8: 37}


def _count_isohedral(n_max):
    counts = {}
    for n, forms in enumerate_free_polykites(n_max):
        counts[n] = sum(
            find_isohedral_surround(shape)["isohedral"] is True
            for shape in forms
        )
    return counts


def test_grid_pose_group_law_and_inverse():
    poses = [
        (operation, tx, ty)
        for operation in range(12)
        for tx, ty in ((0, 0), (2, 2), (-2, 4))
    ]
    cells = ((0, 0, 0), (2, 2, 3), (-2, 4, 5))
    for left in poses:
        inverse = inverse_grid_pose(left)
        assert compose_grid_poses(left, inverse) == (0, 0, 0)
        assert compose_grid_poses(inverse, left) == (0, 0, 0)
        for right in poses:
            composed = compose_grid_poses(left, right)
            for cell in cells:
                assert apply_grid_pose(composed, cell) == apply_grid_pose(
                    left, apply_grid_pose(right, cell)
                )


def test_single_kite_has_cold_verified_isohedral_surround():
    shape = ((0, 0, 0),)
    result = find_isohedral_surround(shape)
    assert result["isohedral"] is True and not result["exhausted"]
    assert verify_isohedral_surround(shape, result["certificate"])
    assert result["stats"]["models"] == 1


def test_tampered_isohedral_surround_is_rejected():
    shape = ((0, 0, 0),)
    certificate = find_isohedral_surround(shape)["certificate"]
    assert verify_isohedral_surround(shape, certificate)
    bad = {**certificate, "placements": certificate["placements"][:-1]}
    assert not verify_isohedral_surround(shape, bad)
    far = {
        **certificate,
        "placements": [*certificate["placements"], [0, 20, 20]],
    }
    assert not verify_isohedral_surround(shape, far)


def test_hat_and_turtle_have_no_isohedral_surround():
    for outline in (HAT_OUTLINE, TURTLE_OUTLINE):
        shape = canonical_form(cells_in_polygon(outline))
        result = find_isohedral_surround(shape)
        assert result["isohedral"] is False and not result["exhausted"]
        assert result["certificate"] is None


def test_periodic_anisohedral_control_separates_a1_from_isohedral_filter():
    forms4 = next(forms for n, forms in enumerate_free_polykites(4) if n == 4)
    witnesses = []
    for shape in forms4:
        isohedral = find_isohedral_surround(shape)["isohedral"]
        periodic, exhausted = find_periodic_tiling(shape, k_max=12)
        assert not exhausted
        if periodic is not None and not isohedral:
            witnesses.append(shape)
    assert len(witnesses) == 1  # Myers: one 2-anisohedral four-kite.


def test_isohedral_counts_match_myers_n6():
    assert _count_isohedral(6) == {
        n: MYERS_ISOHEDRAL[n] for n in range(1, 7)
    }


@pytest.mark.slow
def test_isohedral_counts_match_myers_n8():
    assert _count_isohedral(8) == MYERS_ISOHEDRAL
