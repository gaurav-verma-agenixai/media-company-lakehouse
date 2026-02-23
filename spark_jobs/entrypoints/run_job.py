"""CLI entrypoint for launching Spark jobs from repository config files."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from lakehouse_framework.spark.job_runner import run_spark_job  # noqa: E402


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for Spark job execution."""
    parser = argparse.ArgumentParser(description="Run a config-driven Spark ETL job")
    parser.add_argument("--job-config", required=True, help="Relative path to Spark job config YAML")
    parser.add_argument("--env", default="dev", help="Environment override name")
    return parser.parse_args()


def main() -> None:
    """Entrypoint main function."""
    args = parse_args()
    run_spark_job(
        repo_root=REPO_ROOT,
        job_config_path=args.job_config,
        environment=args.env,
    )


if __name__ == "__main__":
    main()
