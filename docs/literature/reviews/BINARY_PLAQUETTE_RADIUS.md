# Binary plaquette and finite-radius audit for ST-M1.B0

**Date:** 2026-07-21

**Status:** primary-source audit in progress under HC-12; no experiment or
geometric construction

## Question and radius vocabulary

The K3B square-diagonal mechanism assigns one bit to each forced square
macrocell.  Three distinct radii must not be conflated:

1. **rule support**: the finite set of bit positions inspected by one allowed
   pattern;
2. **decoder radius**: the finite neighborhood needed to recover a colored
   source state; and
3. **geometric visibility**: the macrocells whose bits one contact or vertex
   gadget of the unmarked polygon can jointly constrain.

An arbitrary large decoder radius does not help when the complete geometric
language enforces only nearest-neighbor or one-corner rules.  Conversely, a
large rectangular rule support can remain binary and need not introduce more
physical prototile shapes.

## Exact substrate identification

The K3F flag carrier is exactly the repository's primitive kite cell after a
uniform scale, not merely a qualitatively similar quadrilateral.

For a cell `(C,M_{d-1},V_d,M_d)`, `substrate/kitegrid.py` gives angles
`60,90,120,90` and cyclic side lengths

```
sqrt(3), 1, 1, sqrt(3).
```

K3F gives angles `60,90,120,90` and lengths

```
1, 1/sqrt(3), 1/sqrt(3), 1.
```

Multiplication by `sqrt(3)` makes the two ordered metric polygons identical.
The existing integer hex-coordinate substrate, its full `D6` action and its
published-coordinate anchors therefore apply directly to the undeformed flag
scaffold.

This observation has two opposite consequences.  It makes later exact
geometry cheap, but any candidate that remains a union of at most 24 such
kites lies inside the published finite polykite horizon.  A free boundary
deformation or contextual retiling gadget is not automatically a polykite and
is not excluded by that horizon.

## Sources admitted to the audit

- `hu-lin-two-color-square-2011`: the peer-reviewed two-color corner- and
  edge-coloring nonemptiness theorem;
- `kari-moutot-low-complexity-2023`: the peer-reviewed binary rectangular
  recoding theorem and its exact local-closure lemma;
- `jeandel-rao-wang-2021`: the sharp 11-tile/four-edge-color Wang lower bound,
  used only to distinguish ordinary edge-colored Wang systems from binary
  corner plaquettes.

The theorem consequences and HC-12 decision are completed in the following
sessions.  No enumeration of the `2^16` binary plaquette rule sets is needed:
Hu--Lin already settle that class.

## N11: the immediate `2x2` binary language is impossible

Let `P` be any subset of the sixteen binary `2x2` blocks and let

```
X_P = {x in {0,1}^{Z^2}: every translated 2x2 block of x belongs to P}.
```

This is exactly Hu--Lin's two-color **corner-coloring** system
`Sigma(B_c)`: their colors occupy lattice vertices, and each unit square is
one allowed four-corner block.  Theorem 2.3 and its conclusion on pp.
1050--1051 prove

```
X_P nonempty  =>  X_P contains a doubly periodic configuration.
```

The proof classifies 17 minimal cycle generators and 56 maximal noncycle
sets; every maximal noncycle set already fails on a `5x4` rectangle.  This is
stronger than decidability and is precisely the statement B0 needs.

### ST-M1.N11

No nonempty binary `2x2` square-plaquette SFT is strongly aperiodic.
Consequently there is no total translation-equivariant period-reflecting map
from such an SFT to the aperiodic S0 language.

Indeed, Hu--Lin supply a periodic `x in X_P`.  If a map to S0 were total and
period-reflecting, its image would inherit nonzero periods, contradicting S0.
Thus the immediate B0 formulation in theory note 17 is refuted without a
`2^16` rule-set census.

This result is about binary **corner** blocks.  Jeandel--Rao's sharp lower
bound concerns ordinary edge-colored Wang tiles: an aperiodic Wang set needs
at least 11 tiles and four edge colors.  Translating a binary `2x2` block to
its four overlapping binary-pair edge colors uses four colors and at most 16
tiles, so the Jeandel--Rao count alone would not exclude it.  Hu--Lin's
special corner theorem does.

Primary anchors:

- Hu--Lin, Definition 2.1 and Theorem 2.3, pp. 1048--1051,
  DOI `10.1090/S0002-9939-2010-10518-X`; archived primary PDF cached as
  `data/literature/papers/2011-hu-lin-two-color-square-tiling.pdf`, SHA-256
  `3f46f0e8f483f87a852f90bc28c0a51a0c798682ff1b4de4e50b1af09b7d5bbd`;
- Jeandel--Rao, abstract and minimality theorem,
  DOI `10.19086/aic.18614`.

## N12: binary finite-radius encoding survives

Hu--Lin do not prove that every binary SFT is periodic.  Kari--Moutot give the
opposite existence result at larger rectangular support.

