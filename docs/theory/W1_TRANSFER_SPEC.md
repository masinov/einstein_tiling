# W1 reference transfer engine — correctness and certificate specification

## Purpose

For a fixed finite grid-aligned tile \(T\) and an arbitrary nonzero period
vector \(v\in\Lambda\), decide exactly whether any tiling has period \(v\).
By T0.1, a positive result can always be converted into a fully periodic A1
certificate; a negative result is an exact vector-specific theorem.

This document specifies the reference implementation. Optimized frontier
representations are permitted only after equivalence to this model is tested
and argued.

## Required mathematical model

1. Encode tile anchors and orientations as the finite-range SFT described in
   `01_periodic_completion.md`.
2. Write \(v=g p\) with \(p\) primitive, and choose a transverse basis vector
   \(u\). A cylinder column contains the \(g\) torsion positions parallel to
   \(p\); implementations must preserve this torsion when \(g>1\).
3. Compute an interaction radius \(R\) in the \(u\)-direction from every
   point-group image of \(T\). No placement may influence constraints farther
   than \(R\) columns.
4. Use a higher-block presentation: vertices are locally legal blocks of
   enough consecutive columns to make one-column overlap Markov-complete;
   edges are legal one-column shifts with exact overlap agreement.
5. Trim vertices not lying on any bi-infinite path, equivalently retain the
   union of directed strongly connected components that contain a cycle and
   their bi-infinite connecting structure as required by the chosen
   presentation.

The reference implementation must not search only from an empty frontier.
A valid cylinder tiling may have tiles crossing every chosen cut; an
empty-boundary seed can therefore miss entire strongly connected components.
Completeness comes from exhaustive higher-block enumeration or an equivalent
greatest-fixed-point construction, not reachability from a privileged state.

## Verdicts

### `cycle`

A directed cycle exists. Emit:

- tile and substrate identifiers;
- the exact vector \(v\) and transverse convention;
- the ordered higher-block state cycle;
- transition witnesses (tile anchors/orientations);
- the two resulting independent period vectors;
- a standard A1 torus exact-cover certificate.

The existing A1 verifier independently checks the lifted torus cover. A
positive W1 verdict is not trusted without that verification.

### `cycle-free`

The complete transfer graph has no directed cycle. Emit:

- the same input/convention metadata;
- interaction radius and complete state/edge counts;
- a canonical hash of every state and adjacency list;
- SCC decomposition and a topological ordering of the condensation graph;
- an exhaustion witness for higher-block enumeration.

The difficult part is completeness, not cycle detection. The reference path
must preserve either independently reproducible exhaustive enumeration or
SAT proof artifacts showing that no additional locally legal higher blocks
exist. A mere list of discovered states is not a proof.

### `resource-exhausted`

Record budget, partial state count, peak memory, and frontier parameters. It
has no mathematical polarity and must never be reported as cycle-free.

## Canonicalization

- Enumerate all nonzero vectors, not only primitive vectors.
- Quotient vector inputs only by transformations explicitly proved to preserve
  the tile's allowed placement group: sign and the applicable `D6` orbit.
- State serialization uses sorted integer tuples only; no floating point.
- Hash manifests include code revision, tile key, coordinate convention,
  vector, interaction radius, and enumerator version.

## Reference algorithm phases

1. **Geometry compilation:** enumerate normalized point-group images and
   their exact column spans.
2. **Column alphabet:** enumerate cylinder-column anchor assignments subject
   to constraints internal to the column.
3. **Higher blocks:** enumerate width sufficient for all cross-column exact
   coverage constraints.
4. **Graph construction:** join blocks by exact overlap.
5. **SCC analysis:** decide cycle existence.
6. **Certificate reconstruction:** produce A1 certificate or cycle-free
   exhaustion manifest.
7. **Independent verification:** use a separate verifier path.

SAT may enumerate column assignments or blocks, but solver models must be
decoded into exact integer records and verified independently.

## Validation ladder

### Positive controls

- At least three Myers-validated periodic polykites with different smallest
  HNF shapes.
- For each, vectors belonging to a certified period lattice must yield cycles.
- Reconstructed cycles must verify through A1.

### Negative and scope controls

- Vectors absent from small, exhaustively classified periodic controls where
  an exact comparison is available.
- Several small vectors for the proven grid-aligned hat/Spectre controls.
- Nonprimitive vector cases deliberately chosen so period \(2p\) is present
  while period \(p\) is absent, preventing primitive-only regressions.

### Cross-engine gate

For every tractable small cylinder, W1 and exhaustive torus enumeration over
a bounded transverse range must agree. A disagreement blocks finalist use.

## Finalist order

Only after controls pass:

1. test all vector orbits through the first feasible norm bound;
2. test the observed coordinate scales 18 and 29;
3. attempt 47 with recorded state-growth profiling;
4. proceed to 76 and 123 only if the preceding state spaces justify it;
5. run the 8/7 ambiguity automaton as a distinct certificate class—do not
   conflate composition ambiguity with translational periodicity.

## Implementation layout

- `src/einstein/theory/transfer.py` — pure-Python reference.
- `tests/test_theory_transfer.py` — controls and certificate verification.
- `tools/transfer.rs` — optional compiled port after the reference gates.
- `docs/notebook/assets/theory-w1-*.json` — versioned run artifacts.
- `docs/theory/PROOF_LEDGER.md` — status transitions only after gates pass.

## Phase-0 implementation status (2026-07-17)

The pure-Python reference now exists at `src/einstein/theory/transfer.py`.
It uses exact lattice coordinates and enumerates every nonoverlapping union of
whole-tile crossing contributions before constructing transitions. It never
uses empty-frontier reachability as its completeness criterion. Directed cycles
are converted to HNF torus covers and independently checked by the existing A1
verifier; declared state/edge limits return `resource-exhausted`.

Initial controls in `tests/test_theory_transfer.py` cover:

- primitive and nonprimitive cylinder-basis arithmetic;
- positive cycle reconstruction for one- and two-kite periodic tilers;
- the Myers-validated pose-free two-kite non-tiler;
- a four-kite torsion control that tiles with period `(2,0)` but not `(1,0)`;
- explicit nonnegative polarity on resource exhaustion.

The versioned phase-0 artifact
`docs/notebook/assets/theory-w1-phase0-controls.json` records 28 vector cases
over every free polykite through n=3, 102 independent bounded-transverse torus
comparisons, 25 A1-verified cycles, the torsion control, and cycle-free hat
results for `(1,0)`, `(0,1)`, `(1,1)` and `(2,0)`. There were zero disagreements
and zero resource exhaustions.

W1.a is not closed. Remaining gates are a standalone negative exhaustion
manifest (the current artifact preserves canonical graph hashes, not complete
adjacency/proof objects), an independent negative verifier, and additional
Myers-validated HNF shapes beyond the n≤3 control matrix. The reference
representation must also be reviewed before an optimized port may claim
equivalence.
