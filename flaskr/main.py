import os
from flask import Flask
from flaskr import db, auth, api


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config = {
        "SECRET_KEY": 'dev',
        'DB_URI': os.path.join(app.instance_path, 'flaskr.sqlite'),
    }
    app.config.from_mapping(config)
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='main.profil')
    db.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