Their Theorem 9 starts from any finite Wang set `T`.  After a checkerboard
doubling that prevents self-neighbor matches, let `t` be the resulting tile
count, `s=2^(t-1)` and `N=3s`.  For every width `n>=N` and every height `m>=2`
they effectively construct allowed binary `n x m` patterns `P`.  Lemma 25 is
the crucial full-closure statement:

```
V(P) = { translate(beta(c)) : c is a valid T-tiling }.
```

Every `1` in `beta(c)` identifies one Wang tile by its horizontal offset in a
sparse, locally recognizable rectangular scaffold.  Hence the construction
preserves nonemptiness and preserves existence of a periodic configuration
in both directions.  Corollary 12 applies it to an aperiodic Wang set and
obtains a strongly aperiodic binary rectangular SFT; height `m=2` is allowed
once the width is sufficiently large.

Here the paper defines `S={2^j-1 : 0<=j<=t-1}` and takes `s` to be its
largest ambient index, `2^(t-1)`. The earlier review transcription `2^t-1`
conflated the set elements with this maximum; the distinction is not
load-bearing for N12 but is corrected here at attribution level.

### ST-M1.N12

Every finite two-dimensional SFT has an effective binary rectangular cover
with exact full local closure and preservation of whether periodic points
exist.  In particular, conditional on the extensional S0 presentation, a
binary period-reflecting encoding of S0 exists at some finite rectangular
support.

The last sentence uses the standard conjugate conversion of a finite SFT to
Wang tiles stated in Kari--Moutot Section 2.3, followed by Theorem 9 and Lemma
25.  Their sparse encoding is a rectangular inflation, not a unit-scale
sliding-block conjugacy to `T`.  Locally recognizing its phase gives a finite
decorated lift of the coarse Wang tiling; that lift is the correct intermediate
object for a later geometric decoder.  A direct unit-scale map to K3F is not
claimed here.

The displayed exponential `N` is an existence bound, not an efficiency
claim.  The paper notes that Sidon/Mian--Chowla positions reduce the coding
growth, but no numerical bound can be instantiated for S0 while SER0 lacks
the extensional source alphabet and rule table.

Primary anchors:

- Kari--Moutot, Section 2.3 (finite SFT to conjugate Wang presentation),
  Theorem 9, Lemmas 23--25 and Corollary 12,
  DOI `10.1007/s00224-021-10063-8`.

## The actual radius boundary

| binary rule support | theorem-level status | implication for K3B |
|---|---|---|
| independent horizontal/vertical pairs | periodic product whenever nonempty (repository N1) | impossible |
| one `2x2` corner plaquette | periodic configuration whenever nonempty (Hu--Lin/N11) | impossible if bits are the complete state |
| `n x 2`, sufficiently large `n` | strongly aperiodic examples exist (Kari--Moutot/N12) | symbolically possible; no direct geometric reader |
| arbitrary finite support | generic binary encoding possible via the same construction | symbolically possible; efficiency and geometry open |

The smallest width of a strongly aperiodic binary height-two rectangular SFT
is not established by the audited sources.  It must not be guessed from the
`2x2` no-go or from the very large constructive upper bound.

## Geometric interpretation: SFT versus sofic projection

Theory note 17 originally said that the physical K3B language “projects to a
binary square-plaquette SFT.” That is true only if the diagonal bit is the
complete macro state. A finite contact atlas may contain locally visible
docking states `Y`; forgetting them gives a binary **sofic** shift `b(Y)`,
which need not be characterized by its allowed `2x2` bit blocks. N11 then
does not apply to `Y`, and `b(Y)` itself need not carry the source decoder.

This is not a loophole that permits post-hoc colors. Every hidden state must
be a bounded function of the unmarked geometry before source legality is
tested. If the complete macro language is ordinary Wang edge matching,
Jeandel--Rao impose at least 11 visible macrostates and four interface colors.
For two diagonal retilings and at most `h` docking modes per diagonal this
gives `h>=6` (ST-M1.N13).

## HC-12 decision

### Permitted claims

- the flag carrier is exactly the existing kite substrate up to scale;
- bit-only `2x2` B0 is impossible by Hu--Lin;
- larger binary rectangular aperiodic SFTs exist by Kari--Moutot;
- a hidden-state edge-Wang compiler needs at least 11 macrostates and four
  interface colors by Jeandel--Rao;
- K4W in theory note 18 is a sufficient contract for turning any fixed
  aperiodic Wang set into one shape-only monotile.

### Forbidden claims

- that a binary or 11-state unmarked polygon has been constructed;
- that the smallest surviving binary rectangle is known;
- that Kari--Moutot supply a unit-scale K3F decoder or a geometric carrier;
- that every sofic binary projection is aperiodic;
- that K4W's factor/period-descent theorem schema is novel.

### Research decision

Do not synthesize a guard for the two-state bit-only diagonal kernel: its
target language is refuted. Do not instantiate the generic long-strip
encoding while SER0 is unavailable. The most focused surviving “happy idea”
route is the K4W internal multi-retiling problem: one common macrocell, at
least 11 exact rooted retilings by one polygon, and boundary subdivisions that
realize four Wang colors. This is an on-paper inverse-dissection question
before it is a search problem.
