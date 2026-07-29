# Repository consolidation control layer

This directory is the non-destructive control layer for consolidating the
repository.  It separates mathematical status, research relevance and storage
lifecycle before any file is moved, rewritten or deleted.

The files have distinct roles:

- `CLAIMS.json` is the goal-level claim registry.  It does not replace the
  row-level proof ledger; it groups the durable results and names their exact
  relationship to the current research goal.
- `DISPOSITION_RULES.json` contains ordered classification rules for tracked
  repository files.
- `FILE_DISPOSITIONS.json` is the generated per-file application of those
  rules.
- `ARTIFACTS.json` is the generated artifact inventory.  Tracked evidence is
  hash-pinned individually; large ignored research stores are summarized by
  group without silently promoting them to evidence.
- `MIGRATIONS.md` records layout changes independently of the historical
  research decisions and notebooks.

The mathematical coverage map is separate:
`docs/theory/reference/SOURCE_MAP.json` proves that every former numbered
theory note has a canonical destination and a preserved proof source.

Regenerate the two inventories with:

```bash
venv/bin/python scripts/maintenance/build_catalog.py
```

Validate all four documents and their path/claim coverage with:

```bash
venv/bin/python scripts/maintenance/check_catalog.py
```

Both commands are read-only with respect to research data.  The builder only
rewrites the two generated JSON catalogs.  It is repository maintenance, not
a research experiment under D-0065.

## Interpretation rules

1. A disposition is not a deletion instruction.  `archive-history` and
   `externalize-after-manifest` require a later
   reviewed migration.
2. `canonical` means reader-facing authority after consolidation.  It does
   not assert novelty.
3. `retained-evidence` means the file supports a surviving claim or control.
   Its mathematical scope remains the scope recorded in `CLAIMS.json` and the
   proof ledger.
4. `generated-cache` and `source-cache` are reproducible workspace state, not
   versioned research conclusions.
5. The append-only notebooks, decisions and errata remain provenance.  The
   consolidation changes their navigation role, not their historical text.

## Migration order

The generated catalogs support the following later phases:

1. keep the extracted canonical synthesis documents synchronized with the
   sources named in `CLAIMS.json`;
2. move compact certificates into a dedicated evidence namespace and leave
   redirects/manifests at old paths;
3. externalize multi-gigabyte payloads only after independent checksum and
   reference verification;
4. keep immutable fixtures, fetched sources and reproducible caches physically
   separate;
5. refactor only code that supports canonical claims or retained controls;
6. maintain executable test tiers for unit, certificate, provenance and
   historical-control roles;
7. keep the public entry points synchronized with the canonical claims; and
8. consider Git packing or history repair as a separate operation.
