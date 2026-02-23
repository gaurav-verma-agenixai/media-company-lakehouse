# DAGs Module

Contains Airflow DAG definitions grouped by team ownership.

## Conventions

- Team DAGs live under `dags/teams/<team_name>/`.
- Reusable DAG bootstrapping helpers live under `dags/common/`.
- DAG files should be thin wrappers that reference config files.

## Why this structure?

It keeps orchestration code clean and standardized while allowing teams to own
their scheduling and dependencies without forking framework patterns.
