# A gauge-safe symbolic compiler for a quadratic Sturmian tiling system

**Status:** consolidated proof draft; no monotile construction and no novelty
claim pending external mathematical and literature review

**Date:** 2026-07-21

## Abstract

This note consolidates the ST-M1 theory branch into one argument. Starting
from the `sqrt(2)-1` three-prototile construction of Akiyama--Hamada--Ito, it
records a proof-draft equal-triangle source presentation, states the exact
full-local-closure condition needed by any quotient, constructs a safe
distributed parity code, and factors its complete tile-star relation through
a gauge-invariant boundary cocycle. It also proves why role erasure,
independent rails, variable-free binary corners, pure orientation and an
unanchored lattice phase cannot realize the selected compiler.

The outcome is not an aperiodic monotile. The source presentation lacks the
extensional SER0 table needed for machine verification, and no polygon meets
the K2J geometric realization contract. The point of the consolidation is to
separate the closed symbolic mathematics from those two exact blockers.

## 1. Objects and claim boundary

Fix

```
beta = sqrt(2)-1.
```

Let `X_beta` denote the decorated Sturmian-lattice source system at that
slope, including its Euclidean images. The primary source proves a finite
three-prototile construction and irrational Sturmian order. Repository notes
08 and 10 derive a limiting colored presentation `Y` on one congruent
equilateral-triangle support.

The following status distinctions are essential.

- `Y` and its decoder are **proof drafts**, not machine-verified tables.
- All quotients below are finite symbolic presentations, not polygonal tiles.
- A total local map from every tiling by a polygon into `Y` would prove
  aperiodicity by period descent, but no such polygon is known.
- Surjectivity and positive entropy are outside the minimal result.

## 2. The arithmetic source selector

The source represents a patch composition `xS+yM+zL` by `[x:2y:z]`. Both
large optimized templates have composition

```
T_I = [12:12:6],
```

and the small template has

```
T_II = [0:2:0].
```

The Sturmian composition curve is

```
C(beta) = [(1-beta)^2 : 2*beta*(1-beta) : beta^2].
```

### Proposition 2.1 (P0)

The projective segment between `T_I` and `T_II` meets the curve on
`0<=beta<=1` exactly at `beta=sqrt(2)-1`.

### Proof

Every non-small point of the segment has first-to-third coordinate ratio two.
An interior curve point therefore satisfies

```
(1-beta)^2 / beta^2 = 2.
```

Positivity gives `(1-beta)/beta=sqrt(2)` and hence the unique solution
`beta=sqrt(2)-1`. Neither curve endpoint equals the small template. At the
solution,

```
a = beta^2/6,
b = beta*(1-2*beta)
```

are positive and `a*T_I+b*T_II=C(beta)` in homogeneous representatives, so
the intersection lies on the segment. \(\square\)

This proves only the composition selector. The source SAB and macro rules are
what force every admitted configuration onto the curve.

## 3. Equal-support colored source

Normalized equidistancing sends every source corridor gap, originally
`kappa` or `kappa+1`, to unit length as `kappa` tends to infinity. The centroid
calculation in note 08 makes every isometric cell one `60/120` rhombus. A
marked diagonal splits it into two equilateral triangles. The two large and
one small templates consequently have constituent counts

```
30, 30, 2.
```

The colored triangle state retains macro/address, internal ports, source
role, boundary/SAB data, line family, physical order, gap symbols and
decorated vertex participation.

Three lemmas supply the proof-draft source closure.

1. **O0:** auxiliary overlap disks contract to decorated vertices retaining
   participant identities and cyclic order.
2. **I0:** physical limiting vertices lie in three exact index cosets. On the
   actual order set `{-1,0,1}`, the coset uniquely recovers source provenance,
   and primitive limiting edges contain no interior vertex.
3. **D0:** internal ports recover complete macros; line-index increments have
   zero face holonomy; repeated gap descriptions agree along corridors; and
   exposed SAB rules decode a source configuration.

### Source hypothesis S0

