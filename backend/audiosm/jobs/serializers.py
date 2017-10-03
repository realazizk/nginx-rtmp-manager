from marshmallow import fields, Schema, post_load
from audiosm.streams.serializers import StreamSchema
from flask import current_app


class FileSchema(Schema):
    fileduration = fields.Float()
    filehash = fields.Str()


class JobSchema(Schema):
    stream = fields.Nested(StreamSchema, only=('name',), required=True)
    # fields.List(fields.Nested(FileSchema))
    # is broken please see https://github.com/marshmallow-code/marshmallow/issues/483
    files = fields.List(fields.Dict, load_only=True)
    streamstart = fields.DateTime()
    id = fields.Int()
    inf = fields.Bool(default=False)
    taskid = fields.Str(dump_only=True)
    streamfinish = fields.DateTime(required=True)

    @post_load
    def normalize_date(self, data):
        # change date from utc to local server time
        current_app.logger.info(data)
        return data


JobsSchema = JobSchema(many=True)  # noqa
JobSchema = JobSchema()  # noqa
