# Legacy certificate tools

These cold verifiers handle historical evidence formats that are not part of
the generic JSON family registry in `scripts/certificates.py`. Shared CNF,
DRAT, solver-model, geometry and tiling logic belongs in `src/einstein/`; files
here should remain thin artifact-specific adapters.

- `holonomy/` replays finite-group and DRAT evidence.
- `spectre/` replays physical-language and hierarchy controls.

Large proof payloads are governed by
`docs/notebook/assets/PROOF_PAYLOADS.md`.
