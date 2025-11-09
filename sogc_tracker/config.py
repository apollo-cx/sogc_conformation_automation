"""
Central configuration file for the SOGC Tracker application.
Holds all file paths, API endpoints, and other constants.
"""

# --- File Paths ---
DEFAULT_INPUT_FILE = "data/companies_to_be_checked.txt"
DEFAULT_OUTPUT_FILE = "output/results.csv"
DEFAULT_OUTPUT_NOT_FOUND_FILE = "output/companies_not_found"
DEFAULT_CACHE_FILE = "cache.json"
DEFAULT_LOG_FILE = "app.log"

# --- API Settings ---
ZEFIX_BASE_URL = "https://www.zefix.ch/ZefixREST/api/v1/firm/search.json"

# --- Other Settings ---
API_REQUEST_TIMEOUT = 150  # Seconds
API_REQUEST_DELAY = 5  # Seconds between requests
