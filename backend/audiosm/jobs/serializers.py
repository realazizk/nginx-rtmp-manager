from marshmallow import fields, Schema
from audiosm.streams.serializers import StreamSchema


class JobSchema(Schema):
    stream = fields.Nested(StreamSchema, only='name', required=True)
    filename = fields.Str()
    begin_date = fields.DateTime()
    id = fields.Int()
    inf = fields.Bool(default=False)

JobSchema = JobSchema()  # noqa
