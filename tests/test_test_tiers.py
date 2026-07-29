from __future__ import annotations

import fnmatch
import json
from pathlib import Path


TESTS = Path(__file__).resolve().parent


def test_every_test_module_has_exactly_one_primary_tier():
    config = json.loads((TESTS / "TEST_TIERS.json").read_text())
    tiers = set(config["tiers"])
    rules = config["rules"]

    assert rules
    assert all(rule["tier"] in tiers for rule in rules)

    modules = sorted(path.name for path in TESTS.glob("test_*.py"))
    for module in modules:
        matches = [rule for rule in rules if fnmatch.fnmatchcase(module, rule["glob"])]
        assert matches, module
        assert matches[0]["tier"] in tiers
