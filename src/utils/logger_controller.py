import sys
from loguru import logger

def log_mode(levels: str):
    logger.remove()

    if isinstance(levels, str):
        levels = [lvl.strip().upper() for lvl in levels.split(",")]

    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    levels = [lvl for lvl in levels if lvl in valid_levels]

    if not levels:
        logger.warning("⚠️ No valid log levels provided. Defaulting to DEBUG.")
        levels = ["DEBUG"]

    priority = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    base_level = min(levels, key=lambda lvl: priority.index(lvl))

    logger.add(
        sys.stderr,
        level=base_level,
        filter=lambda record: record["level"].name in levels
    )

    logger.debug(f"📩 Active log levels: {', '.join(levels)}")

def setup_logger(log_level: str = None):
    logger.remove()
    log_mode(log_level)