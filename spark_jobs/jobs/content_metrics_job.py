"""Spark ETL job for deriving content-level engagement metrics."""

from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

from lakehouse_framework.spark.base_job import BaseSparkJob


class ContentMetricsJob(BaseSparkJob):
    """Example team ETL job implementing the shared Spark contract."""

    def extract(self) -> DataFrame:
        source = self.config.source
        # Config-driven source read keeps pipeline logic flexible per environment.
        return self.spark.read.format(source["format"]).load(source["path"])

    def transform(self, dataframe: DataFrame) -> DataFrame:
        dimensions = self.config.transformations.get("group_by", ["content_id"])
        aggregations = self.config.transformations.get("aggregations", {})

        agg_exprs = []
        for alias, expression in aggregations.items():
            agg_exprs.append(F.expr(expression).alias(alias))

        return dataframe.groupBy(*dimensions).agg(*agg_exprs)

    def load(self, dataframe: DataFrame) -> None:
        target = self.config.target
        (  # noqa: WPS317
            dataframe.write.mode(target.get("mode", "overwrite"))
            .format(target.get("format", "parquet"))
            .save(target["path"])
        )
