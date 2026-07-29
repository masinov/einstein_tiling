import json
from collections import Counter
from pathlib import Path

from einstein.repository import repository_root


ROOT = repository_root(Path(__file__))
QUOTIENT = ROOT / "data/sturmian-source/ahi-corridor-quotient.json"


def test_corridor_quotient_has_twelve_states_and_three_macros():
    quotient = json.loads(QUOTIENT.read_text())
    assert len(quotient["alphabet"]) == 12
    assert set(quotient["macros"]) == {"large_A", "large_B", "small_M"}
    assert len(quotient["euclidean_frame_action"]) == 12


def test_corridor_roles_are_exactly_the_gap_pairs():
    quotient = json.loads(QUOTIENT.read_text())
    role_bits = {"S": [0, 0], "L": [1, 1]}
    for macro in quotient["macros"].values():
        for embedding in macro["embeddings"]:
            for state in embedding:
                bits = state["corridor_bits"]
                if state["role"] in role_bits:
                    assert bits == role_bits[state["role"]]
                else:
                    assert sorted(bits) == [0, 1]


def test_each_large_macro_has_two_s_and_one_l_on_every_axis():
    quotient = json.loads(QUOTIENT.read_text())
    m_distributions = {}
    for name in ("large_A", "large_B"):
        [embedding] = quotient["macros"][name]["embeddings"]
        by_axis = {
            axis: Counter(
                state["role"] for state in embedding if state["axis"] == axis
            )
            for axis in range(3)
        }
        assert all(
            counts["S"] == 2 and counts["L"] == 1
            for counts in by_axis.values()
        )
        m_distributions[name] = sorted(by_axis[axis]["M"] for axis in range(3))
    assert m_distributions == {
        "large_A": [0, 3, 3],
        "large_B": [2, 2, 2],
    }
