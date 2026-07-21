# Single-tile simulation and the K5C boundary

**Audit date:** 2026-07-22

**Question:** do published single-tile, small-polyomino, marked-tile or
corner-tile constructions already supply K5C's closed-corridor compiler, and
what geometric obligation—if any—remains available for research?

## Decision

The symbolic compiler is prior art.  Encoding a finite tileset by a selector,
propagating its interfaces through wires, recoding colored edges as boundary
geometry, and proving that every admitted configuration decodes are all
present in the audited literature.  K5C's prefix trie and length-42 word are a
convenient specification, not a new simulation method.

No audited source supplies the conjunction K5C actually needs:

1. one connected unmarked planar polygon;
2. ordinary gapless coverage of the plane, with no prescribed lattice, seed,
   atlas, colors, magnetic/growth rule or finite-group fibre;
3. copies admitted by the declared Euclidean isometries; and
4. a total finite-radius decoder on **every** shape-only tiling.

This leaves one legitimate target: a geometric lemma that closes that exact
gap.  Merely replacing K5C's trie by another finite automaton, zipper, wire or
corner relation is redundant.  HC-14 may therefore examine one exact
boundary-forcing mechanism for K5C.1--K5C.3.  If it cannot prove bounded
cycles, pre-decoding state visibility and contact completeness, the cyclic
corridor route closes without enumeration.

## Source-by-source findings

### Greenfeld--Tao: one equation via an auxiliary fibre

`greenfeld-tao-periodic-counterexample-2024` proves an aperiodic single
translational tiling equation in `Z^2 x G_0`, with `G_0` a finite abelian
2-group.  Theorem 3.1 is the relevant compiler: a finite system

```text
A + F_m = G  for m=1,...,M
```

is concatenated into one tile

```text
F_tilde = disjoint_union_m (F_m x E_m)
```

using a rigid partition of a finite cyclic fibre.  Thus “many constraints can
be compiled into one tile” is not a novel abstract claim.

The result does not provide K5C geometry.  Its extra finite-group coordinate
stores the selector state.  The Euclidean consequence occurs in sufficiently
high dimension, and the resulting measurable tile is a finite union of cubes
that need not be connected.  Section 10.2 explicitly leaves an open connected
version.  This is not a connected planar polygon under rotations/reflections.

Primary anchors: Theorem 1.4, Theorem 3.1 and equation (3.4), and Question
10.3.  Cached PDF SHA-256:
`1bae5cc27ae45095636ca71b2dc5f031aa970edcdd79039660081bf8335addbd`.

### Ollinger: the selector-and-wire architecture already exists

`ollinger-fixed-polyominoes-2009` converts an arbitrary Wang set into five
dented-polyomino roles:

- a **meat** concatenates every source tile code;
- a **jaw** selects exactly one code;
- **teeth** erase the unselected bit profiles;
- **filler** closes the unused jaw area; and
- **wires** propagate the four selected colors.

Lemma 3 constructs a polyomino tiling from every Wang tiling.  Lemma 4 proves
the all-tilings converse: markers force bi-infinite jaw/meat lines, wires force
a lattice of selected diamonds, and prefix/suffix codes force a common
orientation.  Theorem 3 obtains undecidability with five polyominoes under
isometries; Theorem 4 replaces the used poses by eleven polyominoes for
translation-only tiling.

This is the closest structural predecessor of K5C.  K5C's “word containing all
source states + local selector + four interface wires” is not method-novel.
Ollinger still uses five noncongruent functional supports (or eleven fixed
poses as separate supports), and its forced components are bi-infinite lines,
not one connected unmarked polygon partitioned into finite cycles.

Primary anchors: Theorems 3--4 and Lemmas 3--4.  Cached PDF SHA-256:
`9d2928ae05e786f6424351ce21c5afab33d72d7d6239a0e04cbe434fb801a321`.

### Demaine et al.: one polygon, but a near-plane model

`demaine-et-al-one-tile-2014` is even closer to the advertised endpoint.
Its full version encodes tile identities in rotations of one many-sided
polygon and colors/glues by bump-and-dent profiles.  Theorem 7.1 converts
colored square or hexagonal systems into a one-tile simulator; Section 7.2
instantiates a Robinson aperiodic source.

