#!/usr/bin/env python
"""Certify the exact D6 covariance visible in the index-45 Layer-D matrix."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from einstein.substrate.kitegrid import N_OPS
from einstein.theory.holonomy_symmetry import (
    hnf_d6_image,
    orbit,
    pullback_s3_images,
    signed_edge_action,
)


ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index45.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-symmetry.json"


def main():
    data = json.loads(MATRIX.read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in data["finalist"]["mapping_representatives"]
    )
    mapping_index = {images: index for index, images in enumerate(mappings)}
    hnfs = tuple(tuple(row["hnf"]) for row in data["finalist"]["by_hnf"])
    verdict = {
        (tuple(row["hnf"]), row["mapping_index"]): row["scan"]["verdict"]
        for row in data["finalist"]["results"]
    }

    def map_action(index, op):
        return mapping_index[pullback_s3_images(mappings[index], op)]

    hnf_orbits = orbit(hnfs, hnf_d6_image)
    mapping_orbits = orbit(range(len(mappings)), map_action)
    effective = tuple(sorted({
        index for (_, index), value in verdict.items()
        if value == "holonomy-obstructed"
    }))
    effective_orbits = tuple(
        item for item in mapping_orbits if set(item) <= set(effective)
    )

    covariance_checks = 0
    for (hnf, index), value in verdict.items():
        for op in range(N_OPS):
            moved = (hnf_d6_image(hnf, op), map_action(index, op))
            if verdict[moved] != value:
                raise AssertionError(
                    f"covariance failure: {(hnf, index)} op {op} -> {moved}"
                )
            covariance_checks += 1

    unseen = set(verdict)
    pair_orbits = []
    while unseen:
        seed = min(unseen)
        current = frozenset(
            (hnf_d6_image(seed[0], op), map_action(seed[1], op))
            for op in range(N_OPS)
        )
        if not current <= unseen:
            raise AssertionError("diagonal action failed to partition the matrix")
        unseen.difference_update(current)
        pair_orbits.append(current)

    sources = (
        ROOT / "src/einstein/theory/holonomy_symmetry.py",
        Path(__file__),
    )
    payload = {
        "kind": "theory-w2-layer-d-d6-covariance",
        "schema_version": 1,
        "date": "2026-07-17",
        "theorem": {
            "id": "T2.D3",
            "statement": (
                "Layer-D satisfiability is invariant under the diagonal D6 "
                "action: move the period HNF covariantly and pull the S3 "
                "edge map back contravariantly."
            ),
            "mechanism": (
                "The kite-grid operation bijects cells, placements, boundary "
                "edges, quotient vertices, commuting twists, and developing "
                "potentials, hence bijects CNF models."
            ),
        },
        "scope": {
            "hnfs": len(hnfs),
            "mapping_classes": len(mappings),
            "matrix_entries": len(verdict),
            "d6_operations": N_OPS,
            "covariance_checks": covariance_checks,
            "all_checks_passed": covariance_checks == len(verdict) * N_OPS,
        },
        "provenance": {
            "matrix": {
                "path": str(MATRIX.relative_to(ROOT)),
                "sha256": sha256(MATRIX.read_bytes()).hexdigest(),
            },
            "sources": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in sources
            ],
        },
        "signed_edge_actions": [
            {"operation": op, "generator_images": list(signed_edge_action(op))}
            for op in range(N_OPS)
        ],
        "hnf_orbits": [[list(hnf) for hnf in item] for item in hnf_orbits],
        "mapping_orbits": [list(item) for item in mapping_orbits],
        "effective_mapping_classes": list(effective),
        "effective_mapping_orbits": [list(item) for item in effective_orbits],
        "diagonal_pair_orbits": {
            "count": len(pair_orbits),
            "size_distribution": {
                str(size): count
                for size, count in sorted(Counter(map(len, pair_orbits)).items())
            },
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["scope"], indent=1))
    print("HNF orbits:", payload["hnf_orbits"])
    print("effective map orbits:", payload["effective_mapping_orbits"])
    print("diagonal pair orbits:", payload["diagonal_pair_orbits"])


if __name__ == "__main__":
    main()
