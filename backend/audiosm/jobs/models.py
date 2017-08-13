from audiosm.database import (db, Column, SurrogatePK, reference_col)
from audiosm.users.models import UserModel
from audiosm.streams.models import StreamModel
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class JobModel(db.Model, SurrogatePK):
    __tablename__ = 'jobs'
    filename = Column(db.String(100))
    stream = relationship(StreamModel, backref=db.backref('jobs'))
    streamid = reference_col('streams')
    admin = relationship(UserModel, backref=db.backref('jobs'))
    adminid = reference_col('users')
    done = Column(db.Boolean, default=False)
    streamstart = Column(db.DateTime, nullable=False, default=func.now())

    def __init__(self, streamid, adminid, **kwargs):
        super().__init__(streamid=streamid, adminid=adminid, **kwargs)

    @hybrid_property
    def username(self):
        return self.admin.username
