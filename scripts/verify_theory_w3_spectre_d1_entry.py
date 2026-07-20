#!/usr/bin/env python
"""Independent SAT replay of the ancestry-free Spectre D1 entry proof."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.solvers import Cadical195

from einstein.theory.spectre_d1_entry import (
    advance_frontier,
    initial_frontier,
)
from einstein.theory.spectre_patch_language import (
    _candidate_ring_tiles,
    poses_overlap,
)
from einstein.theory.substitution_certificate import file_sha256


ROOT = Path(__file__).resolve().parents[1]


def independent_advance(item):
    """Enumerate next rings with a verifier-owned one-hot CNF."""
    corona_index, patch = item
    exposed, candidate_cover = _candidate_ring_tiles(patch)
    candidates = tuple(sorted(candidate_cover))
    variables = tuple(range(1, len(candidates) + 1))
    clauses = []
    by_edge = [[] for _ in exposed]
    for index, pose in enumerate(candidates):
        for edge in candidate_cover[pose]:
            by_edge[edge].append(variables[index])
    if not all(by_edge):
        return corona_index, 0, len(candidates), 0, ()
    for covering in by_edge:
        clauses.append(list(covering))
        clauses.extend(
            [-left, -right]
            for offset, left in enumerate(covering)
            for right in covering[offset + 1:]
        )
    for left, pose in enumerate(candidates):
        for right in range(left):
            if poses_overlap(pose, candidates[right]):
                clauses.append([-variables[left], -variables[right]])

    children = []
    calls = 0
    with Cadical195(bootstrap_with=clauses) as solver:
        while True:
            calls += 1
            if not solver.solve():
                break
            positive = {literal for literal in solver.get_model() if literal > 0}
            selected = tuple(
                candidates[index]
                for index, variable in enumerate(variables)
                if variable in positive
            )
            children.append(tuple(sorted((*patch, *selected))))
            selected_set = set(selected)
            solver.add_clause([
                -variables[index] if pose in selected_set else variables[index]
                for index, pose in enumerate(candidates)
            ])
    result = tuple(sorted(children))
    return corona_index, len(result), len(candidates), calls, result


def verify(path, workers):
    artifact = json.loads(Path(path).read_text())
    if (
        artifact.get("schema") != "einstein.w3.spectre-d1-entry"
        or artifact.get("version") != 1
        or artifact.get("status") != "EDGE_TO_EDGE_L18_ENTRY_PROVED_RADIUS5"
    ):
        return False, "unsupported schema or status"
    provenance = artifact["provenance"]
    physical = ROOT / provenance["physical_language_source"]
    if file_sha256(physical) != provenance["physical_language_sha256"]:
        return False, "physical-language source hash mismatch"
    source = json.loads(physical.read_text())["analysis"]
    if source["radius3"]["unobserved_survivor_indices"] != [33, 44, 155]:
        return False, "source extra-corona set changed"

    frontier = initial_frontier()
    replay = []
    for expected in artifact["elimination"]["radius_records"]:
        frontier, summary = advance_frontier(
            frontier,
            expected["radius"],
            workers=workers,
            advance=independent_advance,
        )
        if summary != expected:
            return False, f"radius-{expected['radius']} census changed"
        replay.append(summary["surviving_patches"])
    if frontier:
        return False, "independent radius-five frontier is nonempty"
    if artifact["elimination"]["decisive_radius"] != 5:
        return False, "decisive radius changed"
    if not artifact["elimination"]["all_extra_coronas_eliminated"]:
        return False, "artifact does not assert elimination"
    return True, f"independent frontiers [3,{','.join(map(str, replay))}]"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("artifact")
    parser.add_argument("--workers", type=int, default=24)
    args = parser.parse_args()
    ok, message = verify(args.artifact, args.workers)
    print(("PASS" if ok else "FAIL") + ": " + message)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
