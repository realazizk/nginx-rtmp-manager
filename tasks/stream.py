from extensions import celery
from time import sleep

###
# Stream tasks
###


@celery.task(ignore_result=True)
def play_task(*a, **kw):
    print(kw)
    print(job)
    print('SLEEPing')
    sleep(10)
    print('WAKING')

