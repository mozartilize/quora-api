from flask import current_app, g
import jwt
import datetime
from dateutil.relativedelta import relativedelta
from flask_httpauth import HTTPBasicAuth
from marshmallow.exceptions import ValidationError

from quora.schemas.account import LoginSchema
from quora.schemas.token import verify_auth_token


def generate_auth_token(account_id, secs=600):
    payload = {
        'exp': datetime.datetime.utcnow() + relativedelta(seconds=secs),
        'account_id': account_id,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'])


auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_email_or_token, password):
    result = verify_auth_token(username_or_email_or_token)
    if result[0]:
        g.account_id = result[1]
        return True
    s = LoginSchema()
    try:
        data = s.load({
            'username_or_email': username_or_email_or_token,
            'password': password,
        })
        g.account_id = data['id']
        return True
    except ValidationError:
        return False
