from flask import g
from flask_restful import Resource
from marshmallow import ValidationError

from quora import auth
from quora.schemas.account import LoginSchema
from quora.models import Account


@auth.verify_password
def verify_password(username_or_email_or_token, password):
    acc = Account.verify_auth_token(username_or_email_or_token)
    if not acc:
        s = LoginSchema(strict=True)
        try:
            result = s.load({
                'username_or_email': username_or_email_or_token,
                'password': password,
            })
            acc = result.data
        except ValidationError:
            return False
    g.account = acc
    return True


class AuthApi(Resource):
    decorators = [auth.login_required]

    def post(self):
        token = g.account.generate_auth_token()
        return {'token': token.decode('ascii')}, 201
