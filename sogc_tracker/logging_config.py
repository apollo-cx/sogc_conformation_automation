"""
Handles the setup of the root logger for the application.
"""

import logging
import logging.handlers

from . import config


def setup_logging():
    """
    Configures the root logger based on settings in config.py.
    This function should be called once at application startup.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(config.DEFAULT_LOG_FILE),  # Get path from config
            logging.StreamHandler(),
        ],
    )
