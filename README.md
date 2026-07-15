# einstein_tiling

Research program to systematically search for new einstein tilings
(aperiodic monotiles) beyond the hat/spectre family.

- **Specification:** [docs/program/einstein_search_program.md](docs/program/einstein_search_program.md)
  (+ [errata](docs/program/ERRATA.md))
- **Current status:** [docs/STATUS.md](docs/STATUS.md)
- **Experiment registry & validation gates:** [docs/EXPERIMENTS.md](docs/EXPERIMENTS.md)
- **Decision log:** [docs/DECISIONS.md](docs/DECISIONS.md)
- **Lab notebook:** [docs/notebook/](docs/notebook/)

## Code

`src/einstein/` — exact-integer-arithmetic kernel: kite substrate
(Laves [3.4.6.4]), free-polyform enumeration (funnel stage A0), torus
periodicity rejection with machine-verified certificates (stage A1), shape
database (`data/shapes.sqlite`), SVG rendering. Validated against OEIS
A057786 (n=1..12), Joseph Myers' polykite tiling census (n=1..8), and the
published hat coordinates.

```sh
venv/bin/pip install -e .
venv/bin/python -m pytest        # fast suite
venv/bin/python -m pytest -m slow  # + OEIS n=10 validation
```
