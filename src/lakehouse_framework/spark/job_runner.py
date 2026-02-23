"""Spark job runner abstraction used by entrypoints and orchestration runtime."""

from __future__ import annotations

from pathlib import Path

from lakehouse_framework.config.registry import ConfigRegistry
from lakehouse_framework.spark.base_job import BaseSparkJob
from lakehouse_framework.spark.session import build_spark_session
from lakehouse_framework.utils.module_loading import load_class
from lakehouse_framework.utils.logging import get_logger


logger = get_logger(__name__)


def run_spark_job(repo_root: str | Path, job_config_path: str | Path, environment: str) -> None:
    """Run Spark job from YAML config path and environment name."""
    registry = ConfigRegistry(repo_root=repo_root, environment=environment)
    config = registry.load_spark_job_config(relative_path=job_config_path)

    job_class = load_class(config.job_class)
    if not issubclass(job_class, BaseSparkJob):
        raise TypeError(f"Configured job class must inherit BaseSparkJob: {config.job_class}")

    spark = build_spark_session(config.job_name, config.spark_conf)
    logger.info("Starting Spark job '%s' in '%s' environment", config.job_name, environment)

    try:
        job_instance = job_class(spark=spark, config=config)
        job_instance.run()
        logger.info("Completed Spark job '%s'", config.job_name)
    finally:
        spark.stop()
