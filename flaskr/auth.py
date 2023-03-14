import base64
import functools, re, hashlib

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def get_user(x):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM logowanie_uzytkownikow WHERE login = %(login)s', {"login": x})
    uzytkownik = cur.fetchall() #todo: fetchone
    cur.close()
    return uzytkownik

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        args = request.form
        user = args.get("user", None)
        password = args.get("password", None)
        email = args.get("email", None)
        city = args.get("city", None)
        error = None
        if not re.fullmatch(regex, email):
            error = "<i>Niepoprawny email</i>"

        if user and password and email:
            password2 = hashlib.sha256(password.encode('utf-8')).hexdigest()
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('INSERT INTO logowanie_uzytkownikow (login, haslo, email, city)'
                            'VALUES (?, ?, ?, ?)',
                            (user,
                             password2,
                             email,
                             city)
                            )
                conn.commit()
                cur.close()
            except:
                error = "<i>ten login lub email jest już zajęty</i>"
            else:
                return redirect(url_for("auth.login"))
        else:
            error = "<i> rejestracja sie nie udala</i>"

        flash(error)
    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        args = request.form
        uzytkownik = get_user(args.get("user", ""))
        error = None
        if uzytkownik:
            password = args.get("password", "")
            password2 = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if password2 == uzytkownik[0][2]:
                session.clear()
                session['user_id'] = uzytkownik[0][0] #todo: uzyc nazwy kolumny
                return redirect(url_for('main.main_page'))
            else:
                error = 'Incorrect password.'
        else:
            error = 'Incorrect username.'
        flash(error)
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_user_by_id(user_id)


class User:
    def __init__(self, user):
        self.id = user[0]
        self.login = user[1]
        self.haslo = user[2]
        self.email = user[3]
        self.city = user[4]
        self.opis = user[5]
        if user[6]:
            self.photo = base64.b64encode(user[6]).decode('ascii')


def get_user_by_id(x):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM logowanie_uzytkownikow WHERE id = %(id)s', {"id": x})
    uzytkownik = cur.fetchone()
    cur.close()
    return User(uzytkownik)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view