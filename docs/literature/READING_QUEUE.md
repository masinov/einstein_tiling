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

## Immediate: research-return decision

The classified-corpus benchmark assessment is closed with a no-go on new
ablations; see `docs/benchmarks/E1_CLASSIFIED_CORPUS_ASSESSMENT.md`. At the
human checkpoint, select one outside-horizon direction for a targeted
primary-source audit before implementation. W2 quotient work and W3 Spectre
radius work remain frozen.

## Next: machine representations

7. `labbe-selinger-markov-2026` — reproduce the Hat SFT/toral coding and
   record its explicit Turtle and Spectre/CASPr open questions.
8. `tatham-transducers-2026` — reproduce one Hat address/neighbor transducer
   and test exact random access against our generator.
9. `james-smith-rhombic-2024` — compare the rhombille coloring game and
   Fibonacci/Sturmian structure with the Akiyama--Araki route.
10. `akiyama-hamada-ito-sturmian-2026` — reproduce one small quadratic-slope
   tile-set construction; treat the July announcement only as a pointer.
11. `coulbois-et-al-groups-2026` — formalize the poly-`K` correspondence for
   our Laves substrate before using group subsets as candidates.

## Characterization controls

12. `baake-gaehler-sadun-hat-2025` — record the exact deformation,
    conjugacy, MLD, cohomology, and model-set statements.
13. `baake-et-al-spectre-order-2025` — do the analogous CASPr audit.
14. `baake-et-al-diffraction-2025` — compare explicit Fourier modules and
    coefficients with the limited outputs of A4.

## Supporting audits

15. `kaplan-path-review-2025` — retain as author-review evidence only; locate
    primary artifacts before promoting quantitative search claims.
16. `jungck-biswas-five-polykites-2025` — use as a secondary pointer only and
    verify named-tile classifications in primary constructions.

The two SMKGS primary papers are already the controlling full-text audits for
the family and chirality baselines. They remain mandatory rereads whenever
the relevant gate changes.
