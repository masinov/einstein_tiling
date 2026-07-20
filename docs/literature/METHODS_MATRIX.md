# Literature-to-code methods matrix

**Snapshot:** 2026-07-21

Status meanings: **implemented** means tested repository code exists;
**partial** means a useful component exists but does not meet the cited
method's complete logical role; **planned** means no claim of implementation.

| Method / invariant | Controlling sources | Repository locus | Status | Required next comparison |
|---|---|---|---|---|
| Canonical polyform identity | `smkgs-hat-2024` | `substrate/`, `src/einstein/e1_candidates.py`, `tests/test_hat.py`, `tests/test_turtle.py` | implemented for Hat/Turtle anchors | Implement full `Tile(a,b)` membership and provenance-bearing family records. |
| Finite census and known horizon | `smkgs-hat-2024`, `kaplan-path-review-2025` | A0 enumeration, `POLYKITE_BASELINE.md` | implemented as fail-closed policy through `n<=24` | Do not treat the reported 500-billion search as a reproducible theorem without its corpus/certificates. |
| Heesch/corona search | `kaplan-heesch-2022`, `kaplan-heesch-sat-code`, `kaplan-8kites-2023` | `src/einstein/funnel/a2_heesch.py`, compiled A2 runners | independent implementation; externally reproduced through `n=8` | Our `n=8` counts exactly match Kaplan's public artifact: 108 with `H_c=1`, five with `H_c=2`, and the same three cases left after finite-Heesch classification. Treat A2 as a benchmark/filter, not novel census data; complete a per-shape coordinate crosswalk before claiming full corpus identity. |
| Isohedral SAT | `kaplan-isohedral-sat-2024` | `src/einstein/funnel/a1_isohedral.py` | implemented | Complete n<=8 counts match Myers; retain as an early portable filter while A1 handles periodic tilings with multiple transitivity classes. |
| General aligned periodic quotient search | `smkgs-hat-2024` Appendix A supplies alignment bridge | `src/einstein/funnel/a1_torus.py` | implemented for bounded quotients | Preserve three-valued bounded verdicts; no finite negative is a general aperiodicity proof. |
| Large exact patches | proof caveats in `cheritat-spectre-clusters-2024` | `src/einstein/funnel/a3_patch.py` | implemented as finite evidence | Add continuability certificates or explicitly label dead-end boundary conditions. |
| Diffraction/module fingerprint | `baake-et-al-diffraction-2025` | `src/einstein/funnel/a4_diffraction.py` | calibrated heuristic | Compare Fourier modules, not only estimated rank/symmetry; never use A4 as proof. |
| Forced clusters and hierarchy | `smkgs-hat-2024`, `smkgs-chiral-2024`, `cheritat-spectre-clusters-2024` | A6 and W3 | partial | The unrestricted hull enters L18, partitions uniquely and contracts to 17 states. D4 now has an exact 17↔17 interface/collar bijection and determinant-one next-phase round trips, but the bare state SFT has 536 overlap stars; exhaust the 80 radius-two survivors against physical provenance before C1/C3/D7. |
| Spectre edge-patch/domain deformation | `smkgs-chiral-2024` Theorem 3.1 and Lemma 2.3 | `spectre_edge_patch_bridge.py`; `SMKGS_CHIRAL_SPECTRE.md` | implemented and independently verified | Thirteen exact maximal sides and the angle bound leave ten interface words; all reduce bijectively to primitive contacts. Reuse this atlas as the D4 physical round-trip boundary layer. |
| General recognisability | `walton-recognisability-2026` | `src/einstein/theory/substitution_certificate.py` | theorem crosswalk implemented; hypotheses unmet | Walton requires a compact Hausdorff expansive `L`-sub hull; in the return-discrete case strict injectivity is equivalent to already excluding every periodic tiling. Use it as a post-aperiodicity theorem/control, not circularly. |
| Golden Hex / Sturmian / Ammann bars | `akiyama-araki-turtle-2025`, `james-smith-rhombic-2024` | `src/einstein/theory/turtle_sturmian.py`; Turtle A3 artifact | partial | Exact word recurrences and density algebra reproduce the published chirality target; encode forced GAB geometry and attempt blind symbolic-language recovery. |
| Sturmian lattice construction | `akiyama-hamada-ito-sturmian-2026` | no implementation | planned | Reproduce a small quadratic-slope tile-set example before using it for candidate generation. |
| Markov partition / toral SFT | `labbe-selinger-markov-2026` | W2 contains finite quotients but not this coding | planned | Reproduce the Hat coding; then study the paper's explicit Turtle/Spectre questions. |
| Finite-state substitution transducers | `tatham-transducers-2026` | exact generators exist, no canonical address automaton | planned | Convert a validated substitution certificate to neighbor/address transducers and test random access. |
| Poly-`K` / group monotiles | `coulbois-et-al-groups-2026` | W2 group/holonomy work is adjacent, not equivalent | planned | Formalize the grid symmetry group and round-trip geometric realization before enumerating subsets. |
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
