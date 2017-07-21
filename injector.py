"""
Fast one file code
Copyright Mohamed Aziz knani <medazizknani@gmai.com>

Started on 2017/07/20 01:20
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
import os


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


db = SQLAlchemy(model_class=CRUDMixin)


###
# The configuration objects
###

class Config:
    SECRET_KEY = os.environ.get('APP_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))


class devConfig(Config):
    """
    The development configuration
    """


class prodConfig(Config):
    """
    The production configuration
    """

###
# Stuff
###

def app_factory(config: Config=devConfig) -> Flask:
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)


def register_blueprints(app: Flask):
    from app import bp
    app.register_blueprint(bp)
