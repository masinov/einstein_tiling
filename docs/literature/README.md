# Literature and prior-art gate

This directory is the mandatory entry point for search, theorem, and novelty
work. It is deliberately split into four layers:

- [`SOURCES.json`](SOURCES.json) is the machine-readable source catalog. It
  records publication status, stable identifiers, themes, workstreams, and
  review depth.
- [`STATE_OF_THE_ART.md`](STATE_OF_THE_ART.md) is the dated synthesis of known
  tile families, proof mechanisms, characterization tools, and open scope.
- [`METHODS_MATRIX.md`](METHODS_MATRIX.md) maps published methods to repository
  components and identifies the gaps between our implementation and the
  literature.
- [`NOVELTY_PROTOCOL.md`](NOVELTY_PROTOCOL.md) defines the evidence required
  before a survivor may be described as a new candidate or a new tiling
  system.
- [`reviews/`](reviews/) contains theorem-level notes for sources that have
  actually completed a full-text audit.
- [`anchors/`](anchors/) contains small tracked, machine-readable source facts
  used by proofs and tests when the full cached primary text is Git-ignored.

The narrower [`POLYKITE_BASELINE.md`](POLYKITE_BASELINE.md) is controlling for
Hat--Turtle family identity and the finite polykite census. The
[`READING_QUEUE.md`](READING_QUEUE.md) prevents an abstract-level scan from
being silently treated as a full audit.

## Local source library

Third-party PDFs and extracted text are useful for reproducible audits but do
not belong in Git. Fetch every catalogued open copy with:

```bash
venv/bin/python scripts/fetch_literature.py
```

This creates ignored files under `data/literature/papers/` and
`data/literature/text/`, plus an ignored SHA-256 lock at
`data/literature/library-lock.json`. The tracked metadata, summaries, and
tests remain small enough to review and commit. A source without an open PDF
may remain metadata-only; that limitation must be visible in its catalog
record.

## Evidence discipline

Publication status and review status are separate. A peer-reviewed paper may
still be only abstract-verified here, and a deeply read preprint remains a
preprint. Claims in repository documentation must cite a catalog ID and must
not exceed both of those levels.

No shape may be promoted as a possible new aperiodic monotile until its
substrate, size range, canonical geometry, parameter family, allowed isometry
group, local tiling system, and current-literature search have been checked.
Absence from the named-shape key registry means only “not registered.”

Refresh `SOURCES.json`, the state-of-the-art snapshot, and the dated search
queries before any public novelty claim, and at least monthly during an active
discovery season.
