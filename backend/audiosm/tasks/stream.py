from audiosm.extensions import celery
from ffmpy import FFmpeg
from audiosm import settings
from audiosm.extensions import DatabaseTask
from audiosm.jobs.models import JobModel


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
                stream=stream,
                host=settings.Config.STREAM_HOST
            ): ['-vn', '-c:a', 'aac', '-strict',  '-2', '-f', 'flv']
        }
    )
    f.run()
    job = self.db.session.query(JobModel).filter_by(id=id).first()
    job.delete()
