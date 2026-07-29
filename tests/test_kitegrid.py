"""Geometric self-consistency of the kite substrate.

Everything here is exact integer arithmetic; failures mean the substrate's
geometry, adjacency, or symmetry action is wrong.
"""

import itertools
import random

from einstein.geometry.kite_grid import (
    MDIR,
    N_OPS,
    VDIR,
    boundary_cycle,
    canonical_form,
    cell_edges,
    cell_neighbors,
    cell_vertices,
    cross,
    is_center,
    norm2,
    rot60,
    shoelace2,
    transform_cell,
    transform_point,
    translate_cell,
)

# a spread of hex centers: integer combos of the lattice generators
LATTICE = [(2, 2), (-2, 4)]


def centers_sample():
    out = []
    for a in range(-2, 3):
        for b in range(-2, 3):
            out.append((a * 2 + b * -2, a * 2 + b * 4))
    return out


def cells_sample():
    return [(cx, cy, d) for cx, cy in centers_sample() for d in range(6)]


def test_direction_tables():
    assert VDIR[0] == (2, 0) and MDIR[0] == (1, 1)
    for k in range(6):
        assert VDIR[(k + 1) % 6] == rot60(VDIR[k])
        assert MDIR[(k + 1) % 6] == rot60(MDIR[k])
        assert norm2(VDIR[k]) == 4  # hex vertex distance 2
        assert norm2(MDIR[k]) == 3  # apothem sqrt(3)


def test_centers_lattice():
    for c in centers_sample():
        assert is_center(c)
    assert not is_center((2, 0)) and not is_center((1, 1)) and not is_center((0, 2))


def test_kite_shape():
    for cell in cells_sample():
        q = cell_vertices(cell)
        assert len(set(q)) == 4
        # edge lengths: long, short, short, long
        lens = [norm2((q[(i + 1) % 4][0] - q[i][0], q[(i + 1) % 4][1] - q[i][1])) for i in range(4)]
        assert lens == [3, 1, 1, 3]
        # convex, counterclockwise
        for i in range(4):
            assert cross(q[i], q[(i + 1) % 4], q[(i + 2) % 4]) > 0
        # area: one kite = 4 in shoelace2 units (true area sqrt(3))
        assert shoelace2(list(q)) == 4


def test_adjacency_symmetric_and_edge_sharing():
    for cell in cells_sample():
        nbrs = cell_neighbors(cell)
        assert len(set(nbrs)) == 4
        my_edges = set(cell_edges(cell))
        shared = []
        for nb in nbrs:
            assert cell != nb
            assert cell in cell_neighbors(nb), "adjacency must be symmetric"
            common = my_edges & set(cell_edges(nb))
            assert len(common) == 1, "each neighbor shares exactly one edge"
            shared.append(next(iter(common)))
        # the four shared edges are exactly the kite's four edges
        assert set(shared) == my_edges


def test_grid_is_exact_cover():
    """Around any hex vertex / midpoint / center, incident kites don't overlap
    and their angles close up: verified via each edge having exactly 2 kites
    in a big patch (interior edges) -- an exact local tiling check."""
    cells = set()
    frontier = {(0, 0, 0)}
    for _ in range(6):
        new = set()
        for c in frontier:
            for nb in cell_neighbors(c):
                if nb not in cells:
                    new.add(nb)
        cells |= frontier
        frontier = new
    edge_count = {}
    for c in cells:
        for e in cell_edges(c):
            edge_count[e] = edge_count.get(e, 0) + 1
    assert set(edge_count.values()) <= {1, 2}
    # interior cells (all 4 neighbors present) have all edges shared exactly twice
    for c in cells:
        if all(nb in cells for nb in cell_neighbors(c)):
            assert all(edge_count[e] == 2 for e in cell_edges(c))


def test_transform_cell_matches_geometry():
    """The combinatorial action on (center, sector) must agree with the
    geometric action on the kite's vertex set."""
    for cell in cells_sample():
        for op in range(N_OPS):
            img = transform_cell(cell, op)
            assert is_center((img[0], img[1]))
            got = set(cell_vertices(img))
            want = {transform_point(p, op) for p in cell_vertices(cell)}
            assert got == want, (cell, op)


def test_ops_form_group_of_order_12():
    cell = (0, 0, 0)
    images = {transform_cell(cell, op) for op in range(N_OPS)}
    # a single kite and an adjacent same-hex pair are mirror-symmetric, so
    # they have 6 images; a chiral configuration must have all 12:
    shape = ((0, 0, 0), (0, 0, 1), (0, 0, 3))  # sectors {0,1,3}: chiral
    imgs = {tuple(sorted(transform_cell(c, op) for c in shape)) for op in range(N_OPS)}
    assert len(imgs) == 12
    assert len(images) == 6  # single kite: mirror axis stabilizes


def test_canonical_form_invariance():
    rng = random.Random(7)
    base = [(0, 0, 0)]
    # grow a random 8-cell shape
    for _ in range(7):
        nbrs = [nb for c in base for nb in cell_neighbors(c) if nb not in base]
        base.append(rng.choice(nbrs))
    canon = canonical_form(base)
    for trial in range(50):
        op = rng.randrange(N_OPS)
        a, b = rng.randrange(-5, 6), rng.randrange(-5, 6)
        t = (a * LATTICE[0][0] + b * LATTICE[1][0], a * LATTICE[0][1] + b * LATTICE[1][1])
        moved = [translate_cell(transform_cell(c, op), t) for c in base]
        assert canonical_form(moved) == canon
    # canonical form of the canonical form is itself
    assert canonical_form(canon) == canon


def test_boundary_cycle_single_kite():
    cyc = boundary_cycle([(0, 0, 0)])
    assert len(cyc) == 4
    assert set(cyc) == set(cell_vertices((0, 0, 0)))
