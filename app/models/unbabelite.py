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
    photo = db.Column(db.String, nullable=True)
    team = db.Column(db.String, nullable=True)
    position = db.Column(db.String, nullable=True)

    @property
    def coordinates(self):
        return {'lat': self.lat, 'lng': self.lng}
