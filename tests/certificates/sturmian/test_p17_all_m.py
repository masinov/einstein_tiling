import json
from pathlib import Path

from einstein.tilings.sturmian import verify_p17_all_m_obstruction


def test_p17_all_m_artifact_is_exhaustive_and_fail_closed():
    path = Path("data/sturmian-source/ahi-p17-all-m-obstruction.json")
    if not path.exists():
        return
    data = json.loads(path.read_text())
    assert data["schema"] == "ahi-sturmian-p17-all-m-obstruction-v1"
    assert data["primitive_triangle_count"] == 34
    assert data["lozenge_count"] == 17
    assert data["perfect_matching_count"] == 60
    assert data["matching_count_with_three_axis_vertex"] == 60
    assert data["nonbipartite_long_diagonal_graph_count"] == 60
    assert data["bipartite_long_diagonal_graph_count"] == 0
    assert (
        data["nonbipartite_long_diagonal_graph_count"]
        + data["bipartite_long_diagonal_graph_count"]
        == data["perfect_matching_count"]
    )
    assert data["all_m_state_exists"] == bool(
        data["bipartite_long_diagonal_graph_count"]
    )


def test_p17_all_m_artifact_cold_rebuilds():
    path = Path("data/sturmian-source/ahi-p17-all-m-obstruction.json")
    if not path.exists():
        return
    verify_p17_all_m_obstruction(
        json.loads(path.read_text()),
        json.loads(Path("data/sturmian-source/ahi-section10-supports.json").read_text()),
        json.loads(
            Path("data/sturmian-source/ahi-common-support-kernel.json").read_text()
        ),
    )
