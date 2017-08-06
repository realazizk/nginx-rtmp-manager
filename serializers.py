from marshmallow import Schema, fields, validates
from marshmallow.exceptions import ValidationError
from marshmallow.validate import OneOf
from models import StreamModel


###
# Serializes
###


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    id_token = fields.Str(dump_only=True)


class StreamSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    stype = fields.Str(required=True, validate=OneOf(['video', 'audio']))


class JobSchema(Schema):
    stream = fields.Nested(StreamSchema, only='name', required=True)
    filename = fields.Str()
    id = fields.Str(load_only=True)

    @validates('stream')
    def validate_stream(self, stream):
        if not StreamModel.query.filter_by(name=stream):
            raise ValidationError('Pass a valid stream name')


StreamsSchema = StreamSchema(many=True)
