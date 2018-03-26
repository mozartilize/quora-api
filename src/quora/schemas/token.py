from datetime import datetime
import pytz
import jwt
from marshmallow import Schema, fields, post_load, validates, ValidationError
from flask import current_app
from sqlalchemy import select
from sqlalchemy.exc import DataError, ProgrammingError

from quora.tables import db, accounts


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
            .where(accounts.c.id == payload['account_id'])
        with db.engine.connect() as conn:
            if conn.execute(query).fetchone():
                return True, '', payload
            else:
                return False, 'Invalid token', payload
    except KeyError:
        return False, 'Missing account id', payload
    except (DataError, ProgrammingError):
        return False, 'Invalid token', payload


def verify_activation_token(token):
    def self_verify(payload):
        try:
            query = select([accounts.c.id, accounts.c.activated_at])\
                .where(accounts.c.id == payload['account_id'])
            with db.engine.connect() as conn:
                acc = conn.execute(query).fetchone()
                if acc:
                    if acc.activated_at:
                        return False, 'Account already activated', payload
                    return True, '', payload
                else:
                    return False, 'Invalid token', payload
        except KeyError:
            return False, 'Missing account id', payload
        except (DataError, ProgrammingError):
            return False, 'Invalid token', payload

    return verify_token(token, self_verify)


def verify_auth_token(token, check_payload=check_payload):
    return verify_token(token, check_payload)


class ActivationTokenSchema(Schema):
    token = fields.Str(required=True)

    @validates('token')
    def validate_token(self, token):
        ok, message, payload = verify_activation_token(token)
        if not ok:
            raise ValidationError(message)
        else:
            self.payload = payload

    @post_load
    def make_object(self, data):
        return {
            'uuid': self.payload['account_id'],
            'activated_at': datetime.now(tz=pytz.utc)
        }
