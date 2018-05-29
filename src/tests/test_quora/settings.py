DEBUG = True
TESTING = True

SECRET_KEY = 'hey there'

SQLALCHEMY_DATABASE_URI = "postgresql://quora:quora@localhost:5001/quora_testing"
SQLALCHEMY_TRACK_MODIFICATIONS = False

PASSLIB_CONTEXT = {
    'schemes': ['pbkdf2_sha512', 'bcrypt'],
    'deprecated': ['auto'],
}
