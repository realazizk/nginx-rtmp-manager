"""
Fast one file code
Copyright Mohamed Aziz knani <medazizknani@gmai.com>

Started on 2017/07/20 01:20
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
import os


###
# The configuration objects
###


class Config:
    SECRET_KEY = os.environ.get('APP_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13


class devConfig(Config):
    """
    The development configuration
    """
    DB_NAME = 'dev.db'
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(DB_PATH)


class prodConfig(Config):
    """
    The production configuration
    """
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'postgresql://localhost/example')


###
# Extension stuff
###

class CRUDMixin(Model):
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the return ecord from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


def jwt_identity(payload):
    user_id = payload['identity']
    return UserModel.get_by_id(user_id)


def authenticate(email, password):
    user = UserModel.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user


db = SQLAlchemy(model_class=CRUDMixin)
bcrypt = Bcrypt()

# doing this workaround on circular imports
# TODO: Make the modules less coupled
from app import UserModel # noqa
jwt = JWT(authentication_handler=authenticate, identity_handler=jwt_identity)


###
# Stuff
###

def app_factory(config: Config=devConfig) -> Flask:
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    bcrypt.init_app(app)

def register_blueprints(app: Flask):
    from app import bp
    app.register_blueprint(bp)
