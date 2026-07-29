from __future__ import annotations

import fnmatch
import json
from pathlib import Path


TESTS = Path(__file__).resolve().parent
CONFIG = json.loads((TESTS / "TEST_TIERS.json").read_text())


def tier_for(filename: str) -> str:
    for rule in CONFIG["rules"]:
        if fnmatch.fnmatchcase(filename, rule["glob"]):
            return rule["tier"]
    raise LookupError(f"no test tier declared for {filename}")


def pytest_collection_modifyitems(items):
    for item in items:
        path = Path(str(item.path))
        try:
            relative = path.resolve().relative_to(TESTS).as_posix()
        except ValueError:
            continue
        if path.name.startswith("test_"):
            item.add_marker(tier_for(relative))
