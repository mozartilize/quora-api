from datetime import datetime
import jwt
import pytz
from flask import request, abort, url_for, current_app
from flask_restful import Resource
from sqlalchemy import select
from marshmallow.exceptions import ValidationError

from quora.services.authentication import (
    auth,
    verify_activation_token,
    generate_auth_token,
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
    def get(self, id):
        q = select([accounts.c.id])\
            .where(accounts.c.id == str(id))
        with db.engine.connect() as conn:
            acc = conn.execute(q).fetchone()
            if not acc:
                return abort(404)
            else:
                token = generate_auth_token(acc.id, secs=15*60)
                return {'token': token}, 200

    def post(self):
        token = request.json.get('token')
        if not token:
            return {'message': 'Missing token'}, 400
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        try:
            q = select([accounts.c.id])\
                .where(accounts.c.id == payload['account_id'])
        except KeyError:
            return {'message': 'Invalid token'}, 400
        with db.engine.connect() as conn:
            acc = conn.execute(q).fetchone()
            if acc:
                stmt = accounts.update()\
                    .where(accounts.c.id == acc.id)\
                    .values(activated_at=datetime.now(tz=pytz.utc))
                conn.execute(stmt)
                return {}, \
                    200, \
                    {'Location': url_for('.accountapi', id=acc.id)}



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
