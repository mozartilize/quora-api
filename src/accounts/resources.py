from flask import request, url_for, g
from flask_restful import Resource, abort
from sqlalchemy import select
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import get_jwt_identity

from db.repository import repo
from accounts.authentication import generate_activation_token
from accounts.tables import accounts
from accounts.schemas import AccountSchema, RegistrationSchema, \
    ActivationTokenSchema, ClientMailContextSchema
from accounts.repository import regist_account, activate_account
from accounts import mailer


class AccountAPI(Resource):
    def get(self, uid=None):
        s = AccountSchema()
        q = select([accounts.c[field] for field in s.fields.keys()])\
            .where(accounts.c.id == (str(uid) if uid else g.account_id))
        acc = repo(q).fetchone()
        if not acc:
            return abort(404)
        else:
            return s.dump(acc), 200

    def put(self):
        pass


class AccountActivationTokenAPI(Resource):
    def get(self):
        s = ActivationTokenSchema()
        try:
            data = s.load(request.args)  # get token from query params
            acc = activate_account(data)
            return {}, \
                200, \
                {'Location': url_for('.accountapi', id=acc.id)}
        except ValidationError as e:
            return {
                'msg': 'Acount activation failed',
                'errors': e.messages
            }, 400

    # resend account activation
    def post(self):
        payload = request.form or request.json
        # logged in
        current_user = get_jwt_identity()
        if current_user:
            q = select([accounts.c.id,
                        accounts.c.email,
                        accounts.c.activated_at])\
                .where(accounts.c.id == current_user)
            acc = repo(q).fetchone()
        else:
            try:
                q = select([
                    accounts.c.id,
                    accounts.c.email,
                    accounts.c.activated_at
                ]).where(accounts.c.email == payload['email'])
                acc = repo(q).fetchone()
            except KeyError:
                return abort(400)
        if not acc:
            return abort(400)
        elif acc and acc.activated_at:
            return abort(400)
        else:
            try:
                cl_mail_ctx_sch = ClientMailContextSchema()
                mail_ctx = cl_mail_ctx_sch.load(payload)
                _send_activation_mail(acc, mail_ctx)
                return {}, 202
            except ValidationError as e:
                return {'errors': e.messages}, 400


class AccountListAPI(Resource):
    def post(self):
        rs = RegistrationSchema()
        cl_mail_ctx_sch = ClientMailContextSchema()
        try:
            payload = request.form or request.json
            acc_data = rs.load(payload)
            mail_ctx = cl_mail_ctx_sch.load(payload)
            acc = regist_account(acc_data)
            _send_activation_mail(acc, mail_ctx)
            return {'id': acc.id}, \
                201, \
                {'Location': url_for('.accountapi', id=acc.id)}
        except ValidationError as e:
            return {'msg': 'Create account failed', 'errors': e.messages}, 400


def _send_activation_mail(acc, mail_ctx):
    token = generate_activation_token(acc.id)
    mailer.send_activation_token(
        acc.email,
        mail_ctx['subject'],
        mail_ctx['sender'],
        mail_ctx['url'],
        token
    )
