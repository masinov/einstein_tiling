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

## ERR-002 (2026-07-17) — Independent disk covers are not patch growth (§4 A3)

The implementation initially treated a SAT cover of each larger disk as
evidence that a candidate "grew." That is weaker than the program's intended
frontier extension: independently solved disks may use incompatible interior
phases and sacrificial boundary crowns that cannot continue.

A3 evidence must therefore be nested. Exact placements from a smaller patch
are frozen inside a protected core while a larger region is solved. The
reported feature is the largest preserved core (and the discarded collar
depth), not merely the largest independently coverable circle. A complete
finite crown being non-extendable does not refute the tile; it refutes that
particular finite patch as a fragment of an infinite tiling.
