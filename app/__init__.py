import logging

from flask import Flask, render_template

from app.views import home_bp
from app.database import db
from config import config

log = logging.getLogger(__name__)


def create_app(config_name=None):
    env_config = config[config_name]

    app = Flask(__name__)
    app.config.from_object(env_config)
    env_config.init_app(app)

    db.init_app(app)

    app.register_blueprint(home_bp)

    return app
