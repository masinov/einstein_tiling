"""Finite planar instances and cold certificates for the V4 Hall conjecture.

The torus is the wrong geometry for Hall neighborhoods because seam
identifications can manufacture deficient sets.  This module builds a finite
*planar* placement universe, learns only translation orbits that fit wholly
inside that universe, and exposes a final SAT check independent of the MIP
used for discovery.
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools

from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Cadical195

from einstein.holonomy.alternating4.circuits import (
    V4EquationSystem,
    affine_compatible,
    build_v4_equation_system,
)
from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED


Placement = tuple[int, int, int]


@dataclass(frozen=True)
class PlanarHallInstance:
    width: int
    height: int
    margin: int
    system: V4EquationSystem
    placements: tuple[Placement, ...]
    global_variables: tuple[int, ...]
    supports: tuple[frozenset[tuple[int, int]], ...]
    centers: tuple[tuple[int, int], ...]
    packing_pairs: tuple[tuple[int, int], ...]
    affine_pairs: tuple[tuple[int, int], ...]

    @property
    def conflicts(self):
        return tuple(sorted(set(self.packing_pairs) | set(self.affine_pairs)))


def build_planar_hall_instance(shape, signature_row, width, height, margin=3):
    """Build an exact seam-free window with one-based local pair conflicts."""
    if width < 1 or height < 1 or margin < 1:
        raise ValueError("window dimensions and margin must be positive")
    ambient_width = width + 2 * margin
    ambient_height = height + 2 * margin
    ambient_width += ambient_width % 2
    ambient_height += ambient_height % 2
    hnf = (ambient_width, 0, ambient_height)
    row = dict(signature_row)
    row["twists"] = list(induced_v4_twists(tuple(row["base_twists"]), hnf))
    system = build_v4_equation_system(shape, hnf, row)
    global_lookup = {
        placement: variable
        for variable, placement in enumerate(system.placements, 1)
    }
    placements = tuple(
        (operation, u, v)
        for operation in range(12)
        for u in range(margin, margin + width)
        for v in range(margin, margin + height)
    )
    global_variables = tuple(global_lookup[p] for p in placements)
    cells = tuple(placement_lattice_cells(shape, placement)
                  for placement in placements)
    supports = tuple(frozenset((u, v) for u, v, _sector in occupied)
                     for occupied in cells)
    if any(len(support) != 4 for support in supports):
        raise ValueError("the planar two-center certificate needs four centers")
    centers = tuple(sorted(set().union(*supports)))
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing_pairs = []
    affine_pairs = []
    for left, right in itertools.combinations(range(len(placements)), 2):
        if (cells[left] & cells[right]
                and canonical_collision_type(cells[left], cells[right]) == target):
            packing_pairs.append((left + 1, right + 1))
        if not affine_compatible(
                system, (global_variables[left], global_variables[right])):
            affine_pairs.append((left + 1, right + 1))
    return PlanarHallInstance(
        width=width,
        height=height,
        margin=margin,
        system=system,
        placements=placements,
        global_variables=global_variables,
        supports=supports,
        centers=centers,
        packing_pairs=tuple(packing_pairs),
        affine_pairs=tuple(affine_pairs),
    )


def local_translation_orbit(instance: PlanarHallInstance, variables):
    """All translates of a local placement set contained in the window."""
    variables = tuple(sorted(set(variables)))
    if not variables:
        raise ValueError("cannot translate an empty placement set")
    lookup = {placement: variable for variable, placement in enumerate(
        instance.placements, 1
    )}
    source = tuple(instance.placements[variable - 1] for variable in variables)
    first = source[0]
    orbit = set()
    for candidate in instance.placements:
        if candidate[0] != first[0]:
            continue
        shift = candidate[1] - first[1], candidate[2] - first[2]
        translated = tuple(sorted(
            lookup.get((operation, u + shift[0], v + shift[1]), -1)
            for operation, u, v in source
        ))
        if -1 not in translated:
            orbit.add(translated)
    return tuple(sorted(orbit))


def build_planar_hall_cnf(instance: PlanarHallInstance, circuits=()):
    """CNF asserting a strict Hall deficiency under supplied circuit cuts."""
    placement_count = len(instance.placements)
    center_variables = {
        center: placement_count + index
        for index, center in enumerate(instance.centers, 1)
    }
    cnf = CNF()
    for left, right in instance.conflicts:
        cnf.append([-left, -right])
    for circuit in circuits:
        cnf.append([-variable for variable in circuit])
    for variable, support in enumerate(instance.supports, 1):
        for center in support:
            cnf.append([-variable, center_variables[center]])
    hall = CardEnc.atleast(
        lits=(list(range(1, placement_count + 1)) * 2
              + [-center_variables[center] for center in instance.centers]),
        bound=len(instance.centers) + 1,
        top_id=max(cnf.nv, placement_count + len(instance.centers)),
        encoding=EncType.cardnetwrk,
    )
    cnf.extend(hall.clauses)
    return cnf


def verify_planar_no_hall_certificate(instance: PlanarHallInstance, result):
    """Cold-check learned affine circuits and the final Hall UNSAT claim."""
    if result.get("status") != "NO_PLANAR_HALL_DEFICIENCY":
        return False
    learned = set()
    placement_lookup = {placement: variable for variable, placement in enumerate(
        instance.placements, 1
    )}
    for row in result.get("learned_orbits", ()):
        try:
            representative = tuple(sorted(
                placement_lookup[tuple(placement)]
                for placement in row["placements"]
            ))
        except (KeyError, TypeError):
            return False
        global_core = tuple(instance.global_variables[variable - 1]
                            for variable in representative)
        if affine_compatible(instance.system, global_core):
            return False
        orbit = local_translation_orbit(instance, representative)
        if row.get("orbit_size") != len(orbit):
            return False
        learned.update(orbit)
    if result.get("learned_clauses") != len(learned):
        return False
    cnf = build_planar_hall_cnf(instance, sorted(learned))
    with Cadical195(bootstrap_with=cnf) as solver:
        return not solver.solve()

