import json
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
KERNEL = ROOT / "data/sturmian-source/ahi-common-support-kernel.json"


def test_common_support_kernel_records_complete_large_supports():
    kernel = json.loads(KERNEL.read_text())
    assert 0 <= kernel["best_primitive_triangle_overlap"] <= 30
    assert 0 <= kernel["best_rhombus_overlap_at_that_support_overlap"] <= 15
    assert kernel["best_alignments"]


def test_equalizer_count_matches_records():
    kernel = json.loads(KERNEL.read_text())
    assert kernel["one_rhombus_equalizer_count"] == len(
        kernel["one_rhombus_equalizers"]
    )
    assert kernel["two_rhombus_equalizer_count"] == len(
        kernel["two_rhombus_equalizers"]
    )
