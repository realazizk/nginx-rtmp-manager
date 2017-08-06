"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from flask import Flask
from flask_uploads import configure_uploads
from settings import devConfig, Config
from extensions import db, bcrypt, jwt, migrate, cors, celery

###
# Extension stuff
###



###
# Stuff
###

def app_factory(config: Config=devConfig) -> Flask:
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_blueprints(app)
    celery.conf.update(app.config)
    
    return app


def register_extensions(app: Flask):
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app)
    from app import uset
    configure_uploads(app, (uset))


def register_blueprints(app: Flask):
    from app import bp
    # use cors

    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(bp, origins=origins)

    app.register_blueprint(bp)
