"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from flask_script import (Manager,
                          prompt_bool,
                          prompt_pass,
                          prompt,
                          Server,
                          Command,
                          Option)
from injector import app_factory
from extensions import db
from models import UserModel
from settings import devConfig
from os import environ
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
    UserModel.create(username=username, password=password, email=email)


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
    server = Server(host="0.0.0.0", port=5000, use_reloader=True, use_debugger=True)
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
