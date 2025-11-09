import time
import dataclasses
import csv
import os
import datetime

from typing import List, Tuple, Dict, Any
from cache_manager import load_cache, save_cache, clear_cache
from zefix_search import ZefixAPI, CompanyInfo

DEFAULT_INPUT_FILE = "test/companies/companies_to_be_checked.txt"
DEFAULT_OUTPUT_FILE = "test/companies/results.csv"
DEFAULT_CACHE_FILE = "cache.json"

def load_companies_to_check(file_path: str) -> list:
    """Loads company names from a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            companies_to_check = [line.strip() for line in infile if line.strip()]
        
        if not companies_to_check:
            print(f"Input file '{file_path}' is empty.")
            return []
            
        return companies_to_check
    
    except FileNotFoundError:
        print(f"Input file '{file_path}' not found.")
        return []
    
    except Exception as e:
        print(f"An error occurred while reading the input file: {e}")
        return []

def process_companies(
        api: ZefixAPI,
        companies: List[str],
        cache_data: Dict[str, Any]
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
                companies_not_found.append(company_name)
            
            continue

        # 2. If not in cache, query API
        company_info = None

        data = api.get_company_data(company_name)

        if data:
            company_info = api.get_cantonal_exerpt(data, company_name)

        if company_info:
            company_info.search_date = todays_date
            newly_found_results.append(company_info)
            cache_data[company_name] = dataclasses.asdict(company_info)

            print(f"Found: {company_name} -> {company_info.company_cantonal_exerpt_link}")

        else:
            companies_not_found.append(company_name)
            cache_data[company_name] = None

            print(f"Not found: {company_name} (API error or no exact match)")
    
        time.sleep(20)

    return newly_found_results, companies_not_found

def save_results_to_csv(results: List[CompanyInfo], output_file: str):
    """
    Saves *newly* found results to CSV file.
    Appends to the file if it already exists.
    """

    if not results:
        print("No *new* results to save.")
        return
    
    file_exists = os.path.exists(output_file)
    
    try:
        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['search_date','company_name', 'company_uid', 'company_cantonal_exerpt_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()
            
            for company_info in results:
                writer.writerow(dataclasses.asdict(company_info))
    
    except IOError:
        print(f"Could not write to file '{output_file}'.")

    except Exception as e:
        print(f"An error occurred while writing to the output file: {e}")

def update_input_file(companies_not_found: List[str], input_file: str):
    """Rewrites the input file with only the companies that were not found."""
    try:
        with open(input_file, 'w', encoding='utf-8') as f:
            for company_name in companies_not_found:
                f.write(f"{company_name}\n")

    except IOError as e:
        print(f"Error: Could not rewrite input file '{input_file}'. Error: {e}")

def main():
    """Main function to demonstrate the ZefixAPI usage."""

    api = ZefixAPI()
    cache_data = load_cache(DEFAULT_CACHE_FILE)

    companies_to_check = load_companies_to_check(DEFAULT_INPUT_FILE)

    if not companies_to_check:
        print("No companies to process. Exiting")
        return
    
    (new_results, remaining_companies) = process_companies(api, companies_to_check, cache_data)

    save_results_to_csv(new_results, DEFAULT_OUTPUT_FILE)
    save_cache(DEFAULT_CACHE_FILE, cache_data)
    update_input_file(remaining_companies, DEFAULT_INPUT_FILE)

if __name__ == "__main__":
    main()
    clear_cache(DEFAULT_CACHE_FILE)