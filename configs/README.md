# Configuration Module

Centralized runtime configurations for all DAGs and Spark jobs.

## Layout

- `configs/environments/`: environment overlays (dev/prod/shared).
- `configs/dags/`: one file per DAG.
- `configs/spark_jobs/`: one file per Spark job.

## Governance

- All config changes require code review from owning team + platform team.
- Keep business logic out of code where a config value is sufficient.
- Prefer additive config changes over breaking schema changes.
