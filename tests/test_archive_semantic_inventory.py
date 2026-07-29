"""The script archive has a complete semantic, not merely physical, map."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "scripts/archive"


def test_semantic_inventory_covers_the_archive_exactly_once():
    manifest = json.loads((ARCHIVE / "MANIFEST.json").read_text())
    inventory = json.loads((ARCHIVE / "SEMANTIC_INVENTORY.json").read_text())
    expected = {row["new_path"] for row in manifest["scripts"]}
    classified = [
        path for cluster in inventory["clusters"] for path in cluster["scripts"]
    ]
    assert len(classified) == len(set(classified))
    assert set(classified) == expected
    assert len(classified) == manifest["script_count"] == 92


def test_semantic_dispositions_and_promoted_targets_are_resolvable():
    inventory = json.loads((ARCHIVE / "SEMANTIC_INVENTORY.json").read_text())
    allowed = set(inventory["dispositions"])
    assert all(cluster["disposition"] in allowed for cluster in inventory["clusters"])
    assert all(cluster["rationale"].strip() for cluster in inventory["clusters"])
    for extraction in inventory["promoted_abstractions"]:
        target = extraction["target"].split(":", 1)[0]
        if "*" not in target:
            assert (ROOT / target).is_file()
        for source in extraction["sources"]:
            assert (ROOT / source).is_file()
