import logging
import sys
from pathlib import Path

from app.config import settings


LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def setup_logging() -> None:
    """Configure application-wide logging."""

    log_directory = settings.project_root / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)

    log_file = log_directory / "datapilot.log"

    formatter = logging.Formatter(LOG_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    if root_logger.handlers:
        return

    root_logger.setLevel(
        logging.DEBUG if settings.debug else logging.INFO
    )

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a logger for the specified module."""

    return logging.getLogger(name)