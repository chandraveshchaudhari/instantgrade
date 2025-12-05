import logging
import sys
from pathlib import Path
from datetime import datetime


class ColorFormatter(logging.Formatter):
    """Adds colored output for Jupyter and terminal readability."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[37m",      # White
        "SUCCESS": "\033[32m",   # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        msg = super().format(record)
        return f"{color}{msg}{self.RESET}"


def setup_logger(
    log_dir: str | Path | None = None,
    level: str = "normal"
) -> logging.Logger:
    """
    Configure logging for the Evaluator pipeline.

    Parameters
    ----------
    log_dir : str or Path or None
        Folder path to store logs. If None, logs are not saved to file.
    level : str, default="normal"
        Logging verbosity level: "minimal", "normal", "verbose", "debug"

    Returns
    -------
    logging.Logger
    """
    # Map string levels
    level_map = {
        "minimal": logging.WARNING,
        "normal": logging.INFO,
        "verbose": logging.DEBUG,
        "debug": logging.DEBUG,
    }
    log_level = level_map.get(level.lower(), logging.INFO)

    logger = logging.getLogger("Evaluator")
    logger.setLevel(log_level)
    logger.handlers.clear()  # avoid duplication in notebooks

    # --- Console Handler (colored output) ---
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(log_level)
    formatter = ColorFormatter("%(asctime)s | %(levelname)-8s | %(message)s", "%H:%M:%S")
    console.setFormatter(formatter)
    logger.addHandler(console)

    # --- File Handler (optional) ---
    if log_dir:
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = Path(log_dir) / f"evaluator_{timestamp}.log"

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)

        logger.info(f"File logging enabled → {log_path}")

    return logger
