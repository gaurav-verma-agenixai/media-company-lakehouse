"""DAG helper module.

This module abstracts repetitive DAG bootstrap logic so team DAG files can stay
small and readable.
"""

from __future__ import annotations

from pathlib import Path

from lakehouse_framework.airflow.dag_factory import build_standard_dag
from lakehouse_framework.config.registry import ConfigRegistry


def build_config_driven_dag(
    repo_root: str | Path,
    dag_config_path: str | Path,
    environment: str = "dev",
):
    """Create a DAG object from YAML configuration and framework standards."""
    registry = ConfigRegistry(repo_root=repo_root, environment=environment)
    dag_config = registry.load_dag_config(relative_path=dag_config_path)
    return build_standard_dag(dag_config=dag_config, environment=environment)
