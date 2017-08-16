from marshmallow import Schema, fields


class UserSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    id_token = fields.Str(dump_only=True)

UserSchema = UserSchema(strict=True)  # noqa
