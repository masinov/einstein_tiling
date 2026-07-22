# Exact lens geometry for the smallest K13F weights

**Status:** HC-23 fixed-instance proof draft; no polygon or candidate

**Fixed data:**

```text
(a,b,c,h,d)=(1,4,6,11,12),
boundary word d,A,d,B,d,C,d,H,d,C,d,B,d,A,d.           (0.1)
```

No alternative tuple or boundary word is admitted in this checkpoint.

## 1. Role-recognition audit from zero

The five numerical length classes are pairwise distinct, but only `H` occurs
once intrinsically. Their boundary multiplicities and retained contexts are:

| class | length | intrinsic occurrences | required context |
|---|---:|---:|---|
| `A` | 1 | 2 | intended terminal code germ versus ERR-009 mixed auxiliary germ |
| `B` | 4 | 2 | intended convex code germ versus two-reflex N26 auxiliary germ |
| `C` | 6 | 2 | intended convex code germ versus two-reflex N26 auxiliary germ |
| `H` | 11 | 1 | unique side; full shield contact or K13F host subdivision |
| `d` | 12 | 8 | ordered neighboring length/angle context; never length alone |

Thus ERR-008/ERR-009 transfer structurally, but the old length-based audit
does not. In particular, the eight `d` sides are highly nonunique and the
paired code classes require their corrected endpoint contexts.

## 2. Scoped full-side arithmetic cover tables

Assume only K11S cover-side vertex alignment V for this section.  Before
transition or angle restrictions, a target side may be partitioned by full
sides whose lengths lie in `{1,4,6,11,12}`.  Order is suppressed below; every
distinct ordering is a separate rooted cover word.

The complete coefficient tables up to each target are:

```text
A=1:
  A.

B=4:
  B; 4A.

C=6:
  C; B+2A; 6A.

H=11:
  H; C+B+A; C+5A; 2B+3A; B+7A; 11A.

d=12:
  d; H+A; 2C; C+B+2A; C+6A;
  3B; 2B+4A; B+8A; 12A.                              (2.1)
```

### Exhaustion

For targets below 11, sides of length 11 or 12 cannot occur. The displayed
lists are the nonnegative solutions of `r+4p+6q=t`. For `t=11`, take
`q=0,1`; for `t=12`, take `q=0,1,2`, then add the single possibilities
`H+A` and `d`. These cases exhaust all coefficients.

K13A plus the forced host transition graph reduces the **intended H-host**
table to `ABC,ACB`, and `[H]` is the shield class. It does not erase the
unrestricted arithmetic coincidences on `A,B,C,d`; those require endpoint,
transition and ultimately geometric contact exclusions. This is the closed
list of side-cover tables HC-23 tracks beyond `H`.

## 3. Exact square-lens frame

K10B's guard has two sides of length `d` meeting at `Gamma` with angle
`pi/2`. Its spine endpoints `R,Q` therefore satisfy

```text
|R-Q|=d*sqrt(2).                                        (3.1)
```

The upper guard path and its half-turn form a square of side `d`, with
vertices `R,Gamma,Q,-Gamma`. Let `u,v` be the orthonormal unit vectors from
`R` toward `Gamma,-Gamma`. Then

```text
R-Q lens = {R+x*u+y*v : 0<=x<=d, 0<=y<=d},
Q-R = d*(u+v).                                          (3.2)
```

Every vertex and every edge of a K10B spine satisfying lens containment must
lie in this square. In particular, every spine-edge length is at most its
diameter `d*sqrt(2)`.

## 4. Fixed first turn

Starting from `R`, the spine begins with `A` of length `a=1`, followed by a
`d=12` side. Their polygon interior angle is the prescribed `pi/4`, so the
signed change of boundary direction is `+3*pi/4` or `-3*pi/4` according to
the reflected orientation. HC-23 must test that two-edge prefix against
(3.2) before solving the remaining closure equations.

## 5. Stop rule

Session 125 derives the exact containment inequality for this prefix and the
central `H` side. If the fixed data violate a necessary inequality, HC-23
closes by theorem and no coordinate list is attempted. Only if every
necessary inequality survives may session 126 give the complete exact vertex
list and both placement tables. Approximate coordinates or a new value of
`d` are not admitted.
