import requests
import os

from requests.auth import HTTPBasicAuth


class GetUnbabelitesService(object):

    def __init__(self):
        self.api_url = 'https://api.bamboohr.com/api/gateway.php/unbabel/v1/reports/166?format=JSON&fd=yes'
        self.api_key = os.environ.get('BAMBOO_API_KEY')

    def call(self):
        try: 
            response = requests.get(self.api_url,  auth=HTTPBasicAuth(self.api_key, 'whatever'))

            if response.status_code != 200:
                raise ValueError(f"GET unbabelites: wrong status code: {response.status_code}")
        
            return response.json()
        except Exception as e:
            raise ValueError(str(e))
