from flask import current_app
import jwt
import datetime
from dateutil.relativedelta import relativedelta


class Account:
    def __repr__(self):
        return '<User %r>' % self.username

    def generate_auth_token(self):
        payload = {
            'exp': datetime.datetime.utcnow() + relativedelta(seconds=600),
            'account_id': self.id,
        }
        return jwt.encode(payload, current_app.config['SECRET_KEY'])

    @staticmethod
    def verify_auth_token(token):
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'])
            try:
                return Account.query.get(payload['account_id'])
            except KeyError:
                return None
        except jwt.ExpiredSignatureError:
            return None
        except jwt.DecodeError:
            return None
