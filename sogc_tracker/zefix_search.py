import logging
from dataclasses import dataclass
from typing import Optional, Dict, Any

import requests
from . import config


logger = logging.getLogger(__name__)


@dataclass
class CompanyInfo:
    """Stores the extracted company details."""

    company_name: str
    company_uid: str
    company_cantonal_exerpt_link: str
    search_date: Optional[str] = None


class ZefixAPI:
    """Handles interactions with the Zefix API."""

    def __init__(self, base_url=config.ZEFIX_BASE_URL):
        self.base_url = base_url

    def get_company_data(self, company_name: str) -> Optional[Dict[str, Any]]:
        """Searches for a company by name using the full POST payload."""

        try:

            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:144.0) Gecko/20100101 Firefox/144.0",
                "Origin": "https://www.zefix.ch",
            }

            payload = {
                "name": company_name,
                "languageKey": "en",
                "maxEntries": 50,
                "offset": 0,
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=config.API_REQUEST_TIMEOUT,
            )

            if response.status_code == 200:
                return response.json()

            if response.status_code == 404:
                logger.info("Company not found via API (404): %s", company_name)
                return None

            logger.error(
                "API request failed with status code %s for company %s. Response: %s",
                response.status_code,
                company_name,
                response.text,
            )
            return None

        except requests.RequestException as e:
            logger.error(
                "An error during the API request occurred: %s", e, exc_info=True
            )
            return None

    def get_cantonal_exerpt(
        self, data: Dict[str, Any], original_search_term: str
    ) -> Optional[CompanyInfo]:
        """
        Extracts the cantonal excerpt link from the company data.
        """

        if not data or not data.get("list"):
            return None

        for company in data["list"]:
            try:
                result_name = company["name"]

                if original_search_term.lower() == result_name.lower():
                    return CompanyInfo(
                        company_name=company["name"],
                        company_uid=company["uid"],
                        company_cantonal_exerpt_link=company["cantonalExcerptWeb"],
                    )

            except (KeyError, IndexError) as e:
                logger.warning("Error parsing company data: %s", e, exc_info=True)
                return None

        return None
