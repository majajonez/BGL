from flask import (
    Blueprint, render_template, request, redirect, url_for, flash
)
from flask import Flask

from flaskr import db, auth
from flaskr.auth import login_required
from flaskr.db import get_db

config = {
    "SECRET_KEY": 'dev'
}
app = Flask(__name__)
app.config.from_mapping(config)

bp = Blueprint('main', __name__)


@bp.route('/profil')
@login_required
def profil():
    return render_template('main/profil.html')


@bp.route('/main_page', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        return redirect(url_for('main.event'))

    return render_template('main/main_page.html')


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
        error = None
        if user and title and description and when and where and the_number_of_seats:
            conn = get_db()
            cur = conn.cursor()
            try:
                cur.execute('INSERT INTO wydarzenia (login, jaka_gra, opis, kiedy, gdzie, ile_miejsc)'
                            'VALUES (%s, %s, %s, %s, %s, %s)',
                            (user,
                             title,
                             description,
                             when,
                             where,
                             the_number_of_seats)
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


if __name__ == '__main__':
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='main.profil')

    app.run()
