from audiosm.database import (db, Column, SurrogatePK)
from audiosm.extensions import bcrypt
from flask_jwt import _default_jwt_encode_handler
from sqlalchemy.sql import func


class UserModel(db.Model, SurrogatePK):
    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(100), unique=True, nullable=False)
    password = Column(db.Binary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=func.now())

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
