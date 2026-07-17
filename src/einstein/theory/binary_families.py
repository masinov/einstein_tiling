"""Compositional binary exact-cover family certificates for W2.C."""

from __future__ import annotations

from einstein.funnel.a1_torus import cell_to_lattice, lattice_to_cell
from einstein.substrate.kitegrid import transform_cell


def lattice_norm2(vector) -> int:
    x, y = vector
    return x * x + x * y + y * y


def hnf_vector_coordinates(hnf, vector) -> tuple[int, int] | None:
    """Coordinates of ``vector`` in HNF generators, or ``None`` if absent."""
    a, b, d = hnf
    x, y = vector
    if a <= 0 or d <= 0 or not 0 <= b < a or y % d:
        return None
    n = y // d
    remainder = x - n * b
    if remainder % a:
        return None
    return remainder // a, n


def quotient_period_obstruction(hnf, excluded_vectors) -> dict | None:
    """Compose a no-period-vector theorem with exact HNF membership."""
    for vector in sorted(excluded_vectors, key=lambda v: (lattice_norm2(v), v)):
        coordinates = hnf_vector_coordinates(hnf, vector)
        if coordinates is not None:
            return {
                "kind": "binary-period-family-obstruction",
                "hnf": list(hnf),
                "quotient_index": hnf[0] * hnf[2],
                "excluded_period": list(vector),
                "period_norm2": lattice_norm2(vector),
                "generator_coefficients": list(coordinates),
                "theorem_dependency": "T1.2-36",
            }
    return None


def verify_quotient_period_obstruction(certificate, max_norm2=36) -> bool:
    """Verify the compositional step, taking T1.2-36 as a theorem dependency."""
    try:
        if (
            certificate["kind"] != "binary-period-family-obstruction"
            or certificate["theorem_dependency"] != "T1.2-36"
        ):
            return False
        hnf = tuple(certificate["hnf"])
        vector = tuple(certificate["excluded_period"])
        coordinates = hnf_vector_coordinates(hnf, vector)
        return (
            coordinates is not None
            and certificate["quotient_index"] == hnf[0] * hnf[2]
            and certificate["period_norm2"] == lattice_norm2(vector)
            and 0 < certificate["period_norm2"] <= max_norm2
            and certificate["generator_coefficients"] == list(coordinates)
        )
    except (KeyError, TypeError, ValueError):
        return False


def lattice_action(op: int) -> tuple[tuple[int, int], tuple[int, int]]:
    """Exact D6 action on center-lattice basis vectors, returned as columns."""
    origin = cell_to_lattice(transform_cell(lattice_to_cell((0, 0, 0)), op))
    columns = []
    for vector in ((1, 0), (0, 1)):
        image = cell_to_lattice(
            transform_cell(lattice_to_cell((vector[0], vector[1], 0)), op)
        )
        columns.append((image[0] - origin[0], image[1] - origin[1]))
    return tuple(columns)


def _apply_action(columns, vector):
    return (
        columns[0][0] * vector[0] + columns[1][0] * vector[1],
        columns[0][1] * vector[0] + columns[1][1] * vector[1],
    )


def _same_index_sublattice(generators, hnf) -> bool:
    """Containment plus equal determinant for two full-rank lattices."""
    determinant = abs(
        generators[0][0] * generators[1][1]
        - generators[0][1] * generators[1][0]
    )
    return (
        determinant == hnf[0] * hnf[2]
        and all(
            hnf_vector_coordinates(hnf, vector) is not None
            for vector in generators
        )
    )


def finalist_thin_family_orbit(index: int) -> tuple[dict, ...]:
    """The three D6-equivalent thin HNF families and explicit symmetry maps."""
    if index < 4:
        raise ValueError("thin-family theorem begins at index 4")
    base_generators = ((1, 0), (0, index))
    targets = (
        (0, (1, 0, index)),
        (8, (index, 0, 1)),
        (2, (index, index - 1, 1)),
    )
    out = []
    for op, hnf in targets:
        action = lattice_action(op)
        images = tuple(_apply_action(action, vector) for vector in base_generators)
        assert _same_index_sublattice(images, hnf)
        out.append({
            "hnf": list(hnf),
            "from_hnf": [1, 0, index],
            "d6_operation": op,
            "action_columns": [list(column) for column in action],
            "mapped_generators": [list(vector) for vector in images],
        })
    return tuple(out)


def verify_finalist_thin_family_orbit(index: int, certificate) -> bool:
    try:
        expected = finalist_thin_family_orbit(index)
        return tuple(certificate) == expected
    except (AssertionError, KeyError, TypeError, ValueError):
        return False
