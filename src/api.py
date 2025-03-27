import os
import traceback
import requests

from src.utils import logger


class TulipApi:

    def __init__(self):
        self.baseUrl = 'https://tuliphost-production.up.railway.app/api'
        self.authUrl = '/authenticate'
        self.__auth__()
        self.headers = {
            "Authorization": "Bearer " + self.__auth__(),  # Replace with your API token
            "Content-Type": "application/json"
        }

    def get(self, api_url):
        try:
            response = requests.get(self.baseUrl + api_url, headers=self.headers, timeout=10)
            response.raise_for_status()  # Raise an exception for 4xx/5xx status codes
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"API call failed: {traceback.format_exc()}")

    def __auth__(self):
        payload = {
            "username": os.environ.get('uName'),
            "password": os.environ.get('key')
        }
        response = requests.post(self.baseUrl + self.authUrl, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("idToken")
