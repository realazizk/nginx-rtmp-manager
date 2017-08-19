"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

import functools
import os
from distutils import util
from os import environ

import flask
from flask import current_app
from flask_migrate import MigrateCommand
from flask_script import Command, Manager, Option, Server, prompt, prompt_pass
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import MethodNotAllowed, NotFound

from audiosm import app_factory
from audiosm.extensions import db
from audiosm.settings import devConfig, prodConfig
from audiosm.users.models import RoleModel, UserModel


isdebug = util.strtobool(environ.get('DEV', None))
app = app_factory(devConfig if isdebug else prodConfig)
manager = Manager(app)


@manager.command
def makesuperuser():
    # make admin role if it doesn't exist
    try:
        role = RoleModel.create(name='admin')
    except IntegrityError:
        db.session.rollback()
        role = RoleModel.query.filter_by(name='admin').first()
    username = prompt('Enter username')
    email = prompt('Enter email')
    password = prompt_pass('Enter password')
    user = UserModel.create(username=username, password=password,
                            email=email, active=True)
    user.add_role(role)
    user.save()


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')


def with_appcontext(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        with app.app_context():
            return f(*args, **kwargs)
    return wrapper


@manager.command
def test():
    """Run the tests."""
    import pytest
    rv = pytest.main([TEST_PATH, '--verbose', '--disable-pytest-warnings'])
    exit(rv)


@manager.command
@manager.option('-u', '--url', help='Url to test (ex. /static/image.png)')
@manager.option('-o', '--order',
                help='Property on Rule to order by (default: rule)')
@with_appcontext
def urls(url=None, order='rule'):
    rows = []
    column_length = 0
    column_headers = ('Rule', 'Endpoint', 'Arguments')

    if url:
        try:
            rule, arguments = (
                current_app.url_map.bind('localhost')
                .match(url, return_rule=True))
            rows.append((rule.rule, rule.endpoint, arguments))
            column_length = 3
        except (NotFound, MethodNotAllowed) as e:
            rows.append(('<{}>'.format(e), None, None))
            column_length = 1
    else:
        rules = sorted(
            current_app.url_map.iter_rules(),
            key=lambda rule: getattr(rule, order))
        for rule in rules:
            rows.append((rule.rule, rule.endpoint, None))
        column_length = 2

    str_template = ''
    table_width = 0

    if column_length >= 1:
        max_rule_length = max(len(r[0]) for r in rows)
        max_rule_length = max_rule_length if max_rule_length > 4 else 4
        str_template += '{:' + str(max_rule_length) + '}'
        table_width += max_rule_length

    if column_length >= 2:
        max_endpoint_length = max(len(str(r[1])) for r in rows)
        # max_endpoint_length = max(rows, key=len)
        max_endpoint_length = (
            max_endpoint_length if max_endpoint_length > 8 else 8)
        str_template += '  {:' + str(max_endpoint_length) + '}'
        table_width += 2 + max_endpoint_length

    if column_length >= 3:
        max_arguments_length = max(len(str(r[2])) for r in rows)
        max_arguments_length = (
            max_arguments_length if max_arguments_length > 9 else 9)
        str_template += '  {:' + str(max_arguments_length) + '}'
        table_width += 2 + max_arguments_length

    print(str_template.format(*column_headers[:column_length]))
    print('-' * table_width)

    for row in rows:
        print(str_template.format(*row[:column_length]))


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
