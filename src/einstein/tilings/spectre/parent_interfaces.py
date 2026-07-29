"""Finite overlap consistency for contracted Spectre parent coronas."""

from __future__ import annotations

from typing import Sequence

from einstein.geometry.cyclotomic import Pose, inverse_pose, relative_pose


ParentCorona = tuple[Pose, ...]


def reciprocal_domains(states: Sequence[ParentCorona], state_index: int):
    """Allowed neighbor-state indices on each directed corona edge."""
    state = states[state_index]
    return tuple(
        tuple(index for index, candidate in enumerate(states)
              if inverse_pose(edge) in candidate)
        for edge in state
    )


def local_overlap_witnesses(
    states: Sequence[ParentCorona], state_index: int, limit: int = 2,
):
    """Assign neighbor coronas with reciprocal and triangle agreement.

    Every neighbor must contain its edge back to the center. For each pair of
    center-neighbors, either both assigned coronas say that pair is adjacent,
    or neither does. This is the complete constraint visible from the
    uncolored radius-one parent-anchor coronas alone.
    """
    if limit < 1:
        raise ValueError("limit must be positive")
    centers = states[state_index]
    domains = reciprocal_domains(states, state_index)
    pair_compatibility = {}
    for left in range(len(centers)):
        for right in range(left):
            lr = relative_pose(centers[left], centers[right])
            rl = relative_pose(centers[right], centers[left])
            pair_compatibility[left, right] = {
                (a, b)
                for a in domains[left]
                for b in domains[right]
                if (lr in states[a]) == (rl in states[b])
            }

    order = tuple(sorted(range(len(centers)), key=lambda i: len(domains[i])))
    assignment = {}
    witnesses = []

    def search(depth):
        if len(witnesses) >= limit:
            return
        if depth == len(order):
            witnesses.append(tuple(assignment[i] for i in range(len(centers))))
            return
        current = order[depth]
        for candidate in domains[current]:
            valid = True
            for other, selected in assignment.items():
                if current > other:
                    pair = current, other
                    values = candidate, selected
                else:
                    pair = other, current
                    values = selected, candidate
                if values not in pair_compatibility[pair]:
                    valid = False
                    break
            if valid:
                assignment[current] = candidate
                search(depth + 1)
                del assignment[current]

    search(0)
    return tuple(witnesses)


def prune_locally_unsupported(states: Sequence[ParentCorona]):
    """Iterate reciprocal/triangle support deletion to a fixed point."""
    alive = set(range(len(states)))
    rounds = []
    while True:
        removed = []
        for index in sorted(alive):
            witnesses = local_overlap_witnesses(states, index, limit=1000)
            if not any(all(neighbor in alive for neighbor in witness)
                       for witness in witnesses):
                removed.append(index)
        if not removed:
            break
        alive.difference_update(removed)
        rounds.append(tuple(removed))
    return tuple(sorted(alive)), tuple(rounds)
