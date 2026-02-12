from loguru import logger
import sys
from pathlib import Path

# Define log paths
BASE_DIR = Path(__file__).parent.parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"
ERROR_LOG_FILE = LOG_DIR / "error.log"

def configure_logger():
    """
    Configures the logger with rotation, retention, and formatting.
    """
    # Remove default handler
    logger.remove()

    # Console Handler (Human readable)
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )

    # File Handler (JSON or Detailed for machine parsing/debugging)
    logger.add(
        LOG_FILE,
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

    # Error Log Handler (Separate file for errors)
    logger.add(
        ERROR_LOG_FILE,
        rotation="10 MB",
        retention="30 days",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        backtrace=True,
        diagnose=True
    )

    logger.info("Logger initialized.")

# Auto-configure on import
configure_logger()
