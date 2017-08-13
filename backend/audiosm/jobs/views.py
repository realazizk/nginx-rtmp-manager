import hashlib
import os

import av
from flask import Blueprint, jsonify, request
from flask_apispec import marshal_with, use_kwargs
from flask_jwt import current_identity, jwt_required
from werkzeug.utils import secure_filename

from audiosm import settings
from audiosm.exceptions import InvalidUsage
from audiosm.extensions import redis_store
from audiosm.jobs.models import JobModel
from audiosm.jobs.serializers import JobSchema
from audiosm.streams.models import StreamModel
from audiosm.tasks.stream import play_audio_task
from audiosm.utils import MyBuffer, allowed_file


bp = Blueprint('jobs', __name__)


@bp.route('/api/upload', methods=('POST',))
@jwt_required()
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
    return '', 200


@bp.route('/api/job', methods=('POST',))
@jwt_required()
@use_kwargs(JobSchema)
@marshal_with(JobSchema)
def newjob(stream, filename, begin_date):
    stream = StreamModel.query.filter_by(name=stream['name']).first()
    if not stream:
        # BUG here debug the traceback
        raise InvalidUsage.stream_not_found()

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
