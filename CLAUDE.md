# Einstein tiling research — repository contract

Current research authority is, in order:

1. `docs/research/charter.md` for the field-level mission and research modes;
2. `docs/research/portfolio.json` for the current program-level option set;
3. `docs/research/status.md` for the concise present state; and
4. `docs/theory/README.md` for canonical mathematics.

The documentation lifecycle is mapped in `docs/README.md`. The original
search specifications, chronological status, decisions, experiments,
checkpoints, and session files are historical sources, not current navigation
or authorization authorities.

## Choose the work mode first

### Mathematical research

Before proposing research work, read:

1. `docs/research/charter.md`;
2. `docs/research/portfolio.json`;
3. `docs/research/status.md`;
4. the relevant canonical theory; and
5. the relevant primary-source reviews in `docs/literature/`.

Research counts as progress only when it directly advances one of the stated
construction, nonexistence or undecidability obligations. A locally correct
lemma about an invented carrier is not progress merely because it is
verifiable.

Free on-paper exploration does not need a formal proposal. It may live in
`docs/research/ideas/`, a problem-centered workspace, or disposable scratch.
It is non-authoritative and cannot silently become a sustained program,
promote a candidate, or authorize nontrivial computation. Gate commitment and
promotion, not mathematical creativity.

Use the append-only notebook, decisions, experiments and errata only when new
research evidence actually requires provenance. Do not create a numbered
session merely to close a work unit, document cleanup, refactor code or report
tests. The former three-session checkpoint cadence is retired; explicit user
scope and the current theorem obligations govern continuation.

### Repository maintenance and consolidation

Read `docs/consolidation/README.md` and use its claim, file and artifact
registries. Record physical layout changes in
`docs/consolidation/MIGRATIONS.md`. Do not update `docs/STATUS.md`,
`docs/DECISIONS.md` or create a session notebook for maintenance-only work.

Preserve append-only provenance and user data. Archive classifications are
not deletion permissions. Large payload movement requires a hash manifest and
explicit review.

## Hard research rules

- **Exact arithmetic only in the search and certificate path.** Floats are
  allowed at render/output time and inside A4's historical numerical spectral
  analysis only; numerical output is a prioritization signal, never a
  certificate. On the kite substrate geometry uses integer pairs in the basis
  `e1=(1,0)`, `e2=(1/2,sqrt(3)/2)` with
  `|v|^2=x^2+xy+y^2`.
- **External anchors before trust.** Validate a new component against
  independent primary data before its output feeds a claim. User-supplied
  prior-art facts are halt conditions until checked against primary sources
  and propagated through the affected claim registry.
- **No nontrivial experiment without an admitted proposal.** Before writing or
  launching a census, radius/index escalation, SAT/SMT/CAD search or other
  research runner, start from
  `docs/research/proposals/TEMPLATE.json`, admit the completed proposal, and
  pass `venv/bin/python scripts/check_experiment_gate.py <proposal>`. Launch
  the exact frozen command through
  `scripts/run_research.py <proposal> -- <command>`. Free on-paper
  exploration, read-only diagnostics, catalog builders and unit/certificate
  regression tests are exempt.
- **Externally supervise native solvers.** A declared wall-clock stop must be
  enforced outside the solver process. An internal timeout alone is not a
  valid stop.
- **Fail closed.** Negative results and budget exhaustion remain recorded.
  Finite evidence never becomes a theorem by accumulation, and a solver
  resource stop is not SAT or UNSAT.
- **Unrestricted tilings are the quantifier.** A candidate is not promoted
  from an attractive patch. It must pass the immediate exact periodicity gate
  and ultimately the full contact-atlas, grouping and total-decoder contract,
  including reflections and unintended contacts.

## Environment

- Python 3.12 virtual environment: `./venv`
- Package install: `venv/bin/pip install -e .`
- Default tests: `venv/bin/python -m pytest`
- Test tiers: see `tests/README.md`
- Exact coordinate cores: `src/einstein/geometry/`
- Python architecture map: `src/einstein/README.md`
- Consolidation validation:
  `venv/bin/python scripts/maintenance/check_catalog.py`
