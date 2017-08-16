from flask_sqlalchemy import SQLAlchemy, Model
from flask_admin import Admin, AdminIndexView
from flask_bcrypt import Bcrypt
from flask_jwt import JWT
from flask_cors import CORS
from celery import Celery
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from audiosm.settings import Config
from celery import Task
from flask import session


class CRUDMixin(Model):
    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the return ecord from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


db = SQLAlchemy(model_class=CRUDMixin)
bcrypt = Bcrypt()
cors = CORS()
celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)
migrate = Migrate(db=db)
redis_store = FlaskRedis()


class DatabaseTask(Task):
    _db = None

    @property
    def db(self):
        if self._db is None:
            self._db = db
        return self._db


def jwt_identity(payload):
    user_id = payload['identity']
    return UserModel.get_by_id(user_id)


def authenticate(email, password):
    user = UserModel.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user

from audiosm.users.models import UserModel # noqa

jwt = JWT(authentication_handler=authenticate, identity_handler=jwt_identity)
from flask_jwt import jwt_required  # noqa


class MyAdminIndexView(AdminIndexView):
    def _handle_view(self, name, **kwargs):
        if not session.get('logged_in'):
            return self.render('login.html')


admin_ob = Admin(name='streammanager', template_mode='bootstrap3',
                 index_view=MyAdminIndexView(), base_template='admin.html')
