# Errata and clarifications to the program document

The program document (`einstein_search_program.md`) is kept verbatim as the
specification. Factual errors found while implementing are recorded here,
with sources. Append-only.

## ERR-001 (2026-07-15) — "The hat being a 13-polykite" (§3.3)

The hat is an **8-kite** polykite on the Laves [3.4.6.4] grid; **13 is its
number of sides** (a tridecagon), not its cell count. Confirmed against the
SMKG paper ("An aperiodic monotile", arXiv:2303.10798) and verified
computationally in this repo: Kaplan's published hat outline contains exactly
8 kite cells (`tests/test_hat.py`). The document's later uses of polykite
horizons (§8 E1 "polykites n ≤ 16", E2 "n ≈ 22–24") are unaffected and remain
sensible budgets.
