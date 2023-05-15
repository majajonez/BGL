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


def create_event(user_id, title, description, when, where, the_number_of_seats, photo):
    conn = get_db()
    cur = conn.cursor()
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



def join_event_db(user_id, id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO uczestnicy_wydarzen (user_id, event_id)'
                'VALUES (?, ?)',
                (user_id, id)
                )
    conn.commit()
    cur.close()
    conn.close()