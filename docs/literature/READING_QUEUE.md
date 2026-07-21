# Reading and reproduction queue

**Updated:** 2026-07-21

Review status is recorded per source in `SOURCES.json`. Promotion to
`full-text-audited` requires notes with theorem/definition locations,
assumptions, exact claims used here, and a repository impact decision.

## Completed full-text audits

1. `akiyama-araki-turtle-2025` — completed 2026-07-20. The theorem map,
   exact chirality consequence, repository comparison, and remaining geometry
   are recorded in `reviews/AKIYAMA_ARAKI_TURTLE.md`. Exact standard-word and
   density controls pass through level 24.
2. `kaplan-isohedral-sat-2024` — completed 2026-07-20. Proposition 1, the SAT
   encoding, the full `n<=8` Myers benchmark, and the edge-versus-vertex halo
   correction are recorded in `reviews/KAPLAN_ISOHEDRAL_SAT.md`.
3. `walton-recognisability-2026` — targeted theorem audit completed
   2026-07-20. Definitions 3.12, 3.25, 3.27, 4.1 and 5.1; Proposition 4.6;
   Theorem 5.2; and Corollaries 5.5--5.6 are mapped to W3 in
   `reviews/WALTON_RECOGNISABILITY.md`. The key result is that strict
   injectivity assumes hull-wide nonperiodicity in our return-discrete case,
   so it is not a standalone aperiodicity proof.
4. `cheritat-spectre-clusters-2024` — targeted hierarchy-chain audit
   completed 2026-07-20. Theorems 30--31 and 51, Proposition 52,
   Corollaries 63 and 65, scope, and the unreproduced local-case burden are
   recorded in `reviews/CHERITAT_SPECTRE_CLUSTERS.md`.
5. `kaplan-heesch-2022`, `kaplan-heesch-sat-code`, and
   `kaplan-8kites-2023` — paper, current public implementation, project-page
   claims, and the 116-page 8-kite artifact audited 2026-07-21. The session-58
   coordinate crosswalk verifies a 116/116 per-shape reproduction; the earlier
   novelty claim is withdrawn. See `reviews/KAPLAN_HEESCH_POLYKITES.md`.
6. `conway-lagarias-tiling-groups-1990` and
   `lidjan-baralic-flat-surface-homology-2021` — targeted abelian-invariant
   audit completed 2026-07-21. W2's GF(2)/integer incidence certificates are
   classical coloring/tile-homology obstructions; the explicit Turtle formula
   remains only a worked control. See `reviews/W2_ABELIAN_INVARIANTS.md`.
7. `akiyama-hamada-ito-sturmian-2026`,
   `coulbois-et-al-groups-2026`, `fletcher-atlas-2010`, and the scope of
   `goodman-strauss-matching-1998` / `vereshchagin-matching-2026` —
   tile-set-to-monotile go/no-go completed 2026-07-21. The finite Sturmian
   construction does not already give a shape-only monotile; nearby machinery
   preserves types, retains atlas rules, or changes the ambient group. ST-M1
   survives as a theorem-design question. See
   `reviews/STURMIAN_MONOTILE_ENCODING.md`.
8. `smkgs-chiral-2024`, `cheritat-spectre-clusters-2024`,
   `walton-recognisability-2026`, `goodman-strauss-matching-1998`,
   `vereshchagin-matching-2026`, `tatham-transducers-2026`, and the adjacent
   `batle-bednorz-qecc-2026` certificate — adversarial W3 method-novelty audit
   completed 2026-07-21. The mathematics and finite-state architecture are
   controlled prior art; the exact verifier implementation remains a
   reproducibility contribution. See `reviews/W3_CERTIFICATE_METHOD.md`.

## Immediate: research-return decision

The classified-corpus benchmark assessment, W2 novelty branch, and W3 novelty
branch are closed. The outside-horizon Sturmian monotile audit is a go for
theorem design only: no runner or shape search precedes a plausible
no-spurious-tilings lemma. Obtain an explicit decision before beginning that
proof design.

## Next: machine representations

9. `labbe-selinger-markov-2026` — reproduce the Hat SFT/toral coding and
   record its explicit Turtle and Spectre/CASPr open questions.
10. `tatham-transducers-2026` — reproduce one Hat address/neighbor transducer
   and test exact random access against our generator.
11. `james-smith-rhombic-2024` — compare the rhombille coloring game and
   Fibonacci/Sturmian structure with the Akiyama--Araki route.
12. `akiyama-hamada-ito-sturmian-2026` — do not reproduce yet; first complete
   the ST-M1 congruence/no-spurious-tilings theorem design.
13. `coulbois-et-al-groups-2026` — use as a cardinality/acting-group boundary,
   not as a tile-set-to-Euclidean-monotile conversion.

## Characterization controls

14. `baake-gaehler-sadun-hat-2025` — record the exact deformation,
    conjugacy, MLD, cohomology, and model-set statements.
15. `baake-et-al-spectre-order-2025` — do the analogous CASPr audit.
16. `baake-et-al-diffraction-2025` — compare explicit Fourier modules and
    coefficients with the limited outputs of A4.

## Supporting audits

17. `kaplan-path-review-2025` — retain as author-review evidence only; locate
    primary artifacts before promoting quantitative search claims.
18. `jungck-biswas-five-polykites-2025` — use as a secondary pointer only and
    verify named-tile classifications in primary constructions.

The two SMKGS primary papers are already the controlling full-text audits for
the family and chirality baselines. They remain mandatory rereads whenever
the relevant gate changes.
