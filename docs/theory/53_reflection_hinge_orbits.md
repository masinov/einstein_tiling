# Reflection-hinge orbit parity

**Date:** 2026-07-27

**Status:** HC-40 exact local-star theorem draft; no carrier, patch or
all-tilings claim

## 1. Invariant local stars

Let `R` be reflection in a line `L`, let `O` lie on `L`, and let a finite set
of congruent polygon occurrences cover a punctured neighborhood of `O` with
pairwise-disjoint interiors.  Assume the local star is invariant under `R`
and that the polygonal support has trivial Euclidean symmetry.

### ST-M1.K45O

Reflection acts freely on the occurrences of the star.  Every occurrence
orbit has size two, and the total number of participants is even.

### Proof

An occurrence orbit under an involution has size one or two.  A size-one
occurrence `T` would obey `R(T)=T`; conjugating by its placement would give a
nonidentity reflection symmetry of the polygonal support.  Trivial symmetry
excludes this.  Hence all orbits have size two. □

### ST-M1.N49

No reflection-invariant three-occurrence hinge exists for a symmetry-free
carrier.

### Proof

Three is not a sum of orbit sizes two. □

This obstruction is stronger than an angle failure.  A purported singleton
third occurrence silently assumes a reflection symmetry of the unmarked
tile.

## 2. The minimum four-sector hinge

The next possible star has two occurrence orbits.  Let their sector angles be
`alpha` and `beta`, preserved within each reflected pair.

### ST-M1.K45H

For a four-occurrence invariant star with no fixed occurrence:

1. the two rays of the mirror axis are opposite contact rays;
2. up to cyclic reversal, the sector sequence is

```text
alpha, beta, beta, alpha;                            (2.1)
```

3. exact local coverage is equivalent to

```text
alpha + beta = pi,       0<alpha,beta<pi.            (2.2)
```

Conversely every pair satisfying (2.2) gives a disjoint abstract sector star
with the required reflection action.

### Proof

Reflection reverses the cyclic order at `O` and has two opposite fixed rays.
If a fixed ray lay in the interior of a sector, that sector and its occurrence
would be setwise fixed, contradicting K45O.  Both fixed rays are therefore
sector boundaries.  The two sectors adjacent to one fixed ray form one
reflected pair, and those adjacent to the opposite ray form the other.  This
gives (2.1).  Summing the four sectors gives
`2*alpha+2*beta=2*pi`, equivalent to (2.2); positivity then makes both angles
strictly convex.  Drawing four rays with successive gaps (2.1) proves the
converse at sector level. □

The explicit control `alpha=pi/3`, `beta=2*pi/3` proves the local angle system
nonempty.  It does not realize four congruent polygon placements beyond their
germs.

## 3. Scope

K45H replaces N48's fixed side by two fixed contact rays.  It neither assigns
binary meaning to the star nor proves that the four germs extend without
collision.  Those are separate state and geometry gates.
