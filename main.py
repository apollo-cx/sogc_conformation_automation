import time
import dataclasses
import csv

import datetime
from typing import List
from zefix_search import ZefixAPI, CompanyInfo

DEFAULT_INPUT_FILE = "test/companies/companies_to_be_checked.txt"
DEFAULT_OUTPUT_FILE = "test/companies/results.csv"

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

def process_companies(api: ZefixAPI, companies: List[str]) -> list[CompanyInfo]:
    """Searches for each company and retrieves their cantonal excerpt links."""
    
    results = []

    for company_name in companies:
        data = api.get_company_data(company_name)

        if data:
            company_info = api.get_cantonal_exerpt(data)

            if company_info:
                results.append(company_info)
                print(f"Found: {company_name} -> {company_info.company_cantonal_exerpt_link}")

            else:
                print(f"Not found: {company_name}")
    
        time.sleep(1)

    return results

def save_results_to_csv(results: List[CompanyInfo], output_file: str):
    """Saves results to CSV file."""

    if not results:
        print("No results to save.")
        return
    
    search_date_str = datetime.date.today().isoformat()
    
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['search_date','company_name', 'company_uid', 'company_cantonal_exerpt_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            for company_info in results:
                row_data = {
                    "search_date": search_date_str,
                    "company_name": company_info.company_name,
                    "company_uid": company_info.company_uid,
                    "company_cantonal_exerpt_link": company_info.company_cantonal_exerpt_link
                }
                writer.writerow(row_data)
    
    except IOError:
        print(f"Could not write to file '{output_file}'.")

    except Exception as e:
        print(f"An error occurred while writing to the output file: {e}")

def main():
    """Main function to demonstrate the ZefixAPI usage."""

    api = ZefixAPI()

    # 1. Read
    companies_to_check = load_companies_to_check(DEFAULT_INPUT_FILE)

    # 2. Process
    all_results = process_companies(api, companies_to_check)

    # 3. Save
    save_results_to_csv(all_results, DEFAULT_OUTPUT_FILE)    

if __name__ == "__main__":
    main()