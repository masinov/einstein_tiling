# Exact rooted-hinge octagon support

**Date:** 2026-07-27

**Status:** HC-41 exact simple-support theorem; boundary-germ level only, no
complete hinge placement, termination, tiling or aperiodicity claim

## 1. Exact data

Put `r=sqrt(3)` and take the vertices in boundary order

```text
v_0=(0,0),
v_1=(13,0),
v_2=(29/2,3r/2),
v_3=(27/2,5r/2),
v_4=(15,4r),
v_5=(9,4r),
v_6=(7,2r),
v_7=(2,2r).                                         (1.1)
```

Label the edges `v_j v_(j+1)` cyclically by

```text
H,Y,P,Y,D,X,Q,X.                                    (1.2)
```

### ST-M1.K49W

The data (1.1)--(1.2) define a simple irredundant symmetry-free octagon with

```text
(h,y,p,y,d,x,q,x)=(13,3,2,3,6,4,5,4),              (1.3)
alpha=pi/3, beta=2*pi/3,                             (1.4)
```

and residual turns

```text
(r_1,r_2,s_1,s_2)=(pi/3,-pi/3,-pi/3,pi/3).          (1.5)
```

It satisfies K48C and realizes the complete K47B rooted boundary germs.

## 2. Lengths, angles and closure

The eight edge vectors are

```text
(13,0),
(3/2,3r/2),
(-1,r),
(3/2,3r/2),
(-6,0),
(-2,-2r),
(-5,0),
(-2,-2r).                                           (2.1)
```

Their squared lengths are respectively

```text
169,9,4,9,36,16,25,16,
```

proving (1.3), and their sum is zero. Their directions are

```text
0, pi/3, 2*pi/3, pi/3, pi, 4*pi/3, pi, 4*pi/3.      (2.2)
```

The signed turns derived from (2.2) are

```text
beta, alpha, r_1, r_2, beta, alpha, s_1, s_2
```

when cyclically rooted at `X|H`; equivalently the four root interior angles
are `alpha,beta,alpha,beta` in the K47B positions and (1.5) holds. No turn is
zero or `+/-pi`, so the boundary is irredundant. Substitution in K48C also
gives closure directly:

```text
x=y+p/2=4,       h=d+p+q=13.                        (2.3)
```

## 3. Exact simplicity proof

Let `E_j=[v_j,v_(j+1)]`. Their closed axis-aligned bounding boxes are

```text
E_0: [0,13]       x {0}
E_1: [13,29/2]    x [0,3r/2]
E_2: [27/2,29/2]  x [3r/2,5r/2]
E_3: [27/2,15]    x [5r/2,4r]
E_4: [9,15]       x {4r}
E_5: [7,9]        x [2r,4r]
E_6: [2,7]        x {2r}
E_7: [0,2]        x [0,2r].                         (3.1)
```

For every nonadjacent pair, the boxes in (3.1) are disjoint in at least one
coordinate. Adjacent boxes meet only at their listed common endpoint; the
first and last do likewise. Hence no two nonadjacent closed edges intersect,
so the closed chain is a simple polygon.

The six numerical length classes `13,3,2,6,4,5` are pairwise distinct, and
K48R therefore recovers every role. In particular any Euclidean symmetry
would fix all six roles and hence every edge, so it is the identity.

## 4. Exact scope

K49W proves the smallest K47B support exists. It does **not** prove:

- four complete copies realize either K46S state without remote overlap;
- the full `H,D,X,Y` side contacts terminate in finite legal stars;
- other contacts of the octagon are excluded;
- a plane tiling exists; or
- any local or global aperiodicity statement.

The object must remain a support witness, not a candidate tile, until those
obligations are discharged in a separately authorized checkpoint.
