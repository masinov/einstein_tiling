# ST-M1.SER0 — source and quotient serialization contract

**Date:** 2026-07-21

**Status:** schema defined; direct primary-source serialization blocked because
the source supplies figures, not extensional tables

**Scope:** the S0/K1P proof-draft chain only; no geometric carrier work

## 1. Purpose

The proof notes define S0 functorially from finite published templates and
transported rules. A cold checker instead needs an extensional object: every
state and every allowed edge/vertex relation listed without consulting a
figure or choosing an occurrence. SER0 specifies that object and prevents a
visual reconstruction from being mislabeled as source transcription.

## 2. Required source object

A complete `stm1-s0-v1` serialization must contain:

1. **provenance:** source version, PDF/TeX/figure hashes, conventions and the
   exact transformation from source coordinates to limiting triangle indices;
2. **templates:** three macro records with exact connected constituent lists
   of sizes `30,30,2`, each constituent carrying a stable address, limiting
   triangle coordinates and orientation;
3. **state fields:** source role, macro/address, split-`M` half, directed
   internal ports, exposed source boundary/SAB data, line family, physical
   order in `{-1,0,1}`, narrow/wide gap slots and O0/I0 vertex participation;
4. **edge relation:** every allowed oriented pair
   `(state,side; state',side')`, including the reflected branch;
5. **vertex relation:** every allowed cyclic participant word, with distinct
   physical sectors retained and auxiliary O0 decorations identified;
6. **decoder data:** macro grouping, line-index increments, repeated-gap
   equalities and the finite-radius output fields required by D0;
7. **K1P table:** one fixed witness/type `tau`, the fixed 32-state core, its
   even-parity bijection, every fresh diagonal tag, and the K1C/K1T contact
   relations derived from the source table.

## 3. Cold-verifier obligations

An independent verifier must check, without regenerating the producer's
choices:

- exact counts `30,30,2`, address uniqueness and template connectivity;
- every internal port has one reciprocal mate and no boundary port is
  mistaken for an internal edge;
- edge involution and cyclic/reflection closure of vertex words;
- the physical order restriction and I0's three-coset incidence equations;
- macro completion and consistency of repeated gap descriptions;
- injectivity and complete coverage of the K1P code table;
- exact equality of its selected codeword set with K2C's parity-plus-diagonal
  relation;
- deterministic centered source decoding and re-encoding on the serialized
  rule domain.

These checks would upgrade a finite table to machine-verified consistency.
They would not by themselves prove that the table equals the full source
tiling hull; that remains the mathematical O0/I0/D0 language theorem.

## 4. Primary-source sufficiency audit

The cached paper is arXiv `2506.19362`, v3. Its source archive was fetched to
temporary storage on 2026-07-21 and has SHA-256

```
de757bfc8e3fe174fc04dd19101f30e13dc6776d245f573ff9554f23a60bad28
```

Relevant members are:

```
SturmianLattice.tex  d319588741643928763e94eaca31f208aa372f8760e130d99af174ebd74f05a6
sqrt2_patches.pdf    0662e35f30b3e771c85b665c5a897160bbf709f073f0ee2c37383cde91a7f3b9
Isometric.pdf        2b57b626fe2f2916cee4aec9f71bc42df79f2d3ea944d87c6fcee2622e9ee136
```

The TeX supplies the exact line/centroid definitions, cell types, density
relations, macro compositions and prose matching rules. Figures 37--45 are
included from standalone PDFs. `sqrt2_patches.pdf` and `Isometric.pdf` report
Adobe Illustrator as creator; the archive contains no generating coordinate
file, constituent-address list, SAB table or vertex-word table.

Consequently the archive is sufficient to audit formulas and visually
identify the three supports, but not to populate SER0 by deterministic
transcription. Parsing Illustrator paths or clicking triangle centers would
be an **independent reconstruction** with semantic choices about addresses,
SAB continuation and auxiliary participant identities.

## 5. Decision

Direct serialization is blocked. No producer or research run is admitted in
HC-10 because its purported input table does not exist in the primary source.

Reopening has two honest routes:

1. obtain author-supplied coordinate/rule data with provenance; or
2. preregister an independent reconstruction, give two independent
   derivations or an external author comparison, and label the output a
   reconstruction rather than source serialization.

The self-contained symbolic write-up may proceed using an abstract finite S0
presentation, but it must mark SER0 as the extensional reproducibility gap.
