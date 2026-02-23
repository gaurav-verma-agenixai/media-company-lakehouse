"""Config registry used by DAG and Spark runtimes.

This abstraction allows teams to use a stable access API while platform engineers
evolve configuration storage strategy over time.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from lakehouse_framework.config.loader import deep_merge, load_yaml
from lakehouse_framework.config.models import DagConfig, SparkJobConfig, SparkSubmitConfig


class ConfigRegistry:
    """Loads and materializes typed configs from repository YAML files."""

    def __init__(self, repo_root: str | Path, environment: str = "dev") -> None:
        self.repo_root = Path(repo_root)
        self.environment = environment
        self.env_overrides = load_yaml(self.repo_root / "configs" / "environments" / f"{environment}.yaml")

    def load_dag_config(self, relative_path: str | Path) -> DagConfig:
        """Read DAG config and map it into `DagConfig`."""
        raw = self._apply_env(load_yaml(self.repo_root / relative_path))
        spark_submit = None
        if raw.get("spark_submit"):
            spark_submit = SparkSubmitConfig(**raw["spark_submit"])

        return DagConfig(
            dag_id=raw["dag_id"],
            description=raw["description"],
            schedule=raw["schedule"],
            start_date=datetime.fromisoformat(raw["start_date"]),
            catchup=raw.get("catchup", False),
            max_active_runs=raw.get("max_active_runs", 1),
            tags=raw.get("tags", []),
            owner=raw["owner"],
            retries=raw.get("retries", 1),
            retry_delay_minutes=raw.get("retry_delay_minutes", 5),
            spark_submit=spark_submit,
        )

    def load_spark_job_config(self, relative_path: str | Path) -> SparkJobConfig:
        """Read Spark job config and map it into `SparkJobConfig`."""
        raw = self._apply_env(load_yaml(self.repo_root / relative_path))
        return SparkJobConfig(**raw)

    def _apply_env(self, config: dict) -> dict:
        """Overlay environment-specific values when present."""
        overrides = self.env_overrides.get("overrides", {})
        return deep_merge(config, overrides)
