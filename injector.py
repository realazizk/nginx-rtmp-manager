"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from flask import Flask
from settings import devConfig, Config
from extensions import (db, bcrypt, jwt, migrate, cors, celery, redis_store)
from exceptions import InvalidUsage
import logging


def app_factory(config: Config=devConfig) -> Flask:
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)
    app.url_map.strict_slashes = False
    register_extensions(app)
    register_blueprints(app)
    celery.conf.update(app.config)

    file_handler = logging.FileHandler('log.0')
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    loggers = [app.logger, logging.getLogger('sqlalchemy'),
               logging.getLogger('werkzeug')]

    for logger in loggers:
        logger.addHandler(file_handler)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        app.logger.error(error)
        response = error.to_json()
        response.status_code = error.status_code
        return response

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app)
    redis_store.init_app(app)


def register_blueprints(app: Flask):
    from app import bp
    # use cors
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(bp, origins=origins)

    app.register_blueprint(bp)
