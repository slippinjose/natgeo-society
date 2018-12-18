from app.database import db


class BulkCreateUnbabelitesService(object):

    def __init__(self, unbabelites):
        self.unbabelites = unbabelites
    
    def call(self):
        db.session.bulk_save_objects(self.unbabelites)
        db.session.commit()
