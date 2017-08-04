from injector import db, bcrypt
import datetime as dt
from flask_jwt import _default_jwt_encode_handler
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from compat import basestring


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

    @property
    def id_token(self):
        return _default_jwt_encode_handler(self).decode('utf-8')


class StreamModel(db.Model, SurrogatePK):
    __tablename__ = 'streams'
    name = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    admin = relationship(UserModel, backref=db.backref('streams'))
    adminid = reference_col('users')
    stype = Column(db.String(80), nullable=False)

    def __init__(self, name, password, **kwargs):
        super().__init__(name=name, password=password, **kwargs)


class JobModel(db.Model):
    __tablename__ = 'jobs'
    id = Column(db.String(80), primary_key=True)
    filename = Column(db.String(100))
    stream = relationship(StreamModel, backref=db.backref('jobs'))
    streamid = reference_col('streams')
    admin = relationship(UserModel, backref=db.backref('jobs'))
    adminid = reference_col('users')

    def __init__(self, streamid, adminid, **kwargs):
        super().__init__(streamid=streamid, adminid=adminid, **kwargs)

    @hybrid_property
    def username(self):
        return self.admin.username
