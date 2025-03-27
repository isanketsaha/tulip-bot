import os
from typing import Dict
import traceback
import requests

from src.utils import logger


class OfficeTimeApi:

    def __init__(self):
        self.baseUrl = 'https://api.etimeoffice.com/api'
        self.headers = {
            "Authorization": "Bearer VHVsaXBTY2hvb2w6dHVsaXBhZG1pbjpSYWtoaUAwNjp0cnVlOg==",
            # Replace with your API token
            # "Content-Type": "application/json"
        }

    def get(self, api_url, params: Dict):
        try:
            response = requests.get(self.baseUrl + api_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {traceback.format_exc()}")


