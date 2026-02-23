"""Typed configuration objects.

Centralized models reduce config drift and prevent each team from inventing
different runtime contracts.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any


@dataclass(slots=True)
class SparkSubmitConfig:
    """Spark submit settings consumed by orchestration layer."""

    application: str
    job_config: str
    master: str = "local[*]"
    deploy_mode: str = "client"
    conf: dict[str, str] = field(default_factory=dict)
    jars: list[str] = field(default_factory=list)


@dataclass(slots=True)
class DagConfig:
    """Airflow DAG-level configuration."""

    dag_id: str
    description: str
    schedule: str
    start_date: datetime
    catchup: bool
    max_active_runs: int
    tags: list[str]
    owner: str
    retries: int = 1
    retry_delay_minutes: int = 5
    spark_submit: SparkSubmitConfig | None = None

    @property
    def retry_delay(self) -> timedelta:
        """Retry delay converted to timedelta for Airflow default args."""
        return timedelta(minutes=self.retry_delay_minutes)


@dataclass(slots=True)
class SparkJobConfig:
    """Spark job runtime config used by job runner and job classes."""

    job_name: str
    job_class: str
    source: dict[str, Any]
    target: dict[str, Any]
    transformations: dict[str, Any] = field(default_factory=dict)
    spark_conf: dict[str, str] = field(default_factory=dict)
