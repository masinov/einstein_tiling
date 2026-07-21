# K5S — a synchronizing twelve-state retiling topology

**Date:** 2026-07-22

**Status:** exact combinatorial topology and conditional unique-grouping lemma;
no unmarked polygon, boundary-color transducer or aperiodicity result

## 1. Target

K4W strategy A asks first for a bounded macrocell topology with at least 11
rooted exact retilings by congruent copies of one support. It also needs a
local invariant that could identify macrocell boundaries in every admitted
tiling. The present note supplies those two *topological* ingredients. It
does not claim that an unmarked polygon forces the admitted language.

Use the ordinary `1 x 2` domino as the exact support and a rooted `2 x 16`
rectangle as the macrocell. Write

```
V = one vertical domino, width 1,
H = two horizontal dominoes filling a 2 x 2 block, width 2.
```

A word in `V,H` is a composition of its total width into parts `1,2` and
specifies one exact domino retiling of a two-row rectangle.

## 2. Twelve selected retilings

Let `W_6` be the composition words of width 6 and let

```
W*_6 = W_6 minus {VVVVVV}.
```

For every `w in W*_6`, define the rooted macro retiling

```
R(w) = VVV H w H VVV.                         (1)
```

The first-piece recurrence

```
d_0 = d_1 = 1,       d_n = d_(n-1) + d_(n-2)
```

counts compositions by `1,2`. Hence `|W_6|=d_6=13` and `|W*_6|=12`.
Every word in (1) has width `3+2+6+2+3=16` and every retiling uses exactly
16 congruent dominoes: six in the two `VVV` collars, four in the two `H`
blocks, and six in the width-six middle. The 12 rooted words are distinct.
Thus this topology clears the 11-state count with one spare state and without
a component-frequency obstruction.

This is a selected subfamily of the rectangle's domino tilings. Geometry
would have to exclude every other retiling; selection on paper is not a
matching rule.

## 3. The delimiter

Concatenate two admitted words in the same two-row band. The terminal `VVV`
of the left macro and initial `VVV` of the right macro form

```
... H VVV | VVV H ... = ... H VVVVVV H ... .  (2)
```

Call the maximal run of six vertical dominoes in (2) a **six-bar**. No
six-bar occurs inside an admitted macro: each collar run has length three and
is isolated by `H`, while a width-six middle word other than `VVVVVV` has
every vertical run of length at most five. Consequently the six-bars occur
exactly at macro seams, and the seam is the unique midpoint between their
third and fourth columns.

## 4. Conditional unique grouping

Define the guarded strip language `G_16` by four extensional conditions on a
plane domino tiling.

1. Every tile belongs to a two-row band containing bi-infinite six-bars.
2. Consecutive six-bars in a band have seam midpoints 16 units apart, and the
   interval between them has form (1).
3. Six-bars in vertically adjacent bands have the same seam coordinates.
4. No other contact admitted by the eventual geometric carrier can imitate a
   vertical domino or a six-bar.

### ST-M1.K5S

Every tiling in `G_16` has a unique radius-16 partition into rooted `2 x 16`
macrocells, and every macrocell carries one of 12 locally visible states.

### Proof

A six-bar consists of six dominoes spanning one and the same pair of rows, so
it identifies that band without a chosen lattice origin. Maximality and (2)
identify the seam at its midpoint. Conditions 1 and 2 give the unique
sequence of width-16 intervals in each band. Condition 3 aligns these
intervals between bands, producing one rectangular macro grid. The word
between consecutive seams is read within distance 16 and recovers `w`.
Condition 4 prevents a second geometric interpretation of the marker.
Therefore grouping and state decoding are finite-radius and unique. □

## 5. What this does and does not buy

The six-bar is a genuine synchronization invariant, not an absolute lattice
residue: it is a bounded configuration of physical occurrences, and its
midpoint is recovered equivariantly from the tiling. It avoids the gauge
failure of N8/N9.

The bare domino does **not** enforce `G_16`. It admits many other tilings,
including periodic ones, and the selected words expose only a one-dimensional
composition channel. Their left and right collars are fixed, while the top
and bottom ownership words are correlated. Nothing here realizes the four
independently checked Wang interfaces.

The remaining geometric burden is finite and explicit:

- force precisely `G_16` with one connected unmarked polygon under full
  isometries;
- make the six-bar recognizable without external marks;
- route the four edge colors of 11 selected Jeandel--Rao states to four
  macro interfaces; and
- prove a complete contact atlas and one whole-plane lift.

Failure of the first two items closes this synchronized-domino
parameterization. It does not close other K4W inverse dissections.