The model boundary is explicit in the source.  A valid simulator tiling is
required to put one tile at every site of the source square/hexagonal lattice,
to use prescribed lattice adjacencies, and to match the designated sides.
The polygons do **not** cover the plane: the paper calls the result
“nearly-plane” because small gaps remain.  Its self-assembly theorem also uses
a seed and attachment dynamics, which are not ordinary tiling hypotheses.

Accordingly, this paper preempts a broad claim that orientation plus boundary
profiles can make one puzzle piece simulate arbitrary local states.  It does
not prove that the same piece is a connected gapless monotile in the ordinary
Euclidean sense.  Eliminating the gaps and the prescribed lattice is exactly
an all-tilings theorem, not a cosmetic thickening.

Primary anchors: the plane-tiling definition in Section 2.4 and Theorem 7.1
with its “nearly-plane” construction.  Cached full-version PDF SHA-256:
`df7ac932ae293ea59a5883a831aa346ce4e1960da98068990115cd0296483355`.

### Socolar--Taylor and Ammann A2: what boundary geometry can force

`socolar-taylor-hexagonal-2011` gives a single marked hexagon with two rules.
The first propagates stripes across contacts; the second compares flags on
tiles separated by an intervening edge.  The planar shape-only realization
uses disconnected satellite components to enforce the remote rule.  A
simply-connected shape-only realization is supplied in three dimensions,
where height carries the missing channel.  The paper explicitly distinguishes
these from the desired connected planar shape-only tile.

`akiyama-ammann-2012` proves aperiodicity for two similar Ammann A2 polygons
under an edge-to-edge equal-length rule.  Boundary subdivision, ghost marks
and a finite interface analysis establish unique composition into enlarged
copies.  This preempts novelty for boundary subdivisions and unique-grouping
proofs; it neither merges the two supports nor compiles an arbitrary finite
automaton into one unmarked support.

Primary anchors: Socolar--Taylor rules R1--R2 and its planar disconnected/
three-dimensional constructions; Akiyama Theorem 1 and the ghost-marking
unique-composition proof.  Cached PDF SHA-256 values:
`2c457370be695692875897b1779adf80072a18ea9935372318dc4d8f2c907f33`
and
`8e709590b183033819c02abe0304054870663cb5caad010c4348bd3589e33abc`.

### Lagae--Kari--Dutre: the exact 44/6 source

`lagae-kari-dutre-corner-2006` is the source of the 44-tile/six-color system
mentioned by Hu--Lin.  It is constructed from a 16-Wang-tile/six-color set by
the horizontal (equally, vertical) translation conversion.  Figure 3 and
Table 1 record `44/6`.  The paper constructs conversions in both directions
between edge-Wang and corner presentations and transfers aperiodicity.

Therefore K5Q cannot claim a new aperiodic corner-source reduction, and
`44/6` is not a minimality theorem: it is the smallest corner set the authors
report constructing.  The objects remain 44 colored square types; the paper
does not erase the relation into one unmarked polygon.

Primary anchors: Section 3, Figure 3 and Tables 1--2.  Cached PDF SHA-256:
`b2f136a499b369b7ce6cce26a5b087f7eb4f22eeff0227bec57a3448504a857f`.

### Atlas and dendrite boundaries

`fletcher-atlas-2010` shows that orientations of congruent supports can encode
tile types when a finite allowed-corona atlas is imposed.  It reduces thirteen
planar Wang squares to two square supports and twenty-one Wang cubes to one
cube, preserving MLD.  The atlas is an external matching rule, not a property
of unrestricted shape-only tilings.

`mampusti-whittaker-dendrite-2020` is especially relevant to cycle language.
Its first adjacent-tile rule can be encoded by shape, while its dendrite rule
requires the union of marked trees to remain globally connected during seeded
growth.  The authors explicitly state that the latter is not local as a rule
on completed tilings and that their object is not an einstein in the technical
sense.  It proves that a global graph condition can exclude cycles, not that a
single unmarked boundary can locally force K5C's finite cycles.

