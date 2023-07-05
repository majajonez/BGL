from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g
)

from flaskr.auth import login_required
from flaskr.repository.event import *
from flaskr.repository.profile import *
from flaskr.repository.user import *

bp = Blueprint('main', __name__)


@bp.route('/profil', methods=['GET'])
@login_required
def profil():
    return render_template('main/profil.html')


@bp.route('/search', methods=['POST'])
def search():
    args = request.form
    fraza = args.get("fraza", None)
    radio = args.get("btnradio", None)
    return render_search(radio, fraza)


def render_search(radio, fraza):
    user_id = session.get('user_id')
    if radio == "login":
        entities = get_profiles_by_login(fraza)
    elif radio == "gra":
        entities = get_events_by_game(user_id, fraza)
    elif radio == "miasto":
        entities = get_events_by_city(user_id, fraza)
    else:
        raise Exception("not supported type")
    if entities:
        return render_template('main/main_page.html', entities=entities)
    else:
        return render_template('main/not_found.html')


@bp.route('/main_page', methods=['GET', 'POST'])
def main_page():
    return render_search("gra", "")


@bp.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        args = request.form
        user_id = session.get('user_id')
        title = args.get("title", None)
        description = args.get("description", None)
        when = args.get("when", None)
        where = args.get("where", None)
        the_number_of_seats = args.get("the_number_of_seats", None)
        photo = request.files['uploaded-file']
        if user_id and title and description and when and where and the_number_of_seats:
            try:
                create_event(user_id, title, description, when, where, the_number_of_seats, photo)
                return redirect(url_for('main.main_page'))
            except:
                error = "Nie udało się utworzyć wydarzenia"
        else:
            error = "Brakuje informacji"
        flash(error)
    return render_template('main/event.html')


@bp.route('/event_details/<id>', methods=['GET', 'POST'])
def event_details(id):
    event = get_events_by_id(id, g.user.id)
    if event is not None:
        return render_template('main/event_details.html', event=event)
    else:
        return render_template('main/not_found.html')


@bp.route('/event/<id>/join', methods=['POST'])
def join_event(id):
    user_id = session.get('user_id')
    join_event_db(user_id, id)
    return render_template("main/main_page.html")


@bp.route('/my_events/', methods=['GET'])
def my_events():
    user_id = session.get('user_id')
    events = get_events_by_user_id(user_id)
    return render_template('main/my_events.html', events=events)


@bp.route('/profile_view/<login>', methods=['GET'])
def profile_view(login):
    user = get_user_by_login(login)
    if user:
        user_id = user.id
        my_events = get_events_by_user_id(user_id)
        joined_events = get_events_non_author(user_id)
        return render_template('main/profile_view.html', user=user, my_events=my_events, joined_events=joined_events)
    else:
        return render_template('main/not_found.html')


@bp.route('/friends', methods=['GET'])
def friends():
    id = session.get('user_id')
    friends_invit = friend_invite(id)
    return render_template('main/friends.html', friends_invit=friends_invit)


@bp.route('/profile_view/<login>/invitation', methods=['POST'])
def send_invit_friend(login):
    user_id = session.get('user_id')
    friend = get_user_by_login(login)
    friend_id = friend.id
    friend_join(user_id, friend_id)
    return profile_view(login)


@bp.route('/friends/<friend_id>/join', methods=['POST'])
def confirm_friends(friend_id):
    user_id = session.get('user_id')
    friend_id = friend_id
    confirm_invit(user_id, friend_id)
    return friends()


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
            try:
                update_profile(file, g)
            except:
                error = "<i>zdjęcie nie zostało zapisane</i>"
                flash(error)
            else:
                return redirect(url_for("main.profil"))
        return redirect(url_for("main.profil"))
