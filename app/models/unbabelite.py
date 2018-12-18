from app.database import db
from app.database.base import ModelMixin


class Unbabelite(ModelMixin, db.Model):
    __tablename__ = 'unbabelite'

    name = db.Column(db.String, nullable=False)
    nationality = db.Column(db.Float, nullable=True)
    country = db.Column(db.Float, nullable=True)
    city = db.Column(db.Float, nullable=True)
