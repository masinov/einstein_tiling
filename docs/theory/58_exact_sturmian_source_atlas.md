# Exact Section 10.1 Sturmian source atlas

**Date:** 2026-07-27
**Status:** exact machine-verified finite reconstruction; source-to-normalized
all-tilings equivalence remains a proof draft

## 0. Retirement of the HC-41 octagon (N52)

Let `T` be the octagon from note 57 and let

```text
T' = (9,4 sqrt(3)) - T.
```

The two copies share the complete `X-Q-X` chain.  Their union is a simple
ten-gon `U`.  Its bottom boundary translated by `(2,4 sqrt(3))` is its top
boundary, and its left `Y-P-Y` chain translated by `(19,0)` is its right
chain.  Moreover

```text
area(U) = 76 sqrt(3)
        = |det((19,0),(2,4 sqrt(3)))|.
```

The standard translation criterion therefore tiles the plane by lattice
translates of `U`, and hence periodically by copies of `T`.  The octagon is
not an aperiodic monotile.  This certificate retires the hinge branch before
the source reconstruction below.

## 1. Result

The pinned arXiv v3 source archive for Akiyama--Hamada--Ito contains vector
figures but no coordinate, address, SAB or vertex tables.  Direct extraction
from `Example1.pdf` page 1, followed by exact triangular-lattice
normalization, gives the three Section 10.1 supports:

```text
large_A boundary: 1105050544323232    area 30
large_B boundary: 0105505443233212    area 30
small_M boundary: 3205                area  2
```

Digits name the six cyclic unit directions in the exact `(u,v)` basis used by
the certificate.  Both large supports are simple connected polyiamonds with
30 primitive triangles; the small support is a two-triangle rhombus.

The magenta vector paths give `15,15,1` continuous SAB components.  After the
bounded bends contract, every component is the long diagonal of exactly two
adjacent primitive triangles.  The role census in either large support is

```text
6 S-pairs + 6 M-cells + 3 L-pairs,
```

which is exactly `12S+6M+6L`.  The components partition all 30 primitive
triangles.  Their two-triangle unions are congruent `60/120` rhombi and their
macro adjacency graphs are connected.

There are two distinct role-labelled placements of the extracted SAB graph
on each large support.  In both cases the two placements form one orbit under
the exact support stabilizer (order four for `large_A`, order two for
`large_B`).  Thus the source atlas is unique up to an isometry of its support;
the vector figure has not introduced an unrecorded choice.

## 2. Consequence: a 31-address common-support source

Pairing primitive triangles along the extracted SAB components replaces the
old 62-triangle address bound by

```text
15 addresses in large_A + 15 in large_B + 1 in small_M = 31.
```

Every address has the same unmarked rhombus support.  Retaining macro type,
address, reflected state, internal adjacency, the SAB diagonal and the source
boundary/vertex data as colors instantiates the equal-support compiler S0C.
The exact artifact therefore supplies the finite extensional input that SER0
was missing.

Together with the existing O0/I0/D0 proof draft, this gives a finite colored
one-support system whose intended tilings decode to the irrational
`sqrt(2)-1` Sturmian source.  The remaining proof-review obligation is the
all-tilings equivalence: the normalized edge/vertex rule must be checked
extensionally against every source boundary contact, including reflected
placements and contracted multi-participant vertices.  No unmarked monotile
claim follows merely from the 31-state compiler.

## 3. Certificate

The source archive and member are pinned by SHA-256.  The producer resolves
the Illustrator SVG uses, classifies the three fixed direction/length
classes, reconstructs the limiting SAB graph, and solves the finite exact
embedding problem.  After that transcription boundary, all checks use integer
arithmetic:

- boundary closure and simplicity;
- exact shoelace area;
- primitive-triangle union and connectedness;
- SAB two-triangle incidence and full support partition;
- connected macro address graphs;
- support stabilizers and the single-orbit test.

The artifact is
`data/sturmian-source/ahi-section10-supports.json` and its cold verifier is
`scripts/verify_sturmian_source.py`.

## 4. Research boundary

This result closes the missing finite source transcription.  It does not
solve color erasure.  The active theorem is now sharply stated:

> Realize the exact 31-state rhombus contact system by one connected unmarked
> polygon with a total decoder on every unrestricted Euclidean tiling; or
> prove that such a realization is impossible in a stated carrier class; or
> prove undecidability for a stated effective realization family.

Any next construction must compile this serialized source and satisfy the
no-spurious-tilings contract from the outset.  A new free-standing gadget or
finite patch that does not decode these 31 addresses is outside the active
problem.
