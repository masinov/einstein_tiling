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

## 9. Pure-pose model

HC-08 first separates two claims that should not be conflated. Four abstract
hidden labels do not require an embedding of `H=(Z/2)^2` into the carrier's
rotation group: four selected poses could be named by four labels without
respecting either group law. The relevant question is whether the side-parity
relations arise equivariantly from one fixed boundary pattern.

Call an auxiliary encoding **pure intrinsic pose** when:

1. a reference carrier pose has one fixed parity triple
   `u=(u_0,u_1,u_2) in {0,1}^3` on its three rooted interfaces; and
2. every other admitted pose changes this triple only through the induced
   permutation of the three interface directions.

This model includes all rotations, and even allowing reflections only
enlarges the acting permutation group to a subgroup of `S_3`.

### ST-M1.N7 — pure-pose orbit no-go

No pure intrinsic pose encoding realizes all four parity patterns required by
K2H.

### Proof

Permuting coordinates preserves Hamming weight. Therefore the orbit of one
reference triple lies in one weight layer of `{0,1}^3`. K2H needs

```
000, 011, 101, 110,
```

which occupy the two distinct weight layers zero and two. No orbit of one
fixed triple under rotations—or even under all of `S_3`—contains both.
Hence it cannot equal the required four-state parity set. \(\square\)

N7 does not say that orientation can never contribute to a carrier state.
It says that rotations of one fixed intrinsic three-side pattern cannot be
the whole K2H mechanism. If one pose supports multiple parity patterns through
different neighbor docking configurations, the state is contextual rather
than pure pose and remains open.

## 10. Fixed core choice for G6

K1P's guaranteed 32-state core must be fixed once, not chosen separately in
each tiling. Choose one known S0 tiling `y_0`, one large macro type `tau`
occurring in it, and let `B` consist of that occurrence's 30 address types
plus the two small-macro address types. Define the parity code on this fixed
`B` and keep it fixed on all of `A_ess`.

G6 must lift a source tiling containing type `tau`; `y_0` is the intended
witness. Other S0 tilings need not contain `tau` for K1P or the total decoder
to remain defined. This closes the quantifier ambiguity without asserting
that both large types occur in every tiling.

## 11. The natural `L/2L` phase

Let `L` be the triangular translation lattice of the recovered frame. Its
index-four quotient

```
L/2L is isomorphic to (Z/2)^2
```

has the right cardinality and group structure for K2H. It does not, by
itself, give a local state of an unmarked carrier.

### ST-M1.N8 — unanchored lattice-coset no-go

There is no translation-equivariant local rule from the bare unmarked
triangular frame to its absolute `L/2L` coset coloring.

### Proof

Let `T_frame` be the bare frame. Every primitive `u in L` is a period:
`T_frame+u=T_frame`. If a translation-equivariant local map `d` produced the
coset coloring, then

```
d(T_frame)+u = d(T_frame+u) = d(T_frame).
```

Thus its output would have every `u in L` as a period. The `L/2L` coset
coloring has period lattice `2L`, not `L`; a primitive vector interchanges
cosets. Contradiction. \(\square\)

The same obstruction appears as gauge ambiguity. Integrating the natural
`L/2L` edge increments on a connected contact graph determines a vertex
phase only up to one global additive element of `L/2L`. Edge differences do
not choose an origin.

N8 does not rule out a carrier whose **additional** bounded contact geometry
breaks the fourfold ambiguity. In that event the phase is a contextual
star invariant, not a consequence of the triangular frame alone. The proof
must display the bounded geometric anchor and show that all four gauge shifts
cannot describe the same unmarked tiling with different K1P decodings.

## 12. What `L/2L` can and cannot contribute

An unobservable coset label cannot enforce the parity relation. If it is used
only as an existential proof variable, the visible three side modes must
already satisfy even parity, which is exactly the N5 obligation. If a bounded
star uniquely determines it, that star—not the abstract quotient—is the
geometric mechanism.

Consequently the natural quotient is useful vocabulary for a future anchor
but does not solve K2G. A valid design must add one locally visible feature
that distinguishes the four phases or replace the auxiliary route by a
genuine ternary exact-cover junction.

## 13. Combined frame-pose obstruction

Consider the complete “pose only” proposal in which the hidden phase is a
function of:

- the carrier's finite orientation class in the recovered triangular frame;
  and
- its absolute translation residue in `L/2L`, with no additional bounded
  landmark or contextual contact feature.

### ST-M1.N9 — unanchored frame pose is insufficient

No such translation-equivariant pose-only state realizes K2H's four parity
classes from one fixed intrinsic boundary pattern.

### Proof

Changing the arbitrary origin of the bare recovered frame changes the
`L/2L` residue by an arbitrary quotient element while leaving the unmarked
tiling and the carrier orientation unchanged. By N8's gauge argument, a local
geometric state must be well defined under every such origin change. It
therefore cannot depend on the unanchored translation residue. What remains
is a function of orientation alone.

The intrinsic side pattern of orientation-related copies lies in one
coordinate-permutation orbit. N7 shows that such an orbit cannot contain both
the weight-zero and weight-two K2H patterns. Hence the combined unanchored
frame pose also fails. \(\square\)

The scope matters. A carrier may have several locally visible docking offsets
relative to a contact frame; those offsets are additional contextual
geometry, not an absolute `L/2L` residue. N9 does not rule them out.

## 14. No free auxiliary variable

K2H's variable `h` reduces a ternary relation to pairwise constraints only if
one physical feature of the central carrier occurrence is shared by all three
interfaces. Formally, a geometric realization must provide a bounded,
translation-equivariant star map

```
eta : geometric rooted stars -> H
```

