import base64
from base64 import b64encode

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)
from flask import Flask
from werkzeug.utils import secure_filename

from flaskr import db, auth
from flaskr.auth import login_required, load_logged_in_user, get_user_by_id
from flaskr.db import get_db

config = {
    "SECRET_KEY": 'dev'
}

bp = Blueprint('main', __name__)


class Event:
    def __init__(self, wydarzenie):
        self.id = wydarzenie[0]
        self.login = wydarzenie[1]
        self.jaka_gra = wydarzenie[2]
        self.opis = wydarzenie[3]
        self.kiedy = wydarzenie[4]
        self.gdzie = wydarzenie[5]
        self.ile_miejsc = wydarzenie[6]
        self.type = "event"
        print(wydarzenie[7])
        if wydarzenie[7]:
            self.photo = base64.b64encode(wydarzenie[7]).decode('ascii')
            print(self.photo)

class Person:
    def __init__(self, profil):
        self.login = profil[1]
        self.city = profil[4]
        self.opis = profil[5]
        self.type = "person"


def get_events():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM wydarzenia')
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
    cur.execute('SELECT * FROM wydarzenia WHERE jaka_gra LIKE %(game)s', {"game": '%' + game + '%'})
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
    cur.execute('SELECT * FROM logowanie_uzytkownikow WHERE login LIKE %(login)s', {"login": '%' + login + '%'})
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
    cur.execute('SELECT * FROM wydarzenia WHERE city LIKE %(city)s', {"city": '%' + city + '%'})
    wydarzenia = cur.fetchall()
    cur.close()
    event_list = []

    for w in wydarzenia:
        event = Event(w)
        event_list.append(event)
    return event_list


@bp.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == "POST":
        args = request.form
        photo = args.get("photo", None)
        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO logowanie_uzytkownikow (photo)'
                        'VALUES (%s)',
                        (photo)
                        )
            conn.commit()
            cur.close()
        except:
            error = "<i>nie udało się przesłać zdjęcia</i>"
        else:
            return render_template('main/profil.html')
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
    events = get_events()
    return render_template('main/main_page.html', events=events)


@bp.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        args = request.form
        user = args.get("user", None)
        title = args.get("title", None)
        description = args.get("description", None)
        when = args.get("when", None)
        where = args.get("where", None)
        the_number_of_seats = args.get("the_number_of_seats", None)
        photo = request.files['uploaded-file']
        error = None
        if user and title and description and when and where and the_number_of_seats:
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('INSERT INTO wydarzenia (login, jaka_gra, opis, kiedy, gdzie, ile_miejsc, photo)'
                            'VALUES (%s, %s, %s, %s, %s, %s, %s)',
                            (user,
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
                print(e)
                error = "Nie udało się utworzyć wydarzenia"
        else:
            error = "Brakuje informacji"
        flash(error)
    return render_template('main/event.html')


@bp.route('/upload_photo', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'uploaded-file' not in request.files:
            flash('No file part')
            print("aaa")
            return redirect('profil')
        file = request.files['uploaded-file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            print("bbb")
            return redirect('profil')
        if file:
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('UPDATE logowanie_uzytkownikow SET photo=%s WHERE id = %s',
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
    app = Flask(__name__)
    app.config.from_mapping(config)
    app.register_blueprint(auth.bp)
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='main.profil')
    db.init_app(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
