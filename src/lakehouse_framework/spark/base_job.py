"""Base classes and contracts for Spark ETL jobs."""

from __future__ import annotations

from abc import ABC, abstractmethod

from pyspark.sql import DataFrame, SparkSession

from lakehouse_framework.config.models import SparkJobConfig


class BaseSparkJob(ABC):
    """Mandatory interface for all Spark ETL jobs in this repository."""

    def __init__(self, spark: SparkSession, config: SparkJobConfig) -> None:
        self.spark = spark
        self.config = config

    @abstractmethod
    def extract(self) -> DataFrame:
        """Read source data and return input DataFrame."""

    @abstractmethod
    def transform(self, dataframe: DataFrame) -> DataFrame:
        """Apply business transformations and return output DataFrame."""

    @abstractmethod
    def load(self, dataframe: DataFrame) -> None:
        """Persist output data to configured target."""

    def run(self) -> None:
        """Run end-to-end ETL lifecycle.

        This hook guarantees every job follows the same execution shape.
        """
        source_df = self.extract()
        transformed_df = self.transform(source_df)
        self.load(transformed_df)
