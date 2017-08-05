"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from flask import (Blueprint, jsonify, request)
from marshmallow.exceptions import ValidationError
from flask_apispec import use_kwargs, marshal_with
from functools import wraps
import logging
from flask_jwt import (current_identity,
                       jwt_required)
from flask_uploads import UploadSet, AUDIO
from tasks.stream import play_task
from models import (JobModel, StreamModel, UserModel)
from serializers import StreamsSchema, JobSchema, UserSchema, StreamSchema


bp = Blueprint(__name__.split('.')[0], import_name='app')


uset = UploadSet('files', AUDIO)


###
# Logging
###

log = logging.getLogger('werkzeug')
log.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)


###
# Wrappers
###

def errorize(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except ValidationError as e:
            return jsonify({'errors': e.messages}), 400
        return result

    return wrapper


###
# Views
###

@bp.route('/api/login', methods=('POST',))
@use_kwargs(UserSchema)
@marshal_with(UserSchema)
@errorize
def login(username=None, password=None):
    if not username or not password:
        raise ValidationError("Specify username and password fields")
    log.info('Username {0} is trying to authenticate'.format(username))
    user = UserModel.query.filter_by(username=username).first()
    print(user)
    if user is not None and user.check_password(password):
        return user
    return '', 400


@bp.route('/api/stream', methods=('POST',))
@jwt_required()
@use_kwargs(StreamSchema)
@marshal_with(StreamSchema)
@errorize
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


@bp.route('/api/uploadfile/<jobid>', methods=('POST',))
def fileupload(jobid):
    # mfile = uset.save(request.files['file'])
    pass
    # update job with file
    

@bp.route('/auth', methods=('GET',))
def authorize():
    log.info('Got an authentication request')
    log.info(request.args)

    return '', 200


@bp.route('/api/job', methods=('POST',))
@jwt_required()
@use_kwargs(JobSchema)
@marshal_with(JobSchema)
@errorize
def newjob(stream):
    stream = StreamModel.query.filter_by(name=stream).first()
    if not stream:
        raise ValidationError('Submit a valid stream faggot')
    job = JobModel(streamid=stream.id, adminid=current_identity.id)
    task = play_task.apply_async(job, countdown=10)
    return job
