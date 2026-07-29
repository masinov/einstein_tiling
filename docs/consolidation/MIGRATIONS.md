# Consolidation migrations

This log records repository-layout changes separately from the append-only
research decision and session histories. A migration changes navigation or
storage responsibility; it does not create a mathematical claim.

## 2026-07-29 — theory and documentation architecture

- Replaced the flat chronological `docs/theory/01...83` surface with
  dependency-oriented domains: `foundations`, `realization`, `research`,
  `sturmian`, `case_studies`, `controls`, and `reference`.
- Preserved notes `07`--`82` byte-for-byte under
  `docs/archive/theory_sources/`; moved the general, goal, control and AHI
  synthesis documents into their canonical domains.
- Added `docs/theory/reference/SOURCE_MAP.json` as an exact source-coverage
  registry and `result_catalog.md` as the integrated theorem index.
- Extracted source-independent interface, weighted-language, involution and
  boundary-germ theorems into the general realization chapter.
- Integrated the exact AHI source, carrier-local phase diagram and all-area
  boundary-active reduction into one benchmark chapter.
- Condensed the retiling, thin-lens, docking, hinge and zipper ladders into a
  mathematical case study while retaining every original proof and erratum.
- Marked the old program specifications as historical. Append-only decisions,
  sessions, experiments, status and errata were not rewritten.

## 2026-07-29 — canonical theory and repository map

- Added the goal-level claim registry, per-file disposition map and artifact
  inventory.
- Extracted architecture-independent results into
  `docs/theory/realization/general_theory.md`.
- Re-stated the live problem and proof boundary in
  `docs/theory/research/sturmian_realization.md`.
- Rewrote the root and theory entry points.
- Preserved the decisions, status and session files unchanged.

Validation: catalog coverage, artifact hashes, relative links and the complete
non-slow test suite.

## 2026-07-29 — fixture, archive and test boundaries

- Moved the immutable n<=8 database snapshot from `data/shapes.sqlite` to
  `tests/fixtures/polykites-n8.sqlite`.
- Preserved SHA-256
  `6956f7c90f6bceae1b63678e8bb86d6df0cf90ce59b2f8db072188850d7c27b9`.
- Reserved the old path as ignored mutable output for historical funnel
  runners and redirected fixture-dependent controls to the immutable path.
- Added enforced read-only fixture access to `ShapeDB`; mutation methods reject
  writes before reaching SQLite.
- Added executable test tiers without moving modules or changing assertions.
- Added navigation for data, scripts, notebooks and archived research.

No large artifact, session record, decision, erratum or proof source was
deleted or rewritten.

## 2026-07-29 — work-mode governance

- Replaced the stale universal session-resume contract in `CLAUDE.md` with
  separate mathematical-research and repository-maintenance modes.
- Kept exact arithmetic, external anchors, experiment preregistration,
  external solver supervision and fail-closed evidence rules.
- Directed maintenance changes to this migration log instead of the research
  decisions, status and session notebooks.
- Retired the three-session cadence in favor of explicit user scope and direct
  theorem obligations.

## 2026-07-29 — AHI implementation decomposition

- Replaced the 4,438-line `sturmian_source.py` implementation with a stable
  compatibility facade.
- Moved unchanged function bodies into dependency-ordered source, contact,
  geometry, compiler and classification modules.
- Added regression checks for facade completeness, dependency acyclicity and
  module-size boundaries.
- Preserved every repository import through the compatibility facade and kept
  all exact certificate artifacts unchanged.

## 2026-07-29 — script archive and certificate interface

- Relocated 92 frozen runners and probes with no live caller, import or test
  path contract to `scripts/archive/`.
- Hash-pinned every old/new path and both file versions in the archive
  manifest; repository-root calculations were adjusted for the new depth.
- Left nine coupled historical scripts at their stable paths.
- Added one registry and dispatcher for eighteen retained exact AHI/Stade
  certificate families, without changing their builders or cold verifiers.

## 2026-07-29 — semantic script mining

- Classified all 92 archived scripts by intellectual disposition, separately
  from their lack of live callers.
- Mapped historical orchestration and worked controls to the tested modules
  that already own their reusable algorithms.
- Extracted exact uniform-demand matching, cold Hall witnesses and generic
  deletion-minimal obstruction reduction into
  `src/einstein/combinatorics/finite_obstructions.py`.
- Adopted the extracted primitives in both the V4 Hall and affine-circuit
  implementations and added architecture-independent regression controls.
- Kept source-specific CEGAR, MIP, taper and symmetry formulations as worked
  examples or future extraction sources; no archived script or evidence was
  deleted.

## 2026-07-29 — domain-oriented Python namespace

- Replaced the chronological `funnel` and blanket `theory` namespaces with
  packages named for mathematical responsibilities.
- Grouped the former `a4_v4_*` modules under
  `holonomy/alternating4/`, Spectre modules under `tilings/spectre/`, and AHI
  modules under `tilings/sturmian/`.
- Renamed `reference` to `analysis/benchmarks`, `render.svg` to the explicitly
  scoped `visualization/kite_svg`, and substrate implementations to
  `geometry/kite_grid` and `geometry/cyclotomic`.
- Moved closed K16W solver code under `historical/thin_lens` so it cannot be
  mistaken for current theory.
- Migrated repository and archived-script imports mechanically and retained
  both pre-migration and current hashes in the archive manifest.
- Added `src/einstein/README.md` as the canonical package and dependency map.

## 2026-07-29 — command and test architecture

- Reduced the script root to stable governance, literature and certificate
  commands; grouped maintenance, benchmarks, visualization, legacy
  certificate tools and coupled historical runners by responsibility.
- Replaced eighteen pairs of source-specific AHI/Stade certificate wrappers
  with one declarative build/verify interface in `einstein.certificates`.
- Moved reusable Stade contact construction and repository catalog logic into
  `src/einstein/`; the corresponding scripts are now thin argument parsers or
  entry points.
- Organized tests by evidence role (`unit`, `certificates`, `controls`, and
  `provenance`) and then by mathematical domain, with location-independent
  repository paths and executable tier coverage.
- Preserved the hash-pinned script archive and research provenance unchanged.
