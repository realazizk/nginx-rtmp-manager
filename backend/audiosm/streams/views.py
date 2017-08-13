from flask import Blueprint
from flask_apispec import marshal_with, use_kwargs
from marshmallow.exceptions import ValidationError
from audiosm.streams.models import StreamModel
from audiosm.streams.serializers import StreamsSchema, StreamSchema
from flask_jwt import jwt_required


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
    return StreamModel.query.all()
