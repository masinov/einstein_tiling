# Einstein tiling search — working notes for Claude

Systematic search for new aperiodic monotiles. The **specification** is
`docs/program/einstein_search_program.md` (read §0–§4 first); corrections to
it live in `docs/program/ERRATA.md` — the spec itself is never edited.

## Resume protocol (start of every session)

1. Read `docs/STATUS.md` — current milestone, verified state, next actions.
2. Read `docs/literature/RESEARCH_RETURN_AUDIT.md` and
   `docs/literature/NOVELTY_PROTOCOL.md` before proposing research work.
3. Skim the latest `docs/notebook/` entry.
4. Work; keep `docs/` in sync (see "end of session" below).

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
- **No run without pre-registration** (D-0065). Before writing or launching a
  nontrivial research runner, create the current session notebook from
  `docs/notebook/EXPERIMENT_TEMPLATE.md`, answer all admission questions, and
  pass `venv/bin/python scripts/check_experiment_gate.py <notebook>`. Launch
  via `scripts/run_research.py <notebook> -- <command>`. A session containing
  an ungated research run is invalid. Unit tests and read-only diagnostics are
  exempt; census/radius/index/SAT/search jobs are not.
- **External wall-clock enforcement for native solvers** (D-0150). When a
  preregistration declares a wall-clock stop, wrap native SAT/SMT/CAD/MIP
  processes in an external supervisor. An internal library timeout alone does
  not satisfy the stop rule; Z3 NLSAT has been observed not to return at it.
- **Human checkpoint cadence** (D-0065): stop after at most three numbered
  research sessions or 1 GiB of new artifacts since the checkpoint recorded
  in `docs/HUMAN_CHECKPOINTS.json`, whichever comes first. Present a decision
  summary and obtain explicit continuation before updating the checkpoint.
- **User facts are gates** (D-0065): a user-supplied prior-art fact, scope
  constraint, or contradiction halts the affected branch. Record it in
  `docs/DECISIONS.md` or `docs/program/ERRATA.md` in the same session, verify
  it against primary sources, and propagate its consequences before resuming.

## Environment

- Python 3.12 venv at `./venv`; package installed editable
  (`venv/bin/pip install -e .`).
- Tests: `venv/bin/python -m pytest` (fast) / `-m slow` (OEIS n=10 check).
- Key modules: `substrate/kitegrid.py` (grid, symmetry, canonical forms),
  `enumeration/polyform.py` (A0), `render/svg.py`.
