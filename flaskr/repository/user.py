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
    sql_update_query = '''SELECT lu.*, z.user_id is null as can_join FROM logowanie_uzytkownikow lu
                        LEFT JOIN znajomi z ON lu.id = z.friend_id
                        WHERE lu.login = ?'''
    cur.execute(sql_update_query, [login])
    uzytkownik = cur.fetchone()
    cur.close()
    if uzytkownik:
        return User(uzytkownik)
    else:
        return None

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


def friend_join(user_id, friend_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('INSERT INTO znajomi (user_id, friend_id)'
                'VALUES (?, ?)',
                (user_id,
                 friend_id)
                )
    conn.commit()
    cur.close()


def friend_invite(user_id):
    id = user_id
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT lu.*, z.friend_id FROM logowanie_uzytkownikow lu
                LEFT JOIN znajomi z ON lu.id = z.user_id
                WHERE z.friend_id = ? AND confirm is NULL''', [id])
    invitations = cur.fetchall()
    cur.close()
    if invitations:
        invitations_list = []
        for invitation in invitations:
            friend = User(invitation)
            invitations_list.append(friend)
        return invitations_list
    else:
        return []


def confirm_invit(user_id, friend_id):
    print(user_id)
    print(friend_id)
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE znajomi SET confirm=? WHERE user_id = ? AND friend_id = ?', (1, friend_id, user_id)
                )
    conn.commit()
    cur.close()


def friends_by_user_id(user_id):
    id = user_id
    conn = get_db()
    cur = conn.cursor()
    cur.execute('''SELECT lu.*, z.friend_id, user_id FROM logowanie_uzytkownikow lu
                LEFT JOIN znajomi z ON lu.id = z.friend_id OR lu.id = z.user_id
                WHERE z.confirm is "1" AND z.friend_id = ? AND lu.id IS NOT ? OR z.confirm is "1" AND z.user_id = ? AND lu.id IS NOT ?''', [id, id, id, id])
    friends = cur.fetchall()
    cur.close()
    if friends:
        friends_list = []
        for friend in friends:
            friend = User(friend)
            friends_list.append(friend)
        return friends_list
    else:
        return []


def friends_brake_off(user_id, friend_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM znajomi WHERE user_id = ? AND friend_id = ? OR user_id = ? AND friend_id = ?', (user_id, friend_id, friend_id, user_id)
                )
    conn.commit()
    cur.close()


def are_friends(user_id, friend_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT confirm FROM znajomi WHERE user_id = ? AND friend_id = ? OR user_id = ? AND friend_id = ?',
                (user_id, friend_id, friend_id, user_id)
                )
    confirm_friend = cur.fetchone()
    cur.close()
    if confirm_friend is None:
        confirm = 3
    else:
        confirm = confirm_friend[0]
    return confirm