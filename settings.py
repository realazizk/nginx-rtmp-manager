"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

import os
from datetime import timedelta


###
# The configuration objects
###


class Config:
    SECRET_KEY = os.environ.get('APP_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    JWT_AUTH_USERNAME_KEY = 'username'
    JWT_AUTH_HEADER_PREFIX = 'Token'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379'
    CELERY_BROKER_URL = 'redis://localhost:6379'
    REDIS_URL = 'redis://localhost:6379/0'
    CELERY_IMPORTS = ['tasks.stream']
    UPLOAD_FOLDER = '/tmp'
    STREAM_HOST = 'localhost'


class devConfig(Config):
    """
    The development configuration
    """
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(os.path.expanduser('~'), DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    JWT_EXPIRATION_DELTA = timedelta(10**6)  # for easier testing


class prodConfig(Config):
    """
    The production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/example')
