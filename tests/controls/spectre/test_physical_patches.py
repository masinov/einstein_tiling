"""Exact ancestry-blind physical Spectre patch-language controls."""

import json
from pathlib import Path

from einstein.repository import repository_root

import pytest

from einstein.tilings.spectre.patches import (
    IDENTITY,
    central_parent_candidates,
    compatible_parents,
    complete_corona_signatures,
    enumerate_first_coronas,
    extend_complete_ring,
)


ROOT = repository_root(Path(__file__))


def _templates():
    selected = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())["selected_rule"]

    def parse(rows):
        return tuple((s, r, tuple(t)) for s, r, t in rows)

    return parse(selected["full"]), parse(selected["missing"])


def test_bare_first_corona_language_is_complete_and_larger_than_generated():
    coronas = enumerate_first_coronas()
    assert len(coronas) == 166
    assert {len(corona) for corona in coronas} == {4, 5, 6, 7}

    from einstein.tilings.spectre.geometry import exact_leaves

    generated = set()
    for label in ("Gamma", "Delta", "Theta", "Lambda", "Xi", "Pi", "Sigma", "Phi", "Psi"):
        poses = [pose for _, pose in exact_leaves(3, label)]
        generated.update(complete_corona_signatures(poses))
    assert len(generated) == 18
    assert generated < set(coronas)


def test_first_corona_does_not_generally_force_parent_ownership():
    full, missing = _templates()
    parents = central_parent_candidates(full, missing)
    assert len(parents) == 17
    counts = [
        len(compatible_parents(corona, parents))
        for corona in enumerate_first_coronas()
    ]
    assert {count: counts.count(count) for count in sorted(set(counts))} == {
        0: 105,
        1: 8,
        2: 42,
        3: 9,
        4: 1,
        5: 1,
    }


def test_identity_has_166_complete_first_ring_extensions():
    extension = extend_complete_ring((IDENTITY,), solution_limit=200)
    assert len(extension.solutions) == 166
    assert extension.candidates == 79
    assert extension.sat_calls == 167
    assert extension.solver == "CaDiCaL 1.9.5"


@pytest.mark.slow
def test_complete_radius2_report_contracts_to_30_survivors():
    from einstein.tilings.spectre.patches import analyze_physical_patch_language

    source = json.loads((
        ROOT / "docs/notebook/assets/a6-spectre-results.json"
    ).read_text())
    report = analyze_physical_patch_language(source)
    assert report["radius2"] == {
        "refuted_first_coronas": 136,
        "unique_extensions": 1,
        "multiple_extensions": 29,
        "surviving_first_coronas": 30,
        "survivor_indices": report["radius2"]["survivor_indices"],
    }
    assert report["substitution_control"]["observed_first_coronas"] == 18
    assert report["substitution_control"]["all_observed_survive_radius2"]
    assert report["substitution_control"]["unobserved_radius2_survivors"] == 12
    assert report["radius3"]["surviving_first_coronas"] == 21
    assert report["radius3"]["unobserved_survivor_indices"] == [33, 44, 155]
    assert report["radius3"]["compatible_parent_count_histogram"] == {
        "2": 17, "3": 3, "5": 1,
    }
    assert report["radius3"]["unique_parent_survivors"] == 0
    assert report["substitution_control"]["all_observed_survive_radius3"]
    assert report["substitution_control"]["unobserved_radius3_survivors"] == 3
    radius4 = report["radius4_targeted_probe"]
    assert radius4["complete_language_enumeration"] is False
    assert radius4["all_three_extend"] is True
    assert [row["corona_index"] for row in radius4["witnesses"]] == [
        33, 44, 155,
    ]
    assert all(
        report["records"][index]["second_ring_status"] == "refuted"
        for index in report["radius1"]["unique_parent_indices"]
    )
