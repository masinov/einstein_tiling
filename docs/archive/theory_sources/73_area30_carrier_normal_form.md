# The exact area-30 carrier-local normal form

**Date:** 2026-07-28  
**Scope:** the carrier-local common-rhombus realization family of N64S

## 1. K65A — composition classification at area 30

At carrier area `A=30`, the only source-macro compositions are

```text
Z=(0 large,30 M),
G=(1 large,15 M),
H=(2 large, 0 M).                                      (1.1)
```

Let their state frequencies be `z,g,h>=0`.  The decoded singleton-to-large
ratio is

```text
R=(30z+15g)/(g+2h).                                    (1.2)
```

The AHI target is `r=6(sqrt(2)-1)`, with `0<r<3`.  If `h=0`, every defined
ratio in (1.2) is at least 15.  If `z=g=0`, it is zero.  Hence every viable
area-30 library contains `H` with positive frequency and contains at least
one of `G` or `Z` with positive frequency.  Conversely, either pair `{H,G}`
or `{H,Z}` has a nonnegative frequency mixture whose ratio is `r`; composition
alone creates no further obstruction.

Thus the entire area-30 question begins with a two-large-macro carrier state.

## 2. K65F — finite support reduction

Normalize the first large macro as `large_A` or `large_B`.  In an `H` state,
the second large macro is another full-isometry copy of `large_A` or
`large_B`, with disjoint primitive-triangle interior.  Since the carrier is a
connected topological disk in the common triangular cellulation, the two
macro supports share at least one complete unit boundary edge.  Aligning the
finite boundary vertices under the twelve lattice point isometries therefore
enumerates every possible `H` support.

For each fixed support, the alternative state problem is also finite:

- `Z`: enumerate every perfect matching of all 60 primitive triangles;
- `G`: enumerate every full-isometry embedding of either large macro whose 30
  triangles lie inside the support, then every perfect matching of the 30
  residual triangles.

Every singleton subset in a source-legal state must have a bipartite
long-diagonal continuation graph: an odd cycle already requires two ordered
corridor bits to alternate inconsistently, independently of the surrounding
large macro.  Consequently zero bipartite `G` and `Z` alternatives would
close area 30 by a necessary-condition argument over a geometric superset.
Any survivor would remain provisional until the complete AHI endpoint-germ
and vertex rules are checked.

## 3. Decision target

The exact finite target is therefore:

> Among every disk union of two published large macros, does any support have
> a `G` or `Z` alternative whose singleton long-diagonal graph is bipartite?

This is the complete next case forced by N64S, not a new carrier family.  No
area above 30 is implicated by either outcome.

## 4. K65C — exact area-30 classification

The complete support quotient contains `65` full-isometry classes of
two-large disk unions.  Across them there are:

```text
164  contained-large G embeddings,
3,390 residual G perfect matchings,
48,652 whole-support Z perfect matchings.
```

Every one of the `52,042` alternative singleton subdivisions has a
nonbipartite long-diagonal graph.  There are zero parity survivors in either
the `G` or `Z` class.  The enumeration retains disconnected and holed `G`
residuals; it does not assume that the 15 singleton macros form a disk.

The exact artifact is cold-rebuilt from the pinned source atlas:

```text
data/sturmian-source/ahi-area30-carrier-classification.json
sha256 adc403154e98a70205ed58284e54de36d795466635489e91cbb03e2a7ad1bab1
bytes  905959
```

## 5. N65S — area 30 is impossible

### Theorem

No area-30 connected common-rhombus carrier admits a carrier-local finite-
state compiler to the exact AHI Section 10.1 source.

### Proof

K65A forces an `H` state and at least one `G` or `Z` state.  K65F proves that
the `H` support belongs to the 65-class census and that every geometric `G`
or `Z` alternative occurs in its corresponding perfect-matching list.  The
singleton long-diagonal graph of every source-legal alternative must be
bipartite.  K65C leaves no such alternative, contradiction.  QED.

Together N64S and N65S prove that the minimum carrier-local area is strictly
greater than 30.  This still does not address cross-carrier decoders.
