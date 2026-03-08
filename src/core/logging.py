import logging
import os
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(level: int | None = None) -> None:
    """Configure root logging.

    `level` can be provided as an int or will be read from environment variable
    `LOG_LEVEL` (e.g. "DEBUG", "INFO"). Defaults to INFO.
    """
    if level is None:
        env = os.getenv("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, env, logging.INFO)

    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
        stream=sys.stderr,
    )


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
