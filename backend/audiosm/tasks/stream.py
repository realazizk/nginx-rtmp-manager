from audiosm.extensions import celery
from ffmpy import FFmpeg
from audiosm import settings

###
# Stream tasks
###


@celery.task(ignore_result=True)
def play_audio_task(filename, stream, *a, **kw):
    f = FFmpeg(
        inputs={
            filename: ['-re']
        },
        outputs={
            'rtmp://{host}:1935/stream/{stream}'.format(
                stream=stream,
                host=settings.Config.STREAM_HOST
            ): ['-vn', '-c:a', 'aac', '-strict',  '-2', '-f', 'flv']
        }
    )
    f.run()
