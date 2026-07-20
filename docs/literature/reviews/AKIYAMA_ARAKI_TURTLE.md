# Akiyama--Araki: alternative Turtle proof

**Catalog ID:** `akiyama-araki-turtle-2025`  
**Audited version:** arXiv:2307.12322v7, 2025-01-20  
**Published:** *Discrete & Computational Geometry* 74 (2025), 771--792,
DOI `10.1007/s00454-025-00717-6`  
**Audit date:** 2026-07-20  
**Status:** full text and source bundle audited; published geometry not yet
fully reimplemented.

## Result and architecture

The paper gives two logically separate pieces for the Turtle:

1. Section 3 constructs arbitrarily large Turtle patches with the Golden Hex
   patch-tile sequence, establishing existence of a plane tiling.
2. Section 4 equips every possible Turtle tiling with dispensable Golden
   Ammann bars and derives an irrational frequency, excluding every nonzero
   translational period without assuming the Golden Hex substitution.

This separation is valuable for W3. The construction proves existence, while
the Ammann-bar argument proves the universal nonperiodicity statement by a
different route.

## Exact theorem map

### Section 2: Sturmian words

The chosen slope is

```text
alpha = (5-sqrt(5))/10 = 1/(1+tau^2) = [3,1,1,1,...].
```

The standard words satisfy

```text
s_-1=1, s_0=0, s_1=001, s_(n+1)=s_n s_(n-1)  (n>=1).
```

For `n>=1`, deleting suffix `01` at odd index and `10` at even index
produces the central palindrome `p_n`. Equations (1) and (2) give the two
alternative decompositions used to close Golden Sturmian Patch boundaries.
Equation (1) starts at `p_3`; equation (2)'s generic form starts at `p_4`
because `s_0` is an exceptional seed.

### Section 3: Golden Hex existence

- **Lemma 1:** the geometric realization of a palindrome and its half-turn
  differ only by four kites at the two ends, hence share upper and lower
  boundaries.
- **Theorem 1:** the sequences of patch-tiles `(T_n, Pi_n)` are well defined.
  Their members contain arbitrarily large balls, giving existence of Turtle
  tilings.

The induction uses exact central-word decompositions to show that the linear
Golden Sturmian Patches filling apparent gaps agree at the next level. The
appendix relates this simpler two-patch sequence to an older primitive
four-patch total substitution.

### Section 4: universal nonperiodicity

- **Lemma 2:** case analysis on Turtle angles and edge lengths forces every
  drawn Golden Ammann Bar (GAB) to continue straight across tile boundaries.
- **Lemma 3:** after fixing two bar directions, their crossings are in
  bijection with flipped Turtles.
- **Lemma 4:** GABs together with complementary GABs form a Kagome
  (trihexagonal) tiling.
- **Lemma 5:** the three indexed bar families obey `k=i+j` and
  `c_(i+j)-a_i-b_j=+-1/2`, producing an approximate hexagonal lattice of
  flipped tiles.
- **Lemma 6:** an Abel-summation calculation equates ordinary natural density
  with the weighted density used in the length count.
- **Theorem 2:** if the GAB frequency in one Kagome direction exists, all
  three frequencies agree and satisfy
  `q^2-q+1/5=0`. A periodic tiling would have a rational frequency, while both
  roots `(5+-sqrt(5))/10` are irrational; therefore every Turtle tiling is
  nonperiodic.

## Exact chirality consequence

The proof counts `n^2 q^2+O(n)` flipped tiles and `(3/5)n^2+O(n)` total
Turtles in its Kagome parallelogram. Therefore the two handedness densities
are

```text
f = (5/3) q^2 = (3 +- sqrt(5))/6,
```

and the minority density is

```text
f_- = (3-sqrt(5))/6 = 1/(1+phi^4) = 0.12732200375...
```

It is the irrational root below one half of `9f^2-9f+1=0`. This is the same
chirality frequency obtained from the Hat substitution matrix, as expected
for the common combinatorial tiling system.

Our independently generated Turtle disk contains 9,239 placements. Under the
repository convention `op=0..5` is orientation preserving and `op=6..11` is
mirrored; the two classes contain 1,181 and 8,058 placements. Its minority
fraction is

```text
1181/9239 = 0.127827687...
```

only `5.06e-4` above the exact infinite-volume prediction. This is a strong
external validation of A3, but finite boundary convergence is not a proof of
the density theorem.

## What is internally reproduced

`src/einstein/theory/turtle_sturmian.py` and its cold-verifiable artifact
reproduce:

- standard words and exact letter counts;
- all central palindromes and both decomposition identities through level 24;
- exact vanishing of the GAB and chirality density polynomials;
- exact handedness counts from the existing Turtle certificate.

The result is rendered in
`docs/notebook/assets/theory-w3-turtle-golden-sturmian.svg`.

## What remains external

The repository does not yet reconstruct:

- the geometric realization of `0` and `1` as linear Turtle patches;
- Lemma 1's four-end-kite half-turn geometry;
- the Golden Hex patch-tile induction and certified inballs;
- Lemma 2's exhaustive local GAB-continuation cases;
- the generalized-bar Kagome lemma or crossing bijection.

Accordingly, the published paper proves Turtle tileability and aperiodicity;
our present artifact is an exact combinatorial/density control, not an
independent full proof.

## Next reproducible steps

1. Encode GAB endpoints as exact points on `TURTLE_OUTLINE` and enumerate all
   legal endpoint neighborhoods to reproduce Lemma 2.
2. Recover generalized bars from exact patches and verify Kagome spacing and
   the crossing-to-minority-tile bijection.
3. Transcribe or reconstruct Golden Sturmian Patch geometry from the paper's
   source figures, then certify Theorem 1's boundary induction.
4. Compare the recovered symbolic factor with the Hat/Turtle A6 language and
   test whether shared tiling language can be detected automatically.
