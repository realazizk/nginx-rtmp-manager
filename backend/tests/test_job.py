from flask import url_for
from .helpers import login


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
