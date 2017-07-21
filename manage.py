from flask_script import Manager, prompt_bool, prompt_pass, prompt
from injector import (app_factory, devConfig, db, prodConfig, UserModel)
from os import environ


app = app_factory(devConfig if bool(environ.get('DEV', None)) else prodConfig)
manager = Manager(app)


@manager.command
def drop():
    if prompt_bool("Are you sure you want to lose all your data"):
        db.drop_all()


@manager.command
def makesuperuser():
    username = prompt('Enter username')
    email = prompt('Enter email')
    password = prompt_pass('Enter password')
    user = UserModel.create(username=username, password=password, email=email)
    user.save()


@manager.command
def create():
    "Creates database tables from sqlalchemy models"
    db.create_all()


if __name__ == "__main__":
    manager.run()
