# Finite automata at rooted T-junctions

**Date:** 2026-07-29  
**Status:** source-independent proof draft; standard finite-state construction  
**Purpose:** extract the general content of the AHI zipper branch and stop the
polygon-by-polygon carrier ladder.

This note deliberately separates two problems that the preceding construction
mixed together:

1. Which finite local relations can a rooted multi-participant contact complex
   express?
2. Can all of its roles be erased into one connected unmarked polygon while
   preserving the relation in **every** tiling?

The first problem has a complete elementary answer below.  The second is not
solved here and is the actual monotile problem.

## 1. Rooted subdivision model

Fix a straight host interval, oriented from left to right, and require it to be
covered in a prescribed order by unit code sides.  At every internal
subdivision point exactly three tile sectors meet: the straight host sector of
angle `pi`, the right endpoint sector of the code side on the left, and the
left endpoint sector of the code side on the right.  The two ends of the word
meet rooted delimiter roles.  Roles, order, unit lengths, vertex alignment,
and the three-participant contact topology are hypotheses of this model; they
are not consequences of an unmarked polygon.

## 2. K74A — finite-automaton compiler

Let

```text
A = (Q, Sigma, E, I, F)
```

be a finite nondeterministic automaton, and fix a word length `n >= 1`.
There is a finite rooted T-junction contact complex whose legal length-`n`
rooted host covers are in bijection with the accepting paths of `A`.

### Construction

Enumerate `Q={q_1,...,q_m}` and assign distinct state angles

```text
lambda(q_j) = pi/3 + j pi/(6(m+1)).                       (2.1)
```

Thus every state angle lies strictly between `pi/3` and `pi/2`.  For each
transition

```text
e = (q, a, r) in E
```

introduce a unit code-side role `T_e` labelled by `a`, with left endpoint
angle `lambda(q)` and right endpoint angle `pi-lambda(r)`.  For each initial
state `i` introduce a left delimiter whose right endpoint angle is
`pi-lambda(i)`.  For each final state `f` introduce a right delimiter whose
left endpoint angle is `lambda(f)`.

All angles are rational multiples of `pi`, and all code-side lengths are one.

### Proof

Suppose `T_(q,a,r)` is followed by `T_(s,b,t)`.  The angle sum at their common
host subdivision is

```text
pi + (pi-lambda(r)) + lambda(s)
  = 2pi + lambda(s)-lambda(r).                            (2.2)
```

Because the state angles are pairwise distinct, the three sectors fill the
plane exactly if and only if `r=s`.  The left delimiter fits the first code
side exactly if and only if that side starts in the named initial state; the
right delimiter gives the analogous final-state condition.  Therefore a
legal rooted cover names exactly an accepting path.  Conversely every
accepting path satisfies every sector equation, so it yields a legal rooted
cover.  These maps are inverse.  QED.

For a deterministic automaton with one initial state, the state path is
uniquely recovered from the visible word whenever the word is accepted.

## 3. K74R — every finite fixed-arity relation

For finite alphabets `Sigma_1,...,Sigma_n` and a finite relation

```text
R subset Sigma_1 x ... x Sigma_n,
```

build the deterministic prefix trie of the words in `R` and apply K74A.
After projecting transition roles to their visible symbols, the rooted legal
covers are exactly `R`; before projection, each legal word has a unique lift.

Hence rooted three-participant T-junction complexes are expressively complete
for finite fixed-arity relations.  This is an existence theorem for a finite
**coloured/role-labelled contact complex**, not for one unmarked support.

## 4. K74G — finite group constraints

Let `G` be a finite group.  Use state set `G`, initial and final state the
identity, and transitions

```text
q --g--> qg.                                               (4.1)
```

K74A then accepts precisely the words `(g_1,...,g_n)` satisfying

```text
g_1 g_2 ... g_n = 1_G.                                    (4.2)
```

The earlier three-bit zipper is the special case `G=Z/2`, `n=3`.  Its parity
relation was therefore not evidence for a privileged Sturmian geometry; it
was the smallest instance of an arbitrary finite-state compiler.

## 5. Local expressivity boundary

The branch now supplies the following source-independent hierarchy.

1. Independent, complete, two-participant port profiles realize precisely
   rectangular/biclique relations (K61R/K62P).
2. Ordinary participant-separable sector sums cannot realize the three-bit
   parity relation (K69A/K70A).
3. Rooted three-participant subdivision vertices with hidden state realize
   every finite fixed-arity relation (K74A/K74R).

Thus local symbolic expressivity is not the missing ingredient.  Once a
rooted multi-participant topology is granted, compiling a finite source rule
is routine finite-state mechanics.

## 6. What remains external to the theorem

K74A does **not** establish any of the following:

- one connected unmarked polygon carries all roles;
- the prescribed host, order, alignment, or participant count is forced;
- reflected or unintended contacts are excluded;
- every whole-plane tiling groups into compiler complexes;
- the grouped tiling decodes to the chosen source system;
- any polygon tiles the plane, or is aperiodic.

Those are jointly the same-support, all-tilings erasure problem.  They cannot
be discharged by adding more local automaton states or by optimizing another
reflex-reset boundary.

## 7. Disposition of the AHI zipper branch

The AHI Section 10.1 reconstruction remains a useful exact benchmark for a
finite source atlas.  K70Z and K72F/K73F are worked physical realizations of
one relation generated abstractly by K74G.  N73W/K73R are valid scoped
obstructions for one attempted convex-flank carrier.

No further AHI-specific zipper carrier, reflex-reset count, comb, or boundary
word is authorized on this branch.  Reopening requires a source-independent
theorem about one-support total erasure, an undecidability reduction for a
clearly specified unmarked realization class, or a construction satisfying
the complete all-tilings decoder contract—not another local role geometry.

## Claim boundary

The compiler theorem is standard finite-state semantics expressed as angle
matching.  No method novelty is claimed.  A separate dated prior-art review
must delimit its relationship to Wang-to-jigsaw conversions, edge-patch
tilings, geometric tiling simulations, and matching-rule theorems before any
public novelty statement.
