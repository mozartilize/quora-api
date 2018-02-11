from flask import request, abort
from flask_restful import Resource

from quora import db, auth
from quora.models import Account
from quora.schemas.account import (
    AccountSchema,
    RegistrationSchema,
)


class AccountAPI(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        acc = Account.query.get(id)
        if not acc:
            return abort(404)
        else:
            acc_schema = AccountSchema()
            return acc_schema.dump(acc).data, 200

    def put(self):
        pass


class AccountListAPI(Resource):
    def post(self):
        rs = RegistrationSchema()
        result = rs.load(request.json)
        if result.errors:
            return {'message': '', 'errors': result.errors}, 400
        else:
            acc = Account(**result.data)
            db.session.add(acc)
            db.session.commit()
            acc_schema = AccountSchema()
            return acc_schema.dump(acc).data, 201
