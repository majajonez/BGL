import base64
from flaskr.db import get_db


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
        self.can_join = bool(wydarzenie[8])
        self.login = wydarzenie[9]


class Person:
    def __init__(self, profil):
        self.login = profil[1]
        self.city = profil[4]
        self.opis = profil[5]
        self.type = "person"


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
    sql_update_query = '''SELECT * FROM logowanie_uzytkownikow WHERE id = ?'''
    id_value = x
    cur.execute(sql_update_query, [ id_value])
    uzytkownik = cur.fetchone()
    cur.close()
    return User(uzytkownik)


def get_user(x):
    conn = get_db()
    cur = conn.cursor()
    sql_update_query = '''SELECT * FROM logowanie_uzytkownikow WHERE login = ?'''
    login_value = x
    cur.execute(sql_update_query, [ login_value ])
    uzytkownik = cur.fetchall() #todo: fetchone
    cur.close()
    return uzytkownik


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