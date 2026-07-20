# Kaplan Heesch machinery and the public polykite baseline

**Audit date:** 2026-07-21
**Repository impact:** withdraw the claim that the `n<=8` A2 polykite
Heesch census is new; retain it as an exact independent reproduction and
positive-control benchmark.

## Sources and evidence tiers

Three distinct sources must not be conflated:

Catalog records: `kaplan-heesch-2022`, `kaplan-heesch-sat-code`, and
`kaplan-8kites-2023`.

1. Kaplan's peer-reviewed paper, *Heesch Numbers of Unmarked Polyforms*,
   defines `H_c` and `H_h`, gives the SAT reduction, and reports exhaustive
   data for polyominoes through 19, polyhexes through 17, and polyiamonds
   through 24. Its published tables do not contain a polykite census.
2. Kaplan's public `heesch-sat` repository subsequently generalized the same
   machinery to additional grids, explicitly including `-kite`. The source
   was audited at commit
   `1adb37204013b96b62b954a616265e49d7cf21ad` (2026-02-17).
3. On his official project page, Kaplan stated on 2023-08-27 that he had
   computed non-tiling polykites through roughly 16 or 17 cells. On
   2023-08-30 he published `8kites.pdf`, containing every non-tiling 8-kite
   with positive Heesch number and three inconclusive cases. These are public
   author artifacts, not a peer-reviewed complete corpus through 17.

The broader discovery horizon is controlled separately by the primary Hat
paper: Smith--Myers--Kaplan--Goodman-Strauss report an exhaustive computer
search finding no aperiodic `n`-kites other than Hat and Turtle for `n<=24`.
That result already makes every `n<=16` funnel run a validation experiment,
regardless of the Heesch corpus.

## Definition and implementation crosswalk

Kaplan defines an `n`-corona recursively. Every interior prefix is a simply
connected patch. `H_c` additionally requires the outermost union to be
simply connected; `H_h` permits holes only in that outermost layer.

The implementations share these `H_c` semantics but not their algorithms:

| feature | Kaplan `heesch-sat` | repository A2 |
|---|---|---|
| search representation | one CNF over cell and `(placement, level)` variables | recursive exact-cover DFS over one corona at a time |
| nesting | level clauses require adjacency to level `k-1` and forbid adjacency to earlier levels | each accepted corona surrounds the cumulative preceding patch |
| overlap | pairwise SAT clauses | occupied-cell exclusion during DFS |
| hole suppression | cheap pair clauses plus iterative flood-fill cuts | flood-fill rejection before descending to the next level |
| positive evidence | SAT model / witness patch | explicit nested-corona certificate with a cold verifier |
| negative evidence | SAT UNSAT | exhaustive DFS, unless the node budget is reached |
| supported grid | templated grids, including the kite grid | repository kite grid |

Thus A2 is an independent implementation of the same invariant. Independence
is useful for cross-validation; it does not make already published values
novel.

## Exact aggregate reproduction at `n=8`

The 116-page public PDF has SHA-256
`8e710b8d9418ca5ab6d4510fb6dba36080eac980166e1b355ed491e6304e8f12`.
Text extraction yields:

| Kaplan artifact classification | count |
|---|---:|
| `H_c=1, H_h=1` | 104 |
| `H_c=1, H_h=2` | 4 |
| `H_c=2, H_h=2` | 5 |
| inconclusive | 3 |

Therefore Kaplan has 108 shapes with `H_c=1` and five with `H_c=2`.
He identifies two inconclusive pages as periodic but anisohedral and the third
as the Hat. Our A1 removes 39 periodic 8-kites, including those two, while A2
classifies the remaining 833 non-tilers as

`720 x H_c=0 + 108 x H_c=1 + 5 x H_c=2`, with the Hat as the sole growing
case. The aggregate signatures agree exactly.

This is strong external validation of A1+A2. Aggregate equality is not yet a
per-shape corpus bijection because the two projects use different kite
coordinates and canonical encodings. A bounded coordinate crosswalk may be
worth adding as a benchmark artifact; it is not a discovery experiment.

## Claims permitted after this audit

- **Permitted:** A2 independently reproduces Kaplan's public `n=8` aggregate
  polykite Heesch results exactly and supplies cold-verifiable witnesses in
  its own representation.
- **Not permitted:** no published polykite Heesch census exists; the six
  deep shapes are novel data; or the `n<=16` funnel explores an unclassified
  discovery range.
- **Not established by the public comments:** a peer-reviewed, reproducible,
  per-shape complete Heesch corpus through 16 or 17. The statement is an
  author report until the corresponding data artifact is located.

## Primary links

- Paper: <https://doi.org/10.55016/ojs/cdm.v17i2.72886>
- Public implementation: <https://github.com/isohedral/heesch-sat>
- Project page and author comments:
  <https://isohedral.ca/heesch-numbers-of-unmarked-polyforms/#comment-182606>
- Eight-kite artifact: <https://cs.uwaterloo.ca/~csk/tmp/8kites.pdf>
- Hat paper: <https://doi.org/10.5070/C64163843>
