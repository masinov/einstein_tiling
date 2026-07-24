from fractions import Fraction
from hashlib import sha256
import json
import importlib.util
from pathlib import Path
import sys

import z3

from einstein.theory.cvc5_models import exact_real_payload
from einstein.theory.k16w_exact import HC34_CELLS, build_problem
from einstein.theory.k16w_tangent import build_tangent_problem


ROOT = Path(__file__).resolve().parent.parent


def test_hc38_tangent_cells_are_polynomial_seven_variable_presentations():
    for cell in HC34_CELLS:
        problem = build_tangent_problem(cell)
        assert set(problem.variables) == {
            "a", "b", "c", "v", "t1", "t2", "sqrt_half",
        }
        assert "t0" not in problem.variables
        assert len(problem.nonadjacent_pairs) == 120
        assert problem.constraint_counts == {
            "base": 11,
            "tangent_substitution": 5,
            "containment_scalar": 32,
            "closure": 1,
            "nonadjacent_segment_pairs": 120,
            "decomposition": 21,
            "total_top_level": 190,
        }
        assert len(problem.solver.assertions()) == 190


def test_hc38_qsqrt2_model_recognizer_is_exact():
    import cvc5

    solver = cvc5.Solver()
    solver.setLogic("QF_NRA")
    solver.setOption("produce-models", "true")
    value = solver.mkConst(solver.getRealSort(), "value")
    solver.assertFormula(solver.mkTerm(
        cvc5.Kind.EQUAL,
        solver.mkTerm(cvc5.Kind.MULT, value, value),
        solver.mkReal(2),
    ))
    solver.assertFormula(solver.mkTerm(cvc5.Kind.GT, value, solver.mkReal(0)))
    assert str(solver.checkSat()) == "sat"
    payload = exact_real_payload(solver, solver.getValue(value))
    assert payload["kind"] == "q_sqrt2"
    assert payload["rational_numerator"] == 0
    assert payload["sqrt2_numerator"] == 1
    assert payload["sqrt2_denominator"] == 1


def test_complete_k16w_formula_has_every_segment_pair():
    problem = build_problem(timeout_ms=1000)
    assert len(problem.first_half) == 9
    assert len(problem.points) == 18
    assert len(problem.nonadjacent_pairs) == 120
    assert problem.constraint_counts == {
        "base": 13,
        "containment_scalar": 32,
        "closure": 1,
        "nonadjacent_segment_pairs": 120,
        "decomposition": 0,
        "total_top_level": 166,
    }


def test_hc31_cells_are_the_exact_two_fixed_decomposition_instances():
    for cell in ("plus-minus", "minus-plus"):
        problem = build_problem(timeout_ms=1000, cell=cell)
        assert problem.constraint_counts["decomposition"] == 8
        assert problem.constraint_counts["total_top_level"] == 174
        assert len(problem.nonadjacent_pairs) == 120


def test_unknown_hc31_cell_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        build_problem(cell="same-polarity")


def test_err010_replacement_is_an_exact_unit_direction():
    x = Fraction(544, 545)
    y = Fraction(33, 545)
    assert x * x + y * y == 1
    assert 2 * x < 2
    assert x < 1


def test_n42_exact_reset_budget_comparisons():
    # sqrt(23/2) > 10/3.
    assert Fraction(23, 2) > Fraction(100, 9)
    # sqrt(42) < 13/2 makes
    # [13(sqrt(21)-sqrt(2))]^2 > 1690 > (6sqrt(46))^2,
    # hence U_0 < 13/6.
    assert Fraction(42) < Fraction(169, 4)
    assert 3887 - 338 * Fraction(13, 2) == 1690
    assert 1690 > 36 * 46
    # sqrt(46)+sqrt(42)>12 makes delta_0<1/6.
    assert 46 > 36 and 42 > 36


def test_err013_central_pairing_preserves_traversed_edge_vectors():
    problem = build_problem(timeout_ms=1000, cell="plus-minus")
    points = problem.points
    # C' (segment 11) has the same traversed vector as C (segment 5),
    # and B' (segment 14) the same as B (segment 2).
    for first, paired in ((5, 11), (2, 14)):
        for axis in (0, 1):
            original = points[first + 1][axis] - points[first][axis]
            mate = points[paired + 1][axis] - points[paired][axis]
            assert z3.is_true(z3.simplify(mate == original))


