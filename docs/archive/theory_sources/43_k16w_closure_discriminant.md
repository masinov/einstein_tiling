# K16W closure-discriminant geometry

**Date:** 2026-07-24

**Status:** HC-36 theorem draft; exact tangent-stratum reduction, no cell
refutation, solver verdict, polygon or candidate

**Scope:** the six complete bounded K34Q cells, normalized by `u=1`

Put

```text
D=(v,1),             d^2=v^2+1,
w_8=X+iY,            Z=C+iS,
p_8=Z*w_8,
A=v*X+Y,             B=X-v*Y,
T=(d^2+4*(X^2+Y^2)-h^2)/4,
R=A^2+B^2=d^2*(X^2+Y^2),
Delta=R-T^2.                                           (0.1)
```

N35 gives `R>0`.  The closure equation is

```text
A*C+B*S=T,          C^2+S^2=1.                       (0.2)
```

Every statement below retains the complete K34Q containment, strand and
nonintersection predicates.  The formulas do not replace those predicates by
a sampled angle or a weakened local test.

## 1. K35D: physical meaning of the two closure roots

Let `D_perp=(-1,v)`.  Direct expansion gives

```text
D dot p_8 = A*C+B*S,
det(D,p_8)=v*p_(8,y)-p_(8,x)=A*S-B*C.                (1.1)
```

### ST-M1.K35D

On `Delta>=0`, the two K30E closure roots are equivalently

```text
p_8=(T*D+epsilon*sqrt(Delta)*D_perp)/d^2,
epsilon in {-1,+1}.                                  (1.2)
```

In particular

```text
D dot p_8=T,
det(D,p_8)=epsilon*sqrt(Delta),                       (1.3)
p_(8,x)=(v*T-epsilon*sqrt(Delta))/d^2,
p_(8,y)=(T+epsilon*v*sqrt(Delta))/d^2.                (1.4)
```

**Admitted form:** exact definitional equivalence; it changes no variable,
root, cell or degree count.

### Proof

The ordered orthogonal basis `(D,D_perp)` has squared norm `d^2`.  Equations
(1.1) therefore give

```text
p_8=((D dot p_8)*D+det(D,p_8)*D_perp)/d^2.            (1.5)
```

Substituting K30E's two roots into the second equation of (1.1) gives

```text
A*S-B*C=epsilon*(A^2+B^2)*sqrt(Delta)/R
       =epsilon*sqrt(Delta).                         (1.6)
```

Closure supplies the first coefficient `T`, proving (1.2)--(1.4).  Conversely
(1.2) has norm `|w_8|`, dot product `T`, and determinant of the stated sign,
so division by the fixed nonzero `w_8` reconstructs exactly the corresponding
K30E unit root.  □

Thus the radical sign is geometric: it records which side of the main
rectangle diagonal contains `p_8`.  It is not an arbitrary solver branch.

## 2. K35T: exact tangent-stratum reduction

Assume `Delta=0`.  Equation (1.2) becomes

```text
p_8=lambda*D,             lambda=T/d^2.              (2.1)
```

Strict rectangle containment gives `0<lambda<1`.  Corrected N42 says the
central host points east, hence

```text
v-2*p_(8,x)=v*(1-2*lambda)>0,
0<lambda<1/2.                                         (2.2)
```

Consequently its complete vector and length are

```text
e_H=D-2*p_8=(1-2*lambda)*D,
h=(1-2*lambda)*d,                                    (2.3)
|w_8|=|p_8|=lambda*d,
d=h+2*|w_8|.                                         (2.4)
```

The alternative circle tangencies are excluded by the strict interior and
eastward-host signs; (2.4) is the only tangent branch retained by K16W.

The complex identity

```text
A+i*B=(v+i)*conj(w_8)                                (2.5)
```

and `R=T^2` give the unique terminal direction

```text
C=A/T,          S=B/T,          Z=(A+i*B)/T.          (2.6)
```

Since the deployed chart is `Z=T(t_0)` with `0<t_0<1`, its inverse is

```text
t_0=S/(1+C)=B/(T+A).                                 (2.7)
```

### ST-M1.K35T

For each of the six K34Q cells, its `Delta=0` intersection is exactly
equisatisfiable with the formula obtained by:

