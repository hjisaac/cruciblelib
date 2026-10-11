# Crucible

From paper or idea to runnable experiment with minimal friction.

`crucible` is a lightweight Python framework for orchestrating reproducible experiments, evaluations, and multi-axis parameter sweeps.

---

## Features

- **Lean Lifecycle**: Structured lifecycle hooks (`on_start` $\to$ `on_prepare` $\to$ `on_execute` $\to$ `on_finalize` $\to$ `on_teardown`).
- **Config-Driven Sweeps**: Scalar config values run once; lists trigger Cartesian product sweeps parallelized across workers (`n_jobs`).
- **Hydra Overrides**: Command-line parameter overrides using Hydra syntax (`-o key=value`).
- **Convention-Over-Configuration**: Automatically discovers jobs in `./jobs` (or custom locations configured in `pyproject.toml` or `crucible.yaml`).
- **Optional Tracker Integration**: Clean hooks for Weights & Biases or custom metric backends.

---

## Installation

```bash
pip install crucible
```

Or with Weights & Biases tracking:

```bash
pip install "crucible[wandb]"
```

---

## Quickstart

### 1. Scaffold a Job

Create a new job package under `jobs/`:

```bash
crucible create my_experiment
```

This creates:
```text
jobs/my_experiment/
├── __init__.py
├── job.py
└── configs/
    └── default.yaml
```

### 2. Implement Your Job

Edit `jobs/my_experiment/job.py`:

```python
import logging
from crucible.core.jobs import AbstractJob

logger = logging.getLogger(__name__)

class Job(AbstractJob):
    def on_prepare(self) -> dict:
        # Load dataset or prepare resources
        return {"data": [1, 2, 3]}

    def on_execute(self, prepared: dict) -> dict:
        # Run calculation, model inference, or benchmark
        factor = self.config.get("multiplier", 1)
        score = sum(x * factor for x in prepared["data"])
        return {"total_score": score}

JOB_CLASS = Job
```

### 3. Run the Job

```bash
# Run with default config
crucible execute my_experiment

# Override parameters on the command line
crucible execute my_experiment -o multiplier=10
```

---

## Parameter Sweeping

In `jobs/my_experiment/configs/sweep.yaml`:

```yaml
log_dir: logs
multiplier: [1, 5, 10]
learning_rate: [0.01, 0.001]
```

Executing with a sweep config executes each Cartesian product combination automatically:

```bash
crucible execute my_experiment -c sweep --n-jobs 4 --out outputs/sweep_results.json
```

---

## Configuration Discovery

By default, `crucible` searches for jobs in the `./jobs` folder relative to your project root.

To customize job directories, add to your project's `pyproject.toml`:

```toml
[tool.crucible]
jobs_dirs = ["eval", "analysis"]
```

Or configure via environment variable:
```bash
export CRUCIBLE_JOBS_ROOT=./eval
```

---

## License

MIT
