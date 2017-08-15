from audiosm.extensions import admin_ob
from flask_admin.contrib.sqla import ModelView
from audiosm.database import db
from audiosm.users.models import UserModel, RoleModel

admin_ob.add_view(ModelView(UserModel, db.session))
admin_ob.add_view(ModelView(RoleModel, db.session))
