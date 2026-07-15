# Program status

> Living dashboard. Update at the end of every working session.
> The specification is [docs/program/einstein_search_program.md](program/einstein_search_program.md)
> (with corrections in [docs/program/ERRATA.md](program/ERRATA.md)).
> Session-by-session detail lives in [docs/notebook/](notebook/); decisions in
> [DECISIONS.md](DECISIONS.md); experiment gates in [EXPERIMENTS.md](EXPERIMENTS.md).

**Last updated:** 2026-07-15 (session 01)

## Where we are

The repo started this session as an empty shell (program document only — the
"spectre engine" the document references is *not* available here; everything
is being built from scratch). Milestone M0 is complete and validated.

| Milestone | Scope (program §) | Status |
|---|---|---|
| M0 — kite substrate + A0 enumeration | §7.1 (kernel v0), §4 A0 | ✅ done, validated (session 01) |
| M1 — A1 fast periodicity rejection | §4 A1 (Conway/BLD, isohedral, torus SAT) | ⬜ next |
| M2 — A2 SAT Heesch engine | §4 A2 | ⬜ |
| M3 — A3 large-patch growth | §4 A3 | ⬜ |
| M4 — A4 diffraction fingerprint + E4 calibration | §4 A4, E4 | ⬜ |
| M5 — A6 hierarchy mining | §4 A6 | ⬜ |
| **Gate G1 — E1 blind hat rediscovery** | §8 E1 | ⬜ blocked by M1–M5 |
| Pipelines B, C; substrates n=5,8; scaling | §5, §6, §3.3 | ⬜ not started |

**No verdicts on new shapes are trusted before Gate G1 passes** (program §8).

## What exists and is verified

- Exact integer-arithmetic kite substrate (Laves [3.4.6.4]) — geometry,
  adjacency, D6+translation symmetry action, canonical forms, boundary
  reconstruction, point-in-polygon. Zero floating point in the search path.
  `src/einstein/substrate/kitegrid.py`
- A0 free-polykite enumeration, counts **match OEIS A057786 exactly for
  n = 1..12** (1, 2, 4, 10, 27, 85, 262, 873, 2917, 10011, 34561, 120815).
  `src/einstein/enumeration/polyform.py`
- The hat, embedded from Kaplan's published outline, recovered as its 8 kite
  cells, boundary and area verified, and confirmed present in our enumerated
  8-cell polykites. `tests/test_hat.py`,
  [notebook/assets/hat-recovered.svg](notebook/assets/hat-recovered.svg)
- Test suite: `venv/bin/python -m pytest` (fast, ~0.5 s) and `-m slow`
  (OEIS n=10). 14 tests green as of session 01.

## Known capacity limits (honest)

- Pure-Python enumeration: n=12 in 40 s, growth ×3.5/level, in-memory sets →
  practical wall around n≈14–15. E1 needs n≤16, E2 needs n≈22–24: requires a
  streaming/compiled enumerator (Redelmeier-style, disk-backed canonical
  store) before those runs. Recorded, not yet built.
- No shape database yet (§7.4); verdicts currently live in tests/notebook
  only. Must exist before A1 produces verdicts at scale.

## Next actions (in order)

1. M1 / A1 stage: periodicity rejection — start with torus/exact-cover tiling
   test (gives certificates), then isohedral-type search. Needs a SAT solver
   dependency decision (kissat/CaDiCaL via python-sat or subprocess).
2. Shape database schema (§7.4) — even minimal (SQLite, keyed by canonical
   form) — so A1 verdicts are recorded, auditable, resumable.
3. Scaling plan for A0 (streaming enumeration) once A1 exists to consume it.
