from flask import (Blueprint, jsonify)
from marshmallow import Schema, fields
from marshmallow.exceptions import ValidationError
from flask_apispec import use_kwargs, marshal_with
from injector import db, bcrypt
import datetime as dt
from functools import wraps
from six import PY2

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



###
# Serializes
###

class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

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


@bp.route('/api/user', methods=('POST',))
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@errorize
def login(username=None, password=None):
    if not username or not password:
        raise ValidationError("Specify username and password fields")

    user = UserModel.filter_by(username=username).first()
    if user is not None and user.check_password(password):
        return ('', 200)
