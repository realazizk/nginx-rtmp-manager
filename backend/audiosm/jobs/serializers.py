from marshmallow import fields, Schema
from audiosm.streams.serializers import StreamSchema


class JobSchema(Schema):
    stream = fields.Nested(StreamSchema, only=('name',), required=True)
    filename = fields.Str()
    streamstart = fields.DateTime()
    id = fields.Int()
    inf = fields.Bool(default=False)
    taskid = fields.Str(dump_only=True)
    streamfinish = fields.DateTime()

JobsSchema = JobSchema(many=True)  # noqa
JobSchema = JobSchema()  # noqa
