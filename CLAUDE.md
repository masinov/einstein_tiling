# Einstein tiling search — working notes for Claude

Systematic search for new aperiodic monotiles. The **specification** is
`docs/program/einstein_search_program.md` (read §0–§4 first); corrections to
it live in `docs/program/ERRATA.md` — the spec itself is never edited.

## Resume protocol (start of every session)

1. Read `docs/STATUS.md` — current milestone, verified state, next actions.
2. Skim the latest `docs/notebook/` entry.
3. Work; keep `docs/` in sync (see "end of session" below).

## End-of-session protocol

- Append a new `docs/notebook/YYYY-MM-DD-session-NN.md`: done / verified
  (with evidence) / failures / open. Honest: failures and dead ends are data.
- Update `docs/STATUS.md` (milestone table, capacity limits, next actions).
- New decisions → `docs/DECISIONS.md` (append-only; reversals are new entries).
- Validation runs → table in `docs/EXPERIMENTS.md`.

## Hard rules

- **Exact arithmetic only** in the search/certificate path. Floats are allowed
  at render/output time and inside A4's numerical spectral analysis only
  (D-0010); A4 emits prioritization signals, never exact certificates. On the
  kite substrate all geometry is integer pairs (basis e1=(1,0),
  e2=(1/2,√3/2); |v|² = x²+xy+y²; hexagon side 2 — matches Kaplan's hatviz
  `hexPt`).
- **External anchors before trust** (D-0005): validate every new component
  against independent data (OEIS, published coordinates) before its output
  feeds anything downstream. Gate experiments E1/E4 must pass before any
  verdict on new shapes is claimed.
- Negative results and budget-exhausted runs are recorded, not discarded
  (program §2, §7.4).

## Environment

- Python 3.12 venv at `./venv`; package installed editable
  (`venv/bin/pip install -e .`).
- Tests: `venv/bin/python -m pytest` (fast) / `-m slow` (OEIS n=10 check).
- Key modules: `substrate/kitegrid.py` (grid, symmetry, canonical forms),
  `enumeration/polyform.py` (A0), `render/svg.py`.
