# K16W budget and encoding audit

**Date:** 2026-07-23

**Status:** HC-32 theorem draft; conservative reductions only, no solver,
coordinates, polygon or candidate

**Normalization:** `u=1`, as in K21Q

## 1. K30W: exact code-edge window

For either rigid hook put `w in {b,c}` and let `(x_w,y_w)` be its unit
length-`v` direction.  N38 gives

```text
v^2>23/2,       w>sqrt(2),
|y_w|<1/v,      x_w*y_w>0.                         (1.1)
```

The hook's code edge has one coordinate displacement
`w*(x_w-y_w)/sqrt(2)`.  Open-rectangle containment therefore gives

```text
w*|x_w-y_w|/sqrt(2)<1.                            (1.2)
```

### ST-M1.K30W

Every K16W point satisfies, for `w=b,c`,

```text
sqrt(2) < w
 < sqrt(2)/(sqrt(1-v^(-2))-v^(-1))
 < sqrt(46)/(sqrt(21)-sqrt(2)).                   (1.3)
```

**Admitted form:** necessary-condition implication from complete K16W.

### Proof

Because the coordinates have the same sign,

```text
|x_w-y_w| >= ||x_w|-|y_w||
 > sqrt(1-v^(-2))-v^(-1)>0.                       (1.4)
```

Combine (1.2) and (1.4).  The denominator in (1.3) is strictly increasing
for `v>1`, since its derivative is

```text
1/(v^3*sqrt(1-v^(-2)))+1/v^2>0.                  (1.5)
```

Thus the upper bound is strictly decreasing.  Substitution at
`v=sqrt(23/2)` gives the final constant in (1.3); N38 is strict.  The lower
bound is N38.  □

The moving upper endpoint tends to `sqrt(2)` as `v` tends to infinity.  This
controls the noncompact end but does not bound `v`, because `a` may still
grow with `v`.

## 2. K30B: exact host component budgets

Use K19E's block form

```text
p_8=F*r_0+H_b*r_b+H_c*r_c,
F=a+q,
H_w=(v-w/sqrt(2))+i*(w/sqrt(2)-1).                (2.1)
```

Write `p_8=(P,Q)`, `D=(v,1)`, and let the central host edge be

```text
e_H=D-2*p_8=h*(x_H,y_H).                          (2.2)
```

### ST-M1.K30B

K17S host closure is exactly equivalent to

```text
v=2P+h*x_H,
1=2Q+h*y_H,
x_H^2+y_H^2=1.                                   (2.3)
```

**Admitted form:** exact definitional equivalence.

### Proof

Since `h=a+b+c>0`, (2.2) defines `(x_H,y_H)` uniquely.  The scalar closure
`|D-2p_8|=h` is then exactly its unit equation, while the two component
identities are (2.2).  Conversely (2.3) reconstructs (2.2) and closure.  □

This is an identity, not yet a compactness theorem.  Adding `(x_H,y_H)` to
K21Q would increase rather than reduce its variable count; Section 4
therefore retains (2.3) as an analytic budget only.

## 3. N40: the two cells have no carrier-word mirror quotient

The cyclic K16B side-role word is

```text
v,A,u,v,B,u,v,C,u,H,u,C,v,u,B,v,u,A,u.           (3.1)
```

### ST-M1.N40

No dihedral automorphism of the intrinsic K16B boundary word exchanges
`P_+-` with `P_-+`.  Consequently traversal reversal or a carrier reflection
does not license deleting either exact cell.

**Admitted form:** exact-bijection audit, negative result.

### Proof

The unique `H` side fixes every rotational symmetry, so a nonidentity word
symmetry would have to be the reflection through `H`.  Reading away from its
two ends gives the same eight roles

```text
u,C,v,u,B,v,u,A
```

on both sides, but the next roles are respectively `u` and `v`.  K16B has
`u!=v`, so the reflection fails.  Hence the labeled cyclic word has trivial
dihedral automorphism group.  Permuting `A,B,C` cannot repair the first
mismatch, which is between `u` and `v` after all three code roles have
already been fixed by the preceding walk.  Any carrier isometry preserving
the intrinsic contact roles induces such a word automorphism.  □

This excludes the proposed geometry-induced universal quotient.  It does
not prove that no unrelated algebraic bijection exists on a special
equal-length subvariety, so both complete cells remain.

## 4. K30E: exact terminal elimination is structurally worse than K21Q

For preterminal `w_8=X+iY`, put

```text
A=v*X+Y,
B=X-v*Y,
T=(v^2+1+4*(X^2+Y^2)-h^2)/4,
R=A^2+B^2=(v^2+1)*(X^2+Y^2)>0.                   (4.1)
```

N35 supplies `R>0`.  The closure line and unit circle are

```text
A*C+B*S=T,       C^2+S^2=1.                      (4.2)
```

With `Delta=R-T^2`, their solutions are exactly

```text
C=(A*T - epsilon*B*sqrt(Delta))/R,
S=(B*T + epsilon*A*sqrt(Delta))/R,                (4.3)
epsilon in {-1,+1},       Delta>=0,
```

subject to the retained first-quadrant signs.

### ST-M1.K30E

Equation (4.3) is an exact two-branch elimination of the terminal direction,
but it gives no variable-count reduction over the actual K21Q tangent chart
and raises the cleared polynomial-degree ceiling.  It is therefore rejected
as an HC-33 encoding unless a later structure theorem changes the count.

**Admitted form:** exact equisatisfiable substitution, audited but not
adopted.

### Accounting

K21Q already represents the terminal unit direction by the single variable
`t0`; the complete normalized formula has eight real variables including
`sqrt_half`.  Clearing the three positive tangent denominators gives point
coordinate numerators of degree at most `7`, orientation/dot numerators of
degree at most `14`, and proper-crossing products of degree at most `28`.

For (4.3), retain the bridge tangent variables and let
`E=(1+t1^2)(1+t2^2)`.  The preterminal coordinates have numerator degree at
most `5` over `E`; `A,B` have numerator degree at most `6`, `T` degree `10`
over `E^2`, and the cleared discriminant has degree `20`.  Replacing `t0` by
one radical variable therefore leaves eight variables.  The substituted
terminal direction has numerator and denominator degree at most `16`; point
coordinates reach degree `21/20`, orientation numerators `42`, and a proper
crossing product `84`.  Thus the proposed substitution changes the maximum
ceiling from `28` to `84` without reducing dimension.

The often-quoted one-variable saving applies only against a naive `(C,S)`
plus circle encoding, not against the serialized K21Q formula.

## 5. Session-145 disposition

K30W is the only new strict necessary inequality to carry into
compactification.  K30B is retained as an exact analytic identity.  N40
keeps both cells.  K30E prevents an unjustified high-degree rewrite.  The
next theorem session must analyze `lambda=1/v`; no formula or solver change
is authorized here.
