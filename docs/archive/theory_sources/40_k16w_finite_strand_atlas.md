# K16W finite strand and direction atlas

**Date:** 2026-07-23

**Status:** HC-32 theorem draft; exhaustive finite cover of the bounded
remaining cell, no solver verdict, polygon or candidate

**Scope:** the sole surviving `P_+-` cell after N41/K31C

## 1. Five forced crossings of the symmetry line

Let `ell` be the vertical line `x=v/2`.  For the first B spoke,

```text
p_(2,x)<delta(v)<v/2,
p_(3,x)>L(v)>v/2.                                (1.1)
```

For the C spoke the inequalities reverse.  Their half-turn partners have
the complementary endpoints, so all four length-`v` segments cross `ell`
once.  The central host has endpoints `p_8` and `D-p_8`; it also crosses
`ell` once.  It cannot lie on `ell`, because its vertical extent is below
`1` while `h=a+b+c>5/sqrt(2)>1`.

Write the B/C crossing heights as `y_B,y_C`.  Central symmetry gives the
other three heights

```text
1-y_B,       1-y_C,       1/2.                    (1.2)
```

All five are distinct in a simple spine: equality would be an intersection
of two nonadjacent closed segments.

## 2. The C strand is above the B strand

Retain K27X's

```text
p_5-p_2=(A+i*B)*r_b,
A=v-b/sqrt(2)>0,
B=b/sqrt(2)-1>0.                                  (2.1)
```

At horizontal coordinate `p_(5,x)`, the parameter on the supporting B line
is

```text
t_*=A-B*y_b/x_b.                                  (2.2)
```

N38 gives `0<y_b/x_b<sqrt(2/21)<1/3`.  K31C gives
`b<98/43`; using `v>3` and `1/sqrt(2)<1` yields

```text
A>31/43>55/129>B/3.                               (2.3)
```

Hence `0<t_*<A<v`, so this vertical line meets the interior of the B spoke.
The C endpoint `p_5` lies above that B-line point by exactly

```text
B/x_b>0.                                          (2.4)
```

Both long segments also contain their intersections with `ell`.  Since the
complete spine forbids their intersection, their vertical order cannot
change over the common horizontal interval.  Therefore

```text
y_C>y_B.                                          (2.5)
```

## 3. K32S: four exhaustive strand orders

Put

```text
d_B=y_B-1/2,       d_C=y_C-1/2.                   (3.1)
```

Simplicity gives `d_B*d_C*(d_B-d_C)*(d_B+d_C)!=0`, while (2.5) gives
`d_B<d_C`.

### ST-M1.K32S

Every K16W point belongs to exactly one of the following four cells:

```text
S_1: 0<d_B<d_C;
S_2: d_B<d_C<0;
S_3: d_B<0<d_C,  d_B+d_C<0;
S_4: d_B<0<d_C,  d_B+d_C>0.                      (3.2)
```

Equivalently, the bottom-to-top orders of the five long strands are

```text
S_1: C',B',H,B,C;
S_2: B,C,H,C',B';
S_3: B,C',H,C,B';
S_4: C',B,H,B',C.                                 (3.3)
```

**Admitted form:** exact exhaustive disjoint partition.

### Proof

Two nonzero real numbers with `d_B<d_C` either have the same sign or straddle
zero.  The straddling case is divided exactly by the nonzero sign of their
sum.  These are disjoint and exhaustive.  Equations (1.2) convert them to
(3.3).  □

The midline heights are rational expressions in the existing endpoints;
their denominators have fixed signs by (1.1).  Thus each cell can be cleared
to exact polynomial signs without adding a geometric assumption.  K32S
does not claim any of the four cells is nonempty.

## 4. K32A: bounded exact circle charts

The current bridge chart

```text
T(t)=((1-t^2)/(1+t^2), 2t/(1+t^2))               (4.1)
```

uses unbounded `t`.  For each bridge direction choose one sign
`sigma in {+1,-1}` and impose

```text
z=sigma*T(t),       -1<=t<=1,       t!=0.         (4.2)
```

### ST-M1.K32A

The two signs in (4.2) cover the unit circle with `z=+1,-1` removed.  For
two bridges, the four sign pairs give an exact finite bounded cover of every
K16W direction choice, without increasing continuous variable count or
polynomial degree.

**Admitted form:** exact finite equisatisfiable cover.

### Proof

`T([-1,1])` is the closed right semicircle and `-T([-1,1])` the closed left
semicircle.  Their overlap is the two vertical directions.  Removing `t=0`
removes `+1` in the positive chart and `-1` in the negative chart, exactly
the two K17S bridge exclusions.  Conversely an old parameter with `|t|<=1`
uses the positive chart; one with `|t|>=1` uses the negative chart with
parameter `-1/t`.  Multiplication by a fixed sign changes no degree.  □

Together with K31C and the already bounded `0<t0<1`, K32A places every
continuous variable in a finite bounded box.  The boxes overlap only on
valid chart seams; overlap does not lose or invent a solution.

## 5. K32R: exact closure regularity split

Use K30E's `R,T,Delta=R-T^2`.  N35 gives `R>0`.

### ST-M1.K32R

The bounded atlas has the exact closure split

```text
Delta<0: no terminal orientation;
Delta=0: one tangent orientation;
Delta>0: two transverse orientations before first-quadrant filtering.
                                                               (5.1)
```

On `Delta>0`, the derivative of closure along the terminal unit circle is
nonzero at either root.  On `Delta=0` it vanishes and the tangent root must be
handled as a separate algebraic stratum.

**Admitted form:** exact exhaustive regularity partition.

### Proof

This is the ordinary line--circle intersection discriminant from K30E.
Strict positivity gives two transverse intersections; equality gives the
unique tangent point; negativity gives none.  N35 excludes an identically
zero line.  □

K32R names the specific place where interval Newton/Krawczyk reasoning can
apply, but does not prove a complete interval algorithm.  Strict containment
and nonintersection boundaries still require exact exclusion certificates or
separate algebraic strata.

## 6. Decision contract after HC-32

The surviving problem has an exact cover by

```text
4 bridge-chart pairs x 4 strand orders = 16 bounded cells,               (6.1)
```

each further split by (5.1) if a future method benefits.  Every cell retains
the original closure, all 32 containment bounds and all 120 nonadjacent-pair
predicates.  A future decision may add K30W, N41/K31C and the selected K32S
signs only because their admitted forms are explicit in the ledger.

No HC-32 result licenses a solver run.  A later preregistration must choose
one exact complete method for all 16 cells and state how SAT witnesses and
UNSAT/tangent boundary cases are independently certified.  Merely increasing
the HC-31 timeout remains forbidden.
