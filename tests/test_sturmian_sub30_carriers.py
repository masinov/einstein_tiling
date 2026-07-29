import json
from pathlib import Path

from einstein.tilings.sturmian import (
    _canonical_triangle_support,
    _cell_from_triangle_vertices,
    _transform_cell_set,
    verify_sub30_carrier_classification,
)


ARTIFACT = Path(
    "data/sturmian-source/ahi-sub30-carrier-classification.json"
)
ATLAS = Path("data/sturmian-source/ahi-section10-supports.json")
KERNEL = Path("data/sturmian-source/ahi-common-support-kernel.json")


def test_sub30_carrier_artifact_has_complete_fixed_scope():
    data = json.loads(ARTIFACT.read_text())
    assert data["schema"] == "ahi-sturmian-sub30-carrier-classification-v1"
    assert data["class_count"] == 6
    assert [
        (item["macro"], item["attachment_count"], item["carrier_area_rhombi"])
        for item in data["classes"]
    ] == [
        ("large_A", 0, 15),
        ("large_A", 1, 16),
        ("large_A", 2, 17),
        ("large_B", 0, 15),
        ("large_B", 1, 16),
        ("large_B", 2, 17),
    ]
    assert data["support_count"] == sum(
        item["support_count"] for item in data["classes"]
    )
    assert data["perfect_matching_count"] == sum(
        support["perfect_matching_count"]
        for item in data["classes"]
        for support in item["supports"]
    )
    assert data["bipartite_matching_count"] == sum(
        support["bipartite_matching_count"]
        for item in data["classes"]
        for support in item["supports"]
    )


def test_sub30_carrier_artifact_cold_rebuilds():
    data = json.loads(ARTIFACT.read_text())
    atlas = json.loads(ATLAS.read_text())
    verify_sub30_carrier_classification(data, atlas)


def test_sub30_census_contains_the_independent_p17_control():
    data = json.loads(ARTIFACT.read_text())
    atlas = json.loads(ATLAS.read_text())
    kernel = json.loads(KERNEL.read_text())
    equalizer = kernel["two_rhombus_equalizers"][0]
    p17 = _transform_cell_set(
        atlas["supports"]["large_A"]["cells"], 0, False, (0, 0)
    ) | _transform_cell_set(
        atlas["supports"]["large_B"]["cells"],
        equalizer["rotation"],
        equalizer["reflected"],
        tuple(equalizer["translation_uv"]),
    )
    p17_key = _canonical_triangle_support(p17)
    controls = [
        (item["macro"], support)
        for item in data["classes"]
        if item["attachment_count"] == 2
        for support in item["supports"]
        if _canonical_triangle_support(
            _transform_cell_set(
                support["primitive_cells"], 0, False, (0, 0)
            )
        ) == p17_key
    ]
    # The same unmarked support can contain more than one normalized large
    # macro embedding, so the carrier census may list its congruence class
    # more than once.  Both source macro types must nevertheless hit it.
    assert {macro for macro, _ in controls} == {"large_A", "large_B"}
    assert all(item["perfect_matching_count"] == 60 for _, item in controls)
    assert all(item["bipartite_matching_count"] == 0 for _, item in controls)
