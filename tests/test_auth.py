import re

import pytest
from flask import g, session
from flaskr.db import get_db


def test_register_page_should_load(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'email': 'a', 'password': 'a'}
    )
    assert response.status_code == 200


# def test_register_should_fail(client, app):
#     response = client.post(
#         '/auth/register', data={'email': 'a', 'password': 'a'}
#     )
#     assert (re.search('rejestracja sie nie udala',
#                       response.get_data(as_text=True)))
# assert response.headers["Location"] == "/auth/login"
#
# with app.app_context():
#     assert get_db().execute(
#         "SELECT * FROM logowanie_uzytkownikow LIMIT 1",
#     ).fetchone() is not None

def test_register_with_valid_email_and_password_should_pass(client, app):
    response = client.post(
        '/auth/register', data={'user': 'tester', 'email': 'tester@gmail.com', 'password': 'tester', 'city': 'tester'}
    )
    assert response.status_code == 302


def test_login_should_pass_after_correct_registration(client, app):
    response = client.post(
        '/auth/register', data={'user': 'tester', 'email': 'tester@gmail.com', 'password': 'tester', 'city': 'tester'}
    )
    assert response.status_code == 302
    response = client.post('/auth/login', data={'user': 'tester', 'password': 'tester'})
    assert response.status_code == 302


def test_register_with_wrong_email_should_fail(auth):
    response = auth.register_raw(data={'email': 'a', 'password': 'a'})
    assert (re.search('Niepoprawny email',
                      response.get_data(as_text=True)))


def test_register_with_empty_email_should_fail(auth):
    response = auth.register_raw(data={'email': '', 'password': 'a'})
    assert (re.search('Niepoprawny email',
                      response.get_data(as_text=True)))


def test_register_without_email_should_fail(auth):
    response = auth.register_raw(data={'password': 'a'})
    assert (re.search('Niepoprawny email',
                      response.get_data(as_text=True)))

def test_register_the_same_login_twice_should_fail(auth):
    auth.register_raw(data={'user': 'lucek', 'email': 'lucek@gmail.com', 'password': 'a'})
    response = auth.register_raw(data={'user': 'lucek', 'email': 'lucek2@gmail.com', 'password': 'a'})
    assert (re.search('ten login lub email jest już zajęty', response.get_data(as_text=True)))

def test_register_the_same_email_twice_should_fail(auth):
    auth.register_raw(data={'user': 'lucek', 'email': 'lucek@gmail.com', 'password': 'a'})
    response = auth.register_raw(data={'user': 'lucek2', 'email': 'lucek@gmail.com', 'password': 'a'})
    assert (re.search('ten login lub email jest już zajęty', response.get_data(as_text=True)))


# def test_login_page_should_load(client, app):
#     assert client.get('/auth/login').status_code == 200
#     response = client.post(
#         '/auth/login', data={'user': 'maja', 'password': '123'}
#     )
#     assert response.status_code == 200

# def test_login_with_wrong_password_should_fail(client, app)

