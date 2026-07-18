#!/usr/bin/env python
"""Extract the exact map-theoretic signature of the A4 index-50 killers."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from einstein.theory.finite_groups import alternating_group
from einstein.theory.holonomy_quotients import pullback_images


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-index50.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-a4-signature.json"


def main():
    matrix_bytes = MATRIX.read_bytes()
    matrix = json.loads(matrix_bytes)
    mappings = tuple(
        tuple(images) for images in matrix["finalist"]["mapping_representatives"]
    )
    mapping_index = {images: index for index, images in enumerate(mappings)}
    group = alternating_group(4)
    v4 = frozenset(
        value for value in range(group.order)
        if group.multiplication[value][value] == group.identity
    )
    if len(v4) != 4:
        raise AssertionError("A4 involution kernel changed")

    unseen = set(range(len(mappings)))
    map_orbits = []
    while unseen:
        seed = min(unseen)
        members = frozenset(
            mapping_index[pullback_images(mappings[seed], op, group)]
            for op in range(12)
        )
        map_orbits.append(tuple(sorted(members)))
        unseen.difference_update(members)

    cosets = []
    unseen_values = set(range(group.order))
    while unseen_values:
        seed = min(unseen_values)
        coset = frozenset(group.multiplication[seed][value] for value in v4)
        cosets.append(coset)
        unseen_values.difference_update(coset)
    coset_index = {
        value: index for index, coset in enumerate(cosets) for value in coset
    }

    observed_killers = frozenset(
        matrix["finalist"]["by_hnf"][0]["killing_mapping_indices"]
    )
    if any(
        frozenset(row["killing_mapping_indices"]) != observed_killers
        for row in matrix["finalist"]["by_hnf"]
    ):
        raise AssertionError("A4 killing signature is not HNF-independent")
    distinct_v4_tail = frozenset(
        index for index, images in enumerate(mappings)
        if all(value in v4 for value in images[3:])
        and len(set(images[3:])) == 3
    )
    if distinct_v4_tail != observed_killers:
        raise AssertionError("distinct-V4-tail signature does not characterize killers")

    effective_orbits = [
        orbit for orbit in map_orbits if frozenset(orbit) <= observed_killers
    ]
    if frozenset(value for orbit in effective_orbits for value in orbit) != observed_killers:
        raise AssertionError("killer maps are not complete D6 orbits")

    payload = {
        "kind": "theory-w2-layer-d-a4-index50-map-signature",
        "schema_version": 1,
        "date": "2026-07-18",
        "scope": {
            "statement_type": "exact finite classification, not an HNF-family theorem",
            "mapping_classes": len(mappings),
            "frontier_hnfs": len(matrix["finalist"]["by_hnf"]),
        },
        "provenance": {
            "matrix": {"path": str(MATRIX.relative_to(ROOT)),
                       "sha256": sha256(matrix_bytes).hexdigest()},
            "source": {"path": str(Path(__file__).relative_to(ROOT)),
                       "sha256": sha256(Path(__file__).read_bytes()).hexdigest()},
        },
        "a4_structure": {
            "v4_indices": sorted(v4),
            "v4_labels": [list(group.labels[value]) for value in sorted(v4)],
            "quotient_cosets": [sorted(coset) for coset in cosets],
            "map_d6_orbits": [list(orbit) for orbit in map_orbits],
        },
        "finite_signature": {
            "hnf_independent": True,
            "killing_mapping_indices": sorted(observed_killers),
            "predicate": (
                "the final three generator images are three distinct elements "
                "of the normal Klein four subgroup V4"
            ),
            "predicate_exact_on_48_classes": True,
            "effective_d6_map_orbits": [list(orbit) for orbit in effective_orbits],
            "effective_d6_orbit_sizes": [len(orbit) for orbit in effective_orbits],
            "quotient_signatures": sorted({
                tuple(coset_index[value] for value in mappings[index])
                for index in observed_killers
            }),
        },
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["finite_signature"], indent=1))


if __name__ == "__main__":
    main()
