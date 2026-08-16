"""
Shared logger for the whole project.
Any secret-like value passed through `mask_secret` before logging.
"""
from __future__ import annotations

import logging
import sys


def setup_logger(name: str = "deployer_bot") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        # Already configured (avoids duplicate handlers on reimport).
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def mask_secret(value: str | None, visible: int = 4) -> str:
    """Masks a secret, keeping only the last `visible` characters.
    Used so bot tokens / API keys never appear in full in logs or messages.
    """
    if not value:
        return "<empty>"
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]


logger = setup_logger()
