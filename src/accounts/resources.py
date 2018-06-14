from datetime import datetime
import jwt
import pytz
from flask import request, url_for, current_app, g
from flask_restful import Resource, abort
from sqlalchemy import select
from marshmallow.exceptions import ValidationError

from utils.tables.repository import repo
from accounts.authentication import auth, generate_auth_token, \
    generate_activation_token
from accounts.tables import accounts
from accounts.schemas import AccountSchema, RegistrationSchema, \
    ActivationTokenSchema
from accounts.repository import regist_account, activate_account
from accounts import mailer


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
    def get(self):
        s = ActivationTokenSchema()
        try:
            data = s.load(request.args)  # get token from query params
            acc = activate_account(data)
            return {}, \
                200, \
                {'Location': url_for('.accountapi', id=acc.id)}
        except ValidationError as e:
            return {'message': '', 'errors': e.messages}, 400


class AccountActivationTokenAPI(Resource):
    def post(self, id):
        q = select([accounts.c.id,
                    accounts.c.email,
                    accounts.c.activated_at])\
            .where(accounts.c.id == str(id))
        acc = repo(q).fetchone()
        if not acc:
            return abort(404)
        elif acc and acc.activated_at:
            return abort(400)
        else:
            token = generate_activation_token(acc.id)
            mailer.send_activation_token(acc.email, token)
            return '', 202


class AccountListAPI(Resource):
    def post(self):
        rs = RegistrationSchema()
        try:
            data = rs.load(request.form or request.json)
            acc = regist_account(data)
            token = generate_activation_token(acc.id)
            mailer.send_activation_token(acc.email, token)
            return {'id': acc.id}, \
                201, \
                {'Location': url_for('.accountapi', id=acc.id)}
        except ValidationError as e:
            return {'message': '', 'errors': e.messages}, 400


class AuthAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        token = generate_auth_token(g.account_id)
        return {'token': token.decode('ascii')}
