from flask import g
from flask_restful import Resource
from marshmallow import ValidationError

from quora.services.authentication import (
    auth,
    verify_auth_token,
    generate_auth_token,
)
from quora.schemas.account import LoginSchema
from quora.models import Account


@auth.verify_password
def verify_password(username_or_email_or_token, password):
    result = verify_auth_token(username_or_email_or_token)
    if result[0]:
        g.account_id = result[1]
        return True
    s = LoginSchema()
    try:
        result = s.load({
            'username_or_email': username_or_email_or_token,
            'password': password,
        }).data
        g.account_id = result['id']
        return True
    except ValidationError:
        return False


class AuthApi(Resource):
    decorators = [auth.login_required]

    def post(self):
        token = generate_auth_token(g.account_id)
        return {'token': token.decode('ascii')}, 201
