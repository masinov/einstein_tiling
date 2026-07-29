"""Translation-orbit hypergraphs and LP probes for affine V4 circuits."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import itertools

from einstein.holonomy.alternating4.circuits import (
    V4EquationSystem,
    affine_compatible,
    canonical_translation_circuit,
    translation_orbit,
)
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED
from einstein.holonomy.constraints import quotient_boundary_data


@dataclass(frozen=True)
class CircuitOrbit:
    """One quotient-translation orbit of forbidden placement sets."""

    kind: str
    representative: tuple[int, ...]
    translates: tuple[tuple[int, ...], ...]

    @property
    def circuit_size(self):
        return len(self.representative)


def make_circuit_orbit(system, placement_variables, kind="affine"):
    representative = canonical_translation_circuit(system, placement_variables)
    return CircuitOrbit(
        kind=kind,
        representative=representative,
        translates=translation_orbit(system, representative),
    )


def packing_circuit_orbits(shape, system):
    """The T2.D6 collision clauses grouped by quotient translation."""
    instance, _, _ = quotient_boundary_data(shape, system.hnf)
    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    clauses = collision_orbit_clauses(shape, system.hnf, instance, target)
    representatives = {
        canonical_translation_circuit(
            system, tuple(sorted(-literal for literal in clause))
        )
        for clause in clauses
    }
    return tuple(
        make_circuit_orbit(system, representative, kind="packing")
        for representative in sorted(representatives)
    )


def affine_pair_circuit_orbits(system):
    """All minimal affine circuits of size two, modulo translation."""
    representatives = set()
    for left, right in itertools.combinations(
        range(1, len(system.placements) + 1), 2
    ):
        pair = (left, right)
        if not affine_compatible(system, pair):
            representatives.add(canonical_translation_circuit(system, pair))
    return tuple(
        make_circuit_orbit(system, representative)
        for representative in sorted(representatives)
    )


def orbit_operation_coefficients(system, orbit):
    """Coefficient of each placement operation after summing the orbit."""
    k = system.hnf[0] * system.hnf[2]
    totals = [0] * 12
    for circuit in orbit.translates:
        for variable in circuit:
            totals[system.placements[variable - 1][0]] += 1
    if any(total % k for total in totals):
        raise AssertionError("translation orbit is not uniform by anchor")
    return tuple(total // k for total in totals)


def orbit_clause_rhs_per_center(system, orbit):
    """RHS density of the summed no-good clauses for one orbit."""
    k = system.hnf[0] * system.hnf[2]
    return Fraction(
        len(orbit.translates) * (orbit.circuit_size - 1), k
    )


def solve_orbit_clause_dual(system, orbits):
    """Minimize a weighted sum of translated circuit no-good inequalities.

    This floating-point LP is a discovery probe.  Returned nonzero weights are
    rationalized separately before they can become certificate data.
    """
    import highspy

    orbits = tuple(orbits)
    highs = highspy.Highs()
    highs.silent()
    variables = []
    coefficients = []
    costs = []
    for index, orbit in enumerate(orbits):
        coefficient = orbit_operation_coefficients(system, orbit)
        cost = float(orbit_clause_rhs_per_center(system, orbit))
        variables.append(highs.addVariable(
            lb=0.0, obj=cost, name=f"orbit_{index}"
        ))
        coefficients.append(coefficient)
        costs.append(cost)
    for operation in range(12):
        expression = highs.expr()
        for variable, coefficient in zip(variables, coefficients):
            if coefficient[operation]:
                expression += coefficient[operation] * variable
        highs.addConstr(expression >= 1.0, name=f"operation_{operation}")
    highs.minimize()
    status = highs.getModelStatus()
    solution = highs.getSolution()
    weights = tuple(solution.col_value)
    return {
        "model_status": highs.modelStatusToString(status),
        "objective": highs.getObjectiveValue(),
        "weights": weights,
        "nonzero": tuple(
            (index, weight) for index, weight in enumerate(weights)
            if abs(weight) > 1e-9
        ),
        "operation_activity": tuple(
            sum(coefficients[index][operation] * weights[index]
                for index in range(len(orbits)))
            for operation in range(12)
        ),
        "row_dual": tuple(solution.row_dual),
        "costs": tuple(costs),
    }
