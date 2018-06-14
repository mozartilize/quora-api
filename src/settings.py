import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DEBUG = True if os.environ.get('DEBUG') == 'TRUE' else False

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PASSLIB_CONTEXT = {
    'schemes': ['pbkdf2_sha512', 'bcrypt'],
    'deprecated': ['auto'],
}

MAIL_SERVER = 'localhost'
MAIL_PORT = '1025'
