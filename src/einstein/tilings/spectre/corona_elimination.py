"""Exact physical-ring elimination for the Spectre D1 entry obligation.

The computation is deliberately ancestry blind.  Its only states are finite
patches of congruent straight Spectres, and its only transition covers every
currently exposed unit edge by a nonoverlapping next ring.  Consequently an
empty finite frontier excludes the rooted corona from every whole-plane
edge-to-edge tiling.
"""

from __future__ import annotations

from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
import json
import multiprocessing
import os
from typing import Callable, Sequence

from einstein.geometry.cyclotomic import Pose
from einstein.tilings.spectre.patches import (
    IDENTITY,
    enumerate_first_coronas,
    extend_complete_ring,
    pose_json,
)


EXTRA_CORONA_INDICES = (33, 44, 155)
Frontier = tuple[tuple[int, tuple[Pose, ...]], ...]


def frontier_digest(frontier: Frontier) -> str:
    digest = sha256()
    for corona_index, patch in sorted(frontier):
        digest.update(str(corona_index).encode())
        digest.update(b":")
        digest.update(json.dumps(
            [pose_json(pose) for pose in sorted(patch)],
            separators=(",", ":"),
        ).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def initial_frontier(
    extra_indices: Sequence[int] = EXTRA_CORONA_INDICES,
) -> Frontier:
    coronas = enumerate_first_coronas()
    return tuple(
        (index, tuple(sorted((IDENTITY, *coronas[index]))))
        for index in extra_indices
    )


def advance_patch(item):
    """Enumerate every exact complete next ring for one rooted patch."""
    corona_index, patch = item
    extension = extend_complete_ring(patch, 1_000_000)
    children = tuple(
        tuple(sorted((*patch, *ring))) for ring in extension.solutions
    )
    return (
        corona_index,
        len(children),
        extension.candidates,
        extension.sat_calls,
        children,
    )


def advance_frontier(
    frontier: Frontier,
    radius: int,
    workers: int | None = None,
    advance: Callable = advance_patch,
):
    """Advance one complete physical ring and return frontier plus census."""
    workers = workers or min(24, os.cpu_count() or 4)
    next_frontier = []
    branch_counts = Counter()
    solution_histogram = Counter()
    candidate_histogram = Counter()
    sat_calls = 0
    dead_inputs = 0
    context = multiprocessing.get_context("fork")
    with ProcessPoolExecutor(
        max_workers=workers, mp_context=context,
    ) as executor:
        for corona, count, candidates, calls, children in executor.map(
            advance, frontier, chunksize=1,
        ):
            branch_counts[corona] += count
            solution_histogram[count] += 1
            candidate_histogram[candidates] += 1
            sat_calls += calls
            dead_inputs += count == 0
            next_frontier.extend((corona, child) for child in children)
    unique = set(next_frontier)
    if len(unique) != len(next_frontier):
        raise ValueError(
            f"duplicate radius-{radius} patches: "
            f"{len(next_frontier) - len(unique)}"
        )
    result = tuple(sorted(unique))
    roots = sorted({root for root, _ in frontier} | set(EXTRA_CORONA_INDICES))
    summary = {
        "radius": radius,
        "input_patches": len(frontier),
        "dead_input_patches": dead_inputs,
        "surviving_patches": len(result),
        "survivors_by_root_corona": {
            str(root): branch_counts[root] for root in roots
        },
        "solutions_per_input_histogram": {
            str(key): value for key, value in sorted(solution_histogram.items())
        },
        "candidate_count_histogram": {
            str(key): value for key, value in sorted(candidate_histogram.items())
        },
        "sat_calls": sat_calls,
        "frontier_sha256": frontier_digest(result),
    }
    return result, summary


def analyze_d1_entry(
    target_radius: int = 5,
    workers: int | None = None,
    callback: Callable[[int, Frontier, dict], None] | None = None,
):
    """Exhaust all three non-L18 corona branches through ``target_radius``."""
    if target_radius < 2:
        raise ValueError("target_radius must be at least two")
    frontier = initial_frontier()
    records = []
    for radius in range(2, target_radius + 1):
        frontier, summary = advance_frontier(
            frontier, radius, workers=workers,
        )
        records.append(summary)
        if callback is not None:
            callback(radius, frontier, summary)
        if not frontier:
            break
    return {
        "extra_corona_indices": list(EXTRA_CORONA_INDICES),
        "initial_frontier_patches": len(EXTRA_CORONA_INDICES),
        "radius_records": records,
        "decisive_radius": (
            records[-1]["radius"] if records and not frontier else None
        ),
        "final_frontier_patches": len(frontier),
        "all_extra_coronas_eliminated": not frontier,
    }
