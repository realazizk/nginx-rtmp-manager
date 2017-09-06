"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

import logging

from flask import Flask, jsonify, _request_ctx_stack
from flask_jwt import _jwt
import jwt as bjwt


from audiosm.exceptions import InvalidUsage
from audiosm.extensions import (bcrypt, celery, cors, db, jwt, migrate,
                                redis_store, admin_ob)
from audiosm.settings import devConfig, Config


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

    @app.errorhandler(422)
    def handle_unprocessable_entity(err):
        # webargs attaches additional metadata to the `data` attribute
        exc = getattr(err, 'exc')
        if config.DEBUG:
            app.logger.warning(exc)
        if exc:
            # Get validations from the ValidationError object
            messages = exc.messages
        else:
            messages = ['Invalid request']
        return jsonify({
            'messages': messages,
        }), 422
    
    # visit http://aziz.tn/technical-blog/flask-jwt-optional.html
    # to know why I do this
    @app.before_request
    def push_to_ctx():
        token = _jwt.request_callback()
        try:
            payload = _jwt.jwt_decode_callback(token)
        except bjwt.exceptions.DecodeError:
            pass
        else:
            _request_ctx_stack.top.current_identity = _jwt.identity_callback(payload)

    # FIXME: ugly hack
    import audiosm.admin        # noqa

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app)
    redis_store.init_app(app)
    admin_ob.init_app(app)


def register_blueprints(app: Flask):
    from audiosm.users.views import bp as ubp
    from audiosm.jobs.views import bp as jbp
    from audiosm.streams.views import bp as sbp

    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(ubp, origins=origins)
    cors.init_app(sbp, origins=origins)
    cors.init_app(jbp, origins=origins)

    app.register_blueprint(ubp)
    app.register_blueprint(sbp)
    app.register_blueprint(jbp)
