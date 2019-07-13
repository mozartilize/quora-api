import os.path
from enum import IntEnum
from flask import Flask
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from db import db
from accounts import passlib_ext
from auth import jwt
from quora.extensions import HashId


class ResourceId(IntEnum):
    accounts = 1
    questions = 2
    answers = 4


def create_app(setting_object, root_path=None):
    app = Flask(__name__, root_path=root_path)
    app.config.from_object(setting_object)

    db.init_app(app)
    Migrate(app, db, directory=os.path.join(root_path, '../migrations'))
    Mail(app)

    CORS(app)

    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = "refresh"
    jwt.init_app(app)

    HashId(app, ResourceId)

    passlib_ext.init_app(app)

    # blueprints
    from quora.api import api_bp  # noqa

    # blueprint registers
    app.register_blueprint(api_bp)

    import accounts
    app.jinja_loader.searchpath.append(
        os.path.join(os.path.dirname(accounts.__file__), 'templates')
    )

    return app
