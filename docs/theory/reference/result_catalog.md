# Integrated result catalog

**Purpose:** compact navigation across the durable mathematics
**Exhaustive row-level authority:** [proof ledger](proof_ledger.md)
**Historical coverage:** [source map](SOURCE_MAP.json)

This catalog groups equivalent and dependent result IDs into mathematical
families.  It does not erase narrow results: every individual identifier,
scope, artifact and correction remains in the proof ledger and source notes.

Status abbreviations:

- `PD` — internal proof draft;
- `MV` — machine-verified finite proposition;
- `EXT` — external theorem;
- `COND` — conditional theorem or construction contract;
- `OPEN` — unresolved;
- `CLOSED` — refuted or classified at the displayed scope;
- `CTRL` — exact control on a published system.

## 1. Foundations and certificate theory

| Integrated result | IDs | Status | Scope / value |
|---|---|---:|---|
| Grid-aligned finite tiles form a `Z^2` SFT | F0.1 | PD | fixed finite lattice tile |
| One nonzero period has a rank-two periodic completion | T0.1, C0.1 | PD | grid-aligned FLC tilings |
| Euclidean periodic polykite tilings have aligned periodic representatives | X0.1 | EXT | Smith et al. Appendix A |
| Fixed-vector transfer graph is an exact decision | T1.1 | PD | finite cylinder state graph |
| Positive and negative transfer certificates | T1.1--T1.3 | PD/MV | cycles or complete cycle-free graph manifests |
| Modular left-cokernel obstruction | T2.C0 | EXT/MV | classical generalized coloring |
| Integral incidence membership | T2.C2 | PD/MV | HNF/Smith normal form |
| Translation-averaged nonnegative cone | T2.C3 | PD/MV | quotient feasibility relaxation |
| Boundary skeleton carries commuting holonomies | T2.D1 | PD | connected periodic boundary skeleton |
| Twisted finite-group potential obstruction | T2.D2 | PD/MV | exact torus cover exclusion |
| Dihedral covariance of quotient tests | T2.D3 | PD/MV | exact symmetry quotient |
| Common-support colored compiler | S0C | PD | finite connected macro systems |
| Lossless contact-incidence recoding | K1C | PD | finite edge/vertex SFTs |
| Compact inverse on an injective image | K1R | PD | finite symbolic quotients |
| Full-local-closure decoder certificate | Q0, K1T | PD | totality, not intended image only |

Canonical sources: `foundations/periodic_completion.md`,
`realization/general_theory.md`, and the control documents.

## 2. General realization and computability

| Integrated result | IDs | Status | Scope / value |
|---|---|---:|---|
| Total equivariant decoder transfers periods | Q0 | PD | direct aperiodicity sufficiency |
| Root-deterministic finite carriers are periodic | N55 | PD | finite rooted `Z^2` carriers |
| Symbolic compiler nonemptiness is undecidable | U1 | PD | product with a fixed aperiodic SFT |
| Marked connected-polygon realization is undecidable | U2, D3 | COND | depends on Stade's unrefereed converse |
| Arbitrary marked source extensions remain undecidable | U3 | PD | fixed aperiodic factor plus arbitrary SFT |
| Directed-graph and fixed-width auxiliaries are decidable | D3 | PD | cycle/transfer-graph tests |

The one-connected-unmarked-polygon realization problem remains open.

## 3. Contact expressivity and erasure

