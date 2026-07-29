# Kaplan: detecting isohedral polyforms with SAT

**Catalog ID:** `kaplan-isohedral-sat-2024`  
**Audited version:** arXiv:2406.16407 / EPTCS 403 (2024), 118--122  
**DOI:** `10.4204/EPTCS.403.25`  
**Audit date:** 2026-07-20  
**Status:** full-text audited and independently implemented for grid-aligned
polykites.

## Exact criterion

Let `S={T_1,...,T_n}` be a surround of an asymmetric tile `T`, with
`T_i=g_i(T)`. Define the transformed surround of `T_i` by

```text
S_i = {g_i o g_j(T) : T_j in S}.
```

A neighbour `T_i` is *extendable* when every member of `S_i` either equals a
tile in the original 1-patch or has disjoint interior from it.

**Proposition 1:** `T` admits an isohedral tiling iff it has a surround in
which every neighbour is extendable. Repeating the congruent surrounds grows
a plane tiling; the Local Theorem of Dolbilin--Schattschneider makes a tiling
with congruent surrounds isohedral.

This is a finite positive-and-negative test for isohedral tileability within
the selected alignment model. It is not a test for periodic tilings requiring
two or more transitivity classes.

## SAT formulation

For every grid-aligned copy capable of occupying a halo cell, introduce one
Boolean variable. The base surround formula contains:

- at least one placement covering each halo cell;
- pairwise exclusion of placements overlapping in any cell;
- lazy blocking clauses for candidate surrounds whose union has a hole.

The extendability restriction adds inverse-neighbour closure and clauses for
the compositions `g_i o g_j`, including the reverse order. Kaplan expresses
the principal positive closure as `not T_i or not T_j or T_k` when the
composition is another candidate neighbour, with related inverse-composition
clauses as optimizations.

## Repository implementation

`src/einstein/polykites/isohedral.py` reuses the exact kite substrate and A2
topology but implements a separate finite SAT layer:

1. enumerate all marked D6+translation neighbours;
2. exactly cover the full vertex halo;
3. force inverse neighbours;
4. forbid every selected composition that would overlap the central
   1-patch, using direct binary/ternary conflict clauses;
5. reject hole-bearing models;
6. independently reconstruct and verify every positive surround.

The direct conflict encoding is logically the extendability definition rather
than a line-for-line copy of Kaplan's compact positive clauses. The cold
verifier does not trust the SAT encoding.

### Important correction found by the benchmark

The first implementation covered only cells sharing an edge with the central
tile. It classified 54 seven-kites as isohedral instead of Myers's 52. Such a
cover can leave an uncovered angular sector meeting the tile only at a vertex,
so the centre is not necessarily in the topological interior of the patch.

Replacing that approximation with A2's full vertex halo changed the complete
counts to

```text
n:          1  2  3  4  5   6   7   8
isohedral:  1  1  4  4  0  70  52  37
```

They agree exactly with the cumulative translation, half-turn and isohedral
categories in Myers's independent table at every order.

## Certificates and controls

The complete `n<=8` run covers all 1,264 free polykites and stores 169 positive
finite surround certificates. A cold verifier checks each certificate without
SAT. Negative classifications remain rerunnable SAT-UNSAT results; the JSON
does not mislabel them as independently checkable proof objects.

Additional controls:

- the monokite has a verified isohedral surround;
- the unique periodic-but-anisohedral four-kite is A1-positive and
  isohedral-SAT-negative;
- Hat and Turtle are isohedral-SAT-negative;
- at `n=8`, 37 shapes are isohedral and two further shapes are periodic but
  three-anisohedral; Hat is excluded from the periodic count.

Artifacts:

- `docs/notebook/assets/a1-isohedral-control.json`;
- `docs/notebook/assets/a1-isohedral-control.svg`;
- `scripts/run_a1_isohedral_control.py`;
- `scripts/verify_a1_isohedral_control.py`;
- `tests/test_a1_isohedral.py`.

## Role and limit

This is a cheap, complete first periodicity filter for isohedral tilings and is
portable to another polyform substrate once its exact symmetry poses and halo
are defined. A1 remains broader because it finds arbitrary periodic quotient
tilings, including anisohedral examples, but its negative result is bounded by
the searched torus index. Neither filter recognizes aperiodicity.

The implementation closes the planned compact benchmark. We should not rerun
the already settled `n<=24` discovery census merely because this filter now
exists.
