#!/usr/bin/env python
"""Independent structural verifier for the W3 component-language artifact."""

from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

from einstein.repository import repository_root

from einstein.tilings.spectre.components import patch_obeys_language
from einstein.tilings.spectre.patches import (
    IDENTITY,
    patch_edge_incidence,
    poses_overlap,
)
from einstein.tilings.spectre.certificates import file_sha256
from einstein.tilings.spectre.source_controls import (
    generated_parent_coronas,
    physical_corona_language,
)


ROOT = repository_root(Path(__file__))
A6_PATH = ROOT / "docs/notebook/assets/a6-spectre-results.json"
PHYSICAL_PATH = ROOT / "docs/notebook/assets/theory-w3-spectre-physical-language.json"


def _pose(row):
    return int(row[0]), int(row[1]), tuple(map(int, row[2]))


def _verify_radius_ball(patch, radius):
    if len(set(patch)) != len(patch) or IDENTITY not in patch:
        return False
    if any(poses_overlap(left, right)
           for index, left in enumerate(patch) for right in patch[:index]):
        return False
    incidence, _ = patch_edge_incidence(patch)
    if any(len(owners) > 2 for owners in incidence.values()):
        return False
    adjacency = {tile: set() for tile in patch}
    exposed = set()
    for owners in incidence.values():
        if len(owners) == 1:
            exposed.add(owners[0])
        elif len(owners) == 2:
            left, right = owners
            adjacency[left].add(right)
            adjacency[right].add(left)
    distance = {IDENTITY: 0}
    queue = deque((IDENTITY,))
    while queue:
        tile = queue.popleft()
        for neighbor in adjacency[tile]:
            if neighbor not in distance:
                distance[neighbor] = distance[tile] + 1
                queue.append(neighbor)
    return (
        len(distance) == len(patch)
        and max(distance.values()) == radius
        and all(tile not in exposed for tile, depth in distance.items()
                if depth < radius)
    )


def verify(path):
    artifact = json.loads(Path(path).read_text())
    if (
        artifact.get("schema") != "einstein.w3.spectre-component-language"
        or artifact.get("version") != 1
        or artifact.get("status")
        != "PARENT_PARTITION_PROVED_CLOSURE_OPEN_RADIUS9"
    ):
        return False, "unsupported schema or status"
    provenance = artifact["provenance"]
    for prefix in ("a6", "physical"):
        source_path = ROOT / provenance[f"{prefix}_source"]
        if file_sha256(source_path) != provenance[f"{prefix}_sha256"]:
            return False, f"{prefix} source hash mismatch"
    transducer = artifact["radius3_transducer"]
    partition = artifact["partition_theorem"]
    if not (
        transducer["rooted_cases"] == 418
        and transducer["all_have_parent"]
        and transducer["all_have_unique_parent_anchor"]
        and partition == {
            "decisive_radius": 6,
            "surviving_radius6_patches": 15216,
            "common_eight_child_core_failures": 0,
            "fiber_types": [8, 9],
            "verdict": "unique-parent-anchor fibers form a full/missing partition",
        }
    ):
        return False, "parent-partition theorem fields changed"
    records = artifact["contraction_audit"]["radius_records"]
    expected = [
        (4, 257, 0, 0, 1861),
        (5, 1517, 0, 0, 5140),
        (6, 4482, 4292, 986, 10924),
        (7, 10048, 51309, 6280, 6280),
        (8, 6199, 0, 1796, 1796),
        (9, 1735, 0, 4482, 4482),
    ]
    actual = [(
        row["radius"], row["dead_input_patches"],
        row["generated_parent_corona_extensions"],
        row["nongenerated_parent_corona_extensions"],
        row["continued_frontier_patches"],
    ) for row in records]
    if actual != expected:
        return False, "radius-frontier census changed"
    expected_digests = [
        "94c888aab312d610d16dcac8adaedbbfafa435344176e346a985f019554e911d",
        "89c1567c0154c150875bf724242a8be2ac06e8eb17a237e98abc235816a81fd4",
        "6c835973dcb1e65d564c2b9dc27f53d99d600db88a862811d82cccba283028e4",
        "dec591c1e19de9befe4df47fefa1a20d7fdb0fb811d9ff0076c8bedf8c8bfa13",
        "12da276d5e7ac11f833d00baab1fdbf99b2a9416ad239d27bd854a041157ea40",
        "ccfeeb916328daf4e82187b8ee7c02b56fc1e93193fd940eecfcfb2742c7a18d",
    ]
    if [row["continued_frontier_sha256"] for row in records] != expected_digests:
        return False, "radius-frontier digest changed"
    witness = artifact["representative_radius9_frontier"]
    patch = tuple(_pose(row) for row in witness["patch"])
    if not _verify_radius_ball(patch, 9):
        return False, "representative is not an exact graph-radius-nine ball"
    physical = json.loads(PHYSICAL_PATH.read_text())
    if not patch_obeys_language(patch, physical_corona_language(physical)):
        return False, "representative violates the L18 corona language"
    parent_corona = tuple(_pose(row) for row in witness["parent_corona"])
    a6 = json.loads(A6_PATH.read_text())
    if parent_corona in generated_parent_coronas(a6):
        return False, "representative contracted corona is generated"
    extras = artifact["contraction_audit"][
        "nongenerated_signature_histogram_through_radius7"
    ]
    if repr(parent_corona) not in extras:
        return False, "representative contracted corona is not cataloged"
    return True, (
        "418-case unique parent transducer; partition forced by radius 6; "
        "a verified L18 nonclosure frontier reaches radius 9"
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    args = parser.parse_args()
    ok, message = verify(args.artifact)
    print(("PASS" if ok else "FAIL") + ": " + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
