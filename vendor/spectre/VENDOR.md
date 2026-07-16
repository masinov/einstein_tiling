# Vendored: spectre / Tile(1,1) exact substitution generator

Source: user-owned and user-provided `spectre.tar.gz` (repo root,
2026-07-16), authored outside this project and explicitly supplied for
integration here. Vendored **source only** — the upstream tarball's
build artifacts (`rust/target/`), GPU viewer (`spectre-view`), WASM bridge
and web app are not needed here and were dropped.

The supplied archive contains no separate license file. That is not an
ownership or integration issue: the repository owner owns the source and
authorized its use here. A license declaration is only needed later if the
owner wants to grant explicit reuse/redistribution rights to third parties.

Role in the program (see D-0010): E4/A4 reference-patch generator with
exact rank-4 module ground truth, and (later) the forward substitution
system that A6 hierarchy mining must re-discover (program §4 A6 references
`gen_tables.py`'s validation loop explicitly).

Local modifications:
- `spectre-core/src/bin/anchors.rs` (new): CSV dump of exact leaf tile
  identities `(kind, s, r, t0..t3)` for a viewport — the A4 feed. No
  upstream file is modified.
- `spectre-core/src/bin/hierarchy.rs` (new): validation-only dump of the same
  exact leaves with hidden child-slot ancestry. A6 consumes `anchors` alone;
  the hierarchy dump is opened only after blind discovery to score recovery.
- `gen_tables.py` writes to hardcoded upstream paths; we do not run it
  (tables.rs is committed). Regenerate only if MAX_LEVEL/rules change.

Trust boundary (D-0005): upstream's own validation (`cargo test` inside
`spectre-core`: reference-leaf match at N=3, substitution-recurrence
counts, culling consistency, pick round-trips, serial/parallel equality)
plus our independent Python cross-checks in
`tests/test_spectre_vendor.py` (leaf multiset vs `ref_leaves_n3_delta.json`
via our own rank-4 module port, tile-count recurrence, single-chirality).
Its output enters the funnel only as *reference/calibration data*, never
as evidence about candidate shapes.

Build / use:
    cd vendor/spectre/spectre-core
    cargo test --release
    cargo run --release --bin anchors -- Delta 7 out.csv [x0 y0 x1 y1]
