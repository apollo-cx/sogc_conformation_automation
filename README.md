Project Structure
sogc_conformation_automation/
│
├── .gitignore
├── pyproject.toml              # Project definition and dependencies
├── README.md                   # This file
│
├── data/
│   └── companies_to_be_checked.txt # INPUT: Your list of companies
│
├── output/                     # OUTPUT: Generated files (ignored by git)
│   ├── results.csv
│   └── companies_not_found.txt
│
├── sogc_tracker/               # The main Python package
│   ├── cache_manager.py        # Handles loading/saving the JSON cache
│   ├── main.py                 # The main application entry point
│   ├── zefix_search.py         # The ZefixAPI client class
│   │
│   └── config/                 # Sub-package for configuration
│       ├── config.py           # All file paths and API settings
│       └── logging_config.py   # Logging setup
│
├── app.log                     # OUTPUT: Log file (ignored by git)
└── cache.json                  # OUTPUT: Cache file (ignored by git)
Setup & Installation
This project uses uv for package management.

Create a virtual environment:

Bash

uv venv
Activate the environment:

Bash

source .venv/bin/activate
(On Windows, use .venv\Scripts\activate)

Install the project in editable mode: This will install requests (from pyproject.toml) and also make your sogc_tracker package available to your environment.

Bash

uv pip install -e .
How to Use
Populate the Input File: Add your list of company names to data/companies_to_be_checked.txt. Each company name should be on a new line.

Run the Application: From the root directory (sogc_conformation_automation/), run the following command:

Bash

uv run python -m sogc_tracker.main
The script will start, load the input file, check the cache, query the API for any new companies, and then save all the results.