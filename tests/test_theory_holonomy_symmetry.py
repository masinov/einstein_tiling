"""Exact symmetry pins for the Layer-D index-45 experiment."""

import json
from pathlib import Path

from einstein.substrate.kitegrid import N_OPS
from einstein.theory.holonomy_symmetry import (
    canonical_s3_images,
    hnf_d6_image,
    inverse_d6_operation,
    orbit,
    pullback_s3_images,
    signed_edge_action,
    transform_s3_images,
)


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index45.json"


def test_d6_edge_action_is_invertible():
    identity = (1, 2, 3, 4, 5, 6)
    assert signed_edge_action(0) == identity
    for op in range(N_OPS):
        inverse = inverse_d6_operation(op)
        first = signed_edge_action(op)
        second = signed_edge_action(inverse)
        composed = []
        for letter in first:
            image = second[abs(letter) - 1]
            composed.append(image if letter > 0 else -image)
        assert tuple(composed) == identity


def test_hnf_action_has_expected_index45_orbits():
    hnfs = (
        (9, 2, 5), (15, 4, 3), (15, 8, 3),
        (45, 6, 1), (45, 12, 1), (45, 19, 1),
        (45, 25, 1), (45, 32, 1), (45, 38, 1),
    )
    assert orbit(hnfs, hnf_d6_image) == (
        ((9, 2, 5), (45, 19, 1), (45, 25, 1)),
        (
            (15, 4, 3), (15, 8, 3), (45, 6, 1),
            (45, 12, 1), (45, 32, 1), (45, 38, 1),
        ),
    )


def test_index45_matrix_is_exactly_d6_covariant():
    data = json.loads(MATRIX.read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in data["finalist"]["mapping_representatives"]
    )
    mapping_index = {images: index for index, images in enumerate(mappings)}
    verdict = {
        (tuple(row["hnf"]), row["mapping_index"]): row["scan"]["verdict"]
        for row in data["finalist"]["results"]
    }
    assert len(verdict) == 9 * 39
    for (hnf, index), value in verdict.items():
        for op in range(N_OPS):
            moved_hnf = hnf_d6_image(hnf, op)
            moved_images = pullback_s3_images(mappings[index], op)
            assert moved_images in mapping_index
            assert verdict[(moved_hnf, mapping_index[moved_images])] == value


def test_transform_then_inverse_returns_inner_class():
    data = json.loads(MATRIX.read_text())
    for row in data["finalist"]["mapping_representatives"]:
        images = tuple(tuple(image) for image in row["generator_images"])
        for op in range(N_OPS):
            moved = transform_s3_images(images, op)
            restored = transform_s3_images(moved, inverse_d6_operation(op))
            assert canonical_s3_images(restored) == images
