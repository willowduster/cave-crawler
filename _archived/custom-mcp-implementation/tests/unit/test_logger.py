"""Unit tests for logger utility."""

import logging
import pytest
from pathlib import Path
from servers.common.logger import setup_logger, get_logger


def test_setup_logger_creates_file_handler(tmp_path: Path) -> None:
    """Test that setup_logger creates a file handler with correct path."""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_logger", str(log_file), level=logging.DEBUG)
    
    assert logger.name == "test_logger"
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0
    
    # Test that log file is created
    logger.info("Test message")
    assert log_file.exists()


def test_setup_logger_with_default_level(tmp_path: Path) -> None:
    """Test that setup_logger uses INFO level by default."""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_default", str(log_file))
    
    assert logger.level == logging.INFO


def test_get_logger_returns_existing_logger(tmp_path: Path) -> None:
    """Test that get_logger returns the same logger instance."""
    log_file = tmp_path / "test.log"
    logger1 = setup_logger("test_singleton", str(log_file))
    logger2 = get_logger("test_singleton")
    
    assert logger1 is logger2


def test_logger_formats_messages_correctly(tmp_path: Path) -> None:
    """Test that logger formats messages with timestamp and level."""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_format", str(log_file))
    
    logger.info("Test message")
    
    content = log_file.read_text()
    assert "INFO" in content
    assert "Test message" in content
    assert "test_format" in content


def test_logger_handles_multiple_levels(tmp_path: Path) -> None:
    """Test that logger handles different log levels correctly."""
    log_file = tmp_path / "test.log"
    logger = setup_logger("test_levels", str(log_file), level=logging.DEBUG)
    
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    content = log_file.read_text()
    assert "DEBUG" in content
    assert "INFO" in content
    assert "WARNING" in content
    assert "ERROR" in content