Cached PDF SHA-256 values:
`c0089272382f4e8773bca02ae7db7c8ece0e621cb4d1ad2a944e420509fd09fb`
and
`1950026f57a65087a8264aa9bc7958255619cfd62c0f97642466991209835bda`.

## Mechanism crosswalk

| K5C obligation | closest audited mechanism | what is already known | residue |
|---|---|---|---|
| K5C.1 bounded disjoint cycles | Ollinger forced lines; Mampusti dendrite/cycle exclusion | boundary roles can force graph-like global organization with several supports or an external growth rule | one unmarked support must force finite cycles in every gapless tiling |
| K5C.2 visible bits/root | Socolar--Taylor/Ammann boundary marks; Demaine rotations | boundary profiles and poses can expose finite states in constrained models | state must be recoverable before source decoding, with no color/lattice/atlas |
| K5C.3 exact selector transitions | Ollinger meat/jaw trie-like selector; Greenfeld--Tao rigid fibre | finite systems and finite codebooks can be selected and concatenated | one connected planar boundary must implement the selector without extra roles/fibre |
| K5C.4 rooted windows | ordinary finite automata and delimiter codes | combinatorially routine | the root must be a geometric equivariant feature, not a post-hoc origin |
| K5C.5 interface matching | Wang-to-jigsaw conversions; Lagae--Kari--Dutre | finite edge/corner interfaces are standard | no unintended full-isometry contacts or vertex faults |
| K5C.6 fill and lift | all cited construction proofs in their own models | existence and converse must be separate | exact gapless equal-count fill by the same polygon plus a whole-plane witness |

## What HC-14 may and may not claim

Permitted:

- K5C is a precise test instance for the still-open geometric erasure step;
- Ollinger already gives the selector/wire/all-tilings architecture with five
  functional polyomino roles;
- Demaine et al. already give a one-polygon orientation compiler in a
  lattice-constrained near-plane model with gaps;
- Greenfeld--Tao give an abstract one-equation concatenation using a finite
  group fibre;
- no audited source supplies the four-part gapless connected planar theorem
  stated in the decision above.

Forbidden:

- “K5C is a new general compiler”;
- “the prefix-trie selector, zipper, wire, delimiter or corner conversion is
  novel”;
- “Demaine's single puzzle piece is already an ordinary Einstein”;
- “Greenfeld--Tao solve the planar connected monotile encoding problem”;
- “44/6 is a lower bound”;
- any claim that absence in this dated audit proves no construction exists.

## Dated searches

Primary-source searches on 2026-07-22 included:

- `single tile simulate Wang tiles puzzle piece plane gaps`;
- `single prototile Wang system geometric encoding rotations`;
- `aperiodic monotile matching rules shape alone dendrite`;
- `polyomino Wang selector wire jaw meat`;
- `44 tiles 6 colors corner tiles horizontal translation`;
- `translational monotile one tiling equation finite group fibre`.

They located the sources above and recent surveys, but no theorem removing the
identified gaps/lattice/atlas/fibre/extra-support hypotheses.  This is a dated
absence report, not evidence of novelty by itself.

## Stop rule

One on-paper mechanism may now be tested against K5C.1--K5C.3.  It must name
the exact boundary contacts and prove, rather than assume, finite-cycle
closure, independently visible transition state, and exclusion of every
unintended contact.  Failure within HC-14's remaining two sessions closes the
cyclic-corridor route.  No boundary enumeration, SAT run, drawing or candidate
promotion follows from this audit.

## HC-14 mechanism outcome

Theory note 20 applies the stop rule. N17 refutes a one-head/one-tail
order-42 rosette: its successor rotation acts transitively, forbidding a
unique root or nonconstant word. N18 shows that disjoint option ports are all
contacted in a gapless tiling, and N19 bounds one full polygonal arc pair to
at most four rigid alignments. No explicit multiplexed arc supplied bounded
42-cycles, exact eleven-word acceptance and a pre-decoding state. The kill
therefore fires after session 99; K5C is frozen under reopening contract
R1--R5, without an experiment.
