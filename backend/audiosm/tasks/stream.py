from audiosm.extensions import celery
from ffmpy import FFmpeg
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
def play_audio_task(self, id, filename, stream, inf, *a, **kw):
    loop = '-1' if inf else '0'
    f = FFmpeg(
        inputs={
            filename: ['-re', '-stream_loop', loop]
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
    f.run(stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    job = self.db.session.query(JobModel).filter_by(id=id).first()
    print("Finish running Command")
    print("Deleting job", job)
    job.delete()
