import os
import psycopg2, hashlib

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
                                        'email text NOT NULL UNIQUE);'
                                         )

        cur.execute('INSERT INTO logowanie_uzytkownikow (login, haslo, email)'
                    'VALUES (%s, %s, %s)',
                    ('maja',
                     haslo,
                     'majonezik93@gmail.com')
                    )

        conn.commit()

    finally:
        cur.close()

finally:
    conn.close()

