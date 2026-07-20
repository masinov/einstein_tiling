"""Coordinated parent-overlap language controls."""

import json
from pathlib import Path

import pytest

from einstein.theory.spectre_geometry import exact_leaves
from einstein.theory.spectre_parent_overlap import (
    analyze_parent_overlap_language,
    build_grouping_problem,
    centered_parent_templates,
    parent_occurrences,
    solve_grouping,
    solve_coordinated_ring_extension,
    verify_coordinated_extension,
    verify_grouping_solution,
)


ROOT = Path(__file__).resolve().parents[1]


def _source():
    return json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())


def test_each_physical_tile_has_seventeen_centered_parent_occurrences():
    centered = centered_parent_templates(_source())
    assert len(centered) == 17
    identity = (0, 0, (0, 0, 0, 0))
    assert len(parent_occurrences(identity, centered)) == 17
    assert {len(parent) for parent in centered} == {8, 9}


def test_generated_patch_has_a_coordinated_buffered_grouping():
    centered = centered_parent_templates(_source())
    patch = [pose for _, pose in exact_leaves(3, "Delta")]
    problem = build_grouping_problem(patch, centered)
    assert problem.safe_tiles
    result = solve_grouping(problem, solution_limit=2)
    assert result.solutions
    assert verify_grouping_solution(problem, result.solutions[0])


def test_generated_patch_admits_coupled_next_ring_and_parent_grouping():
    centered = centered_parent_templates(_source())
    patch = [pose for _, pose in exact_leaves(2, "Delta")]
    extension = solve_coordinated_ring_extension(patch, centered)
    assert extension.physical_ring is not None
    assert extension.target_tiles
    assert verify_coordinated_extension(patch, extension, centered)


@pytest.mark.slow
def test_extra_coronas_are_exhausted_by_coordinated_radius_four():
    physical = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
    ).read_text())
    analysis = analyze_parent_overlap_language(_source(), physical)
    assert analysis["summary"] == {
        "physical_radius3_survivors": 21,
        "substitution_observed": 18,
        "extras_tested": [33, 44, 155],
        "extras_surviving_coordinated_grouping": [],
        "radius3_frontier_states_exhausted": 224,
        "radius4_frontier_inputs_exhausted": 224,
        "conditional_language_after_grouping": 18,
    }
    assert [
        (row["corona_index"], row["radius3_frontier_states"],
         row["radius4_frontier_states"])
        for row in analysis["extra_coronas"]
    ] == [(33, 200, 0), (44, 0, 0), (155, 24, 0)]
    assert [
        row["radius3_input_mode_histogram"][
            "unbuffered-physical-extension"
        ]
        for row in analysis["extra_coronas"]
    ] == [0, 3, 12]
