import os
import logging
from dotenv import load_dotenv


if os.path.isfile('.env'):
    load_dotenv('.env')

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False

    APP_ENV = os.environ.get("APP_ENV", "development")
    SECRET_KEY = os.environ.get("SECRET_KEY", "somesecret")



    RQ_DEFAULT_URL = RQ_REDIS_URL = os.environ.get('REDIS_URL')
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')

    @classmethod
    def init_app(cls, app):
        pass


class ProductionConfig(BaseConfig):
    DEBUG = False


class StagingConfig(BaseConfig):
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    @classmethod
    def init_app(cls, app):
        super(DevelopmentConfig, cls).init_app(app)
        app.logger.setLevel(logging.DEBUG)


class TestingConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = False
    

config = {
    '_baseconfig': BaseConfig,
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}

__all__ = ['config']