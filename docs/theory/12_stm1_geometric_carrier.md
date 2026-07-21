# ST-M1.K2G — exact geometric carrier contract

**Date:** 2026-07-21

**Status:** exact-realization contract and arity obstruction proved in draft;
no polygon or geometric existence claim

**Scope:** the parity-selected symbolic compiler K1P; full Euclidean
isometries; proof design only

## 1. Why K2G uses a stronger target than minimal ST-M1

Minimal ST-M1 only asks every shape tiling to map into some nonempty
aperiodic source subsystem. It does not require every K1P state or source
tiling to lift. N4 therefore cannot be advertised as a necessary condition
for every possible Sturmian monotile.

K2G deliberately studies the stronger **exact compiler realization**:

1. every geometric carrier tiling has a finite-radius K1P decoding;
2. every primitive geometric contact and rooted star belongs to a finite
   stated atlas;
3. the extendable rooted star language is exactly the selected K1P language;
4. at least one source tiling containing the guaranteed 32-state core lifts.

This strength makes the construction auditable and makes K1P/N4 applicable.
Failure would close this exact-compiler route, not minimal ST-M1 in all
possible forms.

## 2. Exact carrier obligations

For one compact polygonal topological disk `P`, K2G consists of the following
finite statements.

- **G1 — frame and contact completeness.** Every `P`-tiling has one locally
  recoverable three-direction triangular frame. Its tile-contact graph is
  connected and locally finite. Every maximal interface, point contact,
  subdivided segment and T-junction belongs to a stated finite exact atlas;
  continuous sliding and unrecorded contacts are impossible.
- **G2 — mode extraction.** Each of the three directed interfaces incident
  with a rooted carrier occurrence has one finite K1P mode. The extraction is
  invariant under translation and equivariant under rotations and reflection.
- **G3 — exact star relation.** The extendable rooted mode triples are exactly
  the selected K1P codewords. In particular the 32 parity-core words occur
  and every odd-parity core word is excluded.
- **G4 — overlap legality.** Modes decoded at adjacent occurrences satisfy all
  K1P edge and vertex rules. Re-encoding returns the same geometric modes, so
  K1T applies on every carrier tiling.
- **G5 — chirality.** Every admitted contact joins equal determinant classes,
  and connectedness propagates one sign globally. The other global branch is
  handled by the reflected decoder.
- **G6 — lift.** At least one S0 tiling containing the selected 32-state core
  has an exact `P`-tiling lift.

G1--G6 imply C1--C5 of the conditional carrier theorem in note 07 and hence
minimal ST-M1. They still do not imply surjectivity or positive entropy.

## 3. Pairwise projections of the parity core

Write

```
E = {(x,y,z) in {0,1,2,3}^3 : x+y+z = 0 mod 2}.
```

Every two-coordinate projection of `E` is the full square
`{0,1,2,3}^2`. Indeed, after fixing any two entries, there are two choices
of the required parity for the third entry. Every one-coordinate projection
is likewise full.

### ST-M1.N5 — binary-corner no-go

No conjunction of constraints, each of which sees at most two of the three
side modes, has `E` as its exact solution relation.

### Proof

Suppose `R` is defined by unary and binary constraints and contains `E`.
Every unary constraint must accept the full one-coordinate projection of
`E`, and every binary constraint must accept the full two-coordinate
projection. Hence none of those constraints removes any word of the full
cube. Therefore `R={0,1,2,3}^3`, which also contains all 32 odd-parity words.
Thus `R` cannot equal `E`. \(\square\)

## 4. Geometric consequence

A construction made only from independent side keys and ordinary corner
checks comparing the two adjacent side modes cannot satisfy G3. Pairwise
neighbor contacts around the carrier do not help if each such contact sees
only its adjacent pair: the parity relation is not binary-decomposable.

An exact K2G construction must therefore expose at least one of the following
mechanisms explicitly:

1. a junction whose exact-cover condition simultaneously depends on all
   three incident modes;
