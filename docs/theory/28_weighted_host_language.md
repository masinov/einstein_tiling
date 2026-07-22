# Weighted subdivision languages for multiplexed host sides

**Status:** proof draft; arithmetic boundary-design tool, not geometry

**Checkpoint:** HC-22; on paper only

## 1. Joint design object

N29 shows that side lengths cannot be chosen independently of the transition
language forced by the selected words.  HC-22 therefore treats a design as

```text
D = (V,E,S,T,w,h,W),                                      (1.1)
```

where:

- `V` is a finite set of directed side roles;
- `E subset V x V` is the complete transition relation forced by the local
  angle/contact equations;
- `S,T subset V` are the allowed initial and terminal roles;
- `w:V -> R_{>0}` assigns exact positive side lengths;
- `h>0` is the host length; and
- `W` is the desired finite set of rooted words, with reversal handled by the
  declared full-isometry convention.

A word `v_1...v_k` is accepted when

```text
v_1 in S,   v_k in T,   (v_i,v_(i+1)) in E,
sum_i w(v_i)=h.                                           (1.2)
```

The graph in (1.1) must be the **closure** of the equations, not merely the
edges appearing in `W`.  Replacing it by the desired adjacency list is the
exact error exposed by `B|B` in N29.

## 2. K13W: finite weighted-path criterion

### ST-M1.K13W

Let all weights in (1.1) be exact positive elements of an ordered arithmetic
domain with decidable equality (in particular positive rationals or elements
of a fixed real algebraic number field). Put

```text
delta = min_(v in V) w(v),       K = floor(h/delta).       (2.1)
```

Then the complete accepted host language is finite and consists exactly of
the directed `S`--`T` paths of at most `K` vertices whose weight is `h`.
Consequently `W` is the complete accepted language if and only if:

1. every word in `W` is an accepted path of weight `h`; and
2. every other `S`--`T` path with at most `K` vertices has weight different
   from `h`.

This is a finite exact-arithmetic pass/fail criterion.

### Proof

Every accepted word with `k` vertices has weight at least `k*delta`. Since
its weight is `h`, necessarily `k<=K`. A finite directed graph has finitely
many paths with at most `K` vertices, even when it contains cycles. Checking
their endpoint classes, edges and exact weight equality enumerates the whole
language. The two stated conditions are therefore necessary and sufficient.
□

For integer weights, the same test can be written as the finite recurrence

```text
R(v,t) = OR_((v,u) in E) R(u,t-w(v)),                (2.2)
```

with the usual terminal base case. Rational weights reduce to integers by a
common denominator. Equation (2.2) is a compact implementation route, but
HC-22 does not authorize a run: the K9A specialization will be solved
symbolically.

## 3. What the theorem does and does not decide

K13W is reusable at the boundary-language stage. It detects repetitions,
alternative compositions and paths produced by forced transition closure
before polygon coordinates are attempted.

It does not prove:

- that the graph `E` has a geometric unmarked realization;
- that accepted paths give interior-disjoint full tile occurrences;
- that no sliding or partial-side cover exists outside the path model;
- whole-plane tileability or aperiodicity; or
- novelty of this standard weighted-automaton argument.

Any later geometry must still satisfy K12C's full-local-closure clauses.

## 4. HC-22 specialization target and stop

Sessions 122--123 must apply K13W to the transition closure forced jointly by
the two selected non-reversal words `ABC,ACB`.  The output must be an exact
necessary-and-sufficient arithmetic condition on `(a,b,c,h)`, not a list of
tried triples.

If the condition has solutions, HC-22 must give a proved reusable family and
state precisely which geometric obligations remain. If it has no solutions,
the multiplexed-host arithmetic class closes. No computation or polygon is
admitted in either branch.
