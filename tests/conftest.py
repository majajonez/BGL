import os
from mimetypes import init

import pytest

from flaskr.db import get_db
from flaskr.init_db import init_prod_db, init_db_for_connection
from flaskr.main import create_app
from tests.AuthFixture import AuthFixture


@pytest.fixture()
def app():
    app = create_app()
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config.update({
        "TESTING": True,
        "DB_URI": os.path.join(basedir, 'test.sqlite'),
    })

    # other setup can go here
    with app.app_context():
        init_db_for_connection(get_db())

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.fixture()
def auth(client):
    return AuthFixture(client)