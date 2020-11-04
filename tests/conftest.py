import pytest

from app.application import app, db

import os
import tempfile
import sys
import json


def fixture():
    with app.open_resource('../fixture.sql', mode='r') as f:
        for q in f.read().split(';'):
            db.session.execute(q)
        db.session.commit()


@pytest.fixture(scope='session')
def _app():
    app.config['TESTING'] = True
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../test.sqlite'

    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()
    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


@pytest.fixture(scope='function')  # TODO: change scope to session
def _db(_app):
    db.drop_all()
    db.create_all()

    fixture()

    yield db

    db.drop_all()


@pytest.fixture(scope='function')
def session(_app, _db):
    session = _db.session
    session.begin_nested()

    yield session

    session.rollback()
    session.remove()


@pytest.fixture(scope='function')
def client(session):
    yield app.test_client()
