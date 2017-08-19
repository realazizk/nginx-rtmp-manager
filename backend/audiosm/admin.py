from audiosm.extensions import admin_ob
from flask_admin.contrib.sqla import ModelView
from audiosm.database import db
from audiosm.users.models import UserModel, RoleModel
from flask_admin import BaseView, expose
from flask import session, redirect, url_for, request, flash
from audiosm.jobs.models import JobModel
from audiosm.streams.models import StreamModel


class LoginView(BaseView):
    @expose('/', methods=('POST', 'GET'))
    def index(self):
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = UserModel.query.filter_by(username=username).first()
            if user is not None and user.check_password(password):
                if user.has_role('admin'):
                    session['logged_in'] = True
                    session['username'] = user.username
                else:
                    flash('You are not admin')
            else:
                flash('Wrong username or password')
        if not session.get('logged_in'):
            return self.render('login.html')
        return redirect(url_for('admin.index'))

    def is_visible(self):
        return False


class LogoutView(BaseView):
    @expose('/', methods=('GET',))
    def index(self):
        session.clear()
        return redirect(url_for('admin.index'))

    def is_visible(self):
        return False


class UserAdminView(ModelView):
    column_exclude_list = ['password', ]
    form_excluded_columns = ['password', ]
    inline_models = [JobModel]


admin_ob.add_view(UserAdminView(UserModel, db.session))
admin_ob.add_view(ModelView(RoleModel, db.session))
admin_ob.add_view(LoginView(name='Login', endpoint='login'))
admin_ob.add_view(LogoutView(name='Logout', endpoint='logout'))
admin_ob.add_view(ModelView(JobModel, db.session))
admin_ob.add_view(ModelView(StreamModel, db.session))
