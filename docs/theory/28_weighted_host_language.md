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

## 5. The forced K9A transition graph

Take `V={A,B,C}` with weights `a,b,c>0` and

```text
h=a+b+c.                                                 (5.1)
```

Selecting both `ABC` and `ACB` under one fixed guard gives K9A equations

```text
ell_B=ell_C=theta,
rho_A=rho_B=rho_C=pi-gamma-theta,
ell_A!=theta.                                            (5.2)
```

The complete transition closure is therefore

```text
E_bar = {A,B,C} x {B,C}.                                 (5.3)
```

Every transition ending in `B` or `C` satisfies the sector equation; every
transition ending in `A` fails it.  In the factorized terminal model of
N29, the start set is `{A,B,C}` and the terminal set is `{B,C}`.  Hence every
accepted word either:

- is a nonempty word over `{B,C}`; or
- has one `A` in its first position, followed by a nonempty word over
  `{B,C}`.

No other placement of `A` is possible.

## 6. K13A: exact semigroup characterization

Write `N_0={0,1,2,...}` and

```text
<b,c> = {p*b+q*c : p,q in N_0}.                          (6.1)
```

### ST-M1.K13A

For the graph (5.3), the complete weight-`h` language is exactly

```text
{ABC, ACB}                                               (6.2)
```

if and only if both conditions hold:

```text
U1.  b+c has the unique nonnegative (b,c)-representation (1,1);
U2.  a+b+c is not in <b,c>.                              (6.3)
```

Equivalently, U1 says neither `b/c` nor `c/b` is a positive integer.

### Proof

An accepted word beginning with `A` has weight `h` exactly when its remaining
counts `p,q` satisfy

```text
p*b+q*c=b+c.                                             (6.4)
```

If U1 holds, `(p,q)=(1,1)` is the only solution.  Its two orderings are
exactly `ABC` and `ACB`. Conversely, any other solution of (6.4) gives an
additional accepted `A`-prefixed word.

For completeness, (6.4) has a solution other than `(1,1)` exactly in one of
the two boundary cases. If `q=0`, then `c=(p-1)b`, so `c/b` is a positive
integer; if `p=0`, then `b=(q-1)c`, so `b/c` is a positive integer. If
`p,q>=1`, positivity makes `(1,1)` the only solution. This proves the
equivalent form of U1.

An accepted word without `A` has weight `h` exactly when

```text
p*b+q*c=a+b+c                                            (6.5)
```

for some nonnegative `p,q`, which is precisely the negation of U2. Thus U2
excludes every no-`A` word, and failure of U2 supplies one. Conditions U1--U2
are jointly necessary and sufficient. □

Because every surviving word has a unique `A`, that endpoint roots its
orientation. Reflection reverses the physical interval but reading from the
`A` endpoint recovers one of the two words in (6.2); no additional full-
isometry class appears.

## 7. The two failed examples are independent failures

The original K10B weights `(a,b,c)=(1,2,4)` violate U1 because `c=2b`:

```text
b+c=6=3b,
```

giving `ABBB`.

The proposed ad hoc replacement `(1,2,3)` passes U1 but violates U2 because

```text
h=6=3b=2c,
```

giving both `BBB` and `CC`.  Changing a length triple without checking both
conditions can therefore move the spurious word rather than remove it.

## 8. Finite arithmetic form

For positive integer or rational weights, U1 is two divisibility tests and
U2 is numerical-semigroup membership.  It is enough to check

```text
0 <= p <= floor(h/b),       0 <= q <= floor(h/c),          (8.1)
```

so the verdict is finite even when `gcd(b,c)` does not immediately decide
membership. For exact algebraic lengths the same bounded equalities give a
finite test in their number field.

K13A is the requested joint characterization. It has not yet shown whether
the conditions admit a useful infinite family; that is session 123's only
remaining arithmetic question.