1. retaining variables `a,b,c,v,t_1,t_2,sqrt_half`;
2. adding `Delta=0`, `T>0`, `A>0`, `B>0` and `2*T<d^2`;
3. replacing `(C,S)` by `(A/T,B/T)`, equivalently replacing `t_0` by
   `B/(T+A)`; and
4. retaining every original containment, strand and 120 nonadjacent-pair
   predicate after clearing only the positive denominator `T`.

**Admitted form:** exact equisatisfiable substitution.  The serialized K21Q
cell uses eight real variables

```text
a,b,c,v,t_0,t_1,t_2,sqrt_half.
```

The tangent presentation uses seven.  Equivalently, it reduces the seven
geometric continuous variables to six while retaining the one fixed algebraic
auxiliary `sqrt_half`.  The measured gain is therefore

```text
solver real variables:       8 -> 7,
geometric variables:         7 -> 6,
closure roots on the stratum: 1 -> 1,
live K32S/chart cells:        unchanged,
maximum degree:              not claimed lower.      (2.8)
```

### Proof

Necessity is (2.1)--(2.7).  In particular `T>0`, and first-quadrant `Z`
gives `A,B>0`.  Conversely, `Delta=0` and `T,A,B>0` imply
`T=sqrt(A^2+B^2)` and make (2.6) a first-quadrant unit vector.  Formula (2.7)
then lies strictly in `(0,1)` because

```text
0<B<T<T+A.                                           (2.9)
```

The inequality `2*T<d^2` is exactly (2.2).  Substitution reconstructs the
unique tangent K21Q terminal direction, while retaining the complete original
predicate set proves both directions of equisatisfiability.  No radical
variable is introduced.  The variable counts follow directly from the two
displayed lists.  □

K35T satisfies HC-36's quantified-reduction criterion.  It does **not** prove
that any tangent cell is nonempty or empty.  In particular the diagonal host
occupies the strict subsegment from `lambda*D` to `(1-lambda)*D`; it does not
touch either rectangle corner, so tangency alone supplies no forbidden
contact.

## 3. K35F: the cheap filters do not select a transverse root

K35D also prevents an unsound shortcut.  First-quadrant terminal orientation,
strict placement of `p_8` in the rectangle and N42's eastward-host sign do not,
by themselves, choose `epsilon`.

Take

```text
D=(2,1),       alpha=1/4,       beta=1/20,
p_+=(9/20,7/20),       p_-=(11/20,3/20).             (3.1)
```

These are exactly `alpha*D +/- beta*D_perp`.  They have common squared norm
`13/40`, lie strictly in `(0,2)x(0,1)`, and both have first coordinate below
`1=v/2`.  Put `w_8=sqrt(13/40)>0` and `Z_+=p_+/w_8`,
`Z_-=p_-/w_8`.  Both terminal directions are unit and first-quadrant.  The
two host vectors have common squared length

```text
|(2,1)-2*p_+|^2=|(2,1)-2*p_-|^2=13/10,              (3.2)
```

and positive horizontal component.  Here

```text
T=5/4,       R=13/8,       Delta=1/16.               (3.3)
```

### ST-M1.K35F

The closure equation, first-quadrant terminal chart, strict `p_8` rectangle
containment and H-east sign admit both transverse roots.  Any uniform
one-root theorem for complete K16W must use an additional spine, strand or
nonintersection predicate.

**Admitted form:** exact separation control, not a K16W feasibility result and
not a complexity reduction.

The control deliberately does not assert that the displayed `w_8` is produced
by the K16B bridge recursion.  Its role is only to prove that the four cheap
filters named above are logically insufficient.

## 4. Remaining HC-36 work

The tangent stratum now has a seven-variable exact presentation.  Sessions
157--158 must use complete per-cell information, not the filters refuted by
K35F, to seek either:

- a tangent-cell contradiction;
- a transverse root elimination in one or more of `S1--,S1-+,S2--,S2-+,
  S3--,S3-+`; or
- a K25X-style nonadjacent-pair squeeze with an explicit lower count.

Absent one of those results, HC-36 stops with K35T as its sole quantified
reduction and K16W otherwise open.
