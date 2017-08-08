from extensions import celery
from ffmpy import FFmpeg
import settings

###
# Stream tasks
###


@celery.task(ignore_result=True)
def play_audio_task(*a, **kw):
    f = FFmpeg(
        inputs={
            kw['filename']: ['-re']
        },
        outputs={
            'rtmp://{host}:1935/stream/{stream}'.format(
                stream=kw['stream'],
                host=settings.Config.STREAM_HOST
            ): ['-vn', '-c:a', 'aac', '-f', 'flv']
        }
    )
    f.run()
