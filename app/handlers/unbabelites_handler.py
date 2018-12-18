from app.services.unbabelites import GetUnbabelitesService, BulkCreateUnbabelitesService
from app.database import drop_tables
from app.models import Unbabelite

class UnbabelitesHandler(object):

    @staticmethod
    def populate_unbabelites():
        unbabelites_list = []

        unbabelites = GetUnbabelitesService().call()
        for unbabelite in unbabelites['employees']:
            if unbabelite['status'] in ['Active', '']:
                unbabelite = {
                    "employee_id": unbabelite['employeeNumber'],
                    "name": f"{unbabelite['firstName']} {unbabelite['lastName']}",
                    "city": unbabelite['city'],
                    "country": unbabelite['country']
                }
                unbabelites_list.append(Unbabelite(**unbabelite))

        BulkCreateUnbabelitesService(unbabelites_list).call()
    