from audiosm.extensions import celery
from ffmpy import FFmpeg, FFRuntimeError
from audiosm import settings
from audiosm.extensions import DatabaseTask
from audiosm.jobs.models import JobModel
import subprocess
# from celery.utils.log import get_task_logger

# logger = get_task_logger(__name__)


###
# Stream tasks
###


@celery.task(ignore_result=True, base=DatabaseTask, bind=True)
def play_audio_task(self, id, files, stream, inf, *a, **kw):
    problem = None

    while True:
        for eachfile in files:
            f = FFmpeg(
                inputs={
                    eachfile['filename']: ['-re']
                },
                outputs={
                    'rtmp://{host}:1935/stream/{stream}'.format(
                        stream=stream['name'],
                        host=settings.Config.STREAM_HOST
                    ): ['-vn', '-c:a', 'aac', '-strict',  '-2', '-f', 'flv']
                }
            )
            print('start')
            print("FFmpeg command", f.cmd)
            print("Running Command")
            try:
                f.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FFRuntimeError as e:
                problem = e
                continue
        if not inf:
            break

    if problem:
        print("An error has occured when running job")
        print(problem)
    job = self.db.session.query(JobModel).filter_by(id=id).first()
    print("Finish running Command")
    if job:
        print("Deleting job", job)
        job.delete()
    else:
        print("Something wrong has occured")
