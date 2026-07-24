# K16W transverse-root strand law

**Date:** 2026-07-24

**Status:** HC-36 theorem draft; exact root-selection criterion, no uniform
root or cell elimination

**Scope:** the `Delta>0` part of the six complete bounded K34Q cells

Retain the notation of K35D and put

```text
w=w_8,            r^2=|w|^2,
W_epsilon=conj(Z_epsilon)*D.                       (0.1)
```

Rotating the physical spine by `conj(Z_epsilon)` sends its terminal frame to
the relative K17S frame, the rectangle diagonal `D` to `W_epsilon`, and its
center to `W_epsilon/2`.

## 1. K36W: the diagonal in the two relative frames

Closure and K35D give

```text
dot(w,W_epsilon)=T,
det(w,W_epsilon)=-epsilon*sqrt(Delta).              (1.1)
```

### ST-M1.K36W

The exact relative-frame rectangle diagonal is

```text
W_epsilon=
  (T*w-epsilon*sqrt(Delta)*i*w)/r^2.                (1.2)
```

**Admitted form:** exact definitional equivalence; no complexity count is
reduced.

### Proof

Rotation preserves dot products and determinants.  Since
`p_8=Z_epsilon*w`, rotating `(D,p_8)` by `conj(Z_epsilon)` gives
`(W_epsilon,w)`.  K35D supplies

```text
dot(W_epsilon,w)=T,
det(W_epsilon,w)=epsilon*sqrt(Delta),                (1.3)
```

which is (1.1) after reversing the determinant.  The orthogonal basis
`(w,i*w)` has squared norm `r^2`, so (1.2) is its unique reconstruction.  □

## 2. K36M: every midline sign is affine in the radical

Consider a directed relative unit strand from `w_j` in direction `rho`, and
suppose its physical image

```text
p=Z_epsilon*w_j -> p+ell*Z_epsilon*rho              (2.1)
```

crosses `x=v/2`.  Let

```text
chi_epsilon=Re(Z_epsilon*rho) != 0                  (2.2)
```

and let `d_epsilon` be its crossing height minus `1/2`.  A direct line
intersection gives

```text
d_epsilon
 =-det(rho,W_epsilon/2-w_j)/chi_epsilon.            (2.3)
```

Define the radical-free coefficients

```text
F(rho,w_j)=T*det(rho,w)-2*r^2*det(rho,w_j),
Q(rho)=dot(rho,w),                                  (2.4)
L_epsilon(rho,w_j)=F(rho,w_j)
                    -epsilon*sqrt(Delta)*Q(rho).     (2.5)
```

Then

```text
2*r^2*det(rho,W_epsilon/2-w_j)=L_epsilon(rho,w_j).
                                                               (2.6)
```

For the two K16W long strands use

```text
rho_B=q*z_1,       w_B=w_2,       chi_B>0,
rho_C=q^3*z_1*z_2, w_C=w_5,       chi_C<0.          (2.7)
```

Write the corresponding coefficients as `F_B,Q_B,L_B^epsilon` and
`F_C,Q_C,L_C^epsilon`.

### ST-M1.K36M

On either transverse closure root,

```text
sign(d_B^epsilon)=-sign(L_B^epsilon),
sign(d_C^epsilon)= sign(L_C^epsilon).               (2.8)
```

Consequently the first two K32S sign requirements are exactly

```text
S1: L_B^epsilon<0,  L_C^epsilon>0;
S2: L_B^epsilon>0,  L_C^epsilon<0;
S3: L_B^epsilon>0,  L_C^epsilon>0,                  (2.9)
```

with S3's additional `d_B+d_C<0` retained separately.  Equality in any
displayed sign would put B or C through the center, an interior point of H,
and is already forbidden by complete spine simplicity.

**Admitted form:** exact necessary-and-sufficient rewriting of the named
strand signs.  It reduces neither roots nor cells until a sign in Section 3
is proved.

### Proof

In physical coordinates, with rectangle center `O=D/2`,

```text
det(Z*rho,O-Z*w_j)=-chi_epsilon*d_epsilon.           (2.10)
```

Rotate by `conj(Z)` and use (1.2); multiplying by the positive `2*r^2`
gives (2.3)--(2.6).  The B strand points east and the C strand west by N39,
so their denominator signs give (2.8).  Substitution of K32S's B/C signs
gives (2.9).  The center belongs to the relative interior of H; a B/C equality
would therefore be a nonadjacent intersection.  □

## 3. K36P: radical-free root-selection test

The two conjugate strand expressions satisfy

```text
L_j^+*L_j^-=F_j^2-Delta*Q_j^2,
j in {B,C}.                                         (3.1)
```

### ST-M1.K36P

For either named long strand:

1. if `F_j^2-Delta*Q_j^2<0`, its two closure roots lie on opposite sides of
   H at the midline, and every fixed K32S strand sign retains at most one
   root;
2. if `F_j^2-Delta*Q_j^2>0`, both roots have the same strand sign, determined
   by `F_j`; and
3. equality is incompatible with a complete simple K16W spine for whichever
   root makes `L_j^epsilon=0`.

Thus a proof that

```text
(F_B^2-Delta*Q_B^2)<0
or
(F_C^2-Delta*Q_C^2)<0                               (3.2)
```

holds throughout one complete K34Q cell would reduce that cell's transverse
closure-root count exactly from two to at most one.

**Admitted form:** exact conditional necessary implication.  The quantified
reduction `2 -> <=1` is **not** booked for any live cell because (3.2) has not
been established there.

### Proof

Equation (3.1) is multiplication of the two expressions (2.5).  A negative
product means opposite nonzero signs; a positive product means equal signs,
whose common sign is the sign of their sum `2*F_j`.  The zero case is the
center contact excluded after (2.9).  Combining with (2.8) proves the three
claims and the conditional reduction.  □

## 4. Why this is not yet a root theorem

K35F already shows that closure and endpoint filters alone allow both roots.
K36P identifies the exact missing full-spine inequalities, but no existing
result fixes the signs of either polynomial in (3.2) over an entire cell.
In particular, using one evaluated parameter point or replacing the retained
120 pair predicates by (3.2) would be unsound.

The final HC-36 session may use the cell-specific S1/S2/S3 signs and bridge
charts to attack (3.2), or derive a different exact chord squeeze.  Failure to
prove a uniform sign leaves both transverse roots and all six cells open.
