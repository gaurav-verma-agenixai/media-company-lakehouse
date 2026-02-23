"""Validate Airflow DAG importability and parse health.

This script is designed for CI quality gates and local pre-merge checks.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from airflow.models import DagBag


def main() -> int:
    """Run DAG import checks and return process exit code."""
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "src"

    # Keep import resolution identical between local runs and CI containers.
    sys.path.insert(0, str(src_path))
    sys.path.insert(0, str(repo_root))

    os.environ.setdefault("AIRFLOW__CORE__LOAD_EXAMPLES", "False")

    dag_bag = DagBag(
        dag_folder=str(repo_root / "dags"),
        include_examples=False,
        safe_mode=False,
    )

    if dag_bag.import_errors:
        print("DAG import errors detected:")
        for dag_file, error_message in dag_bag.import_errors.items():
            print(f"- {dag_file}: {error_message}")
        return 1

    if not dag_bag.dags:
        print("No DAGs found in dags/ directory.")
        return 1

    print(f"DAG parse successful. Loaded {len(dag_bag.dags)} DAG(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
