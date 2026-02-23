# Media Company Lakehouse Platform

Config-driven data engineering framework for a media organization, with Airflow orchestration and Spark ETL execution in one repository.

## Goals

- Keep orchestration (`dags/`), compute (`spark_jobs/`), and configurations (`configs/`) clearly separated.
- Provide reusable abstractions so >30 engineers and multiple teams can ship consistently.
- Optimize for long-term maintainability with modular packages, conventions, and documentation.

## Repository Structure

```text
.
├── configs/                      # All runtime configurations (env, DAG, Spark jobs)
│   ├── dags/
│   ├── environments/
│   └── spark_jobs/
├── dags/                         # Airflow DAG definitions (team-scoped)
│   ├── common/
│   └── teams/
├── docs/                         # Architecture + engineering standards
├── requirements/                 # Dependency groups by runtime concern
├── spark_jobs/                   # Spark ETL jobs + entrypoints
│   ├── entrypoints/
│   └── jobs/
├── src/lakehouse_framework/      # Shared framework abstractions
│   ├── airflow/
│   ├── config/
│   ├── spark/
│   └── utils/
└── tests/
```

## Quick Start

1. Create virtual environment and install dependencies.
2. Export `PYTHONPATH=src` for local runs.
3. Build new pipeline by adding:
	 - one DAG config in `configs/dags/`
	 - one Spark job config in `configs/spark_jobs/`
	 - one DAG Python file in `dags/teams/<team>/`
	 - one Spark job class in `spark_jobs/jobs/`

Example command for local Spark execution:

```bash
python spark_jobs/entrypoints/run_job.py \
	--job-config configs/spark_jobs/content_metrics_job.yaml \
	--env dev
```

## Engineering Principles

- **Config over code**: pipeline behavior should be controlled by YAML where feasible.
- **Separation of concerns**: framework abstractions in `src/`, team logic in `dags/` and `spark_jobs/`.
- **Domain ownership**: teams own their folders and configs; platform team owns framework.
- **Standardized execution**: use base classes and factories, avoid ad-hoc DAG/job patterns.

## CI/CD Quality Gates

- CI workflow: `.github/workflows/ci.yml`
	- Lint with `ruff`
	- Unit tests with `pytest`
	- Airflow DAG parse check via `scripts/check_dags.py`
- CD scaffold: `.github/workflows/cd.yml`
	- Manual trigger with environment selection
	- Re-validates tests and DAG parse
	- Packages deployable artifacts (`dags`, `spark_jobs`, `configs`, `src`)

Run quality checks locally:

```bash
export PYTHONPATH=src:$PWD
ruff check src dags spark_jobs tests scripts
pytest -q
python scripts/check_dags.py
```

See `docs/architecture.md`, `docs/standards.md`, and `docs/onboarding.md` for detailed guidance.
