from app.services.unbabelites import GetUnbabelitesService, BulkCreateUnbabelitesService
from app.database import drop_tables
from app.models import Unbabelite

class UnbabelitesHandler(object):

    @staticmethod
    def populate_unbabelites():
        unbabelites_list = []

        unbabelites = GetUnbabelitesService().call()
        for unbabelite in unbabelites['employees']:
            if unbabelite['status'] == 'Active':
                unbabelite = {
                    "employee_id": unbabelite['id'],
                    "nationality": unbabelite['customNationality'],
                    "city": unbabelite['city'],
                    "country": unbabelite['country']
                }
                unbabelites_list.append(Unbabelite(**unbabelite))

        BulkCreateUnbabelitesService(unbabelites_list).call()