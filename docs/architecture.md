# Lakehouse ETL Architecture

## Purpose

This repository is a shared execution platform for media data pipelines, where:

- Airflow handles orchestration and scheduling.
- Spark handles scalable ETL processing.
- YAML configs control runtime behavior.

## High-Level Design

1. DAG files (`dags/teams/*`) declare pipeline identity and reference config.
2. `ConfigRegistry` applies environment overlays and returns typed config models.
3. `dag_factory` creates a standardized DAG task pattern.
4. Airflow launches Spark via generated `spark-submit` command.
5. Spark entrypoint resolves configured job class and executes contract methods.

## Abstractions

- `ConfigRegistry`: centralized config loading and environment overlay.
- `DagConfig` / `SparkJobConfig`: typed contracts for stable interfaces.
- `BaseSparkJob`: mandatory ETL lifecycle interface (`extract/transform/load`).
- `run_spark_job`: execution harness to reduce per-job boilerplate.

## Extensibility Model

- Teams extend by adding job classes and configs.
- Platform extends by evolving framework internals without breaking team code.
- New runtimes (dbt, Flink, streaming) can be added as sibling framework modules.
