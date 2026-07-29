# The marked one-polygon Sturmian compiler is undecidable

**Date:** 2026-07-28  
**Scope:** one connected polygonal prototile with a finite edge-to-edge
matching relation; the shape-only unmarked problem is excluded

## 1. Fixed source and decision family

Let `Y` be a fixed finite Wang presentation of the nonempty aperiodic AHI
`sqrt(2)-1` source.  Such a presentation exists because the exact 31-address
system is a finite local system on its recovered rank-two frame; ordinary
higher-block recoding replaces its finite edge and vertex rules by Wang edge
colors.  The projection back to the geometric AHI source is finite-radius and
period-reflecting.

For a finite Wang tile set `W`, form the product Wang system

```text
Z_W = Y x W.                                             (1.1)
```

Apply the effective Wang-to-`A/B` conversion of Stade's Lemma 5 and then the
effective `A/B`-to-stick conversion of his Theorem 15.  Denote the resulting
connected polygon and finite edge matching relation by `S(W)`.  Include with
the instance the decoder obtained by composing:

```text
marked stick tiling
  -> weave schematic
  -> A/B tiling
  -> product Wang tiling Z_W
  -> first coordinate Y.                               (1.2)
```

Call the computable output class `MARKED-STURMIAN-STICK`.

The decision problem asks whether an instance has at least one tiling.  On
every tiling the specified decoder (1.2) must be total and land in `Y`; that
property is promised by the construction and is independently part of the
family definition.

## 2. U2 — geometric Sturmian realization is undecidable with edge rules

### Theorem

`MARKED-STURMIAN-STICK` tileability is undecidable.  Every nonempty instance
is a connected marked aperiodic monotile whose complete tiling hull has a
total finite-radius factor to the fixed AHI source.

### Proof

The fixed system `Y` is nonempty, hence

```text
Z_W is nonempty  <=>  W is nonempty.                    (2.1)
```

Stade's Lemma 5 is a two-way local recoding between a Wang tiling and its
`A/B` tiling: private index colors force the four `A/B` pieces representing a
Wang symbol into the corresponding `S`-tetromino.  His Lemma 4 forces every
valid stick tiling into the weave, and Sections 2.3--2.9 recover the bounded
gap states, the `A/B` symbols and their matched colors.  All dimensions and
the state-cycle length are finite computable functions of `W`, so the
composite map (1.2) has finite computable radius.  Theorem 15 gives

```text
S(W) tiles  <=>  Z_W is nonempty  <=>  W is nonempty.   (2.2)
```

If a valid `S(W)` tiling had a nonzero translational period, equivariance of
(1.2) would transfer that period to its image in `Y`, contradicting the
aperiodicity of `Y`.  Thus every nonempty instance is aperiodic.  An algorithm
deciding the left side of (2.2) would decide the domino problem.  QED.

The construction can either forbid reflections or use Stade's finite
handedness rule from Section 3, so allowing full Euclidean isometries does not
alter the reduction.

## 3. D3 — meaningful decidable subfamilies

Undecidability comes from the unrestricted auxiliary two-dimensional Wang
system `W`, not from the fixed Sturmian factor.  Restricting `W` gives natural
decidable subclasses of the same geometric construction.

### 3.1 Directed-graph auxiliaries

For a finite directed graph `G`, let `W_G` contain one Wang tile for each edge
`e:u->v`.  Give it west/east colors `u,v` and give both its north and south
edge the private color `e`.  A `W_G` tiling is one bi-infinite directed walk
copied identically in every row.  Therefore

```text
W_G is nonempty  <=>  G has a directed cycle.            (3.1)
```

Cycle existence is decidable in linear time.  Consequently `S(W_G)` is a
Sturmian marked monotile exactly when `G` has a directed cycle.  This is a
nontrivial positive/negative decidable subfamily, not merely a finite list.

### 3.2 Fixed-width cylindrical auxiliaries

Fix a width `w`.  From an input Wang set, enumerate its legal cyclic
width-`w` rows.  Build an auxiliary Wang tile that stores one complete row
word and a phase in `Z/w`; horizontal matching increments the phase while
retaining the word, and vertical matching accepts exactly compatible
successive row words.  Hence every auxiliary configuration is the periodic
lift of a width-`w` cylinder configuration, with no external global promise.

Join two row words when their vertical colors match.  A whole-plane auxiliary
tiling exists exactly when this finite transfer graph has a directed cycle.
Thus the corresponding `S(W)` family is decidable for every supplied finite
`w` (exponential in `w`, but finite).

### 3.3 Shape-only carrier-local fusion

On the unmarked side, N60C gives a separate exact decidable rejection test:
if the AHI occurrence ray is outside the rational cone of a finite
carrier-local composition library, no total decoder exists.  N60P applies
that test plus complete vertex legality to close P17.  Passing the cone is
not a decision procedure; this subfamily supplies decidable no-certificates,
not a positive synthesis algorithm.

## 4. The unmarked boundary

U2 proves that no algorithm can enumerate marked connected Sturmian
compilers and decide every case.  It does not settle the user-facing
one-connected-unmarked-polygon question.  Stade geometrizes the finite edge
relation by adding a second staple prototile.  Removing that second support
while preserving the all-tilings decoder is precisely the missing
**self-stapling color-erasure theorem**.

Accordingly, the unrestricted research problem has a sharp boundary:

```text
one connected polygon + finite edge rules       undecidable (U2)
two connected unmarked polygons                 undecidable (Stade)
one connected unmarked polygon                  open here
```

Any proposed universal classification of all Sturmian polygons must either
prove that the last line is structurally tamer than the first two, or prove a
self-stapling reduction that transfers U2 across the unmarked boundary.  A
sequence of individual carrier families cannot establish either statement.
