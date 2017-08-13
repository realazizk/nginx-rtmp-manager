from os import environ
from audiosm import app_factory
from audiosm.settings import prodConfig, devConfig
from distutils import util
from audiosm.extensions import celery # noqa

isdebug = util.strtobool(environ.get('DEV', None))
app = app_factory(devConfig if isdebug else prodConfig)

app.app_context().push()
