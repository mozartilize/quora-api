import os.path
from flask import Flask, g
from flask_migrate import Migrate

from quora.tables import db
from accounts import passlib_ext


def create_app(setting_object):
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, root_path=root_path)
    app.config.from_object(setting_object)

    db.init_app(app)

    Migrate(app, db, directory=os.path.join(root_path, 'migrations'))

    passlib_ext.init_app(app)

    # blueprints
    from quora.api import api_bp  # noqa

    # blueprint registers
    app.register_blueprint(api_bp)

    return app
