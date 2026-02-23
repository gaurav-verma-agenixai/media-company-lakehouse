"""Dynamic import utilities for runtime class loading."""

from __future__ import annotations

from importlib import import_module


def load_class(dotted_path: str) -> type:
    """Load class from dotted path, e.g. `spark_jobs.jobs.foo.BarJob`."""
    module_path, class_name = dotted_path.rsplit(".", maxsplit=1)
    module = import_module(module_path)
    return getattr(module, class_name)
