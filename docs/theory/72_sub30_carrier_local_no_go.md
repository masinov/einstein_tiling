# No carrier-local AHI compiler has area below 30

**Date:** 2026-07-28  
**Scope:** one connected common-rhombus carrier; every decoded Section 10.1
macro lies wholly inside one carrier; full Euclidean isometries allowed

## 1. The finite class

K64A proves that a carrier-local decoder of area `A<30` can satisfy the exact
AHI source frequencies only for

```text
A=15,16,17,
```

and then its state library must contain both

```text
(one large macro + (A-15) singleton M macros)
and
(A singleton M macros).                                  (1.1)
```

Fix the large macro in a canonical pose.  Because the carrier and every
decoded macro are disks in the common triangular cellulation, the adjacency
graph of the pieces in the first state of (1.1) is connected.  The singleton
pieces can therefore be ordered so that each new rhombus shares a complete
unit boundary edge with the union already built.  Hence every possible
support occurs in the following finite construction:

1. start with the exact published `large_A` or `large_B` support;
2. add zero, one, or two full-isometry copies of the exact singleton support;
3. require disjoint primitive-triangle interiors and at least one shared unit
   boundary edge at each addition; and
4. retain exactly the connected topological-disk unions.

No source marking is used in this construction.  It is a geometric superset:
supports with illegal AHI endpoint germs or vertex stars are deliberately
retained.

## 2. K64C — exact support and subdivision census

For every support above, pair its primitive triangles across unit edges in
every possible way.  These perfect matchings are exactly its subdivisions
into common rhombi.  The exhaustive exact counts are:

| large macro | attached `M` | area | supports | lozenge subdivisions |
|---|---:|---:|---:|---:|
| `large_A` | 0 | 15 | 1 | 27 |
| `large_A` | 1 | 16 | 28 | 816 |
| `large_A` | 2 | 17 | 472 | 14,650 |
| `large_B` | 0 | 15 | 1 | 24 |
| `large_B` | 1 | 16 | 28 | 736 |
| `large_B` | 2 | 17 | 467 | 13,190 |
| **total** |  |  | **997** | **29,443** |

For each subdivision, join the endpoints of every rhombus's long diagonal.
Every one of the 29,443 graphs contains an odd cycle.  The number of
bipartite subdivisions is exactly zero.

The certificate records the complete primitive-cell list, matching count,
and a shortest odd-cycle witness for every support.  A cold rebuild reproduces
the whole census.  As an independent internal anchor, the previously derived
P17 support occurs from both macro classes; each occurrence reproduces its
known count of 60 subdivisions and zero bipartite cases.

## 3. N64S — sub-30 carrier-local impossibility

### Theorem

There is no carrier-local finite-state compiler from a connected common-
rhombus carrier of area below 30 to the exact AHI Section 10.1 source.

### Proof

Assume such a compiler exists.  K64A restricts its area to 15, 16, or 17 and
requires the two compositions (1.1).  Its large-containing state belongs to
the geometric support census of Section 1.  Its all-singleton state is a
perfect matching of that same primitive-triangle support.

K64B is a necessary source-language condition: continuation of the two
ordered corridor bits colors the long-diagonal graph bipartitely.  K64C proves
that every perfect matching of every possible support has an odd cycle.
Therefore the required all-singleton state cannot exist, a contradiction.
QED.

This is a family theorem, not a finite-radius inference: K64A proves that the
six enumerated classes exhaust every sub-30 composition, and the attachment
argument proves that their support lists are complete.

## 4. Exact boundary of the result

N64S raises the minimum possible carrier area in this realization family from
15 to **at least 30**.  It does not assert that area 30 works.  At area 30,
new composition pairs such as `(2,0)` and `(1,15)` become arithmetically
possible and the present zero/one/two-attachment census no longer applies.

The theorem does not cover a decoder whose source macrotiles cross carrier
boundaries, nor a nonseparable construction that recovers the source only
from multi-carrier junctions.  Those are not loopholes in the proof; they are
different realization families and remain the principal ST-M1 frontier.

## 5. Machine certificate

```text
data/sturmian-source/ahi-sub30-carrier-classification.json
sha256 20ae6ff936eb0674ab0c7facf2a9e21969b0cdb71dbbd0287aaa4a6bccc6fc9c
bytes  4779407
```

The producer and cold verifier are respectively
`scripts/build_sturmian_sub30_carriers.py` and
`scripts/verify_sturmian_sub30_carriers.py`.
