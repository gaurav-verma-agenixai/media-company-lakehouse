"""Central logging setup for framework and jobs."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Return logger configured with platform-wide default format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)
