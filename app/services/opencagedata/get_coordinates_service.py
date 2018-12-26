import requests
import os


class GetCoordinatesService(object):

    def __init__(self, address):
        self.api_url = (f"https://api.opencagedata.com/geocode/v1/json?q={address}"
                        f"&key={os.environ.get('GEOCODE_API_KEY')}")

    def call(self):
        try:
            response = requests.get(self.api_url)
            if not response.json()['results']:
                import code; code.interact(local=dict(globals(), **locals()))

            coordinates = response.json()['results'][0]['geometry']

            return coordinates['lat'], coordinates['lng']
        except Exception as e:
            raise ValueError(e)
