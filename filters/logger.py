import logging
import sys
from pathlib import Path


LOG_DIR = Path("./artifacts/logs")
LOG_DIR.mkdir(exist_ok=True)


def get_filter_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(LOG_DIR / f"{name}.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
