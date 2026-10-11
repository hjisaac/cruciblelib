from pathlib import Path
from crucible.core.constants import _find_project_root, _load_configured_jobs_roots
from crucible.interface.cli.utils import create_job_package


def test_find_project_root_pyproject(tmp_path: Path, monkeypatch) -> None:
    proj_dir = tmp_path / "my_project"
    sub_dir = proj_dir / "src" / "deep"
    sub_dir.mkdir(parents=True)
    (proj_dir / "pyproject.toml").write_text("[project]\nname='test'\n", encoding="utf-8")

    monkeypatch.chdir(sub_dir)
    assert _find_project_root() == proj_dir


def test_load_configured_jobs_roots_from_pyproject(tmp_path: Path) -> None:
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        """[tool.crucible]
jobs_dirs = ["custom_eval", "custom_analysis"]
""",
        encoding="utf-8",
    )
    roots = _load_configured_jobs_roots(tmp_path)
    assert roots == [tmp_path / "custom_eval", tmp_path / "custom_analysis"]


def test_create_job_scaffold(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("CRUCIBLE_JOBS_ROOT", str(tmp_path / "jobs"))
    created = create_job_package("sample_benchmark")
    assert created.exists()
    assert (created / "job.py").exists()
    assert (created / "configs" / "default.yaml").exists()
    assert (created / "__init__.py").exists()
