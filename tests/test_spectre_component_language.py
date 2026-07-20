"""Ancestry-blind 18-corona SFT controls."""

import json
from pathlib import Path

from einstein.theory.spectre_component_language import (
    extend_language_ring,
    verify_language_extension,
)
from einstein.theory.spectre_patch_language import IDENTITY, enumerate_first_coronas


ROOT = Path(__file__).resolve().parents[1]


def _language():
    artifact = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"
    ).read_text())["analysis"]
    coronas = enumerate_first_coronas()
    indices = artifact["substitution_control"]["observed_indices"]
    return tuple(coronas[index] for index in indices)


def test_one_tile_has_exactly_the_eighteen_allowed_coronas():
    language = _language()
    extension = extend_language_ring((IDENTITY,), language)
    assert len(extension.solutions) == 18
    assert all(
        verify_language_extension((IDENTITY,), ring, language)
        for ring in extension.solutions
    )


def test_component_artifact_records_partition_and_open_closure():
    artifact = json.loads((
        ROOT / "docs/notebook/assets/theory-w3-spectre-component-language.json"
    ).read_text())
    assert artifact["status"] == "PARENT_PARTITION_PROVED_CLOSURE_OPEN_RADIUS9"
    assert artifact["radius3_transducer"]["rooted_cases"] == 418
    assert artifact["radius3_transducer"]["raw_grouping_solution_histogram"] == {
        "1": 370, "2": 46, "4": 2,
    }
    assert artifact["partition_theorem"] == {
        "decisive_radius": 6,
        "surviving_radius6_patches": 15216,
        "common_eight_child_core_failures": 0,
        "fiber_types": [8, 9],
        "verdict": "unique-parent-anchor fibers form a full/missing partition",
    }
    assert [
        row["continued_frontier_patches"]
        for row in artifact["contraction_audit"]["radius_records"]
    ] == [1861, 5140, 10924, 6280, 1796, 4482]
