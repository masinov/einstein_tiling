import importlib.util
from pathlib import Path
import pytest


ROOT = Path(__file__).resolve().parents[2]


def load_runner():
    path = ROOT / "scripts/run_research.py"
    spec = importlib.util.spec_from_file_location("run_research", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_final_checks_catch_processes_that_exit_between_polls() -> None:
    runner = load_runner()
    classify = runner.classify_completed_process
    common = {
        "prior_status": "completed",
        "wall_seconds": 10,
        "max_growth": 100,
        "return_code": 0,
    }
    assert classify(elapsed=10.01, final_growth=0, **common) == "resource_stop_wall"
    assert classify(elapsed=9.0, final_growth=101, **common) == "resource_stop_artifact"
    assert classify(elapsed=9.0, final_growth=100, **common) == "completed"
    assert classify(
        elapsed=9.0,
        final_growth=0,
        prior_status="completed",
        wall_seconds=10,
        max_growth=100,
        return_code=7,
    ) == "process_error"
    assert classify(
        elapsed=20.0,
        final_growth=1000,
        prior_status="interrupted",
        wall_seconds=10,
        max_growth=100,
        return_code=-15,
    ) == "interrupted"


def test_runner_contract_records_null_verdict_and_preexec_memory_limit() -> None:
    source = (ROOT / "scripts/run_research.py").read_text()
    assert "resource.setrlimit" in source
    assert "preexec_fn=" in source
    assert '"research_verdict": None' in source
    assert '"proposal_sha256"' in source
    assert '"admission_sha256"' in source
    assert '"stdout_sha256"' in source
    assert '"stderr_sha256"' in source


def test_execution_manifest_writer_refuses_overwrite(tmp_path: Path) -> None:
    runner = load_runner()
    path = tmp_path / "manifest.json"
    runner.write_manifest(path, {"first": True})
    with pytest.raises(FileExistsError):
        runner.write_manifest(path, {"second": True})
    assert '"first": true' in path.read_text()
