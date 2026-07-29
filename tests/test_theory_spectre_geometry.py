"""Exact W3 Spectre geometry recurrence and vendor-table agreement."""

from pathlib import Path

from einstein.tilings.spectre.geometry import (
    ANNIHILATING_POLYNOMIAL,
    binary_boundary_prefix,
    boundary_word_recurrence_evidence,
    boundary_simplicity_prefix,
    compare_vendored_translations,
    integer_determinant,
    level_geometry,
    matrix_polynomial,
    macro_word_recurrence_evidence,
    realized_patch_evidence,
    recurrence_matrix,
    verify_stationary_recurrence,
    verify_binary_geometry_quotient,
    verify_all_level_macro_side_chains,
)


ROOT = Path(__file__).resolve().parents[1]


def test_first_level_is_the_materialized_exact_transform():
    children = level_geometry(1)[0]["children"]
    assert [(pose[0], pose[1]) for pose in children] == [
        (1, 0), (1, 10), (1, 10), (1, 8),
        (1, 6), (1, 6), (1, 4), (1, 8),
    ]
    assert [pose[2] for pose in children] == [
        (0, 0, 0, 0),
        (2, 0, -1, 0),
        (1, 2, 1, -1),
        (2, 2, -1, -1),
        (1, 2, -2, -1),
        (3, 1, -3, -2),
        (1, 1, -2, -2),
        (0, -2, -3, 1),
    ]


def test_recurrence_is_unimodular_and_exactly_annihilated():
    matrix = recurrence_matrix()
    assert integer_determinant(matrix) == 1
    assert not any(
        any(row) for row in matrix_polynomial(matrix, ANNIHILATING_POLYNOMIAL)
    )
    result = verify_stationary_recurrence(8)
    assert result["dimension"] == 16
    assert result["expanding_two_level_factor"] == "4+sqrt(15)"


def test_all_32_materialized_vendor_levels_equal_the_recurrence():
    source = (
        ROOT / "vendor/spectre/spectre-core/src/tables.rs"
    ).read_text()
    result = compare_vendored_translations(source)
    assert result == {
        "levels": 32,
        "children_per_level": 8,
        "vectors_compared": 256,
        "all_equal": True,
    }


def test_all_base_and_first_level_label_patches_are_exactly_legal():
    result = realized_patch_evidence(1)
    assert result["patches_checked"] == 18
    assert result["all_legal"]
    level_one = [row for row in result["checks"] if row["level"] == 1]
    assert {row["tiles"] for row in level_one} == {8, 9}
    assert all(row["interiors_disjoint"] for row in level_one)
    assert all(row["edge_connected"] for row in level_one)
    assert not result["inductive_all_levels"]


def test_nine_labels_have_two_geometric_support_types_at_every_level():
    result = verify_binary_geometry_quotient()
    assert result["geometric_support_types"] == 2
    assert result["type_for_label"]["Gamma"] == "missing"
    assert set(result["type_for_label"].values()) == {"full", "missing"}
    assert result["valid_at_all_levels_by_induction"]


def test_binary_supports_are_abstract_disks_through_level_three():
    result = binary_boundary_prefix(3)
    assert result["all_abstract_disks"]
    assert not result["proves_planar_nonintersection"]
    lengths = {
        (row["level"], row["kind"]): row["boundary_cycles"][0]["length"]
        for row in result["reports"]
    }
    assert lengths[(3, "full")] == 758
    assert lengths[(3, "missing")] == 652


def test_candidate_side_word_recurrence_survives_five_exact_levels():
    result = boundary_word_recurrence_evidence(5)
    assert result["all_equal"]
    assert [row["length"] for row in result["checks"]] == [
        2, 8, 34, 144, 610, 2584,
    ]
    assert result["dominant_root"] == "2+sqrt(5)"
    assert not result["inductive_derivation_from_child_gluing"]


def test_macro_side_endpoint_grammar_holds_at_every_level():
    result = verify_all_level_macro_side_chains()
    assert result["quad_levels_checked"] == list(range(8))
    assert result["all_level_endpoint_identity"]
    assert result["missing_slot_two_complement_is_virtual"]
    assert not result["proves_boundary_simplicity_or_nonintersection"]


def test_graph_directed_macro_words_match_leaf_boundaries():
    result = macro_word_recurrence_evidence(3)
    assert result["all_equal"]
    assert result["derived_from_macro_chain_grammar"]
    assert len(result["checks"]) == 30
    assert not result["all_level_simplicity_or_nonintersection"]


def test_exact_boundary_simplicity_prefix_includes_transverse_crossings():
    result = boundary_simplicity_prefix(3)
    assert result["all_simple"]
    assert len(result["reports"]) == 6
    assert all(not row["nonadjacent_segment_intersections"]
               for row in result["reports"])
    assert not result["all_level_induction"]
