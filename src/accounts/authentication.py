from flask import current_app, g
import jwt
import datetime
from dateutil.relativedelta import relativedelta
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from marshmallow.exceptions import ValidationError

from accounts.schemas import LoginSchema, verify_auth_token


def generate_auth_token(account_id, secs=600):
    payload = {
        'exp': datetime.datetime.utcnow() + relativedelta(seconds=secs),
        'sub': 'auth',
        'account_id': account_id,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'])


def generate_activation_token(account_id, secs=15*60):
    payload = {
        'exp': datetime.datetime.utcnow() + relativedelta(seconds=secs),
        'sub': 'activation',
        'account_id': account_id,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'])


basic_auth = HTTPBasicAuth()
auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username_or_email, password):
    s = LoginSchema()
    try:
        data = s.load({
            'username_or_email': username_or_email,
            'password': password,
        })
        g.account_id = data['id']
        return True
    except ValidationError:
        return False


@auth.verify_token
def verify_token(token):
    result = verify_auth_token(token)
    if result[0]:
        g.account_id = result[1]
        return True
    return False
