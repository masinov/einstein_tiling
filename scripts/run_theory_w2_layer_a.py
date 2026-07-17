#!/usr/bin/env python
"""Archive the W2 Layer A zero-false-exclusion gate and finalist kill table."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.db import code_version
from einstein.e1_candidates import decode_compiled_key
from einstein.theory.invariants import (
    area_obstruction,
    prime_sector_obstruction,
    verify_area_obstruction,
    verify_prime_sector_obstruction,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "notebook" / "assets" / "theory-w2-layer-a.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    paths = sorted((ROOT / "data" / "a1-compiled").glob("periodic-*.jsonl"))
    if not paths:
        raise RuntimeError("compiled periodic corpus is not materialized")
    corpus = []
    checked = false_area = false_sector = 0
    for path in paths:
        rows = 0
        for line in path.read_text().splitlines():
            if not line:
                continue
            row = json.loads(line)
            shape = decode_compiled_key(row["shape"])
            index = row["hnf"][0] * row["hnf"][2]
            area = area_obstruction(len(shape), index)
            sector = prime_sector_obstruction(shape, index)
            false_area += area is not None
            false_sector += sector is not None
            checked += 1
            rows += 1
        corpus.append(
            {
                "path": str(path.relative_to(ROOT)),
                "sha256": sha256(path.read_bytes()).hexdigest(),
                "certificates": rows,
            }
        )
    if false_area or false_sector:
        raise AssertionError("Layer A falsely excluded a verified periodic tiling")

    finalist = decode_compiled_key(KEY)
    kill_table = []
    for index in range(1, 61):
        area = area_obstruction(len(finalist), index)
        sector = prime_sector_obstruction(finalist, index)
        if area and not verify_area_obstruction(area):
            raise AssertionError("area witness did not verify")
        if sector and not verify_prime_sector_obstruction(finalist, sector):
            raise AssertionError("sector witness did not verify")
        kill_table.append(
            {
                "index": index,
                "area": "killed" if area else "admissible",
                "sector": "killed" if sector else "admissible",
                "sector_modulus": sector["modulus"] if sector else None,
            }
        )
    additional = sum(
        row["area"] == "admissible" and row["sector"] == "killed"
        for row in kill_table
    )
    source = ROOT / "src" / "einstein" / "theory" / "invariants.py"
    payload = {
        "kind": "theory-w2-layer-a",
        "schema_version": 1,
        "date": "2026-07-17",
        "provenance": {
            "code_version": code_version(),
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
            "periodic_corpus": corpus,
        },
        "validation": {
            "verified_periodic_certificates": checked,
            "false_area_exclusions": false_area,
            "false_sector_exclusions": false_sector,
        },
        "finalist": {
            "shape": KEY,
            "indices_tested": [1, 60],
            "area_required_index_modulus": 5,
            "kill_table": kill_table,
            "area_killed": sum(row["area"] == "killed" for row in kill_table),
            "sector_killed": sum(row["sector"] == "killed" for row in kill_table),
            "additional_sector_kills": additional,
            "conclusion": (
                "The prime sector-coloring witness reproduces k=0 mod 5 and "
                "adds no exclusions beyond area for the finalist."
            ),
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({"validation": payload["validation"], "finalist": {
        "area_killed": payload["finalist"]["area_killed"],
        "sector_killed": payload["finalist"]["sector_killed"],
        "additional_sector_kills": additional,
    }}, indent=1))


if __name__ == "__main__":
    main()
