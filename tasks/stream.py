from injector import celery
from models import JobModel

###
# Stream tasks
###


@celery.task(ignore_result=True)
def play_task(job: JobModel):
    if not isinstance(job, JobModel):
        raise NotImplemented
    print(job)
