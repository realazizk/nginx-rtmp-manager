from marshmallow import fields, Schema
from audiosm.streams.serializers import StreamSchema


class JobSchema(Schema):
    stream = fields.Nested(StreamSchema, only='name', required=True)
    filename = fields.Str()
    begin_date = fields.DateTime()
    id = fields.Str(load_only=True)

JobSchema = JobSchema(strict=True)  # noqa
