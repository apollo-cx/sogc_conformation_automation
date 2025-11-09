import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def load_cache(cache_file: str) -> Dict[str, Any]:
    """Loads the persistence cache from a JSON file."""
    
    if not os.path.exists(cache_file):
        logger.info(f"No cache file found at '{cache_file}'. Starting fresh.")
        return {}
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            logger.info(f"Cache loaded from '{cache_file}'")
            return cache
        
    except (json.JSONDecodeError, IOError) as e:
        logger.error(
            f"Could not load cache from '{cache_file}'. Starting with an empty cache Error: {e}",
            exc_info=True
        )
        return {}

def save_cache(cache_file: str, cache_data: Dict[str, Any],):
    """Saves the cache data to a JSON file."""
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=4)
        logger.info(f"Cache saved to '{cache_file}'")
            
    except IOError as e:
        logger.error(
            f"Could not save cache to '{cache_file}'. Error: {e}",
            exc_info=True
        )

def clear_cache(cache_file: str):
    """Clears the cache by deleting the cache file."""
    try:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            logger.info(f"Cache file '{cache_file}' has been deleted.")
        else:
            logger.info(f"No cache file found at '{cache_file}' to delete.")
            
    except IOError as e:
        logger.error(
            f"Could not delete cache file '{cache_file}'. Error: {e}",
            exc_info=True
        )