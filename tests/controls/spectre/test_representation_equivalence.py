"""Fast pins for the W3 Spectre D4 finite equivalence kernel."""

import json
from pathlib import Path

from einstein.repository import repository_root

from sympy import Matrix, symbols

from einstein.geometry.cyclotomic import apply_sr, compose_pose
from einstein.tilings.spectre.colored_interfaces import colored_corona_from_json
from einstein.tilings.spectre.equivalence import (
    NORMALIZATION_INVERSE,
    NORMALIZATION_LINEAR,
    audit_component_state_roundtrips,
    colored_collar_bijection,
    denormalize_parent_pose,
    normalize_parent_pose,
    two_level_translation_matrices,
)
from einstein.tilings.spectre.parent_overlaps import parent_templates


ROOT = repository_root(Path(__file__))
A6 = ROOT / "docs/notebook/assets/a6-spectre-results.json"
COLORED = ROOT / "docs/notebook/assets/theory-w3-spectre-colored-interface.json"
D4 = ROOT / "docs/notebook/assets/theory-w3-spectre-d4-equivalence.json"


def matvec(matrix, vector):
    return tuple(
        sum(coefficient * value for coefficient, value in zip(row, vector))
        for row in matrix
    )


def test_normalization_is_unimodular_and_exactly_invertible():
    samples = (
        (0, 0, (0, 0, 0, 0)),
        (0, 7, (2, -1, 3, 4)),
        (1, 2, (-5, 8, 1, -3)),
        (1, 11, (9, 0, -2, 6)),
    )
    assert all(
        denormalize_parent_pose(normalize_parent_pose(pose)) == pose
        for pose in samples
    )
    for chirality in (0, 1):
        assert Matrix(NORMALIZATION_LINEAR[chirality]).det() == 1
        assert Matrix(NORMALIZATION_LINEAR[chirality]).inv() == Matrix(
            NORMALIZATION_INVERSE[chirality]
        )


def test_normalization_preserves_translation_action_within_a_phase():
    vectors = (
        (1, 0, 0, 0), (0, 1, 0, 0),
        (0, 0, 1, 0), (0, 0, 0, 1),
    )
    for chirality in (0, 1):
        for rotation in range(12):
            parity = rotation % 2
            pose = (chirality, rotation, (2, -1, 3, 4))
            for vector in vectors:
                effective = apply_sr(
                    0,
                    parity,
                    matvec(
                        NORMALIZATION_LINEAR[chirality],
                        apply_sr(0, -parity, vector),
                    ),
                )
                assert normalize_parent_pose(
                    compose_pose((0, 0, vector), pose)
                ) == compose_pose(
                    (0, 0, effective), normalize_parent_pose(pose)
                )


def test_colored_collar_and_component_roundtrips_are_bijective():
    a6 = json.loads(A6.read_text())
    colored = json.loads(COLORED.read_text())
    states = tuple(map(
        colored_corona_from_json, colored["generated_colored_states"],
    ))
    ids, language = colored_collar_bijection(states)
    assert len(states) == len(language) == len(set(ids)) == 17
    records = audit_component_state_roundtrips(states, parent_templates(a6))
    assert all(
        row["pairwise_component_disjoint"]
        and row["central_exposed_edges"] == 0
        and row["central_external_edges"] == row["contact_colors"]
        and row["roundtrip_exact"]
        for row in records
    )


def test_d4_artifact_records_the_context_gap_without_promoting_it():
    artifact = json.loads(D4.read_text())
    assert artifact["status"] == "FAITHFUL_FINITE_KERNEL_CONTEXT_LANGUAGE_OPEN"
    assert artifact["finite_kernel_verified"]
    assert artifact["colored_collar_bijection"]["bijective"]
    assert artifact["component_state_roundtrips"]["all_exact"]
    assert all(
        row["next_physical_patch_exact"]
        and row["inverse_first_exact"]
        and row["inverse_second_exact"]
        for row in artifact["level_pair_roundtrips"]
    )
    assert artifact["radius1_context_probe"]["total_stars"] == 3565
    assert artifact["radius1_context_probe"]["outcomes"]["output_overlap"] == 536
    assert artifact["radius2_context_filter"]["radius2_extendible_seed_stars"] == 80
    assert artifact["d4_assessment"]["status"] == "partial"
    assert not artifact["d4_assessment"]["standalone_d4_verified"]
    x = symbols("x")
    assert {
        str(Matrix(matrix).charpoly(x).as_expr().factor())
        for matrix in two_level_translation_matrices().values()
    } == {"(x**2 - 8*x + 1)**2"}
