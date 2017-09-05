from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow.exceptions import ValidationError
from audiosm.streams.models import StreamModel
from audiosm.streams.serializers import StreamsSchema, StreamSchema
from flask_jwt import jwt_required, current_identity
from audiosm.exceptions import InvalidUsage


bp = Blueprint('streams', __name__)


@bp.route('/api/stream', methods=('POST',))
@jwt_required()
@use_kwargs(StreamSchema)
@marshal_with(StreamSchema)
def make_stream(name=None, password=None, stype=None):
    if not name or not password or not stype:
        raise ValidationError("Specify name, password and stream type fields")

    if StreamModel.query.filter_by(name=name).first():
        raise ValidationError("Stream already existing")

    stream = StreamModel.create(name=name, password=password,
                                admin=current_identity, stype=stype)
    return stream


@bp.route('/api/streams', methods=('GET',))
@marshal_with(StreamsSchema)
def streams():
    if current_identity:
        user = current_identity
        return user.streams
    else:
        return StreamModel.query.all()


@bp.route('/api/stream/<int:id>', methods=('DELETE',))
@marshal_with(StreamsSchema)
def delete_stream(id):
    stream = StreamModel.get_by_id(id)
    if not stream:
        raise InvalidUsage.stream_not_found()

    result = stream.delete()
    if not result:
        raise InvalidUsage.unkown_error()

    return '', 200
