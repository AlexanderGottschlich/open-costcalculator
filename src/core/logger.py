# filter/logger.py

import logging
import sys


def setup_logging(level="INFO"):
    log_level = getattr(logging, level.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def warn(message):
    logging.warning(f"WARNING: {message}")


def info(message):
    logging.info(f"INFO: {message}")


def error(message):
    logging.error(f"ERROR: {message}")


def success(message):
    logging.info(f"SUCCESS: {message}")


def debug(message):
    logging.debug(f"DEBUG: {message}")
