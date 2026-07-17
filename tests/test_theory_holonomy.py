"""W2.D exact primary-source Cayley-diagram controls."""

from einstein.theory.holonomy import (
    A,
    IDENTITY,
    U,
    affine_compose,
    line_tile_boundary_words,
    polykite_boundary_relators,
    p3_value,
    s3_displacement_kernel,
    s3_boundary_surjections,
    s3_cosets_all_admit_commuting_pairs,
    staircase_boundary_word,
    u_triangle_winding,
    verify_s3_boundary_quotient,
)


def _power(value, exponent):
    out = IDENTITY
    for _ in range(exponent):
        out = affine_compose(out, value)
    return out


def test_p3_affine_presentation_relations():
    assert _power(A, 3) == IDENTITY
    assert _power(U, 3) == IDENTITY
    u_inverse_a = p3_value("uA")
    assert _power(u_inverse_a, 3) == IDENTITY


def test_conway_lagarias_line_tile_invariant_control():
    for boundary in line_tile_boundary_words():
        assert p3_value(boundary) == IDENTITY
        assert u_triangle_winding(boundary) == 0


def test_conway_lagarias_staircase_formula():
    for index in range(0, 25):
        boundary = staircase_boundary_word(index)
        if index % 3 in (0, 2):
            assert p3_value(boundary) == IDENTITY
            assert u_triangle_winding(boundary) == (index + 1) // 3


def test_polykite_free_boundary_relators_are_reduced_and_closed():
    single = ((0, 0, 0),)
    relators = polykite_boundary_relators(single)
    assert relators
    assert all(len(word) == 4 for word in relators)
    assert all(
        all(left != -right for left, right in zip(word, word[1:]))
        for word in relators
    )


def test_s3_displacement_kernel_extremes():
    identity = (0, 1, 2)
    transposition = (1, 0, 2)
    three_cycle = (1, 2, 0)
    assert len(s3_displacement_kernel([identity] * 6)) == 1
    images = [identity, identity, transposition, three_cycle, identity, identity]
    assert len(s3_displacement_kernel(images)) == 6
    assert s3_cosets_all_admit_commuting_pairs(frozenset({identity})) is False
    assert s3_cosets_all_admit_commuting_pairs(
        frozenset({identity, three_cycle, (2, 0, 1)})
    )


def test_finalist_s3_surjections_reduce_to_conjugacy_classes():
    from einstein.e1_candidates import decode_compiled_key

    shape = decode_compiled_key("010001010104010502f002f1030b030c04fa04fb")
    kernel3 = s3_boundary_surjections(shape, displacement_kernel_order=3)
    kernel6 = s3_boundary_surjections(shape, displacement_kernel_order=6)
    assert len(kernel3) == 39
    assert len(kernel6) == 387
    assert all(
        verify_s3_boundary_quotient(shape, images, require_surjective=True)
        for images in kernel3 + kernel6
    )
