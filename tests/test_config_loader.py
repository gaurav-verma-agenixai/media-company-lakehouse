"""Unit tests for configuration loading primitives."""

from lakehouse_framework.config.loader import deep_merge


def test_deep_merge_replaces_leaf_values() -> None:
    base = {
        "spark_submit": {
            "master": "local[*]",
            "conf": {"spark.sql.shuffle.partitions": "8"},
        }
    }
    overlay = {
        "spark_submit": {
            "master": "yarn",
            "conf": {"spark.sql.shuffle.partitions": "300"},
        }
    }

    merged = deep_merge(base, overlay)
    assert merged["spark_submit"]["master"] == "yarn"
    assert merged["spark_submit"]["conf"]["spark.sql.shuffle.partitions"] == "300"
