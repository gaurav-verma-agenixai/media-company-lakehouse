# Spark Jobs Module

Contains all Spark ETL implementations and runtime entrypoints.

## Conventions

- Job classes live in `spark_jobs/jobs/`.
- Entrypoints live in `spark_jobs/entrypoints/`.
- Jobs inherit from `BaseSparkJob` and remain config-driven.

## Team usage model

Each team contributes job classes while the platform team maintains shared
contracts in `src/lakehouse_framework/spark/`.
