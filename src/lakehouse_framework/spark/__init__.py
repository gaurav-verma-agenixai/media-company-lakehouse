"""Spark framework abstractions for config-driven ETL jobs."""

from lakehouse_framework.spark.base_job import BaseSparkJob
from lakehouse_framework.spark.job_runner import run_spark_job

__all__ = ["BaseSparkJob", "run_spark_job"]
