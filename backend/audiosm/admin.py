from audiosm.extensions import admin_ob
from flask_admin.contrib.sqla import ModelView
from audiosm.database import db
from audiosm.users.models import UserModel, RoleModel
from flask_admin import BaseView, expose
from flask import session, redirect, url_for, request, flash
from audiosm.jobs.models import JobModel
from audiosm.streams.models import StreamModel
from wtforms.fields import PasswordField
from audiosm.extensions import celery


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

class MyModelView(ModelView):

    def is_accessible(self):
        if not session.get('logged_in'):
            return False
        a = session['username']
        user = UserModel.query.filter_by(username=a).first()
        if not user or not user.is_active:
            return False

        if user.has_role('admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if session.get('logged_in'):
                # permission denied
                abort(403)
            else:
                # login
                return self.render('login.html')
        self._template_args['username'] = session.get('username')

class LogoutView(BaseView):
    @expose('/', methods=('GET',))
    def index(self):
        session.clear()
        return redirect(url_for('admin.index'))

    def is_visible(self):
        return False


class UserAdminView(MyModelView):

    form_extra_fields = {
        'password2': PasswordField('password')
    }
    inline_models = [JobModel]

    column_exclude_list = ('password',)

    form_excluded_columns = ('password',)

    def on_model_change(self, form, model: UserModel, is_created):
        if len(model.password2):
            model.set_password(model.password2)


class JobAdminView(MyModelView):
    def on_model_delete(self, model):
        celery.control.revoke(model.taskid, terminate=True, signal='SIGKILL')


admin_ob.add_view(UserAdminView(UserModel, db.session, name='Users'))
admin_ob.add_view(MyModelView(RoleModel, db.session, name='Roles'))
admin_ob.add_view(LoginView(name='Login', endpoint='login'))
admin_ob.add_view(LogoutView(name='Logout', endpoint='logout'))
admin_ob.add_view(JobAdminView(JobModel, db.session, 'Jobs'))
admin_ob.add_view(MyModelView(StreamModel, db.session, 'Streams'))
