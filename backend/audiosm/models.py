"""
Audio Stream Manager
Copyright Mohamed Aziz knani <medazizknani@gmai.com> 2017

"""

from extensions import db, bcrypt
import datetime as dt
from flask_jwt import _default_jwt_encode_handler
from compat import basestring


###
# Extensions
###


Column = db.Column


###
# Models
###

