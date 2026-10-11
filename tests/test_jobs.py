import pytest
from crucible.core.jobs import AbstractJob
from crucible.core.runtime.sweeping import run_job
from crucible.core.types import RunState


class DummyJob(AbstractJob):
    def on_prepare(self) -> dict:
        return {"data": [1, 2, 3]}

    def on_execute(self, prepared: dict) -> dict:
        multiplier = self.config.get("multiplier", 1)
        total = sum(x * multiplier for x in prepared["data"])
        return {"total": total}


def test_single_job_run(tmp_path) -> None:
    config = {
        "log_dir": str(tmp_path / "logs"),
        "multiplier": 2,
    }
    runs = run_job(DummyJob, config)
    assert len(runs) == 1
    assert runs[0]["state"] == RunState.COMPLETE
    assert runs[0]["result"] == {"total": 12}


def test_cartesian_sweep(tmp_path) -> None:
    config = {
        "log_dir": str(tmp_path / "logs"),
        "multiplier": [1, 2, 3],
        "dummy_param": ["a", "b"],
    }
    runs = run_job(DummyJob, config, n_jobs=1)
    assert len(runs) == 6
    totals = {r["result"]["total"] for r in runs if r["state"] == RunState.COMPLETE}
    assert totals == {6, 12, 18}
