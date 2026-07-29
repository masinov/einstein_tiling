# Initial consolidation assessment

**Snapshot:** 2026-07-29
**Scope:** non-destructive classification before any move, rewrite or deletion

> Historical snapshot. This assessment records the repository before the
> domain migration. The current theory layout is documented in
> [`../theory/README.md`](../theory/README.md), while the exact old-to-new
> provenance mapping is maintained in
> [`../theory/reference/SOURCE_MAP.json`](../theory/reference/SOURCE_MAP.json).

The generated catalogs currently cover 993 repository files, including all
files tracked at the start of the consolidation branch and the new canonical,
navigation and control-layer files.  No file remains in the catch-all
`review-required` state.

## Claim-level result

`CLAIMS.json` reduces the research record to fifteen goal-level entries:

- one open global problem;
- six reusable source-independent theorem or contract groups;
- three known-system controls;
- one exact AHI source benchmark;
- two scoped AHI/erasure closure groups;
- one frozen zipper/carrier history group; and
- one reusable exact-certificate engineering asset.

The registry makes two boundaries explicit:

1. local finite-relation expressivity is already closed by the rooted
   hidden-state T-junction normal form; and
2. the unresolved mathematical step is forcing a one-support, shape-only
   system with a total decoder on every unrestricted tiling.

Consequently, the old carrier and zipper ladder is not an active route merely
because its individual derivations remain correct.

## File dispositions

The first generated inventory assigns:

| Disposition | Files | Meaning |
|---|---:|---|
| `canonical` | 51 | Governance, literature, theory synthesis and navigation |
| `retained-toolbox` | 78 | Reusable exact core, verifiers, source and test tooling |
| `retained-control` | 269 | Known-system reproduction, bounded controls and fixtures |
| `retained-evidence` | 32 | Exact AHI/source and external-anchor evidence |
| `archive-provenance` | 207 | Session, decision, errata and experiment history |
| `archive-history` | 247 | Frozen runners, probes, proof sources, carrier derivations and result records |
| `split-required` | 107 | Mixed-responsibility code/tests/configuration |
| `rewrite-entrypoint` | 2 | STATUS and the stale monograph outline |

These counts are planning categories, not deletion permissions.

## Artifact boundary

The artifact inventory hash-pins 290 versioned evidence files totaling about
223 MB.  Separately it records 2,626 ignored files in twelve research stores,
totaling about 8.37 GB.

The large ignored stores are:

- A0/A1/A2 compiled caches: about 1.68 GB, reproducible;
- fetched literature: about 133 MB, source cache;
- W3 frontiers: about 1.2 MB, reproducible;
- six W2 DRAT families: about 6.55 GB, external-archive candidates; and
- the pinned Spectre source archive: about 12.8 MB, source cache.

No ignored store is treated as mathematical evidence merely because it is
present on this machine.  Conversely, no DRAT payload is deleted merely
because its compact result summary is tracked.

## First safe migration tranche

The semantic part of the first tranche is complete:

- `theory/realization/general_theory.md` extracts the reusable proof sources;
- `theory/research/sturmian_realization.md` separates the open problem from
  the AHI benchmark; and
- the root and theory READMEs now enter through those documents.

The first physical separation is also complete:

- the checked-in `data/shapes.sqlite` snapshot moved to the immutable
  `tests/fixtures/polykites-n8.sqlite` path with its hash unchanged;
- the old path is now an ignored mutable workspace database for historical
  runners;
- tests have executable unit, certificate, control and provenance tiers; and
- archive, notebook, script and data navigation layers explain the lifecycle
  boundaries without moving append-only history; and
- the former 4,438-line `sturmian_source.py` monolith is now a compatibility
  facade over five acyclic responsibility-specific modules;
- 92 uncoupled historical runners and probes are isolated behind a hash-pinned
  archive manifest; and
- eighteen retained AHI/Stade certificate families share a discoverable
  registry and command interface.

The following structural work can proceed without changing mathematical
claims:

1. extract the live consumers of the nine coupled historical scripts so those
   scripts can join the archive; and
2. move common JSON loading, writing and schema validation out of the thin
   certificate wrappers and into reusable library code.

Large artifact movement, proof-note deletion, dependency removal and Git
history repair are deliberately excluded from this first tranche.  Each
requires a later manifest-backed review.
