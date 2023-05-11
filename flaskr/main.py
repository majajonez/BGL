import base64
import os
from base64 import b64encode

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from flask import Flask
from werkzeug.utils import secure_filename

from flaskr import db, auth
from flaskr.auth import login_required, load_logged_in_user, get_user_by_id, User
from flaskr.db import get_db

bp = Blueprint('main', __name__)


class Event:
    def __init__(self, wydarzenie):
        self.id = wydarzenie[0]
        self.user_id = wydarzenie[1]
        self.jaka_gra = wydarzenie[2]
        self.opis = wydarzenie[3]
        self.kiedy = wydarzenie[4]
        self.gdzie = wydarzenie[5]
        self.ile_miejsc = wydarzenie[6]
        self.type = "event"
        if wydarzenie[7]:
            self.photo = base64.b64encode(wydarzenie[7]).decode('ascii')
            print(self.photo)
        self.can_join = bool(wydarzenie[8])
        self.login = wydarzenie[9]


class Person:
    def __init__(self, profil):
        self.login = profil[1]
        self.city = profil[4]
        self.opis = profil[5]
        self.type = "person"


def get_user_by_login(login):
    conn = get_db()
    cur = conn.cursor()
    sql_update_query = '''SELECT * FROM logowanie_uzytkownikow WHERE login = ?'''
    cur.execute(sql_update_query, [login])
    uzytkownik = cur.fetchone()
    cur.close()
    return User(uzytkownik)


def get_events(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT w.*, uw.user_id is null as can_join, lu.login FROM wydarzenia w
                LEFT JOIN uczestnicy_wydarzen uw ON w.id = uw.event_id and uw.user_id = ?
                LEFT JOIN logowanie_uzytkownikow lu ON w.user_id = lu.id''', [user_id])
    wydarzenia = cur.fetchall()
    cur.close()
    event_list = []

    for w in wydarzenia:
        event = Event(w)
        event_list.append(event)
    return event_list


def get_events_by_game(game):
    conn = get_db()
    cur = conn.cursor()
    sql_update_query = '''SELECT * FROM wydarzenia WHERE jaka_gra LIKE ?'''
    cur.execute(sql_update_query, ['%' + game + '%'])
    wydarzenia = cur.fetchall()
    cur.close()
    event_list = []

    for w in wydarzenia:
        event = Event(w)
        event_list.append(event)
    return event_list


def get_events_by_login(login):
    conn = get_db()
    cur = conn.cursor()
    sql_update_query = '''SELECT * FROM logowanie_uzytkownikow WHERE login LIKE ?'''
    cur.execute(sql_update_query, ['%' + login + '%'])
    profile = cur.fetchall()
    cur.close()
    profil_list = []

    for p in profile:
        person = Person(p)
        profil_list.append(person)
    return profil_list


def get_events_by_city(city):
    conn = get_db()
    cur = conn.cursor()
    sql_update_query = '''SELECT * FROM wydarzenia WHERE city LIKE ?'''
    cur.execute(sql_update_query, ['%' + city + '%'])
    wydarzenia = cur.fetchall()
    cur.close()
    event_list = []

    for w in wydarzenia:
        event = Event(w)
        event_list.append(event)
    return event_list


def get_events_by_id(id, user_id):
    conn = get_db()
    cur = conn.cursor()
    sql_update_query = ('SELECT w.*, uw.user_id is null as can_join, lu.login FROM wydarzenia w'
                        ' LEFT JOIN uczestnicy_wydarzen uw ON w.id = uw.event_id'
                        ' LEFT JOIN logowanie_uzytkownikow lu ON w.user_id = lu.id'
                        ' WHERE w.id = ? AND uw.user_id = ?')
    cur.execute(sql_update_query, [id, user_id])
    wydarzenie = cur.fetchone()
    cur.close()
    return Event(wydarzenie)


@bp.route('/profil', methods=['GET'])
@login_required
def profil():
    return render_template('main/profil.html')


@bp.route('/search', methods=['POST'])
def search():
    args = request.form
    fraza = args.get("fraza", None)
    radio = args.get("btnradio", None)
    events = []
    if radio == "login":
        events = get_events_by_login(fraza)
    elif radio == "gra":
        events = get_events_by_game(fraza)
    elif radio == "city":
        events = get_events_by_city(fraza)
    else:
        raise Exception("not supported type")
    return render_template('main/main_page.html', events=events)


@bp.route('/main_page', methods=['GET', 'POST'])
def main_page():
    user_id = session.get('user_id')
    events = get_events(user_id)
    return render_template('main/main_page.html', events=events)


@bp.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        args = request.form
        user_id = session.get('user_id')
        print(user_id)
        title = args.get("title", None)
        description = args.get("description", None)
        when = args.get("when", None)
        where = args.get("where", None)
        the_number_of_seats = args.get("the_number_of_seats", None)
        photo = request.files['uploaded-file']
        error = None
        if user_id and title and description and when and where and the_number_of_seats:
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('INSERT INTO wydarzenia (user_id, jaka_gra, opis, kiedy, gdzie, ile_miejsc, photo)'
                            'VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (user_id,
                             title,
                             description,
                             when,
                             where,
                             the_number_of_seats,
                             photo.stream.read())
                            )
                conn.commit()
                cur.close()
                return redirect(url_for('main.main_page'))
            except Exception as e:
                error = "Nie udało się utworzyć wydarzenia"
        else:
            error = "Brakuje informacji"
        flash(error)
    return render_template('main/event.html')


@bp.route('/event_details/<id>', methods=['GET', 'POST'])
def event_details(id):
    event = get_events_by_id(id, g.user.id)
    return render_template('main/event_details.html', event=event)


@bp.route('/event/<id>/join', methods=['POST'])
def join_event(id):
    user_id = session.get('user_id')
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO uczestnicy_wydarzen (user_id, event_id)'
                'VALUES (?, ?)',
                (user_id, id)
                )
    conn.commit()
    cur.close()
    conn.close()
    return render_template("main/main_page.html")


@bp.route('/profile_viev/<login>', methods=['GET'])
def profile_viev(login):
    user = get_user_by_login(login)
    user_id = user.id
    events = get_events(user_id)
    return render_template('main/profile_viev.html', user=user, events=events)


@bp.route('/upload_photo', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'uploaded-file' not in request.files:
            flash('No file part')
            return redirect('profil')
        file = request.files['uploaded-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect('profil')
        if file:
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('UPDATE logowanie_uzytkownikow SET photo=? WHERE id = ?',
                            (file.stream.read(), g.user.id)
                            )
                conn.commit()
                cur.close()
            except:
                error = "<i>zdjęcie nie zostało zapisane</i>"
            else:
                return redirect(url_for("main.profil"))
        return redirect(url_for("main.profil"))


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config = {
        "SECRET_KEY": 'dev',
        'DB_URI': os.path.join(app.instance_path, 'flaskr.sqlite'),
    }
    app.config.from_mapping(config)
    app.register_blueprint(auth.bp)
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='main.profil')
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
