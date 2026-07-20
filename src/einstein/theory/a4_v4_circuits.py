"""Exact affine-circuit elimination for the Layer-D V4 potential system.

Each selected placement asserts equations

``potential[end] XOR potential[start] = constant``

over ``V4 = GF(2)^2``.  A collection is compatible exactly when these edge
labels integrate to a shared vertex potential.  The union-find implementation
below eliminates the potential variables without SAT and returns
deletion-minimal inconsistent placement sets: the affine gluing circuits used
by the T2.D7 density search.
"""

from __future__ import annotations

from dataclasses import dataclass

from einstein.theory.a4_semidirect import c3_action, canonical_a4_semidirect
from einstein.theory.a4_v4_sft import _deck_v4, _signed_coordinate
from einstein.theory.holonomy_csp import quotient_boundary_data


@dataclass(frozen=True)
class V4EquationSystem:
    """Placement-indexed affine equations on quotient vertices."""

    hnf: tuple[int, int, int]
    placements: tuple[tuple[int, int, int], ...]
    vertices: tuple[tuple[int, int, int, int], ...]
    equations: tuple[tuple[tuple[int, int, int], ...], ...]


class _XorUnionFind:
    """Union-find with packed two-bit XOR differences."""

    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size
        self.xor_to_parent = [0] * size

    def find(self, item: int):
        parent = self.parent[item]
        if parent == item:
            return item, 0
        root, prefix = self.find(parent)
        self.xor_to_parent[item] ^= prefix
        self.parent[item] = root
        return root, self.xor_to_parent[item]

    def add(self, left: int, right: int, value: int) -> bool:
        """Add ``potential[right] XOR potential[left] = value``."""
        left_root, left_xor = self.find(left)
        right_root, right_xor = self.find(right)
        if left_root == right_root:
            return (left_xor ^ right_xor) == value
        root_xor = value ^ left_xor ^ right_xor
        if self.rank[left_root] > self.rank[right_root]:
            self.parent[right_root] = left_root
            self.xor_to_parent[right_root] = root_xor
        else:
            self.parent[left_root] = right_root
            self.xor_to_parent[left_root] = root_xor
            if self.rank[left_root] == self.rank[right_root]:
                self.rank[right_root] += 1
        return True


def build_v4_equation_system(shape, hnf, signature_row):
    """Extract the exact packed-V4 equations used by the CNF encoder."""
    hnf = tuple(hnf)
    images = tuple(signature_row["images"])
    twists = tuple(signature_row["twists"])
    model = canonical_a4_semidirect()
    c3_values = tuple(model.coordinate(element).q for element in images)
    geometric = (1, 2, 1, 0, 0, 0)
    if c3_values == geometric:
        c3_sign = 1
    elif c3_values == tuple((-value) % 3 for value in geometric):
        c3_sign = -1
    else:
        raise ValueError("signature does not project to the geometric C3 character")

    instance, vertices, boundaries = quotient_boundary_data(shape, hnf)
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    equations = []
    for edges in boundaries:
        rows = []
        for start, start_deck, end, end_deck, letter in edges:
            label = _signed_coordinate(letter, images)
            q_start = (c3_sign * start[0]) % 3
            displacement = _deck_v4(start_deck, twists) ^ _deck_v4(
                end_deck, twists
            )
            constant = displacement ^ c3_action(q_start, label.v)
            rows.append((vertex_index[start], vertex_index[end], constant))
        equations.append(tuple(rows))
    return V4EquationSystem(
        hnf=hnf,
        placements=tuple(placement for placement, _ in instance.placements),
        vertices=tuple(vertices),
        equations=tuple(equations),
    )


def affine_compatible(system: V4EquationSystem, placement_variables) -> bool:
    """Whether the one-based placement variables share a V4 potential."""
    union = _XorUnionFind(len(system.vertices))
    for variable in placement_variables:
        if not 1 <= variable <= len(system.placements):
            raise ValueError("placement variable out of range")
        for left, right, value in system.equations[variable - 1]:
            if not union.add(left, right, value):
                return False
    return True


def minimal_affine_circuit(system: V4EquationSystem, placement_variables):
    """Return a deterministic deletion-minimal inconsistent subset."""
    core = sorted(set(placement_variables))
    if affine_compatible(system, core):
        return ()
    changed = True
    while changed:
        changed = False
        for variable in tuple(core):
            trial = [item for item in core if item != variable]
            if not affine_compatible(system, trial):
                core = trial
                changed = True
                break
    return tuple(core)


def translate_placement(placement, hnf, shift):
    """Translate one quotient placement and reduce its anchor through HNF."""
    operation, u, v = placement
    a, b, d = hnf
    shift_u, shift_v = shift
    quotient_v, reduced_v = divmod(v + shift_v, d)
    reduced_u = (u + shift_u - quotient_v * b) % a
    return operation, reduced_u, reduced_v


def translation_orbit(system: V4EquationSystem, placement_variables):
    """All distinct translates of a placement set, as variable tuples."""
    lookup = {
        placement: variable
        for variable, placement in enumerate(system.placements, 1)
    }
    out = set()
    a, _, d = system.hnf
    for shift_u in range(a):
        for shift_v in range(d):
            translated = tuple(sorted(
                lookup[translate_placement(
                    system.placements[variable - 1], system.hnf,
                    (shift_u, shift_v),
                )]
                for variable in placement_variables
            ))
            out.add(translated)
    return tuple(sorted(out))


def canonical_translation_circuit(system, placement_variables):
    """Canonical variable tuple for a circuit's quotient-translation orbit."""
    return min(translation_orbit(system, placement_variables))
