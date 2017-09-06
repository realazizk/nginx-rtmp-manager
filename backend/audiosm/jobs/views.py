import hashlib
import os

import av
from flask import Blueprint, jsonify, request, current_app
from flask_apispec import marshal_with, use_kwargs
from flask_jwt import current_identity, jwt_required

from audiosm import settings
from audiosm.exceptions import InvalidUsage
from audiosm.extensions import redis_store
from audiosm.jobs.models import JobModel
from audiosm.jobs.serializers import JobSchema, JobsSchema
from audiosm.streams.models import StreamModel
from audiosm.tasks.stream import play_audio_task
from audiosm.utils import MyBuffer, allowed_file
from datetime import datetime as dt
from audiosm.extensions import celery


bp = Blueprint('jobs', __name__)


@bp.route('/api/upload', methods=('POST',))
@jwt_required()
def fileupload():
    file = request.files['file_data']
    if file and allowed_file(file.filename):
        f = MyBuffer(file.read())
        m = hashlib.sha256()
        m.update(f.getvalue())
        hashid = m.hexdigest()
        pth = os.path.join(settings.Config.UPLOAD_FOLDER, hashid)
        f.save(pth)
        redis_store.set(hashid, pth)
        container = av.open(pth)
        return jsonify(dict(uploaded='OK',
                            duration=container.duration / av.time_base,
                            hashid=hashid))
    return jsonify(dict(uploaded='ERROR'))


@bp.route('/auth', methods=('GET',))
def authorize():
    if (request.args['addr'] == '127.0.0.1'):
        return '', 200
    # check if the idhash is right
    streamname = request.args.get('name')
    idhash = request.args.get('swfurl').split("?")[-1]
    stream = StreamModel.query.filter_by(name=streamname,
                                         password=idhash).first()
    if not stream:
        return '', 400
    return '', 200


@bp.route('/api/jobs', methods=('GET',))
@jwt_required()
@marshal_with(JobsSchema)
def getjobs():
    user = current_identity
    if user.jobs:
        return user.jobs
    return []


@bp.route('/api/job', methods=('POST',))
@jwt_required()
@use_kwargs(JobSchema)
@marshal_with(JobSchema)
def newjob(stream, filename, streamstart, inf, **kwargs):
    stream = StreamModel.query.filter_by(name=stream['name']).first()
    if not stream:
        # BUG here debug the traceback
        raise InvalidUsage.stream_not_found()

    fpth = redis_store.get(filename)
    if not fpth:
        raise InvalidUsage.file_not_found()
    fpth = fpth.decode('utf-8')

    job = JobModel.create(streamid=stream.id,
                          adminid=current_identity.id, filename=fpth, inf=inf,
                          streamstart=streamstart, **kwargs)

    instancejs = JobSchema
    result = instancejs.dump(job)
    current_app.logger.info(result.data)
    if job.streamstart > dt.now():
        task = play_audio_task.apply_async(
            kwargs=result.data, eta=job.streamstart, serializers="json")
    else:
        task = play_audio_task.apply_async(kwargs=result.data,
                                           serializers="json")
    job.taskid = task.id
    return job.save()


@bp.route('/api/job/<int:id>', methods=('DELETE',))
@jwt_required()
@use_kwargs(JobSchema)
@marshal_with(JobSchema)
def deletejob(id):
    job = JobModel.get_by_id(id)
    if job is None:
        raise InvalidUsage.job_not_found()
    # terminate the job
    celery.control.revoke(job.taskid, terminate=True, signal='SIGKILL')
    job.delete()
    return '', 200