| Integrated result | IDs | Status | Scope / value |
|---|---|---:|---|
| Independent two-body erasure iff relation is biclique-union | K61R | PD | complete rooted disjoint collars |
| Physical required/forbidden sandwich test | K62P | PD | biclique closure avoids forbidden graph |
| Connected required contacts preserve a periodic carrier | N62S general lemma | PD | spanning periodic contact graph |
| Ordinary sector star cannot realize ternary parity | K69A | PD | participant-separable sectors |
| Torsion-free additive tests cannot realize parity | K70A, N70T | PD | any finite additive budget family |
| Hidden-state parity needs four product boxes | K2H, N6 | PD | immediate three-interface star |
| Unary/binary constraints cannot define parity | N5 | PD | full low-arity projections |
| Finite automaton has a rooted T-junction compiler | K74A | PD | roles and topology prescribed |
| Every finite fixed-arity relation has such a compiler | K74R | PD | deterministic prefix trie |
| Finite-group identity words have such a compiler | K74G | PD | group-state automaton |
| Positive weighted host language is finite and decidable | K13W | PD | exact positive weights |

The hierarchy is exact:

```text
independent profiles  <  ordinary/additive stars  <  hidden-state T-junctions.
```

The last class is locally universal.  Shape-only role/topology forcing is not
included.

## 4. General polygon-interface geometry

| Integrated result | IDs | Status | Scope / value |
|---|---|---:|---|
| Two-participant interface cannot end without a third participant | N23 | PD | polygonal disks, local coverage |
| Positive point participant forces secondary contacts | N24 | PD | maximal common-boundary arcs |
| Prescribed convex side germs coexist on one polygon | K71B | PD | local alphabet only |
| Copy-exchanging isometry is half-turn or reflection | K43I | PD | symmetry-free disk |
| Reflection-invariant stars have even participant count | K45O, N49 | PD | symmetry-free disk |
| Minimum reflection hinge has four sectors | K45H | PD | abstract local star |
| Clean off-axis two-copy reflection spine is impossible | K43R, N48 | CLOSED | no T-junction/third participant |
| Edge-minimal clean-spoke word classification | K42P, K42M, N46 | CLOSED | fixed role order and half-turn docking |

## 5. Exact AHI source benchmark

| Integrated result | IDs | Status | Scope / value |
|---|---|---:|---|
| Optimized composition selects `sqrt(2)-1` | P0 | PD | source projective composition |
| Exact supports `30,30,2`; rhombi `15,15,1` | G0, SER1 | MV | pinned Section 10.1 figure |
| 31 addressed roles and 44 internal contacts | K50C, K51K | MV | exact source atlas |
| Auxiliary overlaps contract to decorated vertices | O0 | PD | general FLC disk contraction |
| Physical incidence has unique prelimit lift | I0 | PD | source orders `{-1,0,1}` |
| Global line-index cocycle has zero holonomy | D0 | PD | complete colored source language |
| Colored 31-address source is aperiodic | S0, L0 | PD/MV premise | total decoder to irrational source |
| Twelve-state corridor quotient | K52Q | MV | `Z/3 x {0,1}^2` |
| Binary ownership/domain-wall encoding fails | N53 | MV/PD | exact contact graph odd cycle |
| Affine pose/orientation laws fail | N54, N56 | PD | source-native contact ownership |
| Binary L-anchor has two exact states | K53H, K53B, K53E | MV | source-specific exact cover |
| Direct Turtle center-spoke transfer fails | N57 | MV | exact finite no-go |
| Common-support macro kernel | K55A--K55C | MV | source-specific |
| Source-native interchangeable pairs | K56A--K56C | MV | source-specific |

## 6. AHI carrier-local classification

