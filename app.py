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
from models import (UserModel, JobModel, StreamModel)
from tasks.stream import play_audio_task
from serializers import StreamsSchema, JobSchema, UserSchema, StreamSchema
from werkzeug.utils import secure_filename
from utils import (allowed_file, MyBuffer)
import settings
import os
import av
import hashlib
from extensions import redis_store
from exceptions import InvalidUsage


bp = Blueprint(__name__.split('.')[0], import_name='app')


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


@bp.route('/api/upload', methods=('POST',))
@jwt_required()
@errorize
def fileupload():
    file = request.files['file_data']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pth = os.path.join(settings.Config.UPLOAD_FOLDER, filename)
        f = MyBuffer(file.read())
        f.save(pth)
        m = hashlib.md5()
        m.update(f.getvalue())
        hashid = m.hexdigest()
        redis_store.set(hashid, pth)
        container = av.open(pth)
        return jsonify(dict(uploaded='OK',
                            duration=container.duration / av.time_base,
                            hashid=hashid))
    return jsonify(dict(uploaded='ERROR'))


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
def newjob(stream, filename, begin_date):
    stream = StreamModel.query.filter_by(name=stream['name']).first()
    if not stream:
        # BUG here debug the traceback
        raise ValidationError('Submit a valid stream faggot')
    fpth = redis_store.get(filename)
    if not fpth:
        raise InvalidUsage.file_not_found()
    job = JobModel.create(streamid=stream.id,
                          adminid=current_identity.id, filename=fpth)
    instancejs = JobSchema()
    result = instancejs.dump(job)
    play_audio_task.apply_async(
        kwargs=result.data, countdown=10, serializers="json")
    return job
