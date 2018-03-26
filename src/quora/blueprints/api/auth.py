from flask import g
from flask_restful import Resource
from marshmallow import ValidationError

from quora.services.authentication import (
    auth,
    generate_auth_token,
)
from quora.schemas.account import LoginSchema
from quora.models import Account


class AuthApi(Resource):
    decorators = [auth.login_required]

    def post(self):
        token = generate_auth_token(g.account_id)
        return {'token': token.decode('ascii')}, 201