| Integrated result | IDs | Status | Scope / value |
|---|---|---:|---|
| Minimal irrational lattice hull | K63M | PD | fixed irrational orientation component |
| Separable schemes reduce to finite biclique components | K63D | PD | total factor to minimal hull |
| Rail-separable schemes admit periodic constant rails | N63R | CLOSED | independent rail profiles |
| Factor-visible finite contacts cannot be pruned | K63E | PD | minimal factor |
| Sub-30 composition has only areas 15,16,17 | K64A | PD | carrier-local macros |
| All-singleton continuation graph must be bipartite | K64B | PD | exact corridor language |
| Complete sub-30 census has no survivor | K64C, N64S | MV/CLOSED | 29,443 subdivisions |
| Area-30 normal form | K65A, K65F | PD | carrier-local macros |
| Complete area-30 census has no survivor | K65C, N65S | MV/CLOSED | 52,042 residual matchings |
| All-area composition phase diagram | K66A | PD | equal-area finite libraries |
| Every library needs a count-changing trade | K66T | PD | all carrier areas |
| Corridor rule is a binary cut condition | K66C | PD | source endpoint equivalence |
| Lozenge orientation counts depend only on support | K67O | PD | general triangular regions |
| Large-macro count is a synchronized directional deficit | K67D, K67G | PD | exact AHI macros |
| Per-axis parity cannot close even trades | N67C | CLOSED | corridor charge method |
| No boundary-neutral count-changing trade exists | N68H | CLOSED | globally admissible patches |
| Residual carrier-local class is boundary-active/contextual | K68R, K69F | PD | reduction, not existence |

## 7. Geometric carrier families

| Family | Principal IDs | Status | Exact disposition |
|---|---|---:|---|
| Flag-kite retiling | K3F, N10 | PD | colored recoding and rigid macro control |
| Binary diagonal square | K3B, N11, B0 | CLOSED | binary plaquette SFT is periodic |
| Synchronizing domino bands | K5S, N14--N16 | CLOSED scoped | natural independent channels periodic |
| Weighted host words | K13W, K13A, K13F | PD | exact arithmetic classification and infinite family |
| Square lens | K15S, N31--N33 | CLOSED | no positive weights |
| Equal-spoke rhombic lens | K22R--K25X, N37 | CLOSED | forced spoke crossing |
| Unequal-guard clean spokes | K28G, N44--N46 | CLOSED | collapses to refuted family |
| Unequal-spoke rectangle | K16B--K40H | OPEN | six bounded cells; solvers inconclusive |
| Clean reflection spine | K43I, K43R, N48 | CLOSED | local half-plane overlap |
| Four-participant hinge | K45H--K49W | CLOSED as candidate | exact octagon tiles periodically (`N52`) |
| Parity zipper | K70Z--K73R | CLOSED scoped | local compiler works; convex-flank carrier impossible |

The integrated proofs and lessons are in
`../case_studies/geometric_carriers.md`; every narrow intermediate result
remains in the ledger.

## 8. Published-tile controls

| Control | Principal IDs | Status | Logical use |
|---|---|---:|---|
| Turtle fixed-vector exclusion through norm 36 | T1.2-36 | MV/CTRL | transfer verifier validation |
| Turtle torus exclusion through index 60 | T2.D2-60 | MV/CTRL | holonomy/DRAT validation |
| V4 local-product blind family | T2.D5 | PD/MV | method-ceiling counterexample |
| Packing orbit closes three index-60 escapes | T2.D6 | MV/CTRL | finite packing mechanism |
| Hall matching conjecture | T2.D7-H | REFUTED | exact planar countermodel |
| Spectre physical corona prefix | T3.0P | MV/CTRL | finite local-language reconstruction |
| Spectre unique parent partition | T3.0C | MV conditional | fixed L18 domain |
| Spectre contraction closure | T3.0M | MV conditional | generated colored states |
| Spectre unrestricted contact bridge | T3.0O | MV | declared straight-Spectre geometry |
| D4 correspondence kernel | T3.0Q | MV partial | reconstruction, no method novelty |

## 9. Open theorem boundary

The following remain unresolved and must not be inferred from the closed
families:

1. a connected unmarked polygon with a total local factor to any aperiodic
   Sturmian source;
2. nonexistence of such polygons in an architecture-independent family;
3. undecidability for one connected unmarked polygon;
4. the six bounded cells of the specific unequal-spoke rectangular family;
5. surjectivity from an unmarked monotile hull onto the positive-entropy AHI
   hull; and
6. a source-independent shape-only self-stapling theorem.

The exact Sturmian-program contract is
[`../research/sturmian_realization.md`](../research/sturmian_realization.md).
