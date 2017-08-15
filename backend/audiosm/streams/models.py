from audiosm.database import (db, Column, SurrogatePK, reference_col)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from audiosm.users.models import UserModel


class StreamModel(db.Model, SurrogatePK):
    __tablename__ = 'streams'
    name = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    admin = relationship(UserModel, backref=db.backref('streams'))
    adminid = reference_col('users')
    stype = Column(db.String(80), nullable=False)
    created_at = Column(db.DateTime, default=func.now())

    def __init__(self, name, password, **kwargs):
        super().__init__(name=name, password=password, **kwargs)

    def __repr__(self):
        return self.name
