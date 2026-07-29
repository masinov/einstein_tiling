#!/usr/bin/env python
"""Cold-check the stored 2-Lambda V4 pullback-family witnesses."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from hashlib import sha256
import json
from pathlib import Path

from einstein.repository import repository_root

from einstein.polykites.known_shapes import decode_compiled_key
from einstein.holonomy.alternating4.lifts import (
    BASE_HNF,
    aggregate_rows,
    even_hnfs,
    lift_2lambda_witness,
    unsatisfied_clauses,
    verify_finite_lift,
)
from einstein.holonomy.alternating4.local_system import build_v4_coverability_cnf
from einstein.holonomy.constraints import _cnf_sha256


ROOT = repository_root(Path(__file__))
ARTIFACT = ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--jobs", type=int, default=24)
    args = parser.parse_args()
    payload = json.loads(ARTIFACT.read_text())
    if payload["kind"] != "theory-w2-layer-d-v4-2lambda-pullback-family":
        raise AssertionError("unexpected artifact kind")
    for section in ("dependencies", "sources"):
        for row in payload["provenance"][section]:
            path = ROOT / row["path"]
            if sha256(path.read_bytes()).hexdigest() != row["sha256"]:
                raise AssertionError(f"provenance mismatch: {row['path']}")
    shape = decode_compiled_key(KEY)
    finite_tasks = []
    for witness in payload["base_witnesses"]:
        images = tuple(witness["images"])
        base_twists = tuple(witness["base_twists"])
        selected = tuple(tuple(row) for row in witness["selected_placements"])
        colors = tuple(
            (tuple(row["vertex"]), row["color"])
            for row in witness["vertex_colors"]
        )
        twists, values = lift_2lambda_witness(
            shape, BASE_HNF, base_twists, selected, colors
        )
        cnf, metadata = build_v4_coverability_cnf(shape, BASE_HNF, images, twists)
        if (metadata != witness["metadata"]
                or _cnf_sha256(cnf) != witness["canonical_cnf_sha256"]
                or unsatisfied_clauses(cnf, values)):
            raise AssertionError("base witness replay failed")
        for hnf in even_hnfs(payload["summary"]["finite_gate_maximum_index"]):
            finite_tasks.append((
                shape, hnf, witness["mapping_index"], images, base_twists,
                selected, colors,
            ))
    finite_rows = []
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(verify_finite_lift, task) for task in finite_tasks]
        for completed, future in enumerate(as_completed(futures), 1):
            finite_rows.append(future.result())
            if completed % 384 == 0 or completed == len(finite_tasks):
                print(f"[{completed:4d}/{len(finite_tasks)}] VERIFIED", flush=True)
    finite_rows.sort(key=lambda row: (row["mapping_index"], row["hnf"]))
    if (len(finite_rows) != payload["summary"]["finite_gate_map_hnf_lifts"]
            or aggregate_rows(finite_rows) != payload["summary"]["finite_gate_aggregate_sha256"]):
        raise AssertionError("finite-gate completeness or aggregate mismatch")
    print(
        f"V4 2-Lambda witnesses VERIFIED: {len(payload['base_witnesses'])} base; "
        f"{len(finite_rows)} finite pullbacks"
    )


if __name__ == "__main__":
    main()
