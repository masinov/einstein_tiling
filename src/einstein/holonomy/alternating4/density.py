"""Density-gap controls for one V4 signature and one packing orbit.

The cover clauses can be replaced by a weaker global consequence of exact
cover: an area-ten tile on a quotient with ``6k`` kite cells requires
``3k/5`` selected placements.  This module asks the sharper experimental
question suggested by the Layer-D scans: do V4 gluing and the six-kite
collision orbit already force at most ``k/2`` selected placements?
"""

from __future__ import annotations

from pysat.card import CardEnc, EncType
from pysat.formula import CNF

from einstein.holonomy.alternating4.lifts import induced_v4_twists
from einstein.holonomy.alternating4.packing import (
    canonical_collision_type,
    collision_orbit_clauses,
    placement_lattice_cells,
)
from einstein.holonomy.alternating4.packing_families import PACKING_COLLISION_SEED
from einstein.holonomy.alternating4.local_system import build_v4_coverability_cnf
from einstein.holonomy.constraints import quotient_boundary_data


def build_signature_density_bound_cnf(shape, hnf, signature_row, bound=None):
    """Assert one signature, one packing orbit, and more than ``bound`` tiles.

    Coverage clauses are deliberately omitted.  The default ``bound=k/2``
    is the candidate extremal density on an HNF quotient with ``k=a*d``
    substrate centers.  UNSAT therefore establishes the finite inequality
    ``selected <= k/2`` for this relaxation.
    """
    hnf = tuple(hnf)
    k = hnf[0] * hnf[2]
    if bound is None:
        bound = k // 2
    if not 0 <= bound < 12 * k:
        raise ValueError("bound must admit at least one placement above it")
    images = tuple(signature_row["images"])
    twists = induced_v4_twists(tuple(signature_row["base_twists"]), hnf)
    covered, cover_metadata = build_v4_coverability_cnf(
        shape, hnf, images, twists=twists, cover_mode="at-least"
    )
    instance, _, _ = quotient_boundary_data(shape, hnf)
    placement_count = len(instance.placements)
    cnf = CNF(from_clauses=covered.clauses[cover_metadata["cover_clauses"]:])
    implication_clauses = len(cnf.clauses)

    target = canonical_collision_type(
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[0]),
        placement_lattice_cells(shape, PACKING_COLLISION_SEED[1]),
    )
    packing = collision_orbit_clauses(shape, hnf, instance, target)
    cnf.extend(packing)
    cardinality = CardEnc.atleast(
        lits=list(range(1, placement_count + 1)),
        bound=bound + 1,
        top_id=cnf.nv,
        # The asserted lower bound is small relative to the 12k placement
        # variables.  A cardinality network propagates this polarity much
        # better than a sequential counter over the complementary literals.
        encoding=EncType.cardnetwrk,
    )
    cnf.extend(cardinality.clauses)
    metadata = {
        "kind": "single-v4-signature-packing-density-bound",
        "hnf": list(hnf),
        "centers": k,
        "images": list(images),
        "mapping_index": signature_row.get("mapping_index"),
        "twists": list(twists),
        "placements": placement_count,
        "potential_bits": cover_metadata["potential_bits"],
        "candidate_upper_bound": bound,
        "asserted_minimum": bound + 1,
        "exact_cover_placements": (
            (6 * k) // len(shape) if (6 * k) % len(shape) == 0 else None
        ),
        "exact_cover_placement_ratio": [6 * k, len(shape)],
        "implication_clauses": implication_clauses,
        "packing_clauses": len(packing),
        "cardinality_variables": cnf.nv - covered.nv,
        "cardinality_clauses": len(cardinality.clauses),
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
    }
    return cnf, metadata
