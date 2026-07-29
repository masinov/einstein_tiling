# K16W selector normal form

**Date:** 2026-07-24

**Status:** HC-37 theorem draft; exact line--chord form and chart-scope
obstruction, no root or cell elimination

**Scope:** K36P on the six complete transverse K34Q cells

For either long strand `j in {B,C}`, abbreviate

```text
rho=rho_j,       w_j=its initial relative vertex,
w=w_8,           r^2=|w|^2,
s=dot(rho,w),    n=det(rho,w),
m=det(rho,w_j).                                    (0.1)
```

Thus `s=Q_j`, `r^2=s^2+n^2`, and K36M gives

```text
F_j=T*n-2*r^2*m.                                   (0.2)
```

## 1. K38N: factored selector identity

### ST-M1.K38N

The complete K36P selector has the exact radical-free normal form

```text
P_j=F_j^2-Delta*Q_j^2
   =r^2*((T-2*n*m)^2-s^2*(d^2-4*m^2)).             (1.1)
```

Whenever `d^2>4*m^2`, root selection is equivalently

```text
P_j<0
iff
|T-2*n*m| < |s|*sqrt(d^2-4*m^2).                  (1.2)
```

**Admitted form:** exact definitional equivalence.  This exposes a geometric
line--chord test but does not lower the deployed variable or degree count and
does not establish (1.2) on a live cell.

### Proof

Use `Delta=d^2*r^2-T^2`, `Q_j=s` and (0.2):

```text
P_j
=(T*n-2*r^2*m)^2-(d^2*r^2-T^2)*s^2
=r^2*(T^2-d^2*s^2-4*T*n*m+4*r^2*m^2)
=r^2*((T-2*n*m)^2-s^2*(d^2-4*m^2)).               (1.3)
```

The last equality uses `r^2=s^2+n^2`.  Since `r^2>0`, (1.2) follows by
moving the positive terms and taking square roots.  □

Geometrically, `m` is the signed distance numerator of the strand's
supporting line from the origin.  The two possible relative rectangle centers
are the endpoints of K36W's root chord.  Equation (1.1) is negative exactly
when that chord crosses the supporting line.  This interpretation retains the
finite strand segment and all other simplicity predicates; it does not replace
them.

## 2. K38B: exact first-bridge offset

Put `k=1/sqrt(2)`.  For B,

```text
rho_B=q*z_1,       w_B=w_2=a+q,
z_1=-T(t_1),       -1<t_1<1, t_1!=0,              (2.1)
```

where the final strict chart range follows from K33C's `Re(z_1)<0`.  Direct
rotation into the B frame gives

```text
m_B=det(rho_B,w_2)
   =[k*a*(1-t_1^2)+2*t_1*(1-k*a)]/(1+t_1^2).       (2.2)
```

### ST-M1.K38B

The fixed bridge-chart sign `sigma_1=-1` does not fix even the sign of the B
support-line offset `m_B` over the admitted weight range:

- if `a<sqrt(2)`, (2.2) is positive near `t_1=0` and negative near
  `t_1=-1`;
- if `a>sqrt(2)`, it is positive near `t_1=0` and negative near `t_1=+1`;
- if `a=sqrt(2)`, it is ` (1-t_1^2)/(1+t_1^2)>0` throughout the strict chart.

**Admitted form:** exact scope obstruction.  It proves that the chart sign
alone supplies no uniform `m_B` sign; it is not a K16W feasibility result and
does not prove that `P_B` takes both signs on a complete cell.

### Proof

Since `conj(rho_B)*w_2=conj(z_1)*(1+a*conj(q))`, taking the imaginary part
and substituting

```text
z_1=(-(1-t_1^2),-2*t_1)/(1+t_1^2)                 (2.3)
```

gives (2.2).  At `t_1=0` its numerator is `k*a>0`.  At the excluded endpoints
its limiting values are respectively

```text
t_1 -> -1: 2*(k*a-1),
t_1 -> +1: 2*(1-k*a).                              (2.4)
```

Continuity gives the first two cases on strict neighborhoods inside the
chart.  At `k*a=1`, (2.2) reduces to the displayed positive expression.  □

## 3. Consequence for HC-37

K38N is the exact selector target, but K38B refutes the hoped-for shortcut
“left bridge semicircle fixes the supporting-line side.”  Any uniform proof
of `P_B<0` must combine the complete K32S strand cell, closure budgets and
additional containment/nonintersection inequalities.  The `sigma_2` chart
still enters C through both its direction and initial point; it receives the
same full-cell test in session 160.
