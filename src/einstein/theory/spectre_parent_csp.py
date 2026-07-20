"""Pinned finite CSPs over exact colored Spectre parent states."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Mapping, Sequence

from pysat.solvers import Cadical195

from einstein.substrate.module12 import Pose, compose_pose, relative_pose
from einstein.theory.spectre_colored_interface import (
    ColoredCorona, colored_states_agree_at_relative,
)
from einstein.theory.spectre_patch_language import IDENTITY, poses_overlap


@dataclass(frozen=True)
class RadiusTwoProblem:
    root_state: int
    root_witness: tuple[int, ...]
    positions: tuple[Pose, ...]
    first_ring: tuple[Pose, ...]
    second_ring: tuple[Pose, ...]
    domains: tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class RadiusTwoResult:
    satisfiable: bool
    minimum_outer_extras: int | None
    minimum_nonroot_extras: int | None
    assignment: tuple[int, ...] | None
    search_nodes: int
    constraint_arcs: int


@dataclass(frozen=True)
class VariableRingResult:
    satisfiable: bool
    rings: int
    positions: int
    optional_positions: int
    assignment: tuple[tuple[Pose, int], ...] | None
    clauses: int


class ParentStateKernel:
    """Compatibility kernel for one fixed colored-state alphabet."""

    def __init__(self, states: Sequence[ColoredCorona], templates):
        self.states = tuple(states)
        self.full, self.missing = map(tuple, templates)
        self._compatibility = {}

    def support(self, relative: Pose, state_index: int):
        template = (
            self.full if self.states[state_index][0] == "full"
            else self.missing
        )
        return tuple(compose_pose(relative, child) for child in template)

    def compatible(self, relative: Pose, left: int, right: int) -> bool:
        """Colored-corona agreement plus exact physical support disjointness."""
        key = relative, left, right
        if key not in self._compatibility:
            agrees = colored_states_agree_at_relative(
                self.states, left, right, relative,
            )
            if agrees:
                left_support = self.support(IDENTITY, left)
                right_support = self.support(relative, right)
                agrees = not any(
                    poses_overlap(a, b)
                    for a in left_support for b in right_support
                )
            self._compatibility[key] = agrees
        return self._compatibility[key]

    def build_radius_two(
        self, root_state: int, root_witness: Sequence[int],
    ) -> RadiusTwoProblem:
        root_neighbors = self.states[root_state][1]
        if len(root_witness) != len(root_neighbors):
            raise ValueError("root witness has the wrong arity")
        fixed = {IDENTITY: root_state}
        first = []
        for neighbor, state_index in zip(root_neighbors, root_witness):
            position = compose_pose(IDENTITY, neighbor[0])
            if position in fixed and fixed[position] != state_index:
                raise ValueError("root witness assigns one anchor twice")
            fixed[position] = state_index
            first.append(position)
        first_set = set(first)
        positions = set(fixed)
        for center in first:
            state_index = fixed[center]
            for relative, _, _ in self.states[state_index][1]:
                positions.add(compose_pose(center, relative))
        second = positions - first_set - {IDENTITY}
        ordered = tuple(sorted(positions))
        all_states = tuple(range(len(self.states)))
        return RadiusTwoProblem(
            root_state=root_state,
            root_witness=tuple(root_witness),
            positions=ordered,
            first_ring=tuple(sorted(first_set)),
            second_ring=tuple(sorted(second)),
            domains=tuple(
                (fixed[position],) if position in fixed else all_states
                for position in ordered
            ),
        )

    def extend_fixed_assignment(
        self, problem: RadiusTwoProblem, assignment: Sequence[int],
    ) -> RadiusTwoProblem:
        """Add one ring named by the current outer-ring state assignment."""
        if len(assignment) != len(problem.positions):
            raise ValueError("assignment has the wrong size")
        fixed = dict(zip(problem.positions, assignment))
        old_positions = set(problem.positions)
        positions = set(old_positions)
        for center in problem.second_ring:
            state_index = fixed[center]
            for relative, _, _ in self.states[state_index][1]:
                positions.add(compose_pose(center, relative))
        outer = positions - old_positions
        ordered = tuple(sorted(positions))
        all_states = tuple(range(len(self.states)))
        return RadiusTwoProblem(
            root_state=problem.root_state,
            root_witness=problem.root_witness,
            positions=ordered,
            first_ring=tuple(sorted(old_positions - {IDENTITY})),
            second_ring=tuple(sorted(outer)),
            domains=tuple(
                (fixed[position],) if position in fixed else all_states
                for position in ordered
            ),
        )

    def enumerate_assignments(
        self, problem: RadiusTwoProblem, limit: int | None = None,
    ):
        """Enumerate complete assignments with an independent SAT encoding."""
        if limit is not None and limit < 1:
            raise ValueError("limit must be positive")
        variables = {}
        clauses = []
        next_variable = 1
        for position, domain in enumerate(problem.domains):
            row = []
            for state in domain:
                variables[position, state] = next_variable
                row.append(next_variable)
                next_variable += 1
            clauses.append(row)
            for offset, variable in enumerate(row):
                for other in row[:offset]:
                    clauses.append([-variable, -other])
        for left in range(len(problem.positions)):
            for right in range(left):
                relative = relative_pose(
                    problem.positions[left], problem.positions[right],
                )
                for a in problem.domains[left]:
                    for b in problem.domains[right]:
                        if not self.compatible(relative, a, b):
                            clauses.append([
                                -variables[left, a], -variables[right, b],
                            ])
        assignments = []
        with Cadical195(bootstrap_with=clauses) as solver:
            while (limit is None or len(assignments) < limit) and solver.solve():
                positive = {
                    literal for literal in solver.get_model() if literal > 0
                }
                assignment = tuple(
                    next(
                        state for state in problem.domains[position]
                        if variables[position, state] in positive
                    )
                    for position in range(len(problem.positions))
                )
                assignments.append(assignment)
                solver.add_clause([
                    -variables[position, state]
                    for position, state in enumerate(assignment)
                ])
        return tuple(assignments)

    def extend_variable_outer_ring(
        self, problem: RadiusTwoProblem, rings: int = 1,
    ) -> VariableRingResult:
        """Test further state rings without enumerating inner assignments.

        The states on ``problem.second_ring`` are not fixed.  For each of
        their possible values we add every neighbor position that value could
        demand, make those new positions optional, and use implications to
        activate precisely the required ones.  This is existentially exact
        for ``rings`` additional rings; unlike :meth:`extend_fixed_assignment`, it
        cannot accidentally discard a viable inner assignment by choosing a
        different SAT model first.
        """
        if rings < 1:
            raise ValueError("rings must be positive")
        mandatory = set(problem.positions)
        old_domain = dict(zip(problem.positions, problem.domains))
        possible = set(mandatory)
        frontier = set(problem.second_ring)
        expanded_centers = set()
        all_states = tuple(range(len(self.states)))
        for _ in range(rings):
            expanded_centers.update(frontier)
            new_frontier = set()
            for center in frontier:
                for state in old_domain.get(center, all_states):
                    for relative, _, _ in self.states[state][1]:
                        neighbor = compose_pose(center, relative)
                        if neighbor not in possible:
                            possible.add(neighbor)
                            new_frontier.add(neighbor)
            frontier = new_frontier
        positions = tuple(sorted(possible))
        index = {pose: offset for offset, pose in enumerate(positions)}
        domains = tuple(
            old_domain.get(position, all_states) for position in positions
        )

        variables = {}
        clauses = []
        next_variable = 1
        for offset, domain in enumerate(domains):
            row = []
            for state in domain:
                variables[offset, state] = next_variable
                row.append(next_variable)
                next_variable += 1
            if positions[offset] in mandatory:
                clauses.append(row)
            for right_index, variable in enumerate(row):
                for other in row[:right_index]:
                    clauses.append([-variable, -other])

        # Any two occupied anchors must agree on their colored adjacency and
        # have disjoint physical 8/9-tile supports.
        for left in range(len(positions)):
            for right in range(left):
                relative = relative_pose(positions[left], positions[right])
                for a in domains[left]:
                    for b in domains[right]:
                        if not self.compatible(relative, a, b):
                            clauses.append([
                                -variables[left, a], -variables[right, b],
                            ])

        # A chosen frontier state demands an occupied, compatible state at
        # each of its six named neighbors.  New third-ring states are boundary
        # variables, so their own outward neighbors are deliberately deferred.
        for center in expanded_centers:
            center_index = index[center]
            for state in domains[center_index]:
                source = variables[center_index, state]
                for relative, _, _ in self.states[state][1]:
                    neighbor = compose_pose(center, relative)
                    neighbor_index = index[neighbor]
                    allowed = [
                        variables[neighbor_index, candidate]
                        for candidate in domains[neighbor_index]
                        if self.compatible(relative, state, candidate)
                    ]
                    clauses.append([-source, *allowed])

        with Cadical195(bootstrap_with=clauses) as solver:
            if not solver.solve():
                return VariableRingResult(
                    False, rings, len(positions), len(possible - mandatory), None,
                    len(clauses),
                )
            positive = {
                literal for literal in solver.get_model() if literal > 0
            }
        assignment = tuple(
            (position, state)
            for offset, position in enumerate(positions)
            for state in domains[offset]
            if variables[offset, state] in positive
        )
        return VariableRingResult(
            True, rings, len(positions), len(possible - mandatory), assignment,
            len(clauses),
        )

    def solve_radius_two(
        self, problem: RadiusTwoProblem, extra_states: set[int],
    ) -> RadiusTwoResult:
        positions = problem.positions
        domains = [set(domain) for domain in problem.domains]
        index = {position: i for i, position in enumerate(positions)}
        outer = {index[position] for position in problem.second_ring}
        nonroot = set(range(len(positions))) - {index[IDENTITY]}
        allowed = {}
        neighbors = {i: set() for i in range(len(positions))}
        all_pairs = len(self.states) ** 2
        for left in range(len(positions)):
            for right in range(left):
                lr = relative_pose(positions[left], positions[right])
                pairs = {
                    (a, b)
                    for a in domains[left]
                    for b in domains[right]
                    if self.compatible(lr, a, b)
                }
                if len(pairs) == all_pairs:
                    continue
                allowed[left, right] = pairs
                allowed[right, left] = {(b, a) for a, b in pairs}
                neighbors[left].add(right)
                neighbors[right].add(left)

        def propagate(current, initial=None):
            queue = deque(
                (left, right)
                for left in range(len(positions))
                for right in neighbors[left]
            ) if initial is None else deque(initial)
            while queue:
                left, right = queue.popleft()
                relation = allowed[left, right]
                keep = {
                    value for value in current[left]
                    if any((value, other) in relation
                           for other in current[right])
                }
                if keep == current[left]:
                    continue
                if not keep:
                    return False
                current[left] = keep
                queue.extend(
                    (other, left) for other in neighbors[left]
                    if other != right
                )
            return True

        if not propagate(domains):
            return RadiusTwoResult(False, None, None, None, 1, len(allowed))

        best_objective = None
        best_assignment = None
        nodes = 0

        def lower_bound(current, selected):
            return sum(
                min(int(value in extra_states) for value in current[position])
                for position in selected
            )

        def search(current):
            nonlocal best_objective, best_assignment, nodes
            nodes += 1
            bound = (
                lower_bound(current, outer),
                lower_bound(current, nonroot),
            )
            if best_objective is not None and bound >= best_objective:
                return
            undecided = [
                position for position, domain in enumerate(current)
                if len(domain) > 1
            ]
            if not undecided:
                best_objective = bound
                best_assignment = tuple(next(iter(domain)) for domain in current)
                return
            chosen = min(
                undecided,
                key=lambda position: (
                    len(current[position]),
                    position not in outer,
                    -len(neighbors[position]),
                ),
            )
            for value in sorted(
                current[chosen], key=lambda item: (item in extra_states, item),
            ):
                branch = [set(domain) for domain in current]
                branch[chosen] = {value}
                if propagate(
                    branch,
                    ((other, chosen) for other in neighbors[chosen]),
                ):
                    search(branch)

        search(domains)
        if best_assignment is None:
            return RadiusTwoResult(False, None, None, None, nodes, len(allowed))
        return RadiusTwoResult(
            True, best_objective[0], best_objective[1], best_assignment,
            nodes, len(allowed),
        )
