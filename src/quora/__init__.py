from flask import Flask, g
from flask_migrate import Migrate

from quora.tables import db
from quora.services.password import passlib_ext


def create_app(setting_object):
    app = Flask(__name__)
    app.config.from_object(setting_object)

    db.init_app(app)

    migrate = Migrate(app, db)

    passlib_ext.init_app(app)

    # blueprints
    from quora.blueprints.api import api_bp  # noqa

    # blueprint registers
    app.register_blueprint(api_bp)

    return app
