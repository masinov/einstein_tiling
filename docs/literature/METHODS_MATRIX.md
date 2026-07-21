# Literature-to-code methods matrix

**Snapshot:** 2026-07-22

Status meanings: **implemented** means tested repository code exists;
**partial** means a useful component exists but does not meet the cited
method's complete logical role; **planned** means no claim of implementation.

| Method / invariant | Controlling sources | Repository locus | Status | Required next comparison |
|---|---|---|---|---|
| Canonical polyform identity | `smkgs-hat-2024` | `substrate/`, `src/einstein/e1_candidates.py`, `tests/test_hat.py`, `tests/test_turtle.py` | implemented for Hat/Turtle anchors | Implement full `Tile(a,b)` membership and provenance-bearing family records. |
| Finite census and known horizon | `smkgs-hat-2024`, `kaplan-path-review-2025` | A0 enumeration, `POLYKITE_BASELINE.md` | implemented as fail-closed policy through `n<=24` | Do not treat the reported 500-billion search as a reproducible theorem without its corpus/certificates. |
| Heesch/corona search | `kaplan-heesch-2022`, `kaplan-heesch-sat-code`, `kaplan-8kites-2023` | `src/einstein/funnel/a2_heesch.py`, `kaplan-8kite-crosswalk.json` | independent implementation; per-shape external reproduction through `n=8` | All 116 public PDF records map bijectively to repository keys with exact `H_c` agreement: 108 at one, five at two, two periodic-anisohedral controls and the Hat. Treat A2 as a benchmark/filter, not novel census data. |
| Isohedral SAT | `kaplan-isohedral-sat-2024` | `src/einstein/funnel/a1_isohedral.py` | implemented | Complete n<=8 counts match Myers; retain as an early portable filter while A1 handles periodic tilings with multiple transitivity classes. |
| General aligned periodic quotient search | `smkgs-hat-2024` Appendix A supplies alignment bridge | `src/einstein/funnel/a1_torus.py` | implemented for bounded quotients | Preserve three-valued bounded verdicts; no finite negative is a general aperiodicity proof. |
| Abelian coloring / tile homology | `conway-lagarias-tiling-groups-1990`, `lidjan-baralic-flat-surface-homology-2021` | `src/einstein/theory/invariants.py`; T2.C0--T2.C5 | classical method; Turtle worked control | Keep the compact thin-family certificate as a verifier example. Do not claim method novelty or extend W2 quotient shells. |
| Large exact patches | proof caveats in `cheritat-spectre-clusters-2024` | `src/einstein/funnel/a3_patch.py` | implemented as finite evidence | Add continuability certificates or explicitly label dead-end boundary conditions. |
| Diffraction/module fingerprint | `baake-et-al-diffraction-2025` | `src/einstein/funnel/a4_diffraction.py` | calibrated heuristic | Compare Fourier modules, not only estimated rank/symmetry; never use A4 as proof. |
| Forced clusters and hierarchy | `smkgs-hat-2024`, `smkgs-chiral-2024`, `cheritat-spectre-clusters-2024` | A6 and W3 | exact partial reconstruction; novelty branch closed | Reduced patch pruning, forced grouping, and all-whole-plane unique hierarchy are published. Preserve the verified W3 controls; do not extend the remaining 80 abstract contexts absent the generic theorem required by D-0070. |
| Spectre edge-patch/domain deformation | `smkgs-chiral-2024` Theorem 3.1 and Lemma 2.3 | `spectre_edge_patch_bridge.py`; `SMKGS_CHIRAL_SPECTRE.md` | implemented and independently verified | Thirteen exact maximal sides and the angle bound leave ten interface words; all reduce bijectively to primitive contacts. Reuse this atlas as the D4 physical round-trip boundary layer. |
| General recognisability | `walton-recognisability-2026` | `src/einstein/theory/substitution_certificate.py` | theorem crosswalk implemented; hypotheses unmet | Walton requires a compact Hausdorff expansive `L`-sub hull; in the return-discrete case strict injectivity is equivalent to already excluding every periodic tiling. Use it as a post-aperiodicity theorem/control, not circularly. |
| Golden Hex / Sturmian / Ammann bars | `akiyama-araki-turtle-2025`, `james-smith-rhombic-2024` | `src/einstein/theory/turtle_sturmian.py`; Turtle A3 artifact | partial | Exact word recurrences and density algebra reproduce the published chirality target; encode forced GAB geometry and attempt blind symbolic-language recovery. |
| Sturmian lattice construction | `akiyama-hamada-ito-sturmian-2026` | theory notes `07`--`14`; no implementation | Minimal colored S0 and symbolic K1P close in proof draft. K2C/K2V give an exact gauge-invariant boundary/sector factorization, but no unmarked geometry meets K2J's visible-sector, contact-completeness and lift contract. No monotile construction or result is established. | Use note 14 as the consolidated entry point. SER0 is blocked by missing extensional source tables; active K2G is closed by the HC-09 kill condition. Reopen only with exact source data/reconstruction for SER0 or an exact polygon/gadget lemma satisfying J1--J6 for K2J; no shape search or radius escalation. |
| Binary square and rectangular SFT recoding | `hu-lin-two-color-square-2011`, `kari-moutot-low-complexity-2023`, `jeandel-rao-wang-2021` | K3B/B0, theory note 18; `reviews/BINARY_PLAQUETTE_RADIUS.md` | HC-12 audit closed: bit-only `2x2` refuted; larger binary support and hidden-state sofic covers survive symbolically | No bit-only guard synthesis. If reopened, pursue the K4W 11-state/four-interface inverse-retiling contract on paper before any run. |
| Matching-rule / atlas prototile reduction | `goodman-strauss-matching-1998`, `fletcher-atlas-2010`, `vereshchagin-matching-2026` | no implementation | prior-art boundary audited | Decorations and atlas rules can force/recode finite systems but do not supply one shape-only planar tile. Use only as controls for the missing congruence and no-spurious-tilings lemmas. |
| Single-tile and small-support simulation | `greenfeld-tao-periodic-counterexample-2024`, `ollinger-fixed-polyominoes-2009`, `demaine-et-al-one-tile-2014`, `socolar-taylor-hexagonal-2011`, `akiyama-ammann-2012`, `lagae-kari-dutre-corner-2006`, `mampusti-whittaker-dendrite-2020`, `fletcher-atlas-2010` | K5C, theory notes 19--20; `reviews/K5C_SINGLE_TILE_SIMULATION.md` | HC-14 closed: compiler architecture is prior art; fixed-rosette and disjoint-port mechanisms fail; no gapless one-polygon realization | K5C is frozen. Reopen only with an explicit boundary satisfying R1--R5 before any computation; do not redesign the selector/trie/wires. |
| Markov partition / toral SFT | `labbe-selinger-markov-2026` | W2 contains finite quotients but not this coding | planned | Reproduce the Hat coding; then study the paper's explicit Turtle/Spectre questions. |
| Finite-state substitution transducers | `tatham-transducers-2026` | exact generators exist, no canonical address automaton | planned | Convert a validated substitution certificate to neighbor/address transducers and test random access. |
| Machine-readable finite retiling certificates | `batle-bednorz-qecc-2026` | W3 JSON/cold-verifier architecture is adjacent | independent control, not a novelty claim | The published 2,490-hat certificate concerns finite local recoverability, not universal Spectre desubstitution. It nevertheless forbids broad claims that exact JSON certificates and re-verifiers are new here. |
| Poly-`K` / group monotiles | `coulbois-et-al-groups-2026` | W2 group/holonomy work is adjacent, not equivalent | targeted theorem audit | The correspondence preserves tile-set cardinality and may change the acting group; it does not collapse the Sturmian finite set to one Euclidean tile. |
| Shape deformation / topological conjugacy | `baake-gaehler-sadun-hat-2025`, `baake-et-al-spectre-order-2025` | no general comparator | planned | Separate geometric-family identity, MLD, and topological conjugacy in candidate records. |
| Cohomology and dynamical eigenvalues | same | no general implementation | planned | Use known CAP/CASPr values as controls before candidate claims. |
| Cut-and-project windows | same | exact module coordinates exist for controls | partial | Recover internal-space windows and compare dimensions/topology, not just reciprocal rank. |
| Chirality semantics | `smkgs-chiral-2024` | orientations represented in substrate/search | partial | Make the allowed isometry group and mixed-handed periodicity tests mandatory metadata. |

## Workstream routing

- **A — generation:** poly-`K` group subsets, Sturmian encodings, deformation
  spaces, and other substrates. It must not be another undocumented extension
  of the same polykite catalog.
- **B — elimination:** known-family identity, Heesch/corona, isohedral SAT,
  bounded general periodic quotients, then exact patch growth.
- **C — proof extraction:** forced clusters, symbolic factors, substitutions,
  recognisability, macro-boundary induction, and divergent inradius.
- **D — characterization:** patch language, LI/MLD, deformation/topological
  conjugacy, cohomology, spectrum, diffraction, and cut-and-project data.

Passing a row in B only allocates work to C. Passing C can prove
aperiodicity. D determines whether the resulting system is genuinely
different from known systems.
