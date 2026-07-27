import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
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
