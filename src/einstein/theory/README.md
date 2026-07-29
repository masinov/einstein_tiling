# Exact theory implementations

This package contains exact implementations supporting canonical theorems,
known-system controls and retained source-specific certificates. It is not a
list of active research directions.

## Reconstructed AHI source system

The former `sturmian_source.py` monolith is decomposed in dependency order:

1. `sturmian_source_core.py` — source transcription, triangular-lattice
   geometry, support verification and atlas construction;
2. `sturmian_contacts.py` — physical contact kernels, periodic scaffolds,
   corridor quotients and rooted selectors;
3. `sturmian_geometry.py` — support surgery, common-support kernels and
   interchangeable assemblies;
4. `sturmian_compiler.py` — rhombus compilers, full germ languages and local
   obstructions; and
5. `sturmian_classification.py` — bounded carrier classifications and exact
   periodicity certificates.

`sturmian_source.py` is a compatibility facade. Existing scripts and stored
certificate workflows may continue to import it; new code should import the
module that owns the relevant responsibility.

These modules implement the exact AHI benchmark and its scoped exclusions.
They do not themselves establish a one-polygon Sturmian monotile. The current
mathematical boundary is documented in
`docs/theory/STURMIAN_REALIZATION_BOUNDARY.md`.
