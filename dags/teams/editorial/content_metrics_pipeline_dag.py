"""Editorial content metrics pipeline DAG.

This DAG is intentionally lightweight and delegates most behavior to framework
and YAML config to reduce long-term maintenance overhead.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    # Ensure framework package is importable in local and Airflow environments.
    sys.path.append(str(SRC_DIR))

from dags.common.config_driven_dag import build_config_driven_dag  # noqa: E402


ENVIRONMENT = os.getenv("LAKEHOUSE_ENV", "dev")

dag = build_config_driven_dag(
    repo_root=REPO_ROOT,
    dag_config_path="configs/dags/content_metrics_pipeline.yaml",
    environment=ENVIRONMENT,
)
