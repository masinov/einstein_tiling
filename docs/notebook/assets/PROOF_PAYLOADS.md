# Local proof payloads

Layer-D proof manifests are committed, but newly generated compressed CNF and
DRAT payload directories are intentionally kept out of git. They are large,
reproducible build artifacts; the manifests retain every expected path, hash,
scope field and checker provenance.

| manifest | local payload | producer | verifier |
|---|---:|---|---|
| `theory-w2-layer-d-proof-index45.json` | 377,474,096 compressed bytes | `scripts/run_theory_w2_layer_d_proofs_index45.py` | `scripts/verify_theory_w2_layer_d_proofs.py` |
| `theory-w2-layer-d-proof-index50.json` | 283,140,121 compressed bytes | `scripts/run_theory_w2_layer_d_proofs_index50.py` | `scripts/verify_theory_w2_layer_d_proofs.py` |
| `theory-w2-layer-d-a4-proof-index50.json` | 2,166,298,658 compressed bytes | `scripts/run_theory_w2_layer_d_a4_proofs_index50.py` | `scripts/verify_theory_w2_layer_d_a4_proofs.py` |
| `theory-w2-layer-d-a4-proof-index55.json` | 3,021,269,794 compressed bytes | `scripts/run_theory_w2_layer_d_a4_proofs_index55.py` | `scripts/verify_theory_w2_layer_d_a4_proofs_index55.py` |
| `theory-w2-layer-d-a4-proof-index60-packing.json` | 4,337,057 compressed bytes | `scripts/run_theory_w2_layer_d_v4_packing.py` | `scripts/verify_theory_w2_layer_d_v4_packing.py` |
| `theory-w2-layer-d-a4-proof-index60-map7.json` | 694,971,396 compressed bytes | `scripts/run_theory_w2_layer_d_v4_proofs_index60.py` | `scripts/verify_theory_w2_layer_d_v4_proofs_index60.py` |

The existing index-40 payload predates this policy and is already tracked.
Do not delete local payload directories merely to prepare a commit: unstage
them and retain them for replay. A fresh clone can regenerate them with the
listed producer after installing `drat-trim`; until then, the manifest remains
auditable but the standalone replay necessarily reports missing payload files.
