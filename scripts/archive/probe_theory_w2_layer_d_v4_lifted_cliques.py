#!/usr/bin/env python
"""Inspect maximal cliques of the explicit-gauge V4 conflict graph."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import time

import networkx as nx

from einstein.e1_candidates import decode_compiled_key
from einstein.theory.a4_v4_circuits import build_v4_equation_system
from einstein.theory.a4_v4_lift import induced_v4_twists
from einstein.theory.a4_v4_marking import lifted_state_conflict_graph


ROOT = Path(__file__).resolve().parents[2]
KEY = "010001010104010502f002f1030b030c04fa04fb"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hnf", nargs=3, type=int, default=(2, 0, 2))
    parser.add_argument("--maximum-cliques", type=int, default=1000000)
    args = parser.parse_args()
    hnf = tuple(args.hnf)
    shape = decode_compiled_key(KEY)
    payload = json.loads((
        ROOT / "docs/notebook/assets/theory-w2-layer-d-v4-2lambda.json"
    ).read_text())
    row = dict(payload["base_witnesses"][0])
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    nodes, edges = lifted_state_conflict_graph(shape, system)
    graph = nx.Graph()
    graph.add_nodes_from(range(len(nodes)))
    graph.add_edges_from(edges)
    print(
        f"hnf={hnf} nodes={len(nodes)} edges={len(edges)} "
        f"density={nx.density(graph):.6f}",
        flush=True,
    )
    counts = Counter()
    largest = []
    started = time.monotonic()
    for index, clique in enumerate(nx.find_cliques(graph), 1):
        counts[len(clique)] += 1
        if len(clique) > len(largest):
            largest = clique
        if index % 100000 == 0:
            print(
                f"cliques={index} largest={len(largest)} "
                f"seconds={time.monotonic() - started:.1f}",
                flush=True,
            )
        if index >= args.maximum_cliques:
            break
    print(f"maximal clique counts={dict(sorted(counts.items()))}")
    print(f"largest={len(largest)} {[nodes[index] for index in largest]}")


if __name__ == "__main__":
    main()
