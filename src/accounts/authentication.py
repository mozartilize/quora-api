from datetime import datetime
from flask import current_app
import jwt
from dateutil.relativedelta import relativedelta


def generate_activation_token(account_id, secs=15*60):
    payload = {
        'exp': datetime.utcnow() + relativedelta(seconds=secs),
        'sub': 'activation',
        'account_id': account_id,
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'])
