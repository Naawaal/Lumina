import logging
from pathlib import Path

import pytest

from lumina.utils.logger import get_logger


def test_state_context_logs(caplog):
    """
    Ensure entering/exiting state messages are emitted to the logger.
    """
    caplog.set_level(logging.INFO)
    logger = get_logger(None, name="lumina_test", file_logging=False)
    with logger.state_context("Thinking", "unit-test"):
        logger.info("inside state")
    # caplog captures logging output; check for entering/exiting markers
    assert "entering unit-test" in caplog.text
    assert "exiting unit-test" in caplog.text
    assert "inside state" in caplog.text


def test_file_logging_option(tmp_path: Path):
    """
    When file_logging=True, a logfile is created and contains log messages.
    """
    logfile = tmp_path / "lumina_test.log"
    assert not logfile.exists()
    logger = get_logger(
        None, name="lumina_file_test", file_logging=True, file_path=logfile
    )
    logger.info("file test message")
    # ensure handler flushed
    logger.logger.handlers and [
        h.flush() for h in logger.logger.handlers if hasattr(h, "flush")
    ]
    assert logfile.exists()
    content = logfile.read_text(encoding="utf-8")
    assert "file test message" in content
