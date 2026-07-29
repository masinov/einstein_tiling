# Frozen research runners

This directory contains one-off runners and probes from closed or frozen
research branches. They remain executable provenance, not active search
entry points.

`MANIFEST.json` records each former path, current path, original SHA-256 and
current SHA-256. Script bodies were not algorithmically refactored; only
repository-root/self-usage paths and imports or implementation-path references
affected by documented layout migrations were adjusted. Pre-migration hashes
remain available for every changed file.

`SEMANTIC_INVENTORY.json` answers the separate question that filesystem
coupling cannot answer: what intellectual value each script retains and where
its reusable implementation lives.  It covers every manifest entry exactly
once.  In particular, archiving does **not** mean that a script was judged to
contain no reusable idea.  The common exact Hall/CEGAR kernel identified by
that audit now lives in `src/einstein/combinatorics/finite_obstructions.py`; other
scripts are mapped to already-extracted modules or retained explicitly as
worked controls, certificate orchestration or source-specific extraction
candidates.

Ninety-two scripts with no live Python caller, import or test-path contract
were moved here. Nine coupled historical scripts remain at `scripts/` until
their consumers are removed or redirected. Do not resume a parameter ladder
from this directory merely because its runner remains executable.
