from flask import url_for


class TestUserViews:

    def test_user_login(self, testapp, user):
        user = user.get()
        resp = testapp.post_json(url_for('users.login'), {
            'username': user.username,
            'password': 'myprecious'
        })
        assert resp.json['id_token'] != 'None'
        assert resp.json['id_token'] != ''
        assert resp.json['username'] == user.username

    def test_admin_login_wrong(self, testapp, adminrole, admin):
        """
        Tests admin can login to interface
        """
        admin = admin.get()
        resp = testapp.get(url_for('admin.index'))
        form = resp.form
        form['username'] = admin.username
        form['password'] = 'wrongpassword'
        resp = form.submit()
        h = str(resp.html).lower()
        assert 'Wrong username or password'.lower() in h.lower()

    def test_admin_login_not_admin(self, testapp, user):
        """
        Tests normal user can't login to interface
        """
        user = user.get()
        resp = testapp.get(url_for('admin.index'))
        form = resp.form
        form['username'] = user.username
        form['password'] = 'myprecious'
        resp = form.submit()
        h = str(resp.html.title).lower()
        assert 'Login'.lower() in h.lower()
        assert 'You are not admin'.lower() in str(resp.html).lower()

    def test_admin_login_work(self, testapp, adminrole, admin):
        """
        Tests admin login
        """
        admin = admin.get()
        resp = testapp.get(url_for('admin.index'))
        form = resp.form
        form['username'] = admin.username
        form['password'] = 'myprecious'
        resp = form.submit()
        h = str(resp.html.title).lower()
        assert 'Login'.lower() not in h.lower()


class TestUserModels:
    def test_is_admin(self, adminrole, admin):
        # Dear maintainer, it is really important that admin role precedes the admin
        # take a look at conftest
        admin = admin.get()
        assert admin.roles[0] == adminrole
