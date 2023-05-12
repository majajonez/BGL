import functools
import hashlib
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db
from flaskr.repository import get_user, get_user_by_id

bp = Blueprint('auth', __name__, url_prefix='/auth')

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        args = request.form
        user = args.get("user", None)
        password = args.get("password", None)
        email = args.get("email", None)
        city = args.get("city", None)
        if not email or not re.fullmatch(regex, email):
            error = "<i>Niepoprawny email</i>"
        else:
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
        if uzytkownik:
            password = args.get("password", "")
            password2 = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if password2 == uzytkownik[0][2]:
                session.clear()
                session['user_id'] = uzytkownik[0][0]  # todo: uzyc nazwy kolumny
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
