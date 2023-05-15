from flaskr.db import get_db


class Person:
    def __init__(self, profil):
        self.login = profil[1]
        self.city = profil[4]
        self.opis = profil[5]
        self.type = "person"


def get_profiles_by_login(login):
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


def update_profile(file, g):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE logowanie_uzytkownikow SET photo=? WHERE id = ?',
                (file.stream.read(), g.user.id)
                )
    conn.commit()
    cur.close()