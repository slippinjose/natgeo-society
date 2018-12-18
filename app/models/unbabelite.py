from app.database import db
from app.database.base import ModelMixin


class Unbabelite(ModelMixin, db.Model):
    __tablename__ = 'unbabelite'

    employee_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=True)
    nationality = db.Column(db.String, nullable=True)
    country = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
