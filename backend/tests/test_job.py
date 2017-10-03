from flask import url_for
from .helpers import login
from audiosm.jobs.models import JobModel
from audiosm.streams.models import StreamModel


class TestJob:
    
    def test_make_new_job(self, testapp, user):
        """
        Test make a new job
        """
        user = user.get()
        token = login(testapp, user)
        # testapp.post_json(url_for('jobs.newjob'), {
            
        # }, headers={
        #     'Authorization': 'Token {}'.format(token)
        # })


class TestJobModel:

    def test_make_new_model_multiple_files(self, user):
        user = user.get()
        stream = StreamModel.create(name='name', password='pass',
                                    adminid=user.id, stype='audio')

        j = JobModel.create(
            streamid=stream.id,
            adminid=user.id
        )

        assert len(j.files) == 0

        j.add_file(
            'smthing'
        )
        assert len(j.files) == 1

        j.add_file(
            'other'
        )
        assert len(j.files) == 2
