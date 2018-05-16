from datetime import datetime
import jwt
import pytz
from flask import request, url_for, current_app, g
from flask_restful import Resource, abort
from sqlalchemy import select
from marshmallow.exceptions import ValidationError

from accounts.authentication import (
    auth,
    generate_auth_token,
    generate_activation_token,
)
from accounts.tables import accounts
from accounts.schemas import AccountSchema, RegistrationSchema, \
    ActivationTokenSchema
from accounts.repository import regist_account, activate_account
from utils.tables.repository import repo


class AccountAPI(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        s = AccountSchema()
        q = select([accounts.c[field] for field in s.fields.keys()])\
            .where(accounts.c.id == str(id))
        acc = repo(q).fetchone()
        if not acc:
            return abort(404)
        else:
            return s.dump(acc), 200

    def put(self):
        pass


class AccountActivationAPI(Resource):
    def get(self, id):
        q = select([accounts.c.id, accounts.c.activated_at])\
            .where(accounts.c.id == str(id))
        acc = repo(q).fetchone()
        if not acc:
            return abort(404)
        elif acc and not acc.activated_at:
            return abort(400)
        else:
            token = generate_activation_token(acc.id)
            return {'token': token}, 200

    def post(self):
        s = ActivationTokenSchema()
        try:
            data = s.load(request.json or request.form)
            acc = activate_account(data)
            return {}, \
                200, \
                {'Location': url_for('.accountapi', id=acc.id)}
        except ValidationError as e:
            return {'message': '', 'errors': e.messages}, 400



class AccountListAPI(Resource):
    def post(self):
        rs = RegistrationSchema()
        try:
            data = rs.load(request.json)
            result = regist_account(data)
            uuid = result.inserted_primary_key[0]
            return {'id': uuid}, \
                201, \
                {'Location': url_for('.accountapi', id=uuid)}
        except ValidationError as e:
            return {'message': '', 'errors': e.messages}, 400


class AuthAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = generate_auth_token(g.account_id)
        return {'token': token.decode('ascii')}
