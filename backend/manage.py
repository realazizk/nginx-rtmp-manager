"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from flask_script import (Manager,
                          prompt_pass,
                          prompt,
                          Server,
                          Command,
                          Option)
from audiosm import app_factory
from audiosm.users.models import UserModel
from audiosm.settings import devConfig, prodConfig
from os import environ
import os
from distutils import util
import flask
from flask_migrate import MigrateCommand


isdebug = util.strtobool(environ.get('DEV', None))
app = app_factory(devConfig if isdebug else prodConfig)
manager = Manager(app)


@manager.command
def makesuperuser():
    username = prompt('Enter username')
    email = prompt('Enter email')
    password = prompt_pass('Enter password')
    UserModel.create(username=username, password=password,
                     email=email, active=True)


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


@manager.command
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose', '--disable-pytest-warnings'])
    exit(rv)


class GunicornServer(Command):

    description = 'Run the app within Gunicorn'

    def __init__(self, host='0.0.0.0', port=5000, workers=4):
        self.port = port
        self.host = host
        self.workers = workers

    def get_options(self):
        return (
            Option('-H', '--host',
                   dest='host',
                   default=self.host),

            Option('-p', '--port',
                   dest='port',
                   type=int,
                   default=self.port),

            Option('-w', '--workers',
                   dest='workers',
                   type=int,
                   default=self.workers),
        )

    def __call__(self, app, host, port, workers):

        from gunicorn import version_info

        if version_info < (0, 9, 0):
            from gunicorn.arbiter import Arbiter
            from gunicorn.config import Config
            arbiter = Arbiter(Config({'bind': "%s:%d" % (host, int(port)), 'workers': workers}), app)
            arbiter.run()
        else:
            from gunicorn.app.base import Application

            class FlaskApplication(Application):
                def init(self, parser, opts, args):
                    return {
                        'bind': '{0}:{1}'.format(host, port),
                        'workers': workers
                    }

                def load(self):
                    return app

            FlaskApplication().run()


if isdebug:
    server = Server(host="0.0.0.0", port=8090, use_reloader=True)
else:
    server = GunicornServer()

manager.add_command("runserver", server)
manager.add_command('db', MigrateCommand)


def drop_into_pdb(app, exception):
    import sys
    import pdb
    import traceback
    traceback.print_exc()
    pdb.post_mortem(sys.exc_info()[2])


flask.got_request_exception.connect(drop_into_pdb)

if __name__ == "__main__":
    manager.run()
