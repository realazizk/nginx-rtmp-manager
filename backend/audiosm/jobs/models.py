from audiosm.database import (db, Column, SurrogatePK, reference_col)
from audiosm.users.models import UserModel
from audiosm.streams.models import StreamModel
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class JobModel(db.Model, SurrogatePK):
    __tablename__ = 'jobs'

    stream = relationship(StreamModel, backref=db.backref('jobs'))
    streamid = reference_col('streams')
    admin = relationship(UserModel, backref=db.backref('jobs'),
                         lazy='subquery')
    adminid = reference_col('users')
    done = Column(db.Boolean, default=False)
    streamstart = Column(db.DateTime, nullable=False, default=func.now())
    inf = Column(db.Boolean, nullable=False, default=False)
    taskid = Column(db.String(100))
    streamfinish = Column(db.DateTime, nullable=True)
    files = relationship('FileModel', backref=db.backref('job'), cascade="all, delete-orphan")

    def __init__(self, streamid=None, adminid=None, **kwargs):
        super().__init__(streamid=streamid, adminid=adminid, **kwargs)

    @hybrid_property
    def username(self):
        return self.admin.username

    def add_file(self, filename, duration):
        FileModel.create(filename=filename, jobid=self.id, duration=duration)


class FileModel(db.Model, SurrogatePK):
    __tablename__ = 'files'

    filename = Column(db.String(300))
    jobid = reference_col('jobs')
    duration = Column(db.Float())

    def __init__(self, filename=None, **kwargs):
        "docstring"
        super().__init__(filename=filename, **kwargs)
