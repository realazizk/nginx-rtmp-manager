# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from audiosm import app_factory
from audiosm.database import db as _db
from audiosm.settings import testConfig
from audiosm.users.models import UserModel, RoleModel
from .exceptions import AdminRoleNotFound

from .factories import UserFactory


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = app_factory(testConfig)

    with _app.app_context():
        _db.create_all()

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """A user for the tests."""
    class User():
        def get(self) -> UserModel:
            muser = UserFactory(password='myprecious')
            db.session.commit()
            return muser
    return User()


@pytest.fixture
def adminrole(db):
    # Add admin role
    return RoleModel.create(name='admin')


@pytest.fixture
def admin(db):
    """A user for the tests."""
    class User():
        def get(self) -> UserModel:
            muser = UserFactory(password='myprecious')
            adminrole = RoleModel.query.filter_by(name='admin').first()
            if not adminrole:
                raise AdminRoleNotFound
            muser.add_role(adminrole)
            db.session.commit()
            return muser
    return User()
