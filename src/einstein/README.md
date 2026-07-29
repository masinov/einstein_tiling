# Python package architecture

The package is organized by mathematical responsibility, not by the order in
which experiments happened.  Names such as `A1`, `A4`, `W2` and `K16W` belong
in historical notebooks and certificate metadata, not in the canonical API.

## Canonical packages

- `geometry/` — exact coordinate systems and rigid motions.  `kite_grid`
  owns the deltoidal-trihexagonal kite substrate; `cyclotomic` owns the exact
  four-coordinate model used by Spectre geometry.
- `polykites/` — enumeration, stored-shape access, named controls, periodic
  quotients, isohedral tests, corona growth, finite patches and hierarchy
  inference for unions of kite cells.
- `periodicity/` — exact period obstructions and cylinder-transfer methods
  that are not tied to one named tiling system.
- `holonomy/` — boundary words, quotient constraints and finite-group
  holonomy.  The former `a4_v4_*` family is grouped under
  `holonomy/alternating4/`; here `A4` and `V4` are mathematical group names,
  not experiment stages.
- `tilings/spectre/` — the reconstructed Spectre geometry and its physical,
  component, parent and equivalence languages.
- `tilings/sturmian/` — the Akiyama–Hamada–Ito source atlas, contacts,
  carrier geometry, compilers, classifications and Turtle control.
- `tilings/stade/` — the independently audited labelled-stick construction.
- `tilings/substitution.py` — generic finite substitution/hierarchy data used
  by more than one named system.
- `combinatorics/` — domain-independent exact finite groups, matchings and
  obstruction minimization.
- `analysis/` — numerical diffraction analysis.  Its `benchmarks/` package
  contains generated known patterns used only for calibration; these are not
  research authorities.
- `visualization/` — output-only drawing helpers.  `kite_svg` specifically
  renders kite-grid cells and outlines; it is not a universal tiling renderer.
- `solvers/` — exact adapters for external algebraic solvers.
- `literature/` — primary-source catalog/cache synchronization behind the
  thin fetch command.
- `repository/` — location-independent paths, research admission primitives,
  and deterministic consolidation catalog construction/validation.
- `historical/` — executable implementations retained from closed research
  branches.  Code here is not a current construction API.

The root `certificates.py` is the small user-facing registry connecting
retained artifacts to builders and cold verifiers.

## Finding an implementation

The filename describes the operation rather than the experiment that first
needed it.  For example:

- enumerate or load polykites: `polykites/enumeration.py` and
  `polykites/database.py`;
- reject a bounded period or grow a corona: `polykites/periodic_quotients.py`
  and `polykites/coronas.py`;
- build or verify a cylinder obstruction: `periodicity/transfer.py` and
  `periodicity/verification.py`;
- work with the AHI source construction: `tilings/sturmian/atlas.py`, then
  `contacts.py`, `carriers.py`, `compiler.py` and `classification.py`;
- work with the Spectre reconstruction: start with `tilings/spectre/geometry.py`
  or `patches.py`; physical-ring elimination is in
  `corona_elimination.py`;
- draw kite-grid output: `visualization/kite_svg.py`.

Package `__init__.py` files are intentionally small.  Import the owning module
directly so that dependencies stay visible.

## Dependency direction

The intended direction is:

```text
geometry + combinatorics
          ↓
polykites + periodicity + holonomy
          ↓
named tiling systems
          ↓
analysis / visualization / certificate commands
```

`repository/` and `literature/` are infrastructure side layers; neither is a
mathematical dependency of the geometry or combinatorics cores.

Named systems may use general mathematics; general mathematics must not
import a named tiling system.  Historical code may depend on canonical code,
but canonical code must not depend on `historical/`.

Archived scripts are executable provenance rather than public APIs.  Layout
migrations may update their imports, but their before/after hashes remain
recorded in `scripts/archive/MANIFEST.json`.