such that interface `i` physically enforces `R_i(eta,x_i)`. If `eta` is
introduced only after observing `(x_0,x_1,x_2)`, its existence is equivalent
to the parity relation itself and supplies no geometric enforcement. N5 then
remains the burden.

Thus the remaining options are exactly:

1. an independently visible four-class central star feature shared by all
   three interfaces; or
2. a genuine ternary or larger-radius exact-cover junction that enforces
   parity directly.

Pure intrinsic pose and unanchored lattice phase supply neither.

## 15. HC-08 disposition

The bounded pose-action question closes negatively. The group-embedding
argument suggested at admission was unnecessary; N7's orbit invariant and
N8's translation gauge combine into N9. The K2H factorization is still a
correct symbolic theorem, but it does not reduce the geometric task until an
actual shared four-class feature is identified.

K2G is frozen at this boundary. Reopening the exact-compiler route requires
an on-paper candidate for `eta` or for a ternary exact-cover junction and a
noncircular explanation of how one fixed unmarked boundary realizes it.
Increasing a collar radius, drawing notches, or searching contacts without
that mechanism is not authorized.

## 16. Boundary-cocycle candidate

HC-09 tests a different auxiliary topology. Retain K1P's base alphabet
`B_i={0,1,2,3}` on side `i`. Regard each remaining diagonal codeword
`(4+t,4+t,4+t)` as a distinct fresh tag `f_t`, disjoint from the base modes.
The full selected tile-star relation is

```
C = E union {(f_t,f_t,f_t) : t indexes a remaining state},
```

where `E` is the 32-word even-parity base relation.

Put a bit `q_i in Z/2` at each of the three corners of a rooted carrier,
with side `i` running from corner `i` to corner `i+1` cyclically. Impose:

1. at every corner, the two incident side modes are either both base modes
   or the same fresh tag;
2. on the base branch, side `i` satisfies
   `q_(i+1)-q_i = x_i mod 2`;
3. on a fresh branch, no corner bit is needed.

### ST-M1.K2C — exact cyclic factorization

Existentially eliminating the corner bits from these corner/side constraints
gives exactly `C`.

### Proof

The corner branch constraints around the three-cycle force either three base
modes or one common fresh tag. The latter case gives exactly a diagonal fresh
codeword.

In the base case, summing the three side equations around the closed boundary
gives

```
x_0+x_1+x_2 = 0 mod 2,
```

so the visible word lies in `E`. Conversely, for any word in `E`, choose
`q_0` arbitrarily and integrate the first two side equations. Even parity
makes the third equation close. There are exactly two lifts, related by the
global gauge flip `q_i -> q_i+1`. Thus the visible relation is precisely
`E`, and the two branches together give precisely `C`. \(\square\)

K2C neither changes nor repairs K1P; it factors the already valid full
codebook, including all diagonal extension states. It also does not
contradict N5 or N6: its auxiliary variables live on a three-cycle rather
than in N5's variable-free binary presentation or N6's single central-star
product-box form.

## 17. Why this candidate survives N7--N9

The `q_i` are contextual corner states, not intrinsic rotations. Their
simultaneous flip is a gauge symmetry, and every constraint depends only on
differences, so no absolute `L/2L` origin is selected. The same corner state
is shared by the two adjacent sides of one carrier, providing the physical
common variable whose absence made K2H circular.

This is still only a symbolic geometric interface specification. To count as
a K2G mechanism, one fixed boundary must make each `q_i` a locally visible
sector state at a six-valent frame vertex, make each side contact enforce the
difference equation, and admit no other point/segment contacts. HC-09's next
question is whether those sector states can remain independent enough at a
shared six-tile vertex to lift a K1P configuration.

## 18. Shared vertices: one bit or six sectors

At a frame vertex `v`, six triangular carriers meet. Their corner potentials
are initially six sector variables `q_(F,v)`, one for each incident face
`F`. They should not silently be identified.

If all sectors are forced to one common bit `Q_v`, then on an edge `vw`
shared by faces `F` and `G`, K2C gives

```
parity(x_(F,vw)) = Q_w-Q_v = parity(x_(G,vw)).
```

Thus common vertex bits require equality of the two directed half-mode
parities across every edge. K1P's code was selected on center states, and its
source edge rule does not establish this extra equality. It cannot be assumed.

If that equality were separately proved, the face parity equations would
make the common edge parities a closed `Z/2` one-cocycle. The simply connected
triangular plane would then integrate it to `Q_v`, uniquely up to global
flip. This is a useful conditional simplification, not the present case.

### ST-M1.K2V — sector-separated vertex lift

Every K1P configuration has a lift to corner potentials in which each
six-valent frame vertex retains the six incident sector bits separately.

### Proof

For every carrier face independently, use K2C to integrate its visible base
word to three corner bits, choosing either gauge; fresh diagonal faces need no
bits. At a shared frame vertex, retain the resulting participant bits with
their cyclic sector identities rather than identifying them. No equation from
one face changes a bit belonging to another face. Hence all face equations
hold simultaneously. \(\square\)

K2V is an existence statement for a finite decorated vertex language. A base
vertex has at most six binary sectors, so at most 64 raw bit words before the
source vertex rule removes illegal combinations. Fresh tags add finitely many
sector symbols because `A_ess` is finite. No occurrence enumeration is needed
for this finiteness claim.

## 19. Geometric consequence

The vertex gadget must be **sector-aware**. One shared point color is too
coarse unless half-mode parity matching is proved. A valid unmarked junction
must let the complete local geometry distinguish the participant/cyclic-order
sector record—exactly the kind of record O0 retained abstractly—while still
using one fixed carrier boundary.

This does not yet prove such a junction exists. It prevents a false shortcut
and leaves a finite exact target: locally visible sector words, side
difference checks, and the already stated source vertex legality.
