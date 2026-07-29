# Consolidation migrations

This log records repository-layout changes separately from the append-only
research decision and session histories. A migration changes navigation or
storage responsibility; it does not create a mathematical claim.

## 2026-07-29 — canonical theory and repository map

- Added the goal-level claim registry, per-file disposition map and artifact
  inventory.
- Extracted architecture-independent results into
  `docs/theory/GENERAL_REALIZATION_THEOREMS.md`.
- Re-stated the live problem and proof boundary in
  `docs/theory/STURMIAN_REALIZATION_BOUNDARY.md`.
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
