"""Small exact finite groups used as Layer-D holonomy targets."""

from __future__ import annotations

from dataclasses import dataclass
import itertools


def _perm_compose(left, right):
    return tuple(left[right[index]] for index in range(len(left)))


def _perm_inverse(value):
    out = [0] * len(value)
    for index, image in enumerate(value):
        out[image] = index
    return tuple(out)


def _perm_parity(value):
    inversions = sum(
        value[left] > value[right]
        for left in range(len(value))
        for right in range(left + 1, len(value))
    )
    return inversions % 2


def _permutation_closure(degree, generators):
    identity = tuple(range(degree))
    seen = {identity}
    frontier = [identity]
    generators = tuple(generators) + tuple(_perm_inverse(g) for g in generators)
    while frontier:
        value = frontier.pop()
        for generator in generators:
            product = _perm_compose(value, generator)
            if product not in seen:
                seen.add(product)
                frontier.append(product)
    return tuple(sorted(seen))


@dataclass(frozen=True)
class FiniteGroup:
    name: str
    multiplication: tuple[tuple[int, ...], ...]
    inverses: tuple[int, ...]
    labels: tuple[object, ...]
    identity: int = 0

    @property
    def order(self):
        return len(self.multiplication)

    def conjugate(self, value, conjugator):
        return self.multiplication[
            self.multiplication[conjugator][value]
        ][self.inverses[conjugator]]


def permutation_group(name, elements):
    elements = tuple(sorted(elements))
    degree = len(elements[0])
    identity = tuple(range(degree))
    if elements[0] != identity:
        elements = (identity, *tuple(value for value in elements if value != identity))
    index = {value: position for position, value in enumerate(elements)}
    multiplication = tuple(tuple(
        index[_perm_compose(left, right)] for right in elements
    ) for left in elements)
    inverses = tuple(index[_perm_inverse(value)] for value in elements)
    return FiniteGroup(name, multiplication, inverses, elements)


def symmetric_group(degree):
    return permutation_group(
        f"S{degree}", tuple(itertools.permutations(range(degree)))
    )


def alternating_group(degree):
    return permutation_group(
        f"A{degree}",
        tuple(
            value for value in itertools.permutations(range(degree))
            if _perm_parity(value) == 0
        ),
    )


def dihedral_group_4():
    rotation = (1, 2, 3, 0)
    reflection = (0, 3, 2, 1)
    return permutation_group("D4", _permutation_closure(4, (rotation, reflection)))


def quaternion_group():
    # Elements are sign * basis, with basis 0=1, 1=i, 2=j, 3=k.
    elements = tuple((sign, basis) for sign in (1, -1) for basis in range(4))
    elements = ((1, 0), (-1, 0), (1, 1), (-1, 1),
                (1, 2), (-1, 2), (1, 3), (-1, 3))
    index = {value: position for position, value in enumerate(elements)}
    positive = {
        (0, 0): (1, 0), (0, 1): (1, 1), (0, 2): (1, 2), (0, 3): (1, 3),
        (1, 0): (1, 1), (2, 0): (1, 2), (3, 0): (1, 3),
        (1, 1): (-1, 0), (2, 2): (-1, 0), (3, 3): (-1, 0),
        (1, 2): (1, 3), (2, 3): (1, 1), (3, 1): (1, 2),
        (2, 1): (-1, 3), (3, 2): (-1, 1), (1, 3): (-1, 2),
    }
    multiplication = []
    for left_sign, left_basis in elements:
        row = []
        for right_sign, right_basis in elements:
            sign, basis = positive[(left_basis, right_basis)]
            row.append(index[(left_sign * right_sign * sign, basis)])
        multiplication.append(tuple(row))
    multiplication = tuple(multiplication)
    inverses = []
    for left in range(8):
        inverses.append(next(
            right for right in range(8)
            if multiplication[left][right] == 0 and multiplication[right][left] == 0
        ))
    labels = ("1", "-1", "i", "-i", "j", "-j", "k", "-k")
    return FiniteGroup("Q8", multiplication, tuple(inverses), labels)


SMALL_NONABELIAN_TARGETS = (
    dihedral_group_4,
    quaternion_group,
    lambda: alternating_group(4),
)
