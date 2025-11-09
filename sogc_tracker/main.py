import time

import os
import csv
import logging
import datetime
import dataclasses

from typing import List, Tuple, Dict, Any

from . import config
from .cache_manager import load_cache, save_cache
from .zefix_search import ZefixAPI, CompanyInfo
from logging_config import setup_logging

logger = logging.getLogger(__name__)


def load_companies_to_check(file_path: str) -> list:
    """Loads company names from a text file."""
    try:
        with open(file_path, "r", encoding="utf-8") as infile:
            companies_to_check = [line.strip() for line in infile if line.strip()]

        if not companies_to_check:
            logger.warning("Input file '%s' is empty.", file_path)
            return []

        logger.info("Loaded %d companies form '%s'", len(companies_to_check), file_path)
        return companies_to_check

    except FileNotFoundError:
        logger.error("Input file '%s' not found.", file_path)
        return []

    except Exception as e:
        logger.error(
            "An error occurred while reading the '%s': %s", file_path, e, exc_info=True
        )
        return []


def process_companies(
    api: ZefixAPI, companies: List[str], cache_data: Dict[str, Any]
) -> Tuple[list[CompanyInfo], List[str]]:
    """Searches for each company and retrieves their cantonal excerpt links."""

    newly_found_results = []
    companies_not_found = []

    todays_date = datetime.date.today().isoformat()

    for company_name in companies:

        # 1. Check cache
        if company_name in cache_data:

            cached_entry = cache_data[company_name]

            if cached_entry is None:
                logger.info("Cache hit (Not Found): %s", company_name)
                companies_not_found.append(company_name)
            else:
                logger.info("Cache hit (Found): %s", company_name)

            continue

        # 2. If not in cache, query API
        logger.info("Querying API for: %s", company_name)
        company_info = None

        data = api.get_company_data(company_name)

        if data:
            company_info = api.get_cantonal_exerpt(data, company_name)

        if company_info:
            company_info.search_date = todays_date
            newly_found_results.append(company_info)
            cache_data[company_name] = dataclasses.asdict(company_info)

            logger.info(
                "Found: %s -> %s",
                company_name,
                company_info.company_cantonal_exerpt_link,
            )

        else:
            companies_not_found.append(company_name)
            cache_data[company_name] = None

            logger.warning("Not found: %s (API error or no exact match)", company_name)

        time.sleep(config.API_REQUEST_DELAY)

    return newly_found_results, companies_not_found


def save_results_to_csv(output_file: str, results: List[CompanyInfo]):
    """
    Saves *newly* found results to CSV file.
    Appends to the file if it already exists.
    """

    if not results:
        logger.info("No *new* results to save.")
        return

    file_exists = os.path.exists(output_file)

    try:
        with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "search_date",
                "company_name",
                "company_uid",
                "company_cantonal_exerpt_link",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for company_info in results:
                writer.writerow(dataclasses.asdict(company_info))

        logger.info("Saved %d new results to '%s'", len(results), output_file)

    except IOError:
        logger.error("Could not write to file '%s'", output_file)

    except Exception as e:
        logger.error(
            "An error occurred while writing to the output file: %s", e, exc_info=True
        )


def save_remaining_companies(output_file: str, companies_not_found: List[str]):
    """Saves the list of companies that were not found to a new text file."""
    try:
        # 'w' mode will create the file or overwrite it if it already exists
        with open(output_file, "w", encoding="utf-8") as f:
            for company_name in companies_not_found:
                f.write(f"{company_name}\n")

        if companies_not_found:
            # Note: Fixed the logging format specifiers (e.g., %d for count, %s for string)
            logger.info(
                "Saved %d remaining companies to '%s'.",
                len(companies_not_found),
                output_file,
            )
        else:
            logger.info("All companies processed. No remaining companies to save.")

    except IOError as e:
        logger.error(
            "Error: Could not write remaining companies file '%s'. Error: %s",
            output_file,
            e,
            exc_info=True,
        )


def main():
    """Main function to demonstrate the ZefixAPI usage."""

    setup_logging()

    logger.info("--- Starting new SOGC conformation run ---")

    api = ZefixAPI()
    cache_data = load_cache(config.DEFAULT_CACHE_FILE)

    companies_to_check = load_companies_to_check(config.DEFAULT_INPUT_FILE)

    if not companies_to_check:

        logger.warning("No companies to process. Exiting")
        return

    (new_results, remaining_companies) = process_companies(
        api, companies_to_check, cache_data
    )

    save_results_to_csv(config.DEFAULT_OUTPUT_FILE, new_results)
    save_cache(config.DEFAULT_CACHE_FILE, cache_data)
    save_remaining_companies(config.DEFAULT_OUTPUT_NOT_FOUND_FILE, remaining_companies)

    logger.info("--- SOGC conformation run finished ---")


if __name__ == "__main__":
    main()
