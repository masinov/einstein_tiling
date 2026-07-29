# ST-M1.K3B — binary square-retiling kernel

**Date:** 2026-07-21

**Status:** concrete two-retiling control and conditional guarded mechanism;
no candidate polygon, source decoder, contact-completeness proof or novelty
claim

## 1. Exact retiling kernel

Let

```
T = {(x,y): x>=0, y>=0, x+y<=1}
```

be the unit right-isosceles triangle and let `M=[0,1]^2`. Two congruent copies
of `T` tile `M` along the diagonal `x+y=1`. Rotating the construction by 90
degrees gives the other diagonal. Thus the same unmarked support has two
rooted exact retilings of one square macrocell, denoted `/` and `\`.

The straight triangle is not a candidate: it has many periodic tilings and
does not force square grouping. Its role is to prove that contextual state by
macro retiling is geometrically possible before boundary guards are added.

## 2. Unique-pairing implication

Name the hypotenuse boundary `H` and the two leg boundaries `L_0,L_1`.
Consider a polygonal deformation `P` of `T` satisfying:

- every occurrence of `H` in every `P`-tiling has exactly one full `H`
  counterpart and no partial, subdivided or point-only alternative;
- the paired copies have disjoint interiors and their union is one copy of a
  fixed square-like macrocell `M_P`;
- the two diagonal pairings give congruent copies of the same rooted `M_P`,
  with boundary subdivisions recording which diagonal was used; and
- leg and corner contacts form a finite complete atlas and force the `M_P`
  copies onto one edge-to-edge square frame, including the reflected branch.

### ST-M1.K3B

Under these guard hypotheses, every `P`-tiling has a unique finite-radius
partition into `M_P` cells, each carrying one binary diagonal state.

### Proof

Each physical occurrence has one `H`. Exclusive full `H` pairing makes the
graph of `H` contacts one-regular, so it partitions occurrences into unique
pairs. By the second and third hypotheses each pair is one rooted macrocell
with one of the two diagonal states. The complete leg/corner atlas supplies
the common square frame and rules out another pairing or a fault component.
All data are visible in the one-neighborhood of a pair. \(\square\)

This is a conditional implication. No boundary word satisfying all guard
hypotheses has been constructed.

## 3. Where constraints can live

The diagonal state changes which physical triangle owns each macro side and
whether a macro corner contains one `90`-degree tip or two `45`-degree tips.
Consequently a guarded leg contact can constrain two adjacent bits, while a
complete macro-corner star can constrain the four bits of the incident
square cells. If these bits are the complete macro state, the full geometric
language is therefore a binary square-plaquette SFT, not merely three
independent one-dimensional rails. In general this needs the HC-12
qualification: a finite physical contact language can retain hidden docking
states, and its bit projection is then only guaranteed to be **sofic**, not an
SFT determined by its observed `2x2` blocks.

This evades the fixed-fusion objection and, in principle, the independent-
rail no-go. It does not show that the resulting binary system is aperiodic or
can decode K3F.

## 4. Symbolic feasibility obligation B0 (refuted in its immediate form)

Before synthesizing a boundary, one must exhibit a finite binary local
language `Z_B` and a total finite-radius map

```
Z_B -> K3F -> S0
```

on the complete binary local closure. The geometry must then realize exactly
`Z_B`, not a sampled subsystem. This is B0.

The 32-state K1P core does not require 32 isolated physical shapes: a
radius-`r` binary neighborhood can encode many states. But alphabet
compression is useful only if synchronization and no-spurious-configurations
are proved. A generic statement that finite alphabets can be binary encoded
does not supply a shape-only square-plaquette realization.

No B0 compiler is claimed. The existence and minimum radius of strongly
aperiodic binary plaquette systems, and their relation to standard higher-
block encodings, require a primary-source audit before any enumeration.

HC-12 completed that audit. Hu--Lin prove that every nonempty binary `2x2`
corner-plaquette SFT contains a periodic configuration, so the bit-complete
B0 written above is impossible. Kari--Moutot prove that sufficiently long
binary rectangular rule supports can encode arbitrary Wang systems with exact
full closure and preservation of periodic-point existence. The surviving B1
route must therefore expose a larger neighborhood or retain independently
visible hidden docking states. See
`docs/literature/reviews/BINARY_PLAQUETTE_RADIUS.md` and theory note 18.

## 5. Superseded boundary-word problem

HC-11 proposed the following bounded inverse problem if B0 survived: choose a
maximum number `N` of rational polygonal segments for `H,L_0,L_1` and solve
simultaneously for:

1. both exact diagonal retiling identities;
2. unique full `H/H` pairing;
3. the prescribed binary leg and corner relations;
4. no unintended partial alignment, T-junction or continuous slide; and
5. a reflected or homochiral full-isometry decoder.

For a fixed `N`, primitive segment/vertex incidences are finite, but that does
not by itself prove whole-plane contact completeness. The preregistration
would have to state the exact guard lemma or exact-real-algebraic certificate
that turns those incidences into R1--R4.

N11 means this bit-only synthesis must not be run. Theory note 18 replaces it
with K4W: at least 11 visible Wang macrostates and four interface colors, or a
non-Wang larger-support contract stated before geometry.

## 6. HC-11 disposition

The diagonal-square kernel is the first concrete contextual-retiling
mechanism produced by the branch. It supplies `M`, `m=2`, two exact retilings
and the locations where boundary and corner modes can live. It does **not**
supply the two load-bearing results:

- a polygonal guard satisfying unrestricted K3B contact completeness; or
- a B0 binary local language with a total decoder to K3F/S0.

Therefore HC-11 admits no geometry run. K3G remains frozen. The efficient
next decision is a literature-and-mathematics audit of B0, followed—only if
B0 survives—by a separately preregistered bounded boundary-word synthesis.
