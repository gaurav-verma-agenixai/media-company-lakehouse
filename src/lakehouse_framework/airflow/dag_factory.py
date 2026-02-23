"""Factory for creating config-driven Airflow DAGs with standard lifecycle tasks."""

from __future__ import annotations

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

from lakehouse_framework.airflow.spark_submit import build_spark_submit_command
from lakehouse_framework.config.models import DagConfig


def _validate_dag_config(dag_config: DagConfig) -> None:
    """Basic config validation task executed in DAG runtime context."""
    if dag_config.spark_submit is None:
        raise ValueError(f"DAG '{dag_config.dag_id}' is missing 'spark_submit' configuration")


def build_standard_dag(dag_config: DagConfig, environment: str = "dev") -> DAG:
    """Create a standard ETL DAG scaffold from typed configuration."""
    default_args = {
        "owner": dag_config.owner,
        "retries": dag_config.retries,
        "retry_delay": dag_config.retry_delay,
    }

    dag = DAG(
        dag_id=dag_config.dag_id,
        description=dag_config.description,
        start_date=dag_config.start_date,
        schedule=dag_config.schedule,
        catchup=dag_config.catchup,
        max_active_runs=dag_config.max_active_runs,
        default_args=default_args,
        tags=dag_config.tags,
    )

    with dag:
        start = EmptyOperator(task_id="start")

        validate_config = PythonOperator(
            task_id="validate_config",
            python_callable=_validate_dag_config,
            op_kwargs={"dag_config": dag_config},
        )

        spark_submit = BashOperator(
            task_id="run_spark_job",
            bash_command=build_spark_submit_command(
                spark_submit=dag_config.spark_submit,
                environment=environment,
            ),
        )

        end = EmptyOperator(task_id="end")

        start >> validate_config >> spark_submit >> end

    return dag
