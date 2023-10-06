import os
import datetime

class Default(object):
    DEBUG = False
    TESTING = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=60)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')
