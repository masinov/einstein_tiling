# K16W thin-lens reset no-go

**Date:** 2026-07-23

**Status:** corrected HC-33 theorem draft; H-west is refuted and the central
host must point east, but K16W remains open

> **ERR-013 correction.**  The original version claimed that central pairing
> reversed the traversed direction of C'.  In fact the half-turn negation and
> reversed vertex indexing cancel:
> `p_12-p_11=p_6-p_5`.  Thus C' is westward like C.  The H-east reset argument,
> the all-cell empty table and the claimed K16W refutation are withdrawn.

**Scope:** the fixed 19-edge K16B unequal-spoke rectangular carrier,
normalized by `u=1`

## 1. A directed reset bound

Consider two directed segments contained in the open vertical strip
`0<x<v`.  Suppose their horizontal displacements have the same nonzero
sign and absolute values strictly above `s_1,s_2`.  If a polygonal path of
total length `P` joins the terminal endpoint of the first segment to the
initial endpoint of the second, then

```text
P>s_1+s_2-v.                                      (1.1)
```

Indeed, for two eastward segments the first terminal endpoint has
`x>s_1`, while the second initial endpoint has `x<v-s_2`.  The joining path
must reset westward by more than `s_1+s_2-v`, and its length strictly exceeds
that horizontal displacement.  Reflection in a vertical line gives the
westward case.

This is a necessary condition only.  It does not replace or weaken any of
K21Q's segment predicates.

## 2. The forced neighboring pair

In the sole N41-surviving polarity cell, the length-`v` B strand is eastward
and the C strand is westward.  Central pairing preserves their **traversed**
edge vectors:

```text
p_12-p_11=p_6-p_5,       p_15-p_14=p_3-p_2.      (2.1)
```

The half-turn negates the geometric vector, but the paired vertex indexing
reverses its order; the two signs cancel.  Hence C' is westward like C and B'
is eastward like B.  Let the central H strand have length

```text
h=a+b+c.                                          (2.2)
```

Every endpoint is in the open `v`-by-1 rectangle.  Therefore the C/C'
horizontal span is strictly above

```text
L=sqrt(v^2-1),                                    (2.3)
```

and the H horizontal span is strictly above

```text
M=sqrt(h^2-1).                                    (2.4)
```

The central strand cannot be vertical because `h>5/sqrt(2)>1`, whereas its
vertical displacement is below `1`.  Hence it points either west or east.

If H points west, C and H have the same polarity.  The intervening path is
exactly the `c,1` path from `p_6` to `p_8`.  Thus (1.1) gives

```text
c+1>M+L-v=M-delta(v),
M<c+1+delta(v),                                  (2.5)
```

where `delta(v)=v-sqrt(v^2-1)`.

## 3. The opposite exact budget

K31C and K30W give

```text
v>v_0=sqrt(23/2),
c<U(v)<U_0=sqrt(46)/(sqrt(21)-sqrt(2)),
delta(v)<delta_0=(sqrt(46)-sqrt(42))/2.           (3.1)
```

The three exact rational comparisons needed below are

```text
v_0>10/3,       U_0<13/6,       delta_0<1/6.     (3.2)
```

The first follows by squaring, since `207>200`.  For the second, both sides
of

```text
6*sqrt(46)<13*(sqrt(21)-sqrt(2))                 (3.3)
```

are positive.  The left square is `1656`; the right square is
`3887-338*sqrt(42)`, which is strictly above `1690` because
`sqrt(42)<13/2`.  The last comparison in (3.2) follows from

```text
delta_0=2/(sqrt(46)+sqrt(42))<1/6.               (3.4)
```

Meanwhile `a>1/sqrt(2)`, `b>sqrt(2)`, and `c>sqrt(2)`, so

```text
h>5/sqrt(2),
M=sqrt(h^2-1)>sqrt(23/2)=v_0>10/3.               (3.5)
```

Equations (3.1)--(3.2) give the incompatible upper bound

```text
c+1+delta(v)<U_0+1+delta_0
                 <13/6+1+1/6=10/3.              (3.6)
```

## 4. Corrected ST-M1.N42: H must point east

Every simple K16W spine in the fixed K16B topology has eastward central H
edge:

```text
Re(p_9-p_8)=v-2*p_(8,x)>0,
p_(8,x)<v/2.                                      (4.1)
```

**Admitted form:** necessary-condition implication from complete K16W,
ending in contradiction.

### Proof

If H were westward, Section 2 would prove the necessary reset inequality
`M<c+1+delta(v)`.  Sections 3.5--3.6 prove the strict reverse chain

```text
M>10/3>c+1+delta(v).
```

Contradiction.  H is nonvertical, so it must point east.  The proof uses only
complete K16W containment, simplicity, the fixed K16B edge order, N38 and the
admitted K30W/K31C bounds.  □

## 5. Corrected disposition of the 16 HC-32 cells

Each K32S strand cell `S_1,...,S_4` and each K32A chart pair
`(+,+),(+,-),(-,+),(-,-)` inherits only (4.1).  The fixed long-strand
traversal pattern is

```text
B east, C west, H east, C' west, B' east.         (5.1)
```

No K32S order or K32A chart pair is refuted by N42.  All sixteen cells remain
open subject to the new exact sign `v-2*p_(8,x)>0`, every original predicate,
and K32R's discriminant/strict-boundary treatment.

## 6. Scope boundary

N42 excludes only the H-west half of K16W.  The H-east half, all four vertical
strand orders, all four bridge-chart pairs and the complete simplicity
problem remain open.  The reset lemma has no corresponding short
terminal-to-initial path in the alternating traversal pattern (5.1).
