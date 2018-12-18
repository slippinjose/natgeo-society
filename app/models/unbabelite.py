from app.database import db
from app.database.base import ModelMixin


class Unbabelite(ModelMixin, db.Model):
    __tablename__ = 'unbabelite'

    employee_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)

    @property
    def coordinates(self):
        return [self.lat, self.lng]