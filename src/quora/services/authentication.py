from flask import current_app, g
import jwt
import datetime
from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from flask_httpauth import HTTPBasicAuth
from quora.tables import db, accounts

auth = HTTPBasicAuth()


def generate_auth_token(account_id):
    payload = {
        'exp': datetime.datetime.utcnow() + relativedelta(seconds=600),
        'account_id': account_id,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'])


def verify_auth_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        try:
            query = select([accounts.c.id])\
                .where(accounts.c.id == payload['account_id'])
            with db.engine.connect() as conn:
                if conn.execute(query).fetchone():
                    return (True, payload['account_id'])
                else:
                    return (False, 'Account not found')
        except KeyError:
            return (False, 'Account Id is not in payload')
    except jwt.ExpiredSignatureError:
        return (False, 'Token was expired')
    except jwt.DecodeError:
        return (False, 'Invalid token')
