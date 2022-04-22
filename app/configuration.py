import os
import datetime
import secrets


class MainConfig:
    JSON_SORT_KEYS = False
    THREADED = False
    SECRET_KEY = secrets.token_hex(16)
    JWT_SECRET_KEY = secrets.token_hex(16)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=30)


class ProductionConfiguration(MainConfig):
    FLASK_ENV = 'production'
    MONGO_URI = os.environ.get('MONGO_URI')
    DEBUG = False
    TESTING = False


class DevelopmentConfiguration(MainConfig):
    FLASK_ENV = 'development'
    MONGO_URI = 'mongodb://localhost:27017/flask'
    TESTING = True
    DEBUG = True