def test_hc34_exact_six_cells_keep_every_segment_pair():
    assert HC34_CELLS == (
        "s1-minus-minus", "s1-minus-plus",
        "s2-minus-minus", "s2-minus-plus",
        "s3-minus-minus", "s3-minus-plus",
    )
    for cell in HC34_CELLS:
        problem = build_problem(timeout_ms=1000, hc34_cell=cell)
        assert len(problem.nonadjacent_pairs) == 120
        assert problem.hc34_cell == cell
        assert problem.constraint_counts == {
            "base": 13,
            "containment_scalar": 32,
            "closure": 1,
            "nonadjacent_segment_pairs": 120,
            "decomposition": 21,
            "total_top_level": 187,
        }


def test_hc34_unknown_or_mixed_cell_is_rejected():
    import pytest

    with pytest.raises(ValueError):
        build_problem(hc34_cell="s4-minus-minus")
    with pytest.raises(ValueError):
        build_problem(cell="plus-minus", hc34_cell=HC34_CELLS[0])


def test_hc34_formula_manifest_pins_all_six_complete_cells():
    path = ROOT / "docs/notebook/assets/k16w-hc34-formulas.json"
    payload = json.loads(path.read_text())
    assert payload["code_version"] == "a984181"
    assert payload["complete"] is True
    assert payload["cell_order"] == list(HC34_CELLS)
    assert len(payload["records"]) == 6
    for record, cell in zip(payload["records"], HC34_CELLS):
        formula = ROOT / record["path"]
        data = formula.read_bytes()
        assert record["cell"] == cell
        assert record["sha256"] == sha256(data).hexdigest()
        assert record["bytes"] == len(data)
        assert record["nonadjacent_pairs"] == 120
        assert record["constraint_counts"]["total_top_level"] == 187
        assert sum(line.startswith(b"(assert") for line in data.splitlines()) == 187


def test_hc34_runner_loads_the_frozen_bytes_instead_of_reserializing():
    path = ROOT / "scripts/run_k16w_hc34_cell.py"
    spec = importlib.util.spec_from_file_location("run_k16w_hc34_cell", path)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)

    for cell in HC34_CELLS:
        solver, record = module.load_frozen_solver(cell)
        assert record["cell"] == cell
        assert len(solver.assertions()) == 187


def test_hc35_launcher_isolates_cell_sessions(monkeypatch, tmp_path):
    path = ROOT / "scripts/run_k16w_hc35.py"
    spec = importlib.util.spec_from_file_location("run_k16w_hc35", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    captured = {}

    class Process:
        pid = 12345

    def fake_popen(command, **kwargs):
        captured["command"] = command
        captured.update(kwargs)
        return Process()

    monkeypatch.setattr(module.subprocess, "Popen", fake_popen)
    with (tmp_path / "cell.log").open("wb") as log:
        process = module.launch_cell(HC34_CELLS[0], log)
    assert process.pid == 12345
    assert captured["start_new_session"] is True
    assert captured["command"][0] == "/usr/bin/timeout"
    assert captured["command"][-1] == HC34_CELLS[0]


def test_hc34_result_manifest_is_fail_closed_and_hash_pinned():
    assets = ROOT / "docs/notebook/assets"
    formulas = json.loads((assets / "k16w-hc34-formulas.json").read_text())
    results = json.loads((assets / "k16w-hc34-results.json").read_text())
    formula_records = {record["cell"]: record for record in formulas["records"]}
    expected = {
        "s1-minus-minus": "resource_stop",
        "s1-minus-plus": "no_result",
        "s2-minus-minus": "no_result",
        "s2-minus-plus": "resource_stop",
        "s3-minus-minus": "resource_stop",
        "s3-minus-plus": "resource_stop",
    }
    assert results["complete"] is True
    assert results["cell_order"] == list(HC34_CELLS)
    assert {record["cell"]: record["status"] for record in results["records"]} == expected
    for record in results["records"]:
        cell = record["cell"]
        payload = json.loads((ROOT / record["result"]).read_text())
        formula = ROOT / formula_records[cell]["path"]
        assert payload["cell"] == cell
        assert payload["status"] == expected[cell]
        assert payload["model"] is None
        assert payload["formula"]["sha256"] == sha256(formula.read_bytes()).hexdigest()
        assert payload["external_returncode"] == (124 if expected[cell] == "resource_stop" else 1)
