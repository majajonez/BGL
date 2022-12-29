from flask import (
    Blueprint, render_template
)
from flask import Flask

from flaskr import db, auth
from flaskr.auth import login_required

config = {
    "SECRET_KEY":'dev'
}
app = Flask(__name__)
app.config.from_mapping(config)

bp = Blueprint('main', __name__)

@bp.route('/profil')
@login_required
def profil():
    return render_template('main/profil.html')


if __name__ == '__main__':
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(bp)
    app.add_url_rule('/', endpoint='auth.login')

    app.run()

