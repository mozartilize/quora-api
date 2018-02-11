from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_httpauth import HTTPBasicAuth
from passlib.context import CryptContext


app = Flask(__name__)
app.config.from_object('settings')

pw_context = CryptContext(schemes=app.config['PASSLIB_SCHEMES'],
                          deprecated=app.config['PASSLIB_DEPRECATED'])

# regist third parties to app
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from quora import tables  # noqa, to maeke migate work

ma = Marshmallow(app)

auth = HTTPBasicAuth()

# blueprints
# from quora.blueprints.api import api_bp  # noqa

# blueprint registers
# app.register_blueprint(api_bp)


__all__ = [
    'app',
    'db',
]

@app.route('/')
def hello_world():
    return 'Hi you'
