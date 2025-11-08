from dataclasses import dataclass

import requests

from typing import Optional, Dict, Any


BASE_URL = "https://www.zefix.ch/ZefixREST/api/v1/firm/search.json"

@dataclass
class CompanyInfo:
    """Stores the extracted company details."""

    company_name: str
    company_uid: str
    company_cantonal_exerpt_link: str

class ZefixAPI:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def get_company_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Searches for a company by name using the full POST payload."""

        try:

            headers = {
                'Accept': 'application/json', 
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0',
                'Origin': 'https://www.zefix.ch'
            }
            
            payload = {
                'name': company_name,
                'languageKey': 'en',
                'maxEntries': 20,
                'offset': 0
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
             
            response.raise_for_status()

        except requests.RequestException as e:
            print(f"An error during the API request occurred: {e}")
            return None

        return None
        
    def get_cantonal_exerpt(self, data: Dict[str, Any]) -> Optional[CompanyInfo]:
        """Extracts the cantonal excerpt link from the company data."""

        if not data or not data.get("list"):
            return None
        try:

            company = data["list"][0]

            return CompanyInfo(
                company_name=company["name"],
                company_uid=company["uid"],
                company_cantonal_exerpt_link=company["cantonalExcerptWeb"]
            )

        except (KeyError, IndexError) as e:
            print(f"Error parsing company data: {e}")
            return None

def main():
    """Main function to demonstrate the ZefixAPI usage."""

    api = ZefixAPI()
    company_name = input("Enter company name: ")

    if not company_name:
        print("No company name provided.")
        return None
    
    print(f"Searching for company: {company_name}")
    data = api.get_company_data(company_name)

    if data:
        company_info = api.get_cantonal_exerpt(data)

        if company_info:
            print(f"Company Name: {company_info.company_name}")
            print(f"Company UID: {company_info.company_uid}")
            print(f"Cantonal Excerpt Link: {company_info.company_cantonal_exerpt_link}")
        
        else:
            print("No company found matching that name.")

if __name__ == "__main__":
    main()
