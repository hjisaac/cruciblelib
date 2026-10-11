import os
import re
from pathlib import Path


def _find_project_root() -> Path:
    if "CRUCIBLE_WORKSPACE_ROOT" in os.environ:
        return Path(os.environ["CRUCIBLE_WORKSPACE_ROOT"]).resolve()
    current = Path.cwd().resolve()
    for directory in (current, *current.parents):
        if (directory / "pyproject.toml").exists() or (directory / "crucible.yaml").exists() or (directory / ".git").exists():
            return directory
    return current


def _load_configured_jobs_roots(workspace: Path) -> list[Path]:
    if "CRUCIBLE_JOBS_ROOT" in os.environ:
        return [Path(os.environ["CRUCIBLE_JOBS_ROOT"]).resolve()]

    # Read from pyproject.toml [tool.crucible] if present
    pyproject_path = workspace / "pyproject.toml"
    if pyproject_path.exists():
        try:
            import tomllib
            with pyproject_path.open("rb") as f:
                data = tomllib.load(f)
            tool_crucible = data.get("tool", {}).get("crucible", {})
            roots = tool_crucible.get("jobs_dirs") or tool_crucible.get("jobs_dir")
            if isinstance(roots, str):
                return [(workspace / roots).resolve()]
            if isinstance(roots, list):
                return [(workspace / r).resolve() for r in roots]
        except Exception:
            pass

    # Read from crucible.yaml if present
    crucible_yaml = workspace / "crucible.yaml"
    if crucible_yaml.exists():
        try:
            from omegaconf import OmegaConf
            cfg = OmegaConf.load(str(crucible_yaml))
            roots = cfg.get("jobs_dirs") or cfg.get("jobs_dir")
            if isinstance(roots, str):
                return [(workspace / roots).resolve()]
            if isinstance(roots, list):
                return [(workspace / r).resolve() for r in roots]
        except Exception:
            pass

    # Default to ./jobs under the workspace root
    return [(workspace / "jobs").resolve()]


def get_workspace_root() -> Path:
    return _find_project_root()


def get_jobs_roots() -> list[Path]:
    return _load_configured_jobs_roots(get_workspace_root())


def get_primary_jobs_root() -> Path:
    roots = get_jobs_roots()
    return roots[0] if roots else (get_workspace_root() / "jobs").resolve()


# Expose module-level properties for backward compatibility
WORKSPACE_ROOT = get_workspace_root()
JOBS_ROOTS = get_jobs_roots()
JOBS_ROOT = get_primary_jobs_root()

SUPPORTED_CONFIG_EXTENSIONS = (".yaml", ".yml")
ROOT_CONFIG_FILENAME = "root.config.yaml"

# Characters a run_id must not contain: it becomes a log and result filename
UNSAFE_IN_FILENAME = re.compile(r"[^A-Za-z0-9_.,=-]")
