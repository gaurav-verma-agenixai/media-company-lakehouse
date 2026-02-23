# Onboarding Guide

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
pip install -r requirements/airflow.txt
pip install -r requirements/spark.txt
export PYTHONPATH=src
```

## Add a New Pipeline

1. Create Spark job class in `spark_jobs/jobs/` extending `BaseSparkJob`.
2. Create Spark config in `configs/spark_jobs/`.
3. Create DAG config in `configs/dags/`.
4. Create DAG file in `dags/teams/<team>/` using `build_config_driven_dag`.
5. Add tests for config contracts or transformation logic.

## Run a Job Locally

```bash
python spark_jobs/entrypoints/run_job.py --job-config configs/spark_jobs/content_metrics_job.yaml --env dev
```

## Run Local Quality Gates

```bash
export PYTHONPATH=src:$PWD
ruff check src dags spark_jobs tests scripts
pytest -q
python scripts/check_dags.py
```

## Expected Team Practices

- Keep module-level docstrings for every new Python module.
- Keep job-level docstrings on each Spark job class.
- Keep comments for non-obvious transformation intent.
