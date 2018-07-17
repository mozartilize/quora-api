import os
from os.path import join, dirname

try:
    from dotenv import load_dotenv

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except ImportError:
    pass

DEBUG = True if os.environ.get('DEBUG') == 'TRUE' else False

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PASSLIB_CONTEXT = {
    'schemes': ['pbkdf2_sha512', 'bcrypt'],
    'deprecated': ['auto'],
}

MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'localhost'
MAIL_PORT = os.environ.get('MAIL_PORT') or '1025'
