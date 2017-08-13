from flask import Blueprint, current_app
from flask_apispec import marshal_with, use_kwargs
from marshmallow.exceptions import ValidationError

from audiosm.users.serializers import UserSchema
from audiosm.users.models import UserModel


bp = Blueprint('users', __name__)


@bp.route('/api/login', methods=('POST',))
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def login(username=None, password=None):
    if not username or not password:
        raise ValidationError("Specify username and password fields")
    current_app.logger.info('Username {0} is trying to authenticate'.format(username))
    user = UserModel.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        return user
    return '', 400
