import logging

from app.services.unbabelites import GetUnbabelitesService, BulkCreateUnbabelitesService
from app.services.opencagedata import GetCoordinatesService
from app.database import drop_tables
from app.models import Unbabelite
from app.finders import UnbabeliteFinder
from app.values.unbabelite import UnbabelitesValue, UnbabelitesGeoJsonValue, UnbabeliteValue


log = logging.getLogger(__name__)


class UnbabelitesHandler(object):

    @staticmethod
    def get_all_per_coordinates():
        unbabelites = UnbabeliteFinder.get_all()

        unbabelites_per_coords = {}
        for unbabelite in unbabelites:
            unbabelite_value = UnbabeliteValue(unbabelite).raw
            if str(unbabelite.coordinates) not in unbabelites_per_coords:
                unbabelites_per_coords[str(unbabelite.coordinates)] = {
                    "coordinates": unbabelite.coordinates,
                    "unbabelites": [unbabelite_value]
                }
            else:
                unbabelites_per_coords[str(unbabelite.coordinates)]['unbabelites'].append(unbabelite_value)

        return unbabelites_per_coords


    @staticmethod
    def get_all():
        unbabelites = UnbabeliteFinder.get_all()

        return UnbabelitesValue(unbabelites)

    @staticmethod
    def geojson_index():
        unbabelites = UnbabeliteFinder.get_all()

        return UnbabelitesGeoJsonValue(unbabelites)

    @staticmethod
    def populate_unbabelites():
        unbabelites_list = []

        unbabelites = GetUnbabelitesService().call()
        for unbabelite in unbabelites['employees']:
            if unbabelite['status'] in ['Active', '']:
                name = f"{unbabelite['firstName']} {unbabelite['lastName']}"
                address = f"{unbabelite['customCityofOrigin']}, {unbabelite['customNationality1']}"
                unbabelite = {
                    "name": name,
                    "city": unbabelite['customCityofOrigin'],
                    "country": unbabelite['customNationality1'],
                }
                
                if UnbabeliteFinder.get_from_name(name):
                    continue

                try:
                    lat, lng = GetCoordinatesService(address).call()
                    unbabelite.update({"lat": lat, "lng": lng})

                except Exception as e:
                    log.info(e)
                    log.info((f"Couldn't get coordinates for {name}: {address}"))
            
                unbabelites_list.append(Unbabelite(**unbabelite))

        BulkCreateUnbabelitesService(unbabelites_list).call()
    
    @staticmethod
    def redo_coordinates():
        unbabelites = UnbabeliteFinder.get_all()

        for unbabelite in unbabelites:
            print(f"Looking at {unbabelite.name}")
            address = f"{unbabelite.city}, {unbabelite.country}"
            lat, lng = GetCoordinatesService(address).call()
            print(f"Got his new coordinates! {lat} - {lng}")
            unbabelite.lat = lat
            unbabelite.lng = lng
            unbabelite.save()
            print("Saved!")
