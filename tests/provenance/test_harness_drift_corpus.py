import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs" / "harness" / "mechanisms" / "registry.json"
CASES = ROOT / "docs" / "harness" / "evaluation" / "drift_cases.json"
REPLAY = ROOT / "docs" / "harness" / "evaluation" / "replays" / "current.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_mechanism_registry_forbids_runtime_self_modification() -> None:
    registry = _load(REGISTRY)
    assert registry["activation_policy"]["automatic_runtime_mutation"] is False
    mechanisms = registry["mechanisms"]
    identifiers = [mechanism["id"] for mechanism in mechanisms]
    assert len(identifiers) == len(set(identifiers))
    assert all(mechanism["status"] in {"active", "proposed", "retired"} for mechanism in mechanisms)


def test_every_drift_case_has_a_current_mechanism_and_decision_boundary() -> None:
    registry = _load(REGISTRY)
    mechanisms = {item["id"]: item for item in registry["mechanisms"]}
    cases = _load(CASES)["cases"]

    identifiers = [case["id"] for case in cases]
    assert len(identifiers) == len(set(identifiers))
    assert len(cases) >= 8

    for case in cases:
        assert case["historical_sources"]
        assert all((ROOT / source).is_file() for source in case["historical_sources"])
        assert len(case["failure_mode"]) >= 30
        assert len(case["input_condition"]) >= 30
        assert len(case["required_decision"]) >= 30
        assert case["forbidden_decisions"]
        assert case["forbidden_actions"]
        assert case["required_action"] not in case["forbidden_actions"]
        assert case["mechanism_tags"]
        for tag in case["mechanism_tags"]:
            assert tag in mechanisms
            assert mechanisms[tag]["status"] == "active"


def test_active_mechanisms_are_exercised_and_preserve_exploration() -> None:
    registry = _load(REGISTRY)
    cases = _load(CASES)["cases"]
    tagged = {tag for case in cases for tag in case["mechanism_tags"]}
    case_ids = {case["id"] for case in cases}

    for mechanism in registry["mechanisms"]:
        if mechanism["status"] != "active":
            continue
        assert mechanism["id"] in tagged
        assert mechanism["evaluation_cases"]
        assert len(mechanism["creative_boundary"]) >= 30
        assert set(mechanism["evaluation_cases"]).issubset(case_ids)


def test_current_replay_matches_every_required_decision_and_creativity_control() -> None:
    corpus = _load(CASES)
    replay = _load(REPLAY)
    mechanisms = {
        item["id"] for item in _load(REGISTRY)["mechanisms"] if item["status"] == "active"
    }
    results = {item["case_id"]: item for item in replay["results"]}
    assert set(results) == {case["id"] for case in corpus["cases"]}

    for case in corpus["cases"]:
        result = results[case["id"]]
        assert result["action"] == case["required_action"]
        assert result["action"] not in case["forbidden_actions"]
        assert result["mechanisms"]
        assert set(result["mechanisms"]).issubset(mechanisms)
        assert len(result["rationale"]) >= 30

    controls = {item["control_id"]: item for item in replay["creativity_controls"]}
    for control in corpus["creativity_controls"]:
        result = controls[control["id"]]
        assert result["action"] == control["required_action"]
        assert result["action"] not in control["forbidden_actions"]
