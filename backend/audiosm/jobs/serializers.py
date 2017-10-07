from marshmallow import fields, Schema, post_load, pre_dump
from audiosm.streams.serializers import StreamSchema
from flask import current_app
from audiosm.jobs.models import JobModel


class FileSchema(Schema):
    fileduration = fields.Float()
    filehash = fields.Str()

    
class ModelFileSchema(Schema):
    filename = fields.Str()
    duration = fields.Float()


class JobSchema(Schema):
    stream = fields.Nested(StreamSchema, only=('name',), required=True)
    mfiles = fields.List(fields.Nested(FileSchema), required=True)
    streamstart = fields.DateTime()
    id = fields.Int()
    inf = fields.Bool(default=False)
    taskid = fields.Str(dump_only=True)
    streamfinish = fields.DateTime(required=True)
    # the duration of all the files
    filesduration = fields.Float(required=True)
    files = fields.List(fields.Nested(ModelFileSchema))

    @post_load
    def normalize_date(self, data):
        # change date from utc to local server time
        current_app.logger.info(data)
        return data


JobsSchema = JobSchema(many=True)  # noqa
JobSchema = JobSchema()  # noqa
