"""Spark session construction helper for consistent runtime behavior."""

from __future__ import annotations

from pyspark.sql import SparkSession


def build_spark_session(app_name: str, spark_conf: dict[str, str]) -> SparkSession:
    """Create Spark session from app name and key-value config map."""
    builder = SparkSession.builder.appName(app_name)
    for key, value in spark_conf.items():
        builder = builder.config(key, value)
    return builder.getOrCreate()
