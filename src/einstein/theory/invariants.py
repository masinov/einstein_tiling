"""Exact W2 algebraic necessary conditions for periodic quotient tilings."""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
import itertools
import math

from einstein.funnel.a1_torus import TorusInstance, cell_to_lattice
from einstein.substrate.kitegrid import N_OPS, transform_cell


def required_index_modulus(tile_cells: int, substrate_cells: int = 6) -> int:
    """Smallest positive ``m`` such that area permits exactly indices m*Z."""
    if tile_cells <= 0 or substrate_cells <= 0:
        raise ValueError("cell counts must be positive")
    return tile_cells // math.gcd(tile_cells, substrate_cells)


def area_allows_index(tile_cells: int, quotient_index: int) -> bool:
    """Whether tile area divides the quotient's ``6*index`` kite cells."""
    return quotient_index > 0 and (6 * quotient_index) % tile_cells == 0


def area_obstruction(tile_cells: int, quotient_index: int) -> dict | None:
    """Return a compact exact divisibility witness, or ``None`` if admissible."""
    if quotient_index <= 0:
        raise ValueError("quotient index must be positive")
    remainder = (6 * quotient_index) % tile_cells
    if remainder == 0:
        return None
    return {
        "kind": "area-congruence-obstruction",
        "tile_cells": tile_cells,
        "quotient_index": quotient_index,
        "quotient_cells": 6 * quotient_index,
        "required_index_modulus": required_index_modulus(tile_cells),
        "remainder": remainder,
    }


def verify_area_obstruction(certificate: dict) -> bool:
    try:
        n = certificate["tile_cells"]
        k = certificate["quotient_index"]
        return (
            certificate["kind"] == "area-congruence-obstruction"
            and n > 0
            and k > 0
            and certificate["quotient_cells"] == 6 * k
            and certificate["required_index_modulus"]
            == required_index_modulus(n)
            and certificate["remainder"] == (6 * k) % n
            and certificate["remainder"] != 0
        )
    except (KeyError, TypeError, ValueError):
        return False


@lru_cache(maxsize=None)
def orientation_profiles(shape: tuple) -> tuple[tuple[int, ...], ...]:
    """Distinct sector-count vectors of every allowed D6 tile orientation."""
    profiles = set()
    for op in range(N_OPS):
        counts = [0] * 6
        for cell in shape:
            sector = cell_to_lattice(transform_cell(cell, op))[2]
            counts[sector] += 1
        profiles.add(tuple(counts))
    return tuple(sorted(profiles))


