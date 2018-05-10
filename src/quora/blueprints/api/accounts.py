from datetime import datetime
import jwt
import pytz
from flask import request, abort, url_for, current_app
from flask_restful import Resource
from sqlalchemy import select
from marshmallow.exceptions import ValidationError

from quora.services.authentication import (
    auth,
    generate_auth_token,
    generate_activation_token,
)
from quora.tables import db, accounts
from quora.schemas.account import (
    AccountSchema,
    RegistrationSchema,
)
from quora.schemas.token import ActivationTokenSchema
from quora.repository.account import regist_account, activate_account


class AccountAPI(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        s = AccountSchema()
        q = select([accounts.c[field] for field in s.fields.keys()])\
            .where(accounts.c.id == str(id))
        with db.engine.connect() as conn:
            acc = conn.execute(q).fetchone()
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
        with db.engine.connect() as conn:
            acc = conn.execute(q).fetchone()
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
