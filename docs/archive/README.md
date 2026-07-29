# Historical research archive

This is the navigation layer for frozen and provenance-only material.  The
underlying files remain at their original paths so hashes and citations stay
valid.

The archive has two distinct classes:

1. **Provenance** — append-only sessions, decisions, experiments, errata and
   the row-level proof ledger.  These explain what happened; they are not
   current entry points.
2. **Research history** — superseded carrier designs, one-off runners,
   historical probes, bounded solver records and legacy candidate artifacts.
   These may contain correct scoped results without defining an active route.

The exact membership is machine-readable in
`../consolidation/FILE_DISPOSITIONS.json` under `archive-provenance` and
`archive-history`.  Mathematical claims are governed separately by
`../consolidation/CLAIMS.json`; archival placement never retracts a valid
claim.

No large ignored proof payload has been moved or deleted.  Those stores remain
listed, with lifecycle status, in `../consolidation/ARTIFACTS.json`.
