# tests/test_logger.py

import logging

from core import logger


def test_logger_methods(caplog):
    caplog.set_level(logging.DEBUG)

    logger.info("Test")
    logger.warn("Warnung")
    logger.error("Fehler")
    logger.success("Erfolg")

    assert "INFO: Test" in caplog.text
    assert "WARNING: Warnung" in caplog.text
    assert "ERROR: Fehler" in caplog.text
    assert "SUCCESS: Erfolg" in caplog.text
