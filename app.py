from flask import (Blueprint, jsonify, request)
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from flask_apispec import use_kwargs, marshal_with
from injector import db, bcrypt
import datetime as dt
from functools import wraps
from six import PY2
import logging
from sqlalchemy.orm import relationship
from flask_jwt import (_default_jwt_encode_handler,
                       current_identity,
                       jwt_required)
import marshmallow


bp = Blueprint(__name__.split('.')[0], import_name='app')


###
# Compatibility (though code is compatible only with PY3K)
###

if PY2:
    text_type = unicode  # noqa
    binary_type = str
    string_types = (str, unicode)  # noqa
    unicode = unicode  # noqa
    basestring = basestring  # noqa
else:
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)


###
# Extensions
###

class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` \
        to any declarative-mapped class.
    """

    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
                (isinstance(record_id, basestring) and record_id.isdigit(),
                 isinstance(record_id, (int, float))),
        ):
            return cls.query.get(int(record_id))


def reference_col(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey('{0}.{1}'.format(tablename, pk_name)),
        nullable=nullable, **kwargs)


Column = db.Column

###
# Logging
###

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


###
# Models
###

class UserModel(db.Model, SurrogatePK):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=dt.datetime.utcnow)

    def __init__(self, username, email, password=None, **kwargs):
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def set_password(self, value):
        self.password = bcrypt.generate_password_hash(value)

    @property
    def id_token(self):
        return _default_jwt_encode_handler(self).decode('utf-8')


class StreamModel(db.Model, SurrogatePK):
    __tablename__ = 'streams'
    name = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    admin = relationship(UserModel, backref=db.backref('streams'))
    adminid = reference_col('users')

    def __init__(self, name, password, **kwargs):
        super().__init__(name=name, password=password, **kwargs)


###
# Serializes
###


def ensure_binary_type(val):
    if isinstance(val, marshmallow.compat.text_type):
        val = val.encode('utf-8')
    return marshmallow.compat.binary_type(val)


class RosString(marshmallow.fields.Field):
    """A ros string, serializing as ros python field type :
    Python <3.0 implies str, python >3.0 implies bytes

    If you need unicode serialization, have a look at RosTextString.

    No marshmallow field class for this, so we're declaring it here.

    :param kwargs: The same keyword arguments that :class:`Field` receives. required is set to True by default.
    """
    default_error_messages = {
        'invalid': 'Not a valid binary string.'
    }

    def __init__(self, **kwargs):
        super(RosString, self).__init__(**kwargs)

    def _serialize(self, value, attr, obj):
        if value is None:
            return None
        return ensure_binary_type(value)

    def _deserialize(self, value, attr, data):
        if not isinstance(value, marshmallow.compat.basestring):
            self.fail('invalid')
        return ensure_binary_type(value)


class UserSchema(Schema):
    username = RosString(required=True)
    password = RosString(required=True, load_only=True)
    id_token = RosString(dump_only=True)


class StreamSchema(Schema):
    name = RosString(required=True)
    password = RosString(required=True)


StreamsSchema = StreamSchema(many=True)


###
# Wrappers
###

def errorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ValidationError as e:
            return jsonify({'errors': e.messages})
        return result

    return wrapper


###
# Views
###

@bp.route('/api/login', methods=('POST',))
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@errorize
def login(username=None, password=None):
    if not username or not password:
        raise ValidationError("Specify username and password fields")
    log.info('Username {0} is trying to authenticate'.format(username))
    user = UserModel.query.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        return user
    return '', 400


@bp.route('/api/stream', methods=('POST',))
@jwt_required()
@use_kwargs(StreamSchema)
@marshal_with(StreamSchema)
@errorize
def make_stream(name=None, password=None):
    if not name or not password:
        raise ValidationError("Specify name and password fields")

    if StreamModel.query.filter_by(name=name).first():
        raise ValidationError("Stream already exisiting")

    stream = StreamModel.create(name=name, password=password,
                                admin=current_identity)
    return stream


@bp.route('/auth', methods=('GET',))
def authorize():
    log.info('Got an authentication request')
    log.info(request.args)

    return '', 200
