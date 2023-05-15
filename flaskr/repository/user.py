import base64
from flaskr.db import get_db


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


def create_user(user, password2, email, city):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO logowanie_uzytkownikow (login, haslo, email, city)'
                'VALUES (?, ?, ?, ?)',
                (user,
                 password2,
                 email,
                 city)
                )
    conn.commit()
    cur.close()