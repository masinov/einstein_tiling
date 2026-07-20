#!/usr/bin/env python
"""Extend exact A1 torus screening for the ten smallest A2 candidates.

The production E1 sweep used k<=12.  A3/A4 evidence showed that several
small candidates had large-period crystal-like patches, so this audit extends
the exact torus quotient through the largest index supported by the compiled
u128 engine (k=21).

Usage:
  venv/bin/python scripts/run_a1_candidates.py
"""

from __future__ import annotations

import json
import re
import struct
import subprocess
import tempfile
from pathlib import Path

from einstein.e1_candidates import (
    PUBLISHED_APERIODIC_POLYKITE_HORIZON,
    SMALLEST_DEPTH3_KEYS,
    aperiodic_discovery_status,
    decode_compiled_key,
    known_polykite_name,
)
from einstein.funnel.a1_torus import verify_certificate

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "tools" / "a1_torus.rs"
BINARY = ROOT / "target" / "a1_torus"
OUTPUT = ROOT / "docs/notebook/assets/a1-extended-small-candidate-results.json"
STATS = re.compile(
    r"periodic=(?P<periodic>\d+) survivors=(?P<survivors>\d+) "
    r"exhausted=(?P<exhausted>\d+)"
)


def compile_engine():
    BINARY.parent.mkdir(parents=True, exist_ok=True)
    if not BINARY.exists() or BINARY.stat().st_mtime < SOURCE.stat().st_mtime:
        subprocess.run(
            [
                "rustc", "--edition=2021", "-C", "opt-level=3",
                str(SOURCE), "-o", str(BINARY),
            ],
            check=True,
        )


def write_stream(path, n, keys):
    with path.open("wb") as output:
        output.write(struct.pack("<4sBBHQ", b"A0PK", 1, n, 0, len(keys)))
        for key in keys:
            for offset in range(0, len(key), 4):
                output.write(struct.pack("<H", int(key[offset:offset + 4], 16)))


def main():
    compile_engine()
    all_results = []
    with tempfile.TemporaryDirectory(prefix="a1-candidates-") as directory:
        temporary = Path(directory)
        for n, keys in sorted(SMALLEST_DEPTH3_KEYS.items()):
            source = temporary / f"candidates-{n}.bin"
            survivors = temporary / f"survivors-{n}.bin"
            certificates = temporary / f"certificates-{n}.jsonl"
            write_stream(source, n, keys)
            completed = subprocess.run(
                [
                    str(BINARY), str(source), str(survivors),
                    str(certificates), "21", "5000000",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            match = STATS.search(completed.stdout)
            if match is None:
                raise RuntimeError(f"missing A1 stats: {completed.stdout!r}")
            if int(match.group("exhausted")):
                raise RuntimeError("extended A1 audit exhausted its node budget")
            rows = [
                json.loads(line)
                for line in certificates.read_text().splitlines()
            ]
            by_key = {row["shape"]: row for row in rows}
            for index, key in enumerate(keys, 1):
                known_name = known_polykite_name(key)
                discovery_status = aperiodic_discovery_status(n, key)
                certificate = by_key.get(key)
                if certificate is not None:
                    certificate["kind"] = "torus-exact-cover"
                    certificate["index"] = (
                        certificate["hnf"][0] * certificate["hnf"][2]
                    )
                    certificate["tiles_per_domain"] = len(
                        certificate["placements"]
                    )
                    assert verify_certificate(
                        decode_compiled_key(key), certificate
                    )
                all_results.append({
                    "n": n,
                    "index": index,
                    "shape": key,
                    "known_name": known_name,
                    "novel_key": known_name is None,
                    "published_aperiodic_horizon": (
                        n <= PUBLISHED_APERIODIC_POLYKITE_HORIZON
                    ),
                    "aperiodic_discovery_status": discovery_status,
                    # Backward-compatible field: novelty means publishable
                    # aperiodic discovery eligibility, not merely a new key.
                    "novel": discovery_status == "eligible",
                    "verdict": (
                        "periodic" if certificate is not None
                        else "no-periodic-at-budget"
                    ),
                    "certificate": certificate,
                })
            print(completed.stdout.strip())

    payload = {
        "kind": "extended-exact-torus-screen",
        "literature_scope": {
            "published_aperiodic_polykite_horizon": (
                PUBLISHED_APERIODIC_POLYKITE_HORIZON
            ),
            "all_rows_are_validation_not_discovery": True,
            "controlling_correction": "ERR-004/D-0049",
        },
        "k_max": 21,
        "node_budget_per_torus": 5_000_000,
        "periodic": sum(
            row["verdict"] == "periodic" for row in all_results
        ),
        "survivors": sum(
            row["verdict"] != "periodic" for row in all_results
        ),
        "results": all_results,
    }
    OUTPUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUTPUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
