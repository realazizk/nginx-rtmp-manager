from audiosm.extensions import redis_store
from audiosm.utils import Jobs
from audiosm.jobs.models import JobModel
from audiosm.streams.models import StreamModel
import pickle

fpth = '/tmp/testfile'

class TestJob:

    def test_make_new_job(self):
        """
        Test make a new job
        """


class TestJobRedis:

    def test_make_job_redis(self, app, user):
        # prepare
        user = user.get()
        redis_store.delete('testcurrjobs')
        stream = StreamModel.create(name='az', password='d',
                                    adminid=user.id, stype='audio')
        job = JobModel.create(streamid=stream.id,
                              adminid=user.id, filename=fpth, inf=False)
        jr = redis_store.get('testcurrjobs')
        if not jr:
            jr = Jobs()
        else:
            jr = pickle.loads(jr)
        jr.addjob(job)
        bo = pickle.dumps(jr)
        redis_store.set('testcurrjobs', bo)
        assert len(jr.jobs) == 1

        jr = redis_store.get('testcurrjobs')
        jr = pickle.loads(jr)
        job = JobModel.create(streamid=stream.id,
                              adminid=user.id, filename=fpth, inf=False)

        jr.addjob(job)
        bo = pickle.dumps(jr)
        redis_store.set('testcurrjobs', bo)

        jr = redis_store.get('testcurrjobs')
        jr = pickle.loads(jr)

        assert len(jr.jobs) == 2
