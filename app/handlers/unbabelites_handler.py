import logging

from app.services.unbabelites import GetUnbabelitesService, BulkCreateUnbabelitesService
from app.services.opencagedata import GetCoordinatesService
from app.database import drop_tables
from app.models import Unbabelite
from app.finders import UnbabeliteFinder
from app.values.unbabelite import UnbabelitesValue, UnbabelitesGeoJsonValue


log = logging.getLogger(__name__)


class UnbabelitesHandler(object):

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
                address = f"{unbabelite['city']}, {unbabelite['country']}"
                unbabelite = {
                    "employee_id": unbabelite['employeeNumber'],
                    "name": name,
                    "city": unbabelite['city'],
                    "country": unbabelite['country'],
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