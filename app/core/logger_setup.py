"""..."""

import logging
from pathlib import Path

from concurrent_log_handler import ConcurrentRotatingFileHandler
from pythonjsonlogger import jsonlogger  # Optional, for JSON formatting

from app.core.config import settings


def configure_logger(
    name: str,
    subfolder: str,
    filename: str,
    level=logging.INFO,
    max_bytes: int = 5_000_000,
    backup_count: int = 5,
    json_indent: int = 1,
    log_dir: Path = settings.logging.LOG_DIR_PATH,
    use_json_format: bool = settings.logging.JSON_FORMAT,
    enable_console_log: bool = settings.logging.CONSOLE_LOG,
) -> logging.Logger:
    """
    Configures a logger for a specific service/module with rotation and optional JSON formatting.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False  # Prevent log bubbling to root logger

    # Avoid adding duplicate file handlers
    log_path = log_dir / subfolder
    log_path.mkdir(parents=True, exist_ok=True)
    file_path = log_path / filename

    if any(
        isinstance(h, ConcurrentRotatingFileHandler)
        and h.baseFilename == str(file_path)
        for h in logger.handlers
    ):
        return logger  # Logger already configured

    # Formatters
    if use_json_format:
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            json_indent=json_indent,
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    # File handler
    file_handler = ConcurrentRotatingFileHandler(
        filename=file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler (optional)
    if enable_console_log:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
