import sqlite3

import psycopg2, re, hashlib
from flask import current_app, g
from flask import current_app


def get_db():
    if 'db' not in g:
        if current_app.config["TESTING"]:
            g.db = sqlite3.connect(current_app.config['DB_URI'])
        else:
            g.db = psycopg2.connect(host='localhost',
                                    database='postgres',
                                    user="postgres",
                                    password="mysecretpassword")
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