Every configuration admitted by this finite colored presentation has a
finite-radius, translation-equivariant decoder

```
d_0 : Y -> X_beta.
```

Existence follows by limiting a physical source tiling. Hence `Y` is nonempty
and aperiodic by period descent.

S0 is closed at proof-draft level. SER0 remains open because the primary
archive does not list the extensional alphabet and rule tables.

## 4. The adversary is the full local closure

Let `q` be a finite symbolic recoding of `Y`. For presentation radius `r`,
write

```
Z(q,r) = {z : every radius-r patch of z occurs in q(Y)}.
```

The intended image `q(Y)` can be strictly smaller than this local-rule space.
All no-spurious-tilings claims must therefore quantify over `Z(q,r)`.

### Proposition 4.1 (Q0, period descent)

If `Z(q,r)` is nonempty and has a total finite-radius translation-equivariant
map to an aperiodic target, then `Z(q,r)` has no periodic configuration.

### Proof

If `z+v=z`, equivariance transfers `v` to the target image, contradicting its
aperiodicity unless `v=0`. \(\square\)

Two obvious quotients fail this criterion.

- Erasing macro ownership and keeping only `S/M/L` plus unrestricted SABs
  admits every Sturmian slope, including rational periodic slopes (N2).
- Replacing the three directions by independent nonempty one-dimensional
  sofic rails admits periodic points in each rail and hence a periodic product
  configuration (N1).

## 5. Lossless contacts and the exact quotient criterion

Let `A` be the finite essential addressed alphabet of `Y`. Replace each
source edge by a directed half-contact record naming the center state, side,
neighbor state and neighbor side. Require the three records incident with one
triangle to name one center state and retain all legal cyclic vertex words.

Reading the common center state and writing the source contacts are inverse
radius-one maps. This is K1C, a lossless higher-block recoding.

### Proposition 5.1 (K1T)

A fixed quotient presentation has a total exact lift to `Y` precisely when
some bounded local decoder, on every admitted quotient patch, satisfies:

1. decoded adjacent and cyclic states obey all source edge/vertex rules; and
2. re-encoding the decoded source reproduces the quotient data.

### Proof

The two local identities give a right inverse on every whole-plane quotient
configuration. Conversely, a finite-radius right inverse supplies those
identities on a bounded enlargement of its radius. \(\square\)

This is a certificate contract, not a decision algorithm for two-dimensional
factor injectivity.

## 6. Parity-selected distributed compiler

Let `A_ess` be the occurring source states. P0 positivity and macro completion
give a fixed 32-state subset `B`: the 30 addresses of one named occurring
large type `tau` in a witness `y_0`, plus the two small addresses.

Define

```
E = {(x,y,z) in {0,1,2,3}^3 : x+y+z = 0 mod 2}.
```

Choose a bijection `B -> E`. Enumerate every remaining state by `t` and map it
to a distinct fresh diagonal word `(f_t,f_t,f_t)`. Put one coordinate on each
directed side. A legal star must be one selected word, while decoded edge and
vertex states obey the source rules.

### Proposition 6.1 (K1P)

This distributed presentation has a radius-one exact source lift on its full
stated local-rule space. No individual base coordinate determines a state,
and the codeword image is non-Cartesian.

### Proof

The complete triple determines a unique state; source edge/vertex checks give
membership in `Y`; re-encoding is the identity, so K1T applies. Each base
coordinate occurs eight times on `E`. All coordinate projections contain
`0` and `1`, but `(0,0,1)` is absent from the code image, proving
non-Cartesianness. \(\square\)

This is information redistribution, not alphabet minimization.

## 7. Sharp local arity facts

Every unary and binary projection of `E` is full. Therefore no conjunction of
constraints seeing at most two visible side modes defines `E` (N5).

A central hidden variable can factor it. With `h=(p,q) in (Z/2)^2`, impose

```
p = x mod 2,
q = y mod 2,
z mod 2 = p+q.
```

