from dataclasses import dataclass

import requests
import json

BASE_URL ="https://www.zefix.ch/ZefixREST/api/v1/company/search"

@dataclass
class CompanyInfo:
    company_name: str
    company_uid: str
    company_cantonal_exerpt_link: str

class ZefixAPI:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def get_company_data(self, company_name):
        try:
            params = {'name': company_name}

            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            
            response.raise_for_status()

        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def get_cantonal_exerpt(self, company_data):
        with open(company_data, 'r') as file:
            data = json.load(file)
        
        company = data["list"][0]

        return CompanyInfo(
            company_name=company["name"],
            company_uid=company["uid"],
            company_cantonal_exerpt_link=company["cantonalExcerptWeb"]
        )

def main():
    api = ZefixAPI()
    print(api.get_cantonal_exerpt("./test/test_peoplewise_ag.json"))

if __name__ == "__main__":
    main()
