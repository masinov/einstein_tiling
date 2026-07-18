#!/usr/bin/env python
"""Classify the verified relaxed models that survive Layer D at index 50."""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.holonomy_csp import (
    build_boundary_holonomy_cnf,
    quotient_boundary_data,
)
from verify_theory_w2_layer_d_index50_sat import verify_clause_model


ROOT = Path(__file__).resolve().parents[1]
WITNESSES = ROOT / "docs/notebook/assets/theory-w2-layer-d-sat-index50.json"
MATRIX = ROOT / "docs/notebook/assets/theory-w2-layer-d-s3-index50.json"
OUT = ROOT / "docs/notebook/assets/theory-w2-layer-d-models-index50.json"
KEY = "010001010104010502f002f1030b030c04fa04fb"


def _components(edges):
    adjacency = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    remaining = set(adjacency)
    sizes = []
    while remaining:
        seed = min(remaining)
        stack = [seed]
        seen = {seed}
        remaining.remove(seed)
        while stack:
            vertex = stack.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    remaining.discard(neighbor)
                    stack.append(neighbor)
        sizes.append(len(seen))
    return tuple(sorted(sizes, reverse=True))


def main():
    witness_payload = json.loads(WITNESSES.read_text())
    matrix = json.loads(MATRIX.read_text())
    mappings = tuple(
        tuple(tuple(image) for image in row["generator_images"])
        for row in matrix["finalist"]["mapping_representatives"]
    )
    shape = decode_compiled_key(KEY)
    rows = []
    for witness in witness_payload["witnesses"]:
        hnf = tuple(witness["hnf"])
        twists = tuple(tuple(value) for value in witness["twists"])
        cnf, metadata = build_boundary_holonomy_cnf(
            shape, hnf, mappings[witness["mapping_index"]], twists,
            cover_mode="at-least",
        )
        if not verify_clause_model(cnf, witness["model_true_variables"]):
            raise AssertionError(f"invalid source witness {witness['pair_orbit']}")
        instance, _, boundaries = quotient_boundary_data(shape, hnf)
        placement_count = len(instance.placements)
        selected = tuple(
            variable - 1
            for variable in witness["model_true_variables"]
            if 1 <= variable <= placement_count
        )
        coverage = [0] * instance.n_cells
        graph_edges = set()
        for placement_index in selected:
            mask = instance.placements[placement_index][1]
            for cell in range(instance.n_cells):
                if (mask >> cell) & 1:
                    coverage[cell] += 1
            for start, _, end, _, _ in boundaries[placement_index]:
                graph_edges.add((start, end) if start < end else (end, start))
        component_sizes = _components(graph_edges)
        histogram = Counter(coverage)
        rows.append({
            "pair_orbit": witness["pair_orbit"],
            "hnf": list(hnf),
            "mapping_index": witness["mapping_index"],
            "twists": witness["twists"],
            "selected_placements": len(selected),
            "exact_cover_tile_count": instance.n_cells // len(shape),
            "coverage_histogram": {
                str(value): count for value, count in sorted(histogram.items())
            },
            "coverage_surplus": sum(coverage) - instance.n_cells,
            "maximum_coverage": max(coverage),
            "active_boundary_vertices": sum(component_sizes),
            "active_boundary_edges": len(graph_edges),
            "active_boundary_components": len(component_sizes),
            "active_boundary_component_sizes": list(component_sizes),
            "canonical_variables": metadata["variables"],
            "true_variables": len(witness["model_true_variables"]),
        })

    def distribution(field):
        return {
            str(value): count
            for value, count in sorted(Counter(row[field] for row in rows).items())
        }

    sources = (Path(__file__),)
    payload = {
        "kind": "theory-w2-layer-d-index50-relaxed-model-analysis",
        "schema_version": 1,
        "date": "2026-07-17",
        "scope": {
            "verified_models": len(rows),
            "interpretation": (
                "diagnostic structure of relaxed at-least-cover models; no row "
                "is an exact cover or tiling certificate"
            ),
        },
        "provenance": {
            "dependencies": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in (WITNESSES, MATRIX)
            ],
            "sources": [
                {
                    "path": str(path.relative_to(ROOT)),
                    "sha256": sha256(path.read_bytes()).hexdigest(),
                }
                for path in sources
            ],
        },
        "summary": {
            "selected_placement_distribution": distribution("selected_placements"),
            "coverage_surplus_distribution": distribution("coverage_surplus"),
            "maximum_coverage_distribution": distribution("maximum_coverage"),
            "boundary_component_count_distribution": distribution(
                "active_boundary_components"
            ),
            "models_with_connected_boundary_network": sum(
                row["active_boundary_components"] == 1 for row in rows
            ),
            "models_at_exact_tile_count": sum(
                row["selected_placements"] == row["exact_cover_tile_count"]
                for row in rows
            ),
        },
        "models": sorted(rows, key=lambda row: row["pair_orbit"]),
    }
    OUT.write_text(json.dumps(payload, indent=1) + "\n")
    print(OUT.relative_to(ROOT))
    print(json.dumps(payload["summary"], indent=1))


if __name__ == "__main__":
    main()
