from os import environ
from injector import app_factory
from settings import prodConfig, devConfig
from distutils import util
from injector import celery # noqa

isdebug = util.strtobool(environ.get('DEV', None))
app = app_factory(devConfig if isdebug else prodConfig)

app.app_context().push()
