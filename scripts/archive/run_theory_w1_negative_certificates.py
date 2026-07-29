#!/usr/bin/env python
"""Emit and independently verify W1 cycle-free control certificates."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from einstein.polykites.database import code_version, deserialize_cells, serialize_cells
from einstein.polykites.enumeration import enumerate_free_polykites
from einstein.polykites.periodic_quotients import find_periodic_tiling
from einstein.periodicity.transfer import CylinderTransfer
from einstein.periodicity.verification import verify_cycle_free_manifest


ROOT = Path(__file__).resolve().parents[2]
OUT = (
    ROOT / "docs" / "notebook" / "assets"
    / "theory-w1-cycle-free-controls.json"
)


def nontiling_two_kite():
    for n, forms in enumerate_free_polykites(2):
        if n == 2:
            for shape in forms:
                if find_periodic_tiling(shape, k_max=6)[0] is None:
                    return shape
    raise RuntimeError("Myers-validated two-kite non-tiler not found")


def hat_shape():
    fixture = ROOT / "tests" / "fixtures" / "polykites-n8.sqlite"
    conn = sqlite3.connect(f"{fixture.resolve().as_uri()}?mode=ro", uri=True)
    row = conn.execute("SELECT key FROM shapes WHERE id=635").fetchone()
    conn.close()
    if row is None:
        raise RuntimeError("hat anchor shape 635 is absent")
    return deserialize_cells(row[0])


def certify(label, shape, vector):
    manifest = CylinderTransfer(shape, vector).cycle_free_manifest()
    if not verify_cycle_free_manifest(manifest):
        raise AssertionError(f"independent verifier rejected {label} {vector}")
    return {
        "label": label,
        "shape_key": serialize_cells(shape),
        "vector": list(vector),
        "independently_verified": True,
        "certificate": manifest,
    }


def main():
    non = nontiling_two_kite()
    hat = hat_shape()
    cases = [certify("two-kite-nontiler", non, (1, 0))]
    cases.extend(
        certify("hat", hat, vector)
        for vector in ((1, 0), (0, 1), (1, 1), (2, 0))
    )
    producer = ROOT / "src" / "einstein" / "theory" / "transfer.py"
    verifier = ROOT / "src" / "einstein" / "theory" / "transfer_verify.py"
    payload = {
        "kind": "theory-w1-cycle-free-controls",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": (
            "finite control vectors only; these certificates do not prove "
            "universal aperiodicity"
        ),
        "provenance": {
            "code_version": code_version(),
            "producer": str(producer.relative_to(ROOT)),
            "producer_sha256": sha256(producer.read_bytes()).hexdigest(),
            "verifier": str(verifier.relative_to(ROOT)),
            "verifier_sha256": sha256(verifier.read_bytes()).hexdigest(),
        },
        "cases": cases,
        "summary": {
            "certificates": len(cases),
            "independently_verified": sum(
                case["independently_verified"] for case in cases
            ),
            "total_states": sum(
                case["certificate"]["counts"]["states"] for case in cases
            ),
            "total_edges": sum(
                case["certificate"]["counts"]["edges"] for case in cases
            ),
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))


if __name__ == "__main__":
    main()
