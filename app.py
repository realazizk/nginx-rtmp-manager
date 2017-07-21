from flask import Blueprint
from marshmallow import Schema, fields
from flask_apispec import use_kwargs, marshal_with
from injector import db # noqa

bp = Blueprint(__name__.split('.')[0], import_name='app')


###
# Serializes
###

class UserSchema(Schema):
    username = fields.Str()
    password = fields.Str()
    email = fields.Email()

@use_kwargs(UserSchema)
@marshal_with(UserSchema)
def login(username, password, **kwargs):
    pass