Four hidden values suffice. Four are necessary because a product box
contained in even parity fixes each coordinate parity and covers at most one
of `000,011,101,110` (N6).

This symbolic factor does not provide a carrier state. Pure orientation only
permutes coordinates and preserves Hamming weight, so it cannot join the
weight-zero and weight-two patterns (N7). The bare triangular frame cannot
select an absolute `L/2L` residue because primitive `L` translations are
periods of the input but not of the coset coloring (N8). Combining the
unanchored residue with orientation reduces to the same orientation orbit
(N9).

## 8. Gauge-invariant boundary factorization

There is a better symbolic topology. Put a bit `q_i` at each corner of a
rooted triangular carrier, cyclically indexed. At every corner require the two
incident side modes either both to be base modes or to carry the same fresh
tag. On the base branch impose along side `i`

```
q_(i+1)-q_i = x_i mod 2.
```

### Proposition 8.1 (K2C)

Eliminating the corner variables gives exactly the complete K1P codeword set:
the base parity relation `E` plus all fresh diagonal words.

### Proof

Branch equality around the three-cycle gives either three base modes or one
common fresh tag. In the base case, summing the side equations telescopes and
forces even parity. Conversely, an even word integrates from either choice of
`q_0`; the two lifts differ by simultaneous gauge flip. \(\square\)

At a six-valent frame vertex, do not identify the six participant corner
bits. A common bit would force the two directed half-mode parities across
every edge to agree, which K1P does not establish.

### Proposition 8.2 (K2V)

Every K1P configuration lifts to sector-separated K2C corner potentials.

### Proof

Integrate each triangular face independently and retain its bit in its own
cyclic sector at shared vertices. No cross-face equation is introduced, so
all face relations hold simultaneously. \(\square\)

The raw base vertex decoration has at most `2^6=64` sector words before source
vertex legality is applied.

## 9. Conditional monotile theorem and blockers

Suppose a compact polygonal disk `P` satisfies K2J:

- bounded unmarked geometry exposes the sector states;
- two sides at one carrier corner read the same sector;
- every side contact realizes exactly the K2C transducer;
- every vertex, maximal segment, point contact and T-junction belongs to a
  complete stated atlas;
- one triangular frame and one handedness are forced; and
- the fixed source witness `y_0` lifts.

Then every `P`-tiling decodes through K2C/K1P/K1T/S0 to `X_beta`; reflection
uses the reflected decoder. Q0 excludes every nonzero translation period, and
the lift proves tileability. Thus `P` would be an aperiodic monotile.

No known polygon satisfies these hypotheses. Zipper and forked-corner
descriptions do not establish an unmarked sector invariant, complete contact
atlas, chirality or lift. K2J is therefore blocked and the geometric branch
is frozen.

Independently, SER0 is blocked: the arXiv source archive contains exact TeX
formulas but the construction geometry only as Illustrator PDFs, with no
address/SAB/vertex tables. Figure digitization would be a new reconstruction,
not direct serialization.

## 10. What is actually established

Closed as internal proof drafts:

- the exact composition selector P0;
- the O0/I0/D0 equal-support source argument;
- Q0 and K1T's no-spurious local-closure contracts;
- K1P's selected non-Cartesian safe code;
- N5--N9's scoped realization obstructions;
- K2C's exact boundary-holonomy factorization; and
- K2V's sector-separated symbolic lift.

Not established:

- an extensional machine-verified S0 table;
- novelty of the symbolic coding or cocycle arguments;
- a polygonal carrier or complete geometric contact atlas;
- an aperiodic monotile, surjectivity, or positive entropy.

## 11. Reopening conditions

The branch may advance only through one of two concrete inputs.

1. **SER0:** author-supplied exact tables, or a preregistered independently
   validated reconstruction of the source figures and rules.
2. **K2J:** an exact polygon or general geometric gadget lemma satisfying all
   visible-sector, transducer, contact-completeness, chirality and lift
   obligations before any search.

Neither a larger finite patch nor a more elaborate drawing changes these
conditions.