2. a finite auxiliary phase carried by the rigid placement and recovered
   locally, with pairwise constraints whose existential elimination gives
   exactly `E`;
3. a larger-radius geometric rule proved to exclude every odd word from all
   whole-plane tilings, together with a proof that this is not merely sampled
   nonoccurrence.

Calling any two-edge notch a “corner coupler” is no longer sufficient.
The construction must state which variable or junction carries the missing
third-order information.

## 5. Claim boundary

Established:

- an exact G1--G6 contract sufficient for the selected compiler route;
- K1P's parity core has relational arity at least three without auxiliaries;
- side-local and binary-corner-only realizations cannot meet G3.

Not established:

- that every possible carrier must realize the full K1P language;
- that an auxiliary-phase or ternary-junction polygon exists;
- a finite geometric contact atlas;
- chirality, lifting, a monotile, or positive entropy.

The next on-paper question is whether a translation-equivariant auxiliary
phase can carry the parity check without smuggling in an absolute lattice
origin. If it cannot, the selected exact-compiler route should close before a
shape is drawn.

## 6. Four-state auxiliary factorization

An auxiliary phase can remove the arity-three obstruction at the symbolic
level. Let

```
H = Z/2 x Z/2,
h = (p,q).
```

Use three binary phase/interface relations

```
R_0(h,x) : p = x mod 2,
R_1(h,y) : q = y mod 2,
R_2(h,z) : z mod 2 = p+q mod 2.
```

Then

```
(x,y,z) in E  iff  there exists h in H with
R_0(h,x), R_1(h,y), and R_2(h,z).
```

The forward direction chooses `h=(x mod 2,y mod 2)`; the reverse direction
sums the three displayed congruences. Thus a tile-centered four-state hidden
phase is sufficient to factor the ternary parity check into three pairwise
phase/interface checks.

### ST-M1.N6 — four auxiliary states are necessary

Any representation of `E` in the star form

```
E = union over h in H of A_h x B_h x C_h
```

needs at least four nonempty product boxes.

### Proof

Reduce each coordinate to even/odd parity. A nonempty product box contained
in the even-parity relation cannot contain both parities in any coordinate:
holding one choice in the other two coordinates fixed would then include one
even and one odd total. Hence each box covers at most one of the four even
parity patterns `000,011,101,110`. All four occur in `E`, so at least four
boxes, and therefore at least four auxiliary values, are necessary. The
construction above attains the bound. \(\square\)

## 7. Gauge condition

The symbol `h` cannot be painted on the carrier. It must be a locally
distinguishable state of one rigid unmarked occurrence—for example a finite
pose/contact-star class. Nor may it be an absolute residue relative to a
chosen lattice origin.

More precisely, suppose a proposed phase is obtained only by integrating
finite edge increments on the connected contact graph. Such an integration
determines vertex phases only up to a global additive constant. If the
geometry and observed side modes are unchanged by that global gauge shift,
then a non-gauge-invariant value of `h` is not locally determined and cannot
serve as a geometric state. Either:

- the four phase classes must be fixed by a bounded geometric star;
- the decoder and all relations must depend only on gauge-invariant phase
  differences; or
- an explicit geometric landmark must break the gauge in a
  translation-equivariant way.

An externally chosen origin is none of these. This is a well-definedness
condition, not a no-go against all auxiliary phases.

## 8. HC-07 disposition

The auxiliary route survives symbolically and has an exact cost: four hidden
states are necessary and sufficient for the K1P parity core. Geometry is
still wholly open. K2G must realize at least four locally distinguishable
phase/star classes of one fixed carrier, couple them to the three side modes,
and satisfy G1--G6. A global coordinate residue does not count.

HC-07 ends here. No polygon should be drawn and no contact atlas searched
until a new checkpoint authorizes an on-paper analysis of which finite pose
actions of one carrier could realize `H` compatibly with homochirality and the
triangular frame.
