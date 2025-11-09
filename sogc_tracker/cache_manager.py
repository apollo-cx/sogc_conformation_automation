import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def load_cache(cache_file: str) -> Dict[str, Any]:
    """Loads the persistence cache from a JSON file."""

    if not os.path.exists(cache_file):
        logger.info("No cache file found at '%s'. Starting fresh.", cache_file)
        return {}

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
            logger.info("Cache loaded from '%s'", cache_file)
            return cache

    except (json.JSONDecodeError, IOError) as e:
        logger.error(
            "Could not load cache from '%s'. Starting with an empty cache Error: %s",
            cache_file,
            e,
            exc_info=True,
        )
        return {}


def save_cache(
    cache_file: str,
    cache_data: Dict[str, Any],
):
    """Saves the cache data to a JSON file."""
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=4)
        logger.info("Cache saved to '%s'", cache_file)

    except IOError as e:
        logger.error(
            "Could not save cache to '%s'. Error: %s", cache_file, e, exc_info=True
        )


def clear_cache(cache_file: str):
    """Clears the cache by deleting the cache file."""
    try:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            logger.info("Cache file '%s' has been deleted.", cache_file)
        else:
            logger.info("No cache file found at '%s' to delete.", cache_file)

    except IOError as e:
        logger.error(
            "Could not delete cache file '%s'. Error: %s", cache_file, e, exc_info=True
        )
