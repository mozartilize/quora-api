from datetime import datetime
import pytz
import jwt
from flask import current_app
from marshmallow import fields, post_load, ValidationError, Schema, \
    validates, validate, EXCLUDE
from sqlalchemy import select
from sqlalchemy.exc import DataError, ProgrammingError
from email.utils import parseaddr
from flask_mail import force_text

from accounts import passlib_ext
from accounts.tables import accounts
from db.repository import repo
from utils.schemas.validations import not_blank, unique


class AccountSchema(Schema):
    class Meta:
        fields = ('id', 'email', 'username',)
        unknown = EXCLUDE


class RegistrationSchema(Schema):
    email = fields.Email(
        validate=lambda value: unique(accounts, 'email', value)
    )
    username = fields.Str(
        required=True, max_length=accounts.c.username.type.length,
        validate=[
            not_blank,
            lambda value: unique(accounts, 'username', value),
        ])
    password = fields.Str(required=True, validate=not_blank)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data):
        pw_hash = passlib_ext.crypt_ctx.hash(data['password']).encode('utf-8')
        del data['password']
        data['pw_hash'] = pw_hash
        return data


def verify_token(token, callback):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        return check_payload(callback, payload)
    except jwt.ExpiredSignatureError:
        return False, 'Token was expired'
    except jwt.DecodeError:
        return False, 'Invalid token'


def check_payload(callback, payload):
    try:
        return callback(payload)
    except KeyError:
        return False, 'Missing account id', payload
    except (DataError, ProgrammingError):
        return False, 'Invalid token', payload


def verify_activation_token(token):
    def self_verify(payload):
        if payload.get('sub') == 'activation':
            query = select([accounts.c.id, accounts.c.activated_at])\
                .where(accounts.c.id == payload['account_id'])
            acc = repo(query).fetchone()
            if acc:
                if acc.activated_at:
                    return False, 'Account already activated', payload
                return True, '', payload
        return False, 'Invalid token', payload

    return verify_token(token, self_verify)


class ActivationTokenSchema(Schema):
    token = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_object(self, data):
        ok, message, payload = verify_activation_token(data['token'])
        if not ok:
            raise ValidationError(message, 'token')
        else:
            return {
                'uuid': payload['account_id'],
                'activated_at': datetime.now(tz=pytz.utc)
            }


class ClientMailContextSchema(Schema):
    subject = fields.Str(required=True, validate=not_blank)
    sender = fields.Str(required=True, validate=not_blank)
    url = fields.Url(required=True)

    class Meta:
        unknown = EXCLUDE

    @validates('subject')
    def validate_subject(self, value):
        if any(char in value for char in ['\r', '\n', '\r\n']):
            raise ValidationError('Subject should not contain newline')

    @validates('sender')
    def validate_sender(self, value):
        _, addr = parseaddr(force_text(value))
        validate.Email()(addr)
