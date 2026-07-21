# W3 Spectre certificate-method novelty audit

**Audit date:** 2026-07-21
**Decision:** close W3 as a novelty branch; retain it as an exact,
machine-readable reconstruction and reproducibility control.
**Scope:** audit only. No radius, seed, SAT, corona, or generated-patch run was
performed for this review.

## Result

The current W3 work does not support a claim of a new aperiodicity theorem or
a new general recognisability method.

Its central proof architecture is already present in the primary literature:

1. Smith--Myers--Kaplan--Goodman-Strauss (`smkgs-chiral-2024`, Section 4)
   generate complete local patch lists, iteratively remove cases that are not
   extendable through compatible overlaps, allow harmless false positives in
   the reduced list, and use reduced 5-patches to force a unique supertile
   assignment. Their Theorem 2.2 concludes that every Spectre tiling has an
   infinite unique hierarchy.
2. Chéritat (`cheritat-spectre-clusters-2024`, especially Theorem 30,
   Theorem 51, Propositions 52 and 60--62, and Corollary 63) gives a more
   explicit all-whole-plane chain of component, interface, triangular-tile,
   cluster, and parent representations. Every correspondence is unique and
   iteration remains in the same language.
3. Goodman--Strauss (`goodman-strauss-matching-1998`) and Vereshchagin
   (`vereshchagin-matching-2026`, Theorem 2) place finite local encodings of
   FLC substitution and hierarchical tilings in the matching-rule/sofic
   framework.
4. Tatham (`tatham-transducers-2026`, Algorithms 2, 6, and 9) gives practical
   finite-state neighbour languages, refinement into unambiguous substitution
   alphabets, and address analysis. A finite-state implementation is therefore
   not by itself a new method.
5. Walton (`walton-recognisability-2026`, Theorem 5.2 and Corollaries
   5.5--5.6) supplies the general recognisability framework. It cannot be used
   circularly here: in the relevant return-discrete spaces, strict injectivity
   is equivalent to the absence of periodic hull elements.

The repository's exact arithmetic, independent cold verifiers, explicit JSON
schemas, tamper tests, and three-valued obligation ledger are useful
reproducibility engineering. But they currently instantiate one published
tiling system and do not come with a generic soundness/completeness theorem.
That is insufficient to distinguish a new method from a careful executable
rendering of published case analysis.

## Adjacent machine-readable certificates

The dated search also found a very recent adjacent control:
Batle--Bednorz (`batle-bednorz-qecc-2026`, arXiv:2607.15326v1, submitted
2026-07-16) publish exact-arithmetic ancillary JSON certificates and a Python
verifier for exhaustive retiling of a 2,490-hat region. Their Proposition 8 is
a finite local-recoverability computation, not an all-tilings Spectre
desubstitution theorem. It therefore does not subsume W3's exact objects, but
it independently rules out the broad claim that machine-readable,
cold-verifiable certificates are new to Hat/Spectre computation.

## Exact disposition of the W3 results

| Repository result | Honest disposition |
|---|---|
| 166 physical coronas, the `166→30→21` prefix, and L18 entry | exact independent finite reconstruction of the published Spectre domain |
| unique 9/8 parent partition and radius-three defect elimination | exact independent reconstruction of forced grouping in a declared finite language |
| unrestricted edge-patch bridge | exact implementation/control for the published Theorem 3.1 domain bridge |
| 17↔17 component/collar bijection and phase round trips | exact partial correspondence kernel |
| 3,565 abstract stars and 80 radius-two survivors | documented over-approximation gap; not a research invitation |
| C1--C5 / D1--D7 schema | useful obligation checklist and software design; no demonstrated new theorem or general method |

The 80 survivors are not evidence against the published hierarchy. They are
states of an intentionally coarser abstract SFT that has not been proved equal
to the physical hull. Eliminating them would reprove a known Spectre theorem
inside another encoding; without a separately stated general-method theorem,
that has insufficient research return.

## What may be claimed

- The repository contains an independent, exact, machine-readable **partial
  reconstruction** of the published Spectre hierarchy.
- The finite propositions in the proof ledger are valid in their explicitly
  declared contact languages and have independent verifiers.
- The C1--C5 and D1--D7 tables are a useful **certificate checklist** that
  exposes domain, existence, uniqueness, faithfulness, iteration, locality,
  and period-descent obligations separately.
- W3 is a reproducibility case study and a control implementation for future
  work outside the known Spectre theorem.
- No directly matching proof-assistant formalisation or generic cold-certificate
  standard was located in the searches below. This is an absence report only.

## What may not be claimed

- that W3 proves Spectre aperiodicity for the first time;
- that local-patch pruning, overlap consistency, finite-state refinement, or
  forced parent grouping is a new method;
- that a JSON artifact plus a cold verifier establishes method novelty;
- that the 80 abstract survivors are candidate Spectre tilings or a gap in the
  published proof;
- that finishing those 80 cases would be a novel theorem;
- that no formal or machine-checkable tiling proofs exist because the dated
  searches did not locate an exact match;
- that T3.1 is a new general theorem before its hypotheses, checker semantics,
  and relation to recognisability/matching-rule theorems are formalized and
  proved independently.

## Reopening conditions

No further Spectre radius or context computation is authorized merely to
complete D4. W3 may be reconsidered only after an on-paper proposition meets
all of the following conditions:

1. it is generic over a stated class of geometric tiling systems, rather than
   a new encoding of the Spectre proof;
2. a soundness theorem maps every accepted finite certificate to a precisely
   scoped whole-plane conclusion;
3. the treatment of geometric-domain equality and spurious abstract states is
   explicit;
4. the checker is applied to at least two structurally independent systems,
   with one not used to design the schema;
5. the proposition is compared clause by clause with Smith et al., Chéritat,
   Walton, Goodman--Strauss/Vereshchagin, and Tatham before implementation;
6. both success and failure would change a named research decision.

Until then, the correct action is preservation, documentation, and no more
W3 computation.

## Dated searches and limits

Searches performed on 2026-07-21:

- `site:arxiv.org aperiodic tiling machine-checkable certificate recognizability substitution tiling`
- `site:arxiv.org formal verification aperiodic tiling Lean Coq Isabelle`
- `site:arxiv.org Spectre tiling computer assisted proof code reduced patches`
- `site:arxiv.org finite state transducers substitution tilings recognizability certificate`
- `Smith Myers Kaplan Goodman-Strauss Spectre reduced patches source code GitHub`
- `Craig Kaplan chiral aperiodic monotile source code reduced patch computation`
- `Chéritat Spectre clusters source code hierarchy`
- `aperiodic tiling proof assistant formalization`

The searches were combined with full-text inspection of the locally pinned
primary sources named above. They located the Batle--Bednorz finite
certificate, but no directly comparable proof-assistant formalisation or
published generic cold-certificate theorem. Search-engine nonappearance is
not a novelty result, and this audit makes no exhaustive-absence claim.
