import os
import psycopg2, hashlib

if __name__ == '__main__':
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="mysecretpassword")

    h = '123'
    haslo = hashlib.sha256(h.encode('utf-8')).hexdigest()
    try:
        cur = conn.cursor()

        try:
            cur.execute('DROP TABLE IF EXISTS logowanie_uzytkownikow;')
            cur.execute('CREATE TABLE logowanie_uzytkownikow (id serial PRIMARY KEY,'
                        'login text NOT NULL UNIQUE,'
                        'haslo text NOT NULL,'
                        'email text NOT NULL UNIQUE,'
                        'city text,'
                        'opis text,'
                        'photo bytea);'
                        )

            cur.execute('INSERT INTO logowanie_uzytkownikow (login, haslo, email, city)'
                        'VALUES (%s, %s, %s, %s)',
                        ('maja',
                         haslo,
                         'majonezik93@gmail.com',
                         'Warszawa')
                        )

            cur.execute('DROP TABLE IF EXISTS wydarzenia;')
            cur.execute('CREATE TABLE wydarzenia (id serial PRIMARY KEY,'
                        'login text NOT NULL,'
                        'jaka_gra text NOT NULL,'
                        'opis text,'
                        'kiedy text NOT NULL,'
                        'gdzie text NOT NULL,'
                        'ile_miejsc smallint,'
                        'photo bytea);'
                        )
            cur.execute('INSERT INTO wydarzenia (login, jaka_gra, opis, kiedy, gdzie, ile_miejsc)'
                        'VALUES (%s, %s, %s, %s, %s, %s)',
                        ('maja',
                         'Azul',
                         'Kafelkowa gra logiczna',
                         '01.01.2023',
                         'Warszawa',
                         4)
                        )

            conn.commit()

        finally:
            cur.close()

    finally:
        conn.close()
