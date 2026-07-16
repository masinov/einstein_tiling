# Decision log

Append-only. Each entry: context → decision → consequences. Reversals get a
new entry referencing the old one, never an edit.

## D-0001 (2026-07-15) — Repository layout

Docs (program spec, status, experiments, decisions, notebook) under `docs/`;
exact-arithmetic library under `src/einstein/` (installable package);
validation in `tests/`; bulk artifacts under `data/` (gitignored when large).
The program document is the *specification*; it is never edited to match
reality — discrepancies go to `docs/program/ERRATA.md`.

## D-0002 (2026-07-15) — Python first, compiled kernel later

The program's performance targets (§7.1: tens of millions of tiles/second)
need compiled code, but correctness and auditability come first: v0 is pure
Python with exact integer arithmetic, validated against external anchors
(OEIS, Kaplan's hat coordinates). The compiled port happens only after the
Python reference implementation exists to test it against. Measured Python
capacity: A0 to n=12 in 40 s (see STATUS "capacity limits").

## D-0003 (2026-07-15) — Integer hex coordinates; rank-4 module deferred

All polykite-substrate geometry lives on the triangular lattice
(basis e1=(1,0), e2=(1/2,√3/2), hexagon side 2): every kite vertex is an
integer pair, squared length is x²+xy+y², and the full grid symmetry group
acts by integer maps. The program's rank-4 ℤ[ζ₁₂] module (§3.3) is *not
needed* for polykites (only 6-fold directions occur) and is deferred until
12-fold rotations actually appear (module polygons, spectre substitution,
diffraction indexing). Scale matches Kaplan's hatviz `hexPt`, so published
hat data embeds verbatim — chosen deliberately for external validation.

## D-0004 (2026-07-15) — Kite cell encoding and canonical forms

Cell = (hex-center x, hex-center y, sector d∈0..5); kite quad
[C, M_{d−1}, V_d, M_d]. Free-polyform canonical form = lex-min over the 12
point-group images of the translation-normalized sorted cell tuple.
Enumeration = grow-by-one-neighbor BFS with canonical dedup (every connected
(n+1)-form contains a connected n-form). Validated: OEIS A057786 exact match
n=1..12.

## D-0005 (2026-07-15) — External anchors before trust

Standing rule (instance of program §8's gate philosophy): every new component
must be validated against data we did not produce — OEIS sequences, published
coordinates, literature values — before its output is used downstream. A
component with no external anchor available gets exact self-consistency tests
plus a note in EXPERIMENTS.md "pre-experiment validation log".

## D-0006 (2026-07-16) — Funnel v0 scope: grid-aligned tilings only

A1 (and later funnel stages as currently designed) consider only placements
in the kite grid's symmetry group p6m. Polyform tilings that break grid
alignment exist in general and are invisible to this machinery. Consequence:
"periodic" verdicts are sound (a certificate is a real periodic tiling), but
survival of A1 does not exclude off-grid periodic tilings. This matches the
scope of Myers' published census (he states the same restriction), which is
what makes his numbers usable as our external anchor. Lifting this
restriction is a recorded open problem for the certification track — any
eventual aperiodicity *proof* must handle off-grid placements (the hat paper
does).

## D-0007 (2026-07-16) — A1 v0 = torus exact-cover only; SQLite for the DB

The program's A1 battery (Conway criterion, BLD factorization, isohedral-type
search, torus search) is ordered by cost, but at current scale (n ≤ 12,
~10⁵ shapes) the torus test alone is fast enough (~30 ms/shape) and is the
only sub-test that both certifies and covers all periodic cases; the others
are deferred as optimizations for the n ≥ 16 sweeps. Shape DB v0 is a single
SQLite file under `data/` (committed while small): zero services, standard
tooling, resumable batch jobs keyed by canonical form.

## D-0008 (2026-07-16) — A2 corona conventions: Kaplan's H_c

Corona of a patch = congruent copies with disjoint interiors, each touching
the patch, covering every empty cell that shares at least a vertex with the
patch; holes (bounded empty edge-connected regions) forbidden at every
level — this is H_c of Kaplan arXiv:2105.09438, chosen so that a future
polyiamond substrate can validate directly against his published data.
Depth claims: "H ≥ k" carries a machine-verified certificate (the corona
chain); "H = k" is an exhaustion result valid only when no budget was hit,
like UNSAT — it carries the budget stamp instead. Latest verdict per shape
in the DB is the operative one (escalations append, never overwrite).

## D-0009 (2026-07-16) — A3 = disk exact cover; SAT (CaDiCaL) is the workhorse

A3 patches are posed as exact cover of a disk-shaped cell region (copies
may overhang; enclosed empty cells are uncovered region cells, so
hole-freeness needs no separate check). Measured on the hat: greedy
most-constrained-first filling with backtracking and restarts walls near
~250 tiles — wrong early commitments hide beyond chronological
backtracking; the A2 corona engine is worse as a grower. The spec's SAT
prescription is therefore adopted now rather than later: `python-sat`
(CaDiCaL 1.9.5) is the project's first external solver dependency. Trust
boundary: solver models are decoded and re-verified by our own exact
verifier before storage, and UNSAT results are recorded as exhaustion
verdicts ("disk-cover-refuted", pose-free when no seed is pinned), so no
claim ever rests on the solver alone. The pure-Python greedy grower is
kept for the growth-profile feature and as fallback. Known limit: CNF
size (~11M clauses at 9×10⁴ cells) caps single-shot patches around 10⁴
tiles; incremental encoding is the recorded escalation path.
