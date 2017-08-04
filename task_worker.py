from os import environ
from injector import (app_factory, devConfig, prodConfig)
from distutils import util
from injector import celery # noqa

isdebug = util.strtobool(environ.get('DEV', None))
app = app_factory(devConfig if isdebug else prodConfig)

app.app_context().push()
