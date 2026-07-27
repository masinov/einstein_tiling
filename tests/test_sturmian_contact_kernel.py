import json
from pathlib import Path

from einstein.theory.sturmian_source import (
    build_contact_kernel,
    verify_contact_kernel,
)


ROOT = Path(__file__).resolve().parents[1]
ATLAS = ROOT / "data/sturmian-source/ahi-section10-supports.json"
KERNEL = ROOT / "data/sturmian-source/ahi-section10-contact-kernel.json"


def test_contact_kernel_cold_verifies():
    atlas = json.loads(ATLAS.read_text())
    kernel = json.loads(KERNEL.read_text())
    verify_contact_kernel(kernel, atlas)


def test_contact_kernel_has_fixed_source_domain():
    kernel = build_contact_kernel(json.loads(ATLAS.read_text()))
    assert len(kernel["states"]) == 31
    assert {state["macro"] for state in kernel["states"]} == {
        "large_A",
        "large_B",
        "small_M",
    }
    assert kernel["binary_domain_wall"]["satisfiable"] in {True, False}
    assert kernel["internal_opposite_handedness"]["satisfiable"] is False
    assert kernel["internal_opposite_handedness"]["odd_triangle_certificate"] == [
        "large_A:0",
        "large_A:1",
        "large_A:2",
    ]
    assert sum(kernel["internal_axis_relation_counts"].values()) == 44