def _nullspace_mod_prime(rows, prime):
    """Basis for the right nullspace of ``rows`` over F_prime."""
    matrix = [[value % prime for value in row] for row in rows]
    rank = 0
    pivots = []
    width = len(matrix[0]) if matrix else 6
    for column in range(width):
        pivot = next(
            (row for row in range(rank, len(matrix)) if matrix[row][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        inverse = pow(matrix[rank][column], -1, prime)
        matrix[rank] = [(value * inverse) % prime for value in matrix[rank]]
        for row in range(len(matrix)):
            if row == rank or not matrix[row][column]:
                continue
            factor = matrix[row][column]
            matrix[row] = [
                (a - factor * b) % prime
                for a, b in zip(matrix[row], matrix[rank])
            ]
        pivots.append(column)
        rank += 1
    free = [column for column in range(width) if column not in pivots]
    basis = []
    for free_column in free:
        vector = [0] * width
        vector[free_column] = 1
        for row, pivot_column in enumerate(pivots):
            vector[pivot_column] = -matrix[row][free_column] % prime
        basis.append(tuple(vector))
    return tuple(basis)


def prime_sector_obstruction(
    shape,
    quotient_index: int,
    primes=(2, 3, 5, 7, 11, 13),
) -> dict | None:
    """Find a sector-coloring obstruction over a small prime field.

    A weight vector ``w`` annihilating every oriented tile profile must also
    annihilate the quotient target ``index*(1,1,1,1,1,1)``. A nonzero target
    residue is therefore an exact impossibility witness.
    """
    if quotient_index <= 0:
        raise ValueError("quotient index must be positive")
    shape = tuple(tuple(cell) for cell in shape)
    profiles = orientation_profiles(shape)
    for prime in primes:
        if prime < 2 or any(prime % d == 0 for d in range(2, math.isqrt(prime) + 1)):
            raise ValueError("moduli must be prime")
        for weights in _nullspace_mod_prime(profiles, prime):
            target = quotient_index * sum(weights) % prime
            if target:
                return {
                    "kind": "prime-sector-coloring-obstruction",
                    "modulus": prime,
                    "weights": list(weights),
                    "quotient_index": quotient_index,
                    "target_residue": target,
                    "orientation_profiles": [list(row) for row in profiles],
                }
    return None


def verify_prime_sector_obstruction(shape, certificate: dict) -> bool:
    try:
        if certificate["kind"] != "prime-sector-coloring-obstruction":
            return False
        prime = certificate["modulus"]
        weights = tuple(certificate["weights"])
        index = certificate["quotient_index"]
        profiles = orientation_profiles(tuple(tuple(cell) for cell in shape))
        return (
            len(weights) == 6
            and certificate["orientation_profiles"] == [list(row) for row in profiles]
            and all(
                sum(a * b for a, b in zip(profile, weights)) % prime == 0
                for profile in profiles
            )
            and certificate["target_residue"]
            == index * sum(weights) % prime
            and certificate["target_residue"] != 0
        )
    except (KeyError, TypeError, ValueError):
        return False


def _gf2_null_witness(rows, width):
    """Return an odd-weight vector orthogonal to every bit-row, if one exists."""
    # Reduced row basis, keyed by pivot bit. New rows are reduced by every
    # existing pivot before insertion; the new pivot is then cleared from all
    # older rows. The result is RREF over F2.
    basis = {}
    for raw in rows:
        row = raw
        for pivot in sorted(basis, reverse=True):
            if (row >> pivot) & 1:
                row ^= basis[pivot]
        if not row:
            continue
        pivot = row.bit_length() - 1
        basis[pivot] = row
        for other in list(basis):
            if other != pivot and (basis[other] >> pivot) & 1:
                basis[other] ^= row

    pivots = set(basis)
    for free in range(width):
        if free in pivots:
            continue
        witness = 1 << free
        for pivot, row in basis.items():
            if (row >> free) & 1:
                witness |= 1 << pivot
        if witness.bit_count() & 1:
            # Internal assertion catches any future elimination regression
            # before a purported certificate can escape.
            assert all(not ((row & witness).bit_count() & 1) for row in rows)
            return witness, len(basis)
    return None, len(basis)


def gf2_cokernel_obstruction(shape, hnf) -> dict | None:
    """Full-quotient mod-2 incidence-cokernel witness.

    If a bit vector is orthogonal to every placement column but has odd dot
    product with the all-ones target, then ``M x = 1`` is impossible even over
    F2, hence impossible over the integers and for 0/1 exact covers.
    """
    shape = tuple(tuple(cell) for cell in shape)
    hnf = tuple(hnf)
    instance = TorusInstance(shape, hnf)
    rows = [mask for _, mask in instance.placements]
    witness, rank = _gf2_null_witness(rows, instance.n_cells)
    if witness is None:
        return None
    support = [bit for bit in range(instance.n_cells) if (witness >> bit) & 1]
    return {
        "kind": "gf2-incidence-cokernel-obstruction",
        "hnf": list(hnf),
        "quotient_index": hnf[0] * hnf[2],
        "n_cells": instance.n_cells,
        "n_placements": len(instance.placements),
        "incidence_rank_mod2": rank,
        "weight_support": support,
        "target_residue": len(support) % 2,
    }


def verify_gf2_cokernel_obstruction(shape, certificate: dict) -> bool:
    """Independently check the compact modular cokernel witness."""
    try:
        if certificate["kind"] != "gf2-incidence-cokernel-obstruction":
            return False
        hnf = tuple(certificate["hnf"])
        instance = TorusInstance(tuple(tuple(cell) for cell in shape), hnf)
        support = certificate["weight_support"]
        if (
            support != sorted(set(support))
            or any(not 0 <= bit < instance.n_cells for bit in support)
        ):
            return False
        witness = sum(1 << bit for bit in support)
        return (
            certificate["quotient_index"] == hnf[0] * hnf[2]
            and certificate["n_cells"] == instance.n_cells
            and certificate["n_placements"] == len(instance.placements)
            and certificate["target_residue"] == len(support) % 2 == 1
            and all(
                not ((mask & witness).bit_count() & 1)
                for _, mask in instance.placements
            )
        )
    except (KeyError, TypeError, ValueError):
        return False


def _smith_signature(rows, backend="flint") -> dict:
    """Rank and top determinantal divisor of an integer row matrix.

    SymPy's public Smith-form API returns the diagonal form (not the
    transformation matrices).  The nonzero diagonal entries nevertheless
    determine precisely the two quantities needed for lattice membership.
    """
    if backend == "flint":
        from flint import fmpz_mat

        diagonal = fmpz_mat(rows).snf()
        height, width = diagonal.nrows(), diagonal.ncols()
    elif backend == "sympy":
        from sympy import Matrix, ZZ
        from sympy.matrices.normalforms import smith_normal_form

        diagonal = smith_normal_form(Matrix(rows), domain=ZZ)
        height, width = diagonal.rows, diagonal.cols
    else:
        raise ValueError(f"unknown Smith backend: {backend}")
    factors = [
        abs(int(diagonal[i, i]))
        for i in range(min(height, width))
        if diagonal[i, i] != 0
    ]
    return {
        "rank": len(factors),
        "invariant_factors": factors,
        "determinantal_divisor": math.prod(factors),
    }


def integer_lattice_membership(rows, target, backend="flint") -> dict:
    """Decide whether ``target`` is in the integer column lattice of ``rows``.

    Let ``L`` be the column lattice of M and ``L' = L + Z target``.  If their
    ranks differ, the target is not even in the rational span.  At equal rank,
    the quotient index ``[L':L]`` is the ratio of their top determinantal
    divisors, so equality of those divisors is equivalent to membership.

    This deliberately returns only compact Smith invariants; it is a reusable
    exact arithmetic lemma, independent of tiling geometry.
    """
    rows = [list(row) for row in rows]
    target = list(target)
    if not rows:
        raise ValueError("matrix must have at least one row")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("matrix rows must have equal width")
    if len(target) != len(rows):
        raise ValueError("target height must equal matrix height")
    matrix = _smith_signature(rows, backend=backend)
    augmented = _smith_signature([
        row + [value] for row, value in zip(rows, target)
    ], backend=backend)
    if augmented["rank"] > matrix["rank"]:
        verdict = "obstructed-rank"
        lattice_index = None
    else:
        # Adding a column cannot reduce rank or increase the determinantal
        # divisor.  Divisibility is asserted so dependency/API regressions fail
        # loudly rather than emitting a misleading verdict.
        assert augmented["rank"] == matrix["rank"]
        assert matrix["determinantal_divisor"] % augmented["determinantal_divisor"] == 0
        lattice_index = (
            matrix["determinantal_divisor"]
            // augmented["determinantal_divisor"]
        )
        verdict = (
            "integer-compatible" if lattice_index == 1
            else "obstructed-index"
        )
    return {
        "verdict": verdict,
        "matrix": matrix,
        "augmented": augmented,
        "lattice_index": lattice_index,
    }


def _flint_hnf_row_basis(rows) -> tuple[tuple[int, ...], ...]:
    """Canonical nonzero row basis of an integer row lattice."""
    from flint import fmpz_mat

    normal = fmpz_mat(rows).hnf()
    basis = []
    for i in range(normal.nrows()):
        row = tuple(int(normal[i, j]) for j in range(normal.ncols()))
        if any(row):
            basis.append(row)
    return tuple(basis)


def integer_lattice_membership_hnf(rows, target) -> dict:
    """Decide integer column-lattice membership by canonical row HNF.

    Transposing turns columns into row generators.  Adjoining the target does
    not change their integer lattice exactly when the two canonical Hermite
    row bases agree.  This decides the same condition as the Smith-divisor
    criterion but avoids unnecessary diagonalization on large matrices.
    """
    rows = [list(row) for row in rows]
    target = list(target)
    if not rows:
        raise ValueError("matrix must have at least one row")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("matrix rows must have equal width")
    if len(target) != len(rows):
        raise ValueError("target height must equal matrix height")
    generators = [list(column) for column in zip(*rows)]
    before = _flint_hnf_row_basis(generators)
    after = _flint_hnf_row_basis(generators + [target])
    equal = before == after
    if equal:
        verdict = "integer-compatible"
    elif len(after) > len(before):
        verdict = "obstructed-rank"
    else:
        verdict = "obstructed-index"
    return {
        "verdict": verdict,
        "normal_form": "flint-row-hnf",
        "matrix_rank": len(before),
        "augmented_rank": len(after),
        "canonical_bases_equal": equal,
        "lattice_index": 1 if equal else None,
    }


def integer_cokernel_snf(shape, hnf, backend="flint") -> dict:
    """Exact integer relaxation of a quotient's incidence cover equation.

    A compatible result means only that ``M x = 1`` has an *integer* solution;
    it does not assert a nonnegative or 0/1 exact cover.  An obstruction proves
    that no exact cover exists.  When GF(2) also detects it, its independently
    checkable compact witness is attached.
    """
    shape = tuple(tuple(cell) for cell in shape)
    hnf = tuple(hnf)
    instance = TorusInstance(shape, hnf)
    masks = [mask for _, mask in instance.placements]
    rows = [
        [(mask >> cell) & 1 for mask in masks]
        for cell in range(instance.n_cells)
    ]
    membership = integer_lattice_membership(
        rows, [1] * instance.n_cells, backend=backend
    )
    result = {
        "kind": "integer-incidence-smith-test",
        "hnf": list(hnf),
        "quotient_index": hnf[0] * hnf[2],
        "n_cells": instance.n_cells,
        "n_placements": len(instance.placements),
        **membership,
    }
    if membership["verdict"].startswith("obstructed"):
        modular = gf2_cokernel_obstruction(shape, hnf)
        if modular is not None:
            result["modular_witness"] = modular
    return result


def integer_cokernel_hnf(shape, hnf) -> dict:
    """Exact quotient incidence-lattice test using canonical FLINT HNF."""
    shape = tuple(tuple(cell) for cell in shape)
    hnf = tuple(hnf)
    instance = TorusInstance(shape, hnf)
    masks = [mask for _, mask in instance.placements]
    rows = [
        [(mask >> cell) & 1 for mask in masks]
        for cell in range(instance.n_cells)
    ]
    membership = integer_lattice_membership_hnf(rows, [1] * instance.n_cells)
    result = {
        "kind": "integer-incidence-hermite-test",
        "hnf": list(hnf),
        "quotient_index": hnf[0] * hnf[2],
        "n_cells": instance.n_cells,
        "n_placements": len(instance.placements),
        **membership,
    }
    if membership["verdict"].startswith("obstructed"):
        modular = gf2_cokernel_obstruction(shape, hnf)
        if modular is not None:
            result["modular_witness"] = modular
    return result


def quotient_placement_profiles(shape, hnf) -> tuple[tuple[int, ...], ...]:
    """Distinct six-sector profiles of legal placements on one quotient."""
    instance = TorusInstance(tuple(tuple(cell) for cell in shape), tuple(hnf))
    profiles = set()
    for _, mask in instance.placements:
        counts = [0] * 6
        for cell in range(instance.n_cells):
            if (mask >> cell) & 1:
                counts[cell % 6] += 1
        profiles.add(tuple(counts))
    return tuple(sorted(profiles))


@lru_cache(maxsize=None)
def _nonnegative_profile_coefficients(profiles):
    """Exact conic representation of all-ones by at most six profiles."""
    from sympy import Matrix

    profiles = tuple(profiles)
    target = Matrix([1] * 6)
    for size in range(1, min(6, len(profiles)) + 1):
        for chosen in itertools.combinations(range(len(profiles)), size):
            matrix = Matrix(6, size, lambda row, col: profiles[chosen[col]][row])
            if matrix.rank() != size:
                continue
            try:
                solution, parameters = matrix.gauss_jordan_solve(target)
            except ValueError:
                continue
            if parameters.rows or any(value < 0 for value in solution):
                continue
            if matrix * solution != target:
                continue
            return tuple(
                (index, int(value.p), int(value.q))
                for index, value in zip(chosen, solution)
                if value
            )
    return None


def nonnegative_cokernel_relaxation(shape, hnf) -> dict:
    """Decide the nonnegative rational incidence relaxation exactly.

    Translation-averaging makes any feasible solution constant on placement
    translation orbits.  Such an orbit is determined, for coverage purposes,
    by its six-sector profile.  Therefore full incidence feasibility is
    equivalent to conic feasibility in six dimensions.
    """
    shape = tuple(tuple(cell) for cell in shape)
    hnf = tuple(hnf)
    instance = TorusInstance(shape, hnf)
    profiles = quotient_placement_profiles(shape, hnf)
    coefficients = _nonnegative_profile_coefficients(profiles)
    result = {
        "kind": "nonnegative-rational-incidence-relaxation",
        "hnf": list(hnf),
        "quotient_index": hnf[0] * hnf[2],
        "n_cells": instance.n_cells,
        "n_placements": len(instance.placements),
        "profiles": [list(profile) for profile in profiles],
    }
    if coefficients is None:
        result["verdict"] = "fractional-obstructed"
        modular = gf2_cokernel_obstruction(shape, hnf)
        if modular is not None:
            result["modular_witness"] = modular
    else:
        result["verdict"] = "fractional-compatible"
        result["profile_coefficients"] = [
            {
                "profile": list(profiles[index]),
                "numerator": numerator,
                "denominator": denominator,
            }
            for index, numerator, denominator in coefficients
        ]
    return result


def verify_nonnegative_cokernel_relaxation(shape, result: dict) -> bool:
    """Check a fractional witness against every full incidence row."""
    try:
        if (
            result["kind"] != "nonnegative-rational-incidence-relaxation"
            or result["verdict"] != "fractional-compatible"
        ):
            return False
        hnf = tuple(result["hnf"])
        instance = TorusInstance(tuple(tuple(cell) for cell in shape), hnf)
        profiles = quotient_placement_profiles(shape, hnf)
        if result["profiles"] != [list(profile) for profile in profiles]:
            return False
        coefficients = {}
        for row in result["profile_coefficients"]:
            profile = tuple(row["profile"])
            if profile not in profiles or profile in coefficients:
                return False
            value = Fraction(row["numerator"], row["denominator"])
            if value < 0:
                return False
            coefficients[profile] = value

        by_profile = {}
        for _, mask in instance.placements:
            profile = [0] * 6
            for cell in range(instance.n_cells):
                if (mask >> cell) & 1:
                    profile[cell % 6] += 1
            by_profile.setdefault(tuple(profile), []).append(mask)

        weights = {
            profile: coefficient * instance.k / len(by_profile[profile])
            for profile, coefficient in coefficients.items()
        }
        for cell in range(instance.n_cells):
            coverage = sum(
                weights.get(profile, Fraction())
                for profile, masks in by_profile.items()
                for mask in masks
                if (mask >> cell) & 1
            )
            if coverage != 1:
                return False
        return True
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return False


def verify_integer_cokernel_snf(shape, result: dict) -> bool:
    """Recompute a Smith test and check any attached independent witness."""
    try:
        if result["kind"] != "integer-incidence-smith-test":
            return False
        expected = integer_cokernel_snf(shape, tuple(result["hnf"]))
        if result != expected:
            return False
        witness = result.get("modular_witness")
        return witness is None or verify_gf2_cokernel_obstruction(shape, witness)
    except (AssertionError, KeyError, TypeError, ValueError):
        return False


def finalist_thin_gf2_support(index: int) -> list[int]:
    """Closed-form GF(2) witness for finalist HNF ``(1,0,index)``.

    Cell indices use TorusInstance's order ``(u=0, v, sector)``. The formula
    has odd support and annihilates both legal thin-cylinder placement types
    for every ``index >= 4``; see T2.C1 in ``docs/theory/04_w2_cokernel.md``.
    """
    if index < 4:
        raise ValueError("thin-family formula requires index >= 4")
    if index % 2 == 0:
        cells = ((0, 3), (2, 4), (2, 5), (index - 1, 1), (index - 1, 3))
    else:
        cells = (
            ((0, 1), (2, 4), (index - 1, 2))
            + tuple((v, 5) for v in range(3, index))
        )
    return sorted(v * 6 + sector for v, sector in cells)
