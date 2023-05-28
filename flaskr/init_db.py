import os
import sqlite3, hashlib


def init_db_for_connection(conn):
    h = '123'
    haslo = hashlib.sha256(h.encode('utf-8')).hexdigest()
    try:
        cur = conn.cursor()

        try:
            cur.execute('DROP TABLE IF EXISTS logowanie_uzytkownikow;')
            cur.execute('CREATE TABLE logowanie_uzytkownikow (id INTEGER PRIMARY KEY,'
                        'login text NOT NULL UNIQUE,'
                        'haslo text NOT NULL,'
                        'email text NOT NULL UNIQUE,'
                        'city text,'
                        'opis text,'
                        'photo bytea);'
                        )

            cur.execute('INSERT INTO logowanie_uzytkownikow (login, haslo, email, city)'
                        'VALUES (?, ?, ?, ?)',
                        ('maja',
                         haslo,
                         'majonezik93@gmail.com',
                         'Warszawa')
                        )

            cur.execute('DROP TABLE IF EXISTS wydarzenia;')
            cur.execute('CREATE TABLE wydarzenia (id INTEGER PRIMARY KEY,'
                        'user_id text NOT NULL,' #todo zmienic na integer
                        'jaka_gra text NOT NULL,'
                        'opis text,'
                        'kiedy text NOT NULL,'
                        'gdzie text NOT NULL,'
                        'ile_miejsc smallint,'
                        'photo bytea);'
                        )
            cur.execute('INSERT INTO wydarzenia (user_id, jaka_gra, opis, kiedy, gdzie, ile_miejsc)'
                        'VALUES (?, ?, ?, ?, ?, ?)',
                        ('1',
                         'Azul',
                         'Kafelkowa gra logiczna',
                         '01.01.2023',
                         'Warszawa',
                         4)
                        )
            cur.execute('DROP TABLE IF EXISTS uczestnicy_wydarzen;')
            cur.execute('CREATE TABLE uczestnicy_wydarzen (user_id integer NOT NULL, '
                        'event_id integer NOT NULL);'
                        )

            conn.commit()

        finally:
            cur.close()

    finally:
        conn.close()


def init_prod_db():
    conn = sqlite3.connect("../instance/flaskr.sqlite")
    init_db_for_connection(conn)


if __name__ == '__main__':
    init_prod_db()
