"""Config loading helpers.

All YAML loads are funneled through this module to keep parsing behavior and
error messages consistent across teams.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict[str, Any]:
    """Load a YAML document into a dictionary.

    Args:
        path: Path to YAML file.

    Returns:
        Parsed dictionary, empty dict when file is empty.
    """
    resolved = Path(path)
    with resolved.open("r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data or {}


def deep_merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge overlay into base and return a new dictionary."""
    merged = dict(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged
