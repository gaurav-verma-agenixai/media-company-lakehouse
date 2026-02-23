"""Utilities for creating Spark submit commands from typed config."""

from __future__ import annotations

from lakehouse_framework.config.models import SparkSubmitConfig


def build_spark_submit_command(spark_submit: SparkSubmitConfig, environment: str) -> str:
    """Construct a deterministic spark-submit command.

    Keeping command generation in one place improves consistency and simplifies
    platform-wide enhancements such as adding observability flags.
    """
    conf_args = " ".join([f"--conf {key}={value}" for key, value in spark_submit.conf.items()])
    jars_args = "" if not spark_submit.jars else f"--jars {','.join(spark_submit.jars)}"

    return (
        "spark-submit "
        f"--master {spark_submit.master} "
        f"--deploy-mode {spark_submit.deploy_mode} "
        f"{conf_args} {jars_args} "
        f"{spark_submit.application} "
        f"--job-config {spark_submit.job_config} "
        f"--env {environment}"
    ).strip()
