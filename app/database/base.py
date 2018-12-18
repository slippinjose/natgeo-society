import logging
import uuid
from datetime import datetime
from flask_sqlalchemy import event, SessionBase

from app.database import db


logger = logging.getLogger(__name__)


class ModelMixin(object):
    id = db.Column(db.UUID, default=uuid.uuid1, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def reload(self):
        db.session.refresh(self)

    def save(self):
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            logger.exception(e)
            db.session.rollback()
        return None

    def update(self, **kwargs):
        try:
            for k, v in kwargs.items():
                if not hasattr(self, k):
                    continue
                setattr(self, k, v)
            db.session.commit()
        except Exception as e:
            logger.exception(e)
            db.session.rollback()


@event.listens_for(SessionBase, "before_flush")
def before_flush_handler(session, _flush_context, _instances):
    for obj in session.dirty:
        obj.updated_at = datetime.utcnow()