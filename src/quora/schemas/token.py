from datetime import datetime
import pytz
import jwt
from marshmallow import Schema, fields, post_load, validates, ValidationError
from flask import current_app
from sqlalchemy import select
from sqlalchemy.exc import DataError, ProgrammingError

from quora.tables import db, accounts
from quora.repository import repo


def verify_token(token, callback):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        return check_payload(callback, payload)
    except jwt.ExpiredSignatureError:
        return False, 'Token was expired'
    except jwt.DecodeError:
        return False, 'Invalid token'


def check_payload(callback, payload):
    """
    for replacing when testing with faked data
    """
    try:
        return callback(payload)
    except KeyError:
        return False, 'Missing account id', payload
    except (DataError, ProgrammingError):
        return False, 'Invalid token', payload


def verify_activation_token(token):
    def self_verify(payload):
        query = select([accounts.c.id, accounts.c.activated_at])\
            .where(accounts.c.id == payload['account_id'])
        acc = repo(query).fetchone()
        if acc:
            if acc.activated_at:
                return False, 'Account already activated', payload
            return True, '', payload
        else:
            return False, 'Invalid token', payload

    return verify_token(token, self_verify)


def verify_auth_token(token):
    def self_verify(payload):
        query = select([accounts.c.id])\
            .where(accounts.c.id == payload['account_id'])
        if repo(query).fetchone():
            return True, '', payload
        else:
            return False, 'Invalid token', payload
    return verify_token(token, self_verify)


class ActivationTokenSchema(Schema):
    token = fields.Str(required=True)

    @post_load
    def make_object(self, data):
        ok, message, payload = verify_activation_token(data['token'])
        if not ok:
            raise ValidationError(message, 'token')
        else:
            return {
                'uuid': payload['account_id'],
                'activated_at': datetime.now(tz=pytz.utc)
            }
