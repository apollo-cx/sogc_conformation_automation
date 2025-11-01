import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class CompanyInfo:
    name: str
    uid: str
    legalSeat: str
    registryOfCommerceId: int
    status: str

    
class ZefixAPI:
    BASE_URL = "https://www.zefix.admin.ch/ZefixPublicREST/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}" if api_key else None
        }
    
    def search_company(self, company_name: str) -> Optional[CompanyInfo]:
        try:
            endpoint = f"{self.BASE_URL}/firm/search"
            params = {"name": company_name}
            
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                return None
                
            company = data[0]
            
            return CompanyInfo(
                name=company["name"],
                uid=company["uid"],
                registryOfCommerceId=company["registryOfCommerceId"],
                status=company["status"]
            )
            
        except requests.RequestException as e:
            print(f"Error searching for company: {e}")
            return None

    def get_chregister_link(self, canton: str, uid: str) -> str:
        canton = canton.lower()
        return f"https://{canton}.chregister.ch/cr-portal/auszug/auszug.xhtml?uid={uid}"

def main():
    
    zefix = ZefixAPI()
    
    company_name = "Example AG"

    result = zefix.search_company(company_name)
    
    if result:
        chregister_link = zefix.get_chregister_link(result.legalSeat, result.uid)
        print(f"CHRegister Link: {chregister_link}")
        
    else:
        print(f"Company '{company_name}' not found")

if __name__ == "__main__":
    main()