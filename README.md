## Setup & Installation (from Source)

This project is built as an installable Python package and uses `uv` for environment management.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/sogc-conformation-automation.git](https://github.com/your-username/sogc-conformation-automation.git)
    ```
    *(Replace with your actual repository URL)*

2.  **Navigate to the project directory:**
    ```bash
    cd sogc-conformation-automation
    ```

3.  **Create a virtual environment:**
    ```bash
    uv venv
    ```

4.  **Activate the environment:**
    ```bash
    source .venv/bin/activate
    ```
    *(On Windows, use `.venv\Scripts\activate`)*

5.  **Install the package:**
    This reads the `pyproject.toml` file, installs dependencies (`requests`), and installs your `sogc-tracker` command.
    ```bash
    uv pip install .
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