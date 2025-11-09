## Setup & Installation

This project uses `uv` for package management.

1.  **Create a virtual environment:**
    ```bash
    uv venv
    ```

2.  **Activate the environment:**
    ```bash
    source .venv/bin/activate
    ```
    *(On Windows, use `.venv\Scripts\activate`)*

3.  **Install the project in editable mode:**
    This will install `requests` (from `pyproject.toml`) and also make your `sogc_tracker` package available to your environment.
    ```bash
    uv pip install -e .
    ```

## Project Structure
```
sogc_conformation_automation/
│
├── .gitignore
├── pyproject.toml                  # Project definition and dependencies
├── README.md                       # This file
│
├── data/
│ └── companies_to_be_checked.txt   # INPUT: Your list of companies
│
├── output/                         # OUTPUT: Generated files (ignored by git)
│ ├── results.csv
│ └── companies_not_found.txt
│
├── sogc_tracker/                   # The main Python package
│ ├── cache_manager.py              # Handles loading/saving the JSON cache
│ ├── main.py                       # The main application entry point
│ ├── zefix_search.py               # The ZefixAPI client class
│ │
│ └── config/                       # Configuration sub-package
│ ├── config.py                     # File paths and API settings
│ └── logging_config.py             # Logging setup
│
├── app.log                         # OUTPUT: Log file (ignored by git)
└── cache.json                      # OUTPUT: Cache file (ignored by git)
```