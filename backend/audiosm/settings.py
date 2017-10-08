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
    CELERY_IMPORTS = ['audiosm.tasks.stream']
    UPLOAD_FOLDER = '/tmp'
    STREAM_HOST = 'localhost'
    DEBUG = False


class devConfig(Config):
    """
    The development configuration
    """
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)
    JWT_EXPIRATION_DELTA = timedelta(10**6)  # for easier testing
    DEBUG = True
    NAME = 'DEV'


class prodConfig(Config):
    """
    The production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/example')
    # FIXME: bad solution
    # should only be used for remember me
    JWT_EXPIRATION_DELTA = timedelta(10**6)
    NAME = 'PROD'


class testConfig(Config):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"
    BCRYPT_LOG_ROUNDS = 4
    NAME = 'TEST'
