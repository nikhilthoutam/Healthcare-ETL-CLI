import requests
import logging

class APIClient:
    """
    Fetches cases & vaccination data from disease.sh API.
    """

    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def fetch_cases(self, country):
        """
        Pull daily case & death timeline.
        """
        url = f"{self.base_url}/historical/{country}?lastdays=all"
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            logging.error(f"Cases API error: {e}")
            return {}

    def fetch_vaccinations(self, country):
        """
        Pull vaccination timeline (total vaccinations only).
        """
        url = f"{self.base_url}/vaccine/coverage/countries/{country}?lastdays=all&fullData=false"
        try:
            res = requests.get(url, timeout=10)
            res.raise_for_status()
            return res.json()
        except Exception as e:
            logging.error(f"Vaccination API error: {e}")
            return {}

    def fetch_both(self, country):
        """
        Pull case and vaccination in one go (used in main).
        """
        return self.fetch_cases(country), self.fetch_vaccinations(country)
