#!/usr/bin/env python
"""Cutting-plane search for a fractional two-center discharging rule."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import highspy

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_marking import (
    enhanced_resource_incidence_conflict_graph,
)


ROOT = Path(__file__).resolve().parents[1]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def solve(
    shape, images, radius, maximum_iterations=1000, signed=False,
    feature_point=None,
):
    tile_types, vertices, edges = enhanced_resource_incidence_conflict_graph(
        shape, images, radius, feature_point=feature_point
    )
    by_type = {}
    for index, (type_index, _, _) in enumerate(vertices):
        by_type.setdefault(type_index, []).append(index)

    master = highspy.Highs()
    master.silent()
    lower = -highspy.kHighsInf if signed else 0.0
    total = 1.0 if signed else 2.0
    capacity = 0.5 if signed else 1.0
    weights = [master.addVariable(lb=lower, name=f"w_{index}")
               for index in range(len(vertices))]
    if signed:
        magnitudes = [master.addVariable(lb=0.0, obj=1.0, name=f"a_{index}")
                      for index in range(len(vertices))]
        for weight, magnitude in zip(weights, magnitudes):
            master.addConstr(magnitude >= weight)
            master.addConstr(magnitude >= -weight)
        master.setMinimize()
    for type_index, indices in sorted(by_type.items()):
        master.addConstr(
            sum(weights[index] for index in indices) == total,
            name=f"type_{type_index}",
        )
    # Global XOR of every V4 potential is a symmetry.  Averaging any rule over
    # it preserves every stable-set inequality, so impose the invariant gauge
    # coordinates up front instead of rediscovering four equivalent cuts.
    gauge_orbits = {}
    for index, (type_index, u, v) in enumerate(vertices):
        operation, gauge, feature = tile_types[type_index]
        normalized_feature = None if feature is None else feature ^ gauge
        gauge_orbits.setdefault(
            (operation, normalized_feature, u, v), []
        ).append(index)
    for orbit_index, indices in enumerate(gauge_orbits.values()):
        for index in indices[1:]:
            master.addConstr(
                weights[index] == weights[indices[0]],
                name=f"gauge_{orbit_index}_{index}",
            )
    for index, variable in enumerate(weights):
        master.addConstr(variable <= capacity, name=f"singleton_{index}")

    separator = highspy.Highs()
    separator.silent()
    chosen = [separator.addBinary(name=f"z_{index}")
              for index in range(len(vertices))]
    for left, right in edges:
        separator.addConstr(chosen[left] + chosen[right] <= 1)
    separator.setMaximize()

    cuts = []
    for iteration in range(1, maximum_iterations + 1):
        master.run()
        if master.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            return {
                "status": "NO_FRACTIONAL_MARKING",
                "master_status": master.modelStatusToString(
                    master.getModelStatus()
                ),
                "iterations": iteration - 1,
                "vertices": len(vertices),
                "tile_types": len(tile_types),
                "edges": len(edges),
                "cuts": cuts,
            }
        values = master.getSolution().col_value[:len(weights)]
        for index, value in enumerate(values):
            separator.changeColCost(index, value)
        separator.run()
        if separator.getModelStatus() != highspy.HighsModelStatus.kOptimal:
            raise AssertionError("stable-set separator did not solve exactly")
        maximum = separator.getObjectiveValue()
        if maximum <= capacity + 1e-8:
            return {
                "status": "FRACTIONAL_MARKING_FOUND",
                "iterations": iteration - 1,
                "vertices": len(vertices),
                "tile_types": len(tile_types),
                "edges": len(edges),
                "maximum_received_charge": maximum,
                "weights": values,
                "cuts": cuts,
            }
        selected = tuple(
            index for index, value in enumerate(
                separator.getSolution().col_value
            ) if value > 0.5
        )
        master.addConstr(
            sum(weights[index] for index in selected) <= capacity,
            name=f"stable_set_{iteration}",
        )
        cuts.append(selected)
        if iteration <= 20 or iteration % 25 == 0:
            print(
                f"iteration={iteration} max_charge={maximum:.9g} "
                f"stable_set={len(selected)}",
                flush=True,
            )
    return {
        "status": "ITERATION_LIMIT",
        "iterations": maximum_iterations,
        "vertices": len(vertices),
        "tile_types": len(tile_types),
        "edges": len(edges),
        "cuts": cuts,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--radius", type=int, default=1)
    parser.add_argument("--maximum-iterations", type=int, default=1000)
    parser.add_argument("--signed", action="store_true")
    parser.add_argument("--feature-point", nargs=2, type=int)
    args = parser.parse_args()
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    result = solve(
        shape, tuple(payload["base_witnesses"][0]["images"]),
        args.radius, args.maximum_iterations, signed=args.signed,
        feature_point=(tuple(args.feature_point) if args.feature_point else None),
    )
    printable = dict(result)
    if "weights" in printable:
        printable["nonzero_weights"] = sum(
            abs(value) > 1e-9 for value in printable.pop("weights")
        )
    printable["cuts"] = len(printable["cuts"])
    print(json.dumps(printable, indent=1))
    return 0 if result["status"] == "FRACTIONAL_MARKING_FOUND" else 1


if __name__ == "__main__":
    raise SystemExit(main())
