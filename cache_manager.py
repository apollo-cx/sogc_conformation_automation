import os
import json
from typing import Dict, Any

def load_cache(cache_file: str) -> Dict[str, Any]:
    """Loads the persistence cache from a JSON file."""
    
    if not os.path.exists(cache_file):
        return {}
    
    try:
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache = json.load(f)
            return cache
        
    except (json.JSONDecodeError, IOError) as e:
        print(f"Could not load cache from '{cache_file}'. Starting with an empty cache Error: {e}")
        return {}

def save_cache(cache_file: str, cache_data: Dict[str, Any],):
    """Saves the cache data to a JSON file."""
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, indent=4)
            
    except IOError as e:
        print(f"Could not save cache to '{cache_file}'. Error: {e}")

def clear_cache(cache_file: str):
    """Clears the cache by deleting the cache file."""
    try:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            print(f"Cache file '{cache_file}' has been deleted.")
        else:
            print(f"No cache file found at '{cache_file}' to delete.")
            
    except IOError as e:
        print(f"Could not delete cache file '{cache_file}'. Error: {e}")