from flask import request, abort, url_for
from flask_restful import Resource
from sqlalchemy import select
from marshmallow.exceptions import ValidationError

from quora.services.authentication import (
    auth,
    verify_activation_token,
)
from quora.tables import db, accounts
from quora.schemas.account import (
    AccountSchema,
    RegistrationSchema,
)
from quora.repository.account import regist_account


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
    def get(self, id, token):
        q = select([accounts.c.id])\
            .where(accounts.c.id == str(id))
        with db.engine.connect() as conn:
            acc = conn.execute(q).fetchone()
            if not acc:
                return abort(404)
            else:
                pass


class AccountListAPI(Resource):
    def post(self):
        rs = RegistrationSchema()
        try:
            data = rs.load(request.json)
            result = regist_account(data)
            uuid = result.inserted_primary_key[0]
            return {'id': uuid}, \
                201, \
                {'Location': url_for('api.accountapi', id=uuid)}
        except ValidationError as e:
            return {'message': '', 'errors': e.messages}, 400
