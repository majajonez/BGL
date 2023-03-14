import re

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'email': 'a', 'password': 'a'}
    )
    assert response.status_code == 200
    assert (re.search('rejestracja sie nie udala',
                         response.get_data(as_text=True)))
    # assert response.headers["Location"] == "/auth/login"
    #
    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM logowanie_uzytkownikow LIMIT 1",
        ).fetchone() is not None