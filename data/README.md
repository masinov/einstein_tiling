# Data boundary

This directory is workspace state, not a single undifferentiated evidence
store.

- `sturmian-source/` contains tracked exact reconstruction and certificate
  artifacts supporting the retained AHI benchmark.
- `literature/` contains the cache policy and ignored copies of fetched
  primary sources.  The versioned catalog lives under `docs/literature/`.
- `a0-compiled/`, `a1-compiled/`, `a2-compiled/` and `w3-frontiers/` are
  ignored reproducible caches.
- `shapes.sqlite`, when present, is a mutable ignored workspace database made
  by the historical funnel runners.

The immutable n<=8 polykite control snapshot is deliberately not here.  It is
versioned as `tests/fixtures/polykites-n8.sqlite`, so a test fixture cannot be
mistaken for the current output of a research run.

See `docs/consolidation/ARTIFACTS.json` for hashes and lifecycle status.  Do
not infer a mathematical claim from the presence of an unversioned cache.
