# Engineering Standards

## Code Organization

- Keep DAG orchestration code in `dags/` only.
- Keep Spark transformation code in `spark_jobs/` only.
- Keep framework abstractions in `src/lakehouse_framework/` only.
- Keep runtime values and environment differences in `configs/`.

## Contribution Rules

- Every new pipeline requires both DAG and Spark job configs.
- DAG files should remain thin wrappers; avoid business logic in DAGs.
- Spark jobs must inherit `BaseSparkJob`.
- Prefer config additions over hardcoded values in Python modules.

## Reliability

- Keep retries/timeouts explicit in DAG config.
- Add data quality and schema validation as dedicated Spark job stages.
- Ensure writes are idempotent where possible.

## Observability

- Use framework logger for consistent logs.
- Tag DAGs with domain/team and data product metadata.
- Keep job names stable for metric continuity.

## Ownership

- Team folders map to ownership and support boundaries.
- Framework changes require review from platform maintainers.

## CI/CD Requirements

- Pull requests must pass lint, unit tests, and DAG parse checks.
- Do not merge DAG changes that fail `scripts/check_dags.py`.
- Keep workflow logic in `.github/workflows/` and review changes with platform team.
