from functools import wraps
from flask import current_app, g
import jwt
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.exc import DataError, ProgrammingError
from flask_httpauth import HTTPBasicAuth
from quora.tables import db, accounts

auth = HTTPBasicAuth()


def generate_auth_token(account_id, secs=600):
    payload = {
        'exp': datetime.datetime.utcnow() + relativedelta(seconds=secs),
        'account_id': account_id,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'])


def verify_token(token, callback, **kwargs):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        return callback(payload, **kwargs)
    except jwt.ExpiredSignatureError:
        return False, 'Token was expired'
    except jwt.DecodeError:
        return False, 'Invalid token'


def check_payload(payload):
    """
    for replacing when testing with faked data
    """
    try:
        query = select([accounts.c.id])\
            .where(accounts.c.id == str(payload['account_id']))
        with db.engine.connect() as conn:
            if conn.execute(query).fetchone():
                return True, payload['account_id']
            else:
                return False, 'Invalid token'
    except KeyError:
        return False, 'Missing account id'
    except (DataError, ProgrammingError):
        return False, 'Invalid token'


def verify_activation_token(token,
                            loaded_id=None,
                            check_payload=check_payload):
    def self_verify(payload, loaded_id):
        try:
            if loaded_id and loaded_id == payload['account_id']:
                return True, payload['account_id']
            elif loaded_id:
                return False, 'Invalid token'
        except KeyError:
            return False, 'Missing account id'
        return check_payload(payload)

    return verify_token(token, self_verify, loaded_id=loaded_id)


def verify_auth_token(token, check_payload=check_payload):
    return verify_token(token, check_payload)
