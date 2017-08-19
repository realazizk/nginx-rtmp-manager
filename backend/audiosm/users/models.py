from audiosm.database import (db, Column, SurrogatePK)
from audiosm.extensions import bcrypt
from flask_jwt import _default_jwt_encode_handler
from sqlalchemy.sql import func
from audiosm.compat import PY2, string_types, text_type


class UserMixin(object):
    '''
    This provides default implementations for the methods that Flask-Login
    expects user objects to have.
    '''

    if not PY2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

    @property
    def is_anonymous(self):
        return False

    @property
    def is_active(self):
        """Returns `True` if the user is active."""
        return self.active

    def has_role(self, role):
        """Returns `True` if the user identifies with the specified role.
        :param role: A role name or `Role` instance"""
        if isinstance(role, string_types):
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    def get_security_payload(self):
        """Serialize user object as response payload."""
        return {'id': str(self.id)}

    def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


roles_users = db.Table('rolesusers',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('role.id')),
                       db.PrimaryKeyConstraint('user_id', 'role_id'))


class UserModel(db.Model, SurrogatePK, UserMixin):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=func.now())
    active = db.Column(db.Boolean(), default=False)
    roles = db.relationship('RoleModel', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


    def __init__(self, username, email, password=None, *args, **kwargs):
        super().__init__(username=username, email=email, *args, **kwargs)
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

    def add_role(self, role):
        self.roles.append(role)

    def has_role(self, role):
        if isinstance(role, string_types):
            return role in (role.name for role in self.roles)
        else:
            return role in self.roles

    def __repr__(self):
        return self.username


class RoleMixin(object):
    """Mixin for `Role` model definitions"""

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name


class RoleModel(db.Model, SurrogatePK, RoleMixin):
    __tablename__ = 'role'
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255))
