# Hinge-octagon roles and closure

**Date:** 2026-07-27

**Status:** HC-41 exact role/closure theorem draft; no simple support,
placements or candidate

## 1. The rooted octagon

Take one side in each K47B residual arc and write the cyclic side-length word

```text
H, Y, P, Y, D, X, Q, X.                              (1.1)
```

Let the `X|H` and `Y|D` root vertices have angle `alpha`, and the `H|Y` and
`D|X` root vertices angle `beta=pi-alpha`, with `alpha!=beta`. Denote the
positive side lengths by lower-case letters.

### ST-M1.K48R

Assume `h,d,p,q,x,y` are pairwise distinct except for the displayed repeats
of `x,y`. Then the unmarked boundary with its angle data recovers every role
`H,D,P,Q,X,Y` up to global reflection.

### Proof

The repeated length classes identify `X,Y`. Of the four singleton classes,
`P` is the unique side flanked by `Y,Y`, while `Q` is flanked by `X,X`.
The remaining singleton sides `H,D` are each flanked once by `X` and once by
`Y`, but their angle incidences differ:

```text
H: alpha next to X, beta next to Y;
D: alpha next to Y, beta next to X.                  (1.2)
```

Since `X!=Y` and `alpha!=beta`, (1.2) distinguishes them. Reversing the
whole boundary reverses every rooted reading together and creates no role
permutation. □

Thus the N50 marking trap does not kill the smallest template.

## 2. Curvature budget

Orient the boundary counterclockwise and let an interior angle `theta` have
signed exterior turn `pi-theta` in `(-pi,pi)`. Write `r_1,r_2` for the turns
around side `P` and `s_1,s_2` around side `Q`.

### ST-M1.N51

Every simple irredundant realization obeys

```text
r_1+r_2+s_1+s_2=0.                                  (2.1)
```

In particular it is nonconvex: at least one residual vertex is reflex and at
least one is convex.

### Proof

The four root turns are

```text
pi-beta=alpha, pi-alpha=beta,
pi-beta=alpha, pi-alpha=beta,
```

and sum to `2*(alpha+beta)=2*pi`, the entire turning number of a simple
counterclockwise polygon. The remaining four turns therefore sum to zero.
They are nonzero by irredundancy, so they cannot all have one sign. □

## 3. Complete turn recursion

Normalize the direction of `H` to `1` in the complex plane and put

```text
A=exp(i*alpha),  U=exp(i*r_1),  Z=exp(i*(r_1+r_2)),
V=exp(i*s_1).                                       (3.1)
```

Equation (2.1) fixes `s_2=-(r_1+r_2+s_1)`. The eight directed edge vectors,
in boundary order, are

```text
h,
y*A,
p*A*U,
y*A*Z,
-d*Z,
-x*A*Z,
-q*A*Z*V,
-x*A.                                               (3.2)
```

### ST-M1.K48C

The rooted octagon closes if and only if

```text
h - d*Z + (y-x)*A*(1+Z) + p*A*U - q*A*Z*V = 0,      (3.3)
```

where all six lengths are positive and the four residual turns obtained from
(3.1) and (2.1) lie strictly in `(-pi,pi)\{0}`.

### Proof

Starting from `H`, the root turn at `H|Y` is `alpha`, giving the second
direction. Applying `r_1,r_2`, then the root turns `beta,alpha`, then
`s_1,s_2`, gives (3.2) term by term; the final root turn `beta` returns the
direction to `1` exactly because of (2.1). Summing (3.2) is (3.3). A closed
oriented edge chain conversely recovers the stated turns and side word. □

K48C is closure only. Segment nonintersection and correct turning number are
still required for a simple support.

## 4. Next exact fork

HC-41 must now do one of three things without sampling:

- give exact algebraic angles and pairwise-distinct positive lengths solving
  (3.3), then prove all eight nonadjacent segment pairs disjoint;
- prove every solution of (3.3) self-intersects or degenerates; or
- freeze after session 172 with the unresolved semialgebraic obligation.
