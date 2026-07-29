#!/usr/bin/env python
"""Run the first W2.D nonabelian boundary/holonomy controls."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.db import code_version
from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy import (
    IDENTITY,
    line_tile_boundary_words,
    p3_value,
    s3_boundary_quotients,
    staircase_boundary_word,
    u_triangle_winding,
)


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-phase0.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    tiles = []
    for word in line_tile_boundary_words():
        tiles.append({
            "word": word,
            "p3_closed": p3_value(word) == IDENTITY,
            "u_triangle_winding": u_triangle_winding(word),
        })
    if not all(row["p3_closed"] and row["u_triangle_winding"] == 0 for row in tiles):
        raise AssertionError("Conway--Lagarias tile control failed")

    staircases = []
    for index in range(61):
        if index % 3 not in (0, 2):
            continue
        word = staircase_boundary_word(index)
        measured = u_triangle_winding(word)
        expected = (index + 1) // 3
        if p3_value(word) != IDENTITY or measured != expected:
            raise AssertionError(f"published staircase formula failed at {index}")
        staircases.append({
            "index": index,
            "word": word,
            "measured": measured,
            "published_formula": expected,
        })

    finalist = decode_compiled_key(KEY)
    s3 = s3_boundary_quotients(finalist)
    if s3["surjections"] == 0:
        raise AssertionError("finalist presentation has no S3 quotient")
    if s3["surjections_with_displacement_coset_obstruction"]:
        raise AssertionError("unexpected displacement-only S3 obstruction")

    source = ROOT / "src/einstein/theory/holonomy.py"
    payload = {
        "kind": "theory-w2-layer-d-phase0",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "completed": (
                "primary-source planar boundary-invariant anchor; finalist "
                "free-boundary presentation; exhaustive S3 quotient spike"
            ),
            "not_completed": (
                "no torus obstruction is claimed; canonical displacement "
                "commutators omit the binary tile-boundary network"
            ),
            "next_certificate": (
                "joint exact-cover plus finite-group boundary-potential CSP, "
                "with commuting torus holonomies checked in the selected network"
            ),
        },
        "primary_source": {
            "title": "Tiling with Polyominoes and Combinatorial Group Theory",
            "authors": ["J. H. Conway", "J. C. Lagarias"],
            "journal": "Journal of Combinatorial Theory, Series A 53 (1990), 183-208",
            "doi": "10.1016/0097-3165(90)90057-4",
            "theorem_anchor": "Theorem 1.2 and Section 3, p3 Cayley winding",
            "audited_pdf_sha256": "92004b6e8b01924305b2709483f0508610a582609f9cc9d71ae1d807d9571ffd",
        },
        "provenance": {
            "code_version": code_version(),
            "source": str(source.relative_to(ROOT)),
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
        },
        "published_control": {
            "line_tile_boundaries": tiles,
            "staircase_range": [0, 60],
            "staircases": staircases,
            "result": (
                "all line-tile invariants are zero; staircase winding equals "
                "floor((N+1)/3), reproducing the obstruction in Theorem 1.2"
            ),
        },
        "finalist": {
            "shape": KEY,
            "boundary_target": s3,
            "conclusion": (
                "nonabelian quotients exist abundantly, but every S3 quotient "
                "loses enough zero-displacement information that all displacement "
                "coset pairs admit commuting representatives; binary coupling is required"
            ),
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps({
        "published_controls": len(staircases),
        "s3": {
            key: value for key, value in s3.items()
            if key not in {"relators", "sample_surjections"}
        },
    }, indent=1))


if __name__ == "__main__":
    main()
