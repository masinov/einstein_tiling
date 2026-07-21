# E1 classified-corpus benchmark assessment

**Decision date:** 2026-07-21
**Decision:** no-go as a quantitative discovery-method result; retain a small
reproduction suite and an honest retrospective case study.

## Candidate claim considered

The strongest defensible candidate claim would have been:

> A frozen, source-agnostic funnel retrieves the Hat and Turtle at high rank
> from a completely enumerated and independently classified polykite corpus,
> with measured false-positive rate and workload reduction relative to
> established Heesch/isohedral baselines.

That would be a method evaluation, not a tile discovery. The current evidence
does not establish it.

## Primary comparison set

- `smkgs-hat-2024` reports the complete no-other-aperiodic horizon through
  24 kites and identifies Hat and Turtle.
- `kaplan-heesch-2022` and `kaplan-heesch-sat-code` supply the established
  finite-corona method; `kaplan-8kites-2023` now matches A1+A2 shape by shape.
- `kaplan-isohedral-sat-2024` supplies the established local isohedral test.
- `kaplan-path-review-2025` explicitly proposes climbing Heesch and isohedral
  ladders in tandem and reports the later 500-billion-polykite search. It is
  an author review, so the quantitative report is context rather than a
  reproducible baseline corpus.

No adopted end-to-end monotile retrieval benchmark with sealed labels,
rank-based metrics and published ablations was located in this targeted
comparison. That absence leaves room for such a benchmark, but does not repair
the design of the runs already completed.

## What the existing record establishes

### Complete exact components

- A0 enumerates every free polykite through `n=16` and matches OEIS counts.
- A1 stores 60,477 positive periodic certificates for `n=9..16`, all cold
  verified; its bounded negatives remain explicitly three-valued.
- A1+A2 reproduces Kaplan's public eight-kite classifications 116/116 by
  canonical shape identity.
- At `n=8`, depth three leaves exactly the Hat among seven conservative
  depth-two survivors.
- At `n=10`, depth three leaves exactly two witnessed shapes, one of which is
  the Turtle.
- In the complete selected `n=10/n=12` ten-shape batch, A3 refutes one shape,
  extended A1 proves all eight `n=12` shapes periodic, and the Turtle remains.

These are strong component and positive-control validations.

### Existing reduction counts

For `n=9..16`:

```text
A0 corpus                   26,463,469
A1 bounded survivors        26,402,992
A2 first-corona survivors       40,216
A2 depth-two survivors           9,841
A2 depth-three witnessed         9,728
A2 exact H_c=2                    105
A2 unknown                           8
```

The two aggregate values are sums of the preserved per-size tables from
sessions 12--13. The individual per-size counts and certificates remain the
controlling record.

## Why this is not a clean benchmark result

### 1. Hat leakage and adaptive development

E1 was explicitly a Hat validation gate. The Hat was used as an external
anchor, its identity is embedded in tests, and stages were redesigned or
calibrated while observing Hat behavior. This is correct validation practice,
but it means the Hat was not a held-out positive and its final rank is not an
unbiased retrieval measurement.

### 2. Turtle was not a sealed surprise

The Turtle canonical key was absent from the registry until ERR-003, so its
identity was concealed from the implementation. However, the frozen program
already said E1 should recover “hat (and turtle)”. The late identity check is
an important postmortem failure, not evidence that the research question was
blind to Turtle's existence.

### 3. No complete global ranking

The full `n<=16` corpus was not assigned one frozen score. Raw corona depth is
strongly size-dependent: depth three retains 7,371 of 7,409 depth-two
survivors at `n=16`. A3/A4 were applied only to the complete smallest batch
(two `n=10`, eight `n=12`), selected by size before the expensive stages.
Consequently the repository knows that Turtle wins this ten-shape bracket; it
does not know Turtle's rank among all 26 million shapes under a specified
end-to-end ranking policy.

### 4. Thresholds and budgets were not sealed before evaluation

Node budgets were escalated for hard cases, A3 radii were extended, the A4
indexer was recalibrated, and exact torus horizons were enlarged in response
to observed candidates. Every change is documented, but there is no
pre-evaluation configuration hash from which an unbiased recall or runtime
can be calculated.

### 5. Comparison and ablation data are missing

The history does not contain matched runs for:

- geometry-only ranking;
- Heesch depth alone;
- Kaplan-style isohedral plus Heesch ladders;
- A1 plus A2 with and without deeper coronas;
- A3 with and without A4.

The effect of A4 is particularly unsuitable for a retrospective success
claim: one exact-periodic `n=12` control received estimated Fourier rank four.
A4 is useful prioritization only after exact periodic filters; its incremental
retrieval value has not been measured.

## Honest public package now

Without any new run, the repository can publish or expose:

1. exact enumeration/canonicalization regression fixtures;
2. the 116-shape Kaplan coordinate crosswalk and independent A1/A2 witnesses;
3. the ten-shape `n=10/n=12` retrospective bracket with all identities and
   selection rules disclosed;
4. the ERR-003/ERR-004/ERR-005 postmortem as a case study in why prior-art and
   identity gates must precede computation;
5. the certificate/cold-verifier architecture and fail-closed verdict schema.

Call this a **reproduction and research-governance case study**, not a blind
discovery benchmark.

## What a future clean benchmark would require

A credible replay would need all of the following before execution:

- a frozen corpus (preferably `n<=12`, which contains both controls without
  the 19-million-shape `n=16` tail);
- an evaluator-held Hat/Turtle label file never imported by the runner;
- one immutable protocol commit and configuration digest;
- a size-stratified ranking policy fixed before results;
- baselines listed above;
- metrics: rank, recall@K, workload reduction, certificate coverage,
  unknown rate, CPU/wall time and peak memory;
- one sealed run, with failure reported rather than tuning and rerunning.

Even that would contain only two positives, one of which shaped development.
It is therefore a regression benchmark, not strong statistical evidence for
general discovery ability. The expected research return does not justify a
new replay now.

## Final disposition

Do not run benchmark ablations. Package the already exact `n=8` crosswalk and
smallest-batch case study during ordinary documentation/release work. Close
E1 as a validation/postmortem rather than an incomplete discovery gate. New
research should move outside the classified polykite catalog and begin from a
literature-backed theorem or open problem.
