import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, JSON


db = SQLAlchemy()
db.UUID = UUID(as_uuid=True)
db.JSON = JSON


def create_tables():
    from app.models import Unbabelite
    db.create_all()


def drop_tables():
    db.reflect()
    db.drop_all()
