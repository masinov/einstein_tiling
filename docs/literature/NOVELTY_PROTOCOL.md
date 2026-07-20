# Candidate and novelty protocol

**Version:** 1.0, 2026-07-20  
**Policy:** fail closed.

This protocol prevents four distinct claims from being conflated:

- **shape identity:** the exact polygon/polyform is not already registered;
- **tiling-system identity:** its admitted tilings are not merely another
  realization of a known local-isomorphism or deformation class;
- **aperiodicity:** it tiles the plane and none of its tilings is periodic;
- **method novelty:** an algorithm or certificate is new even when its control
  tile is known.

## 1. Required machine-readable dossier

Every promoted survivor must eventually serialize the following fields. A
missing field is represented as `unknown` or `not-tested`, never inferred from
another field.

```json
{
  "candidate_id": "stable exact identifier",
  "geometry": {
    "substrate": "named grid or free polygon",
    "canonical_boundary": "exact boundary word / vectors",
    "occupancy_key": "canonical polyform key or null",
    "allowed_isometries": "full E(2), orientation-preserving, or explicit",
    "chirality": "mixed / weak / strict / unknown"
  },
  "prior_art": {
    "catalog_snapshot": "YYYY-MM-DD",
    "named_identity": "rejected / matched:<id> / unknown",
    "parameter_family": "rejected / matched:<family> / unknown",
    "finite_census_scope": "inside / outside / unknown",
    "queries_and_sources": ["catalog IDs and dated searches"]
  },
  "tiling_evidence": {
    "periodic_positive_certificate": null,
    "bounded_periodic_negative_scope": null,
    "finite_patch_certificate": null,
    "whole_plane_construction": null,
    "all_tilings_aperiodic_proof": null
  },
  "hierarchy": {
    "local_case_completeness": "verified / partial / absent",
    "desubstitution": "unique / nonunique / unknown",
    "macro_boundary_legality": "verified / partial / absent",
    "divergent_inradius": "verified / partial / absent"
  },
  "system_comparison": {
    "patch_languages": {},
    "LI_or_MLD": "matched / rejected / unknown",
    "topological_conjugacy": "matched / rejected / unknown",
    "substitution_matrix": null,
    "cohomology": null,
    "dynamical_eigenvalues": null,
    "diffraction_module": null,
    "cut_and_project": null
  },
  "claim": {
    "shape_status": "known / unclassified / novel-after-audit",
    "aperiodicity_status": "not-tested / finite-evidence / proved",
    "system_status": "known-class / unclassified / independent-after-audit",
    "method_status": "control / replication / new-method"
  }
}
```

The eventual production schema may normalize large certificates into hashes
and references, but it must preserve these semantic distinctions.

## 2. Promotion gates

### Gate A: exact identity

1. Canonicalize under the declared motion convention.
2. Compare exact named anchors.
3. Run parameter-family classifiers, especially `Tile(a,b)` for polykites.
4. Check the substrate/size against published exhaustive ranges.
5. Refresh the catalog and dated searches.

Output labels allowed here are `known`, `unclassified`, and
`novel-after-audit`. “Not in our registry” is not an output label.

### Gate B: staged elimination

1. Enumerate exact first surrounds and finite corona depth.
2. Run the isohedral control.
3. Search bounded general periodic quotients with explicit coverage bounds.
4. Grow independently seeded exact patches and distinguish coverage from
   boundary continuability.
5. Use spectral or learned features only for prioritization.

A positive periodic certificate refutes aperiodicity. Negative bounded
searches and large patches remain finite evidence.

### Gate C: proof extraction

A proof package must establish whole-plane tileability and exclude every
periodic tiling. Acceptable routes include a forced recognizable hierarchy,
a factor onto a known aperiodic symbolic system, Sturmian/Ammann-bar
arithmetic, geometric incommensurability, or another explicit theorem.

For a substitution route, the certificate must separately verify construction,
legality, exhaustive/unique desubstitution, and unbounded supertile scale. A
single generated substitution tiling proves neither completeness nor
aperiodicity of all admitted tilings.

### Gate D: system novelty

Compare complete radius-`r` patch languages for increasing `r`, then test LI,
MLD, and shape deformation/topological conjugacy when appropriate. Calculate
stronger invariants only after the cheaper comparisons. A new outline in the
Hat deformation class is not a new aperiodic system.

## 3. Turtle as a blinded positive control

The Turtle identity is known and must be hidden from ranking algorithms, not
from the final evaluator.

### Control experiment

1. Freeze a corpus containing Hat, Turtle, periodic tilers, finite-Heesch
   non-tilers, and all smallest A2 survivors.
2. Remove names and registry membership from all ranking inputs.
3. Run A1--A4 and record the rank assigned to Hat and Turtle, the number of
   false positives, and resource use.
4. Run hierarchy/symbolic extraction without seeding known metatiles, Golden
   Hexes, Sturmian words, or substitution tables.
5. Only after outputs are frozen, reveal identities and compare with
   `smkgs-hat-2024`, `akiyama-araki-turtle-2025`, and
   `james-smith-rhombic-2024`.

### Ablations

- remove A4 to measure the value of diffraction;
- replace A1 with isohedral-only filtering;
- remove substrate-specific features;
- change patch seeds and boundary objectives;
- withhold Hat or Turtle independently;
- perturb the search to another grid symmetry group;
- score whether the method detects their shared tiling language.

### Legitimate success claims

- “blindly rediscovered and ranked the known Turtle”;
- “recovered a published symbolic/hierarchical structure independently”;
- “found a more efficient certificate or discovery feature”;
- “calibrated false-positive rates on a known classified corpus.”

It is not legitimate to call the Turtle a new tile, or to infer aperiodicity
from its finite repository experiments when the proof being cited is external.

## 4. Claim language

Use the weakest accurate phrase:

| Evidence | Allowed phrase |
|---|---|
| finite local survival only | locally extensible survivor |
| large exact patch | finite patch candidate |
| no quotient found within stated bounds | no periodic certificate at budget |
| spectral signal | quasicrystal-prioritized candidate |
| explicit whole-plane construction only | tileable by the exhibited construction |
| proof all tilings lack periods | aperiodic monotile |
| source-aware equivalence audit incomplete | system novelty unclassified |
| complete dated comparison supports separation | independent system candidate / theorem, matching proof strength |

Every public table must include the evidence scope next to the verdict.
