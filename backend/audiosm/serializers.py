"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from marshmallow import Schema, fields
from marshmallow.validate import OneOf


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
    begin_date = fields.DateTime()
    id = fields.Str(load_only=True)


StreamsSchema = StreamSchema(many=True)
