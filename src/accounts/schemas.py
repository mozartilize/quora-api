from datetime import datetime
import pytz
import jwt
from flask import current_app, g
from marshmallow import fields, post_load, ValidationError, Schema
from sqlalchemy import or_, select
from sqlalchemy.exc import DataError, ProgrammingError

from accounts import passlib_ext
from accounts.tables import accounts
from utils.tables.repository import repo
from utils.schemas.validations import not_blank, unique


class AccountSchema(Schema):
    class Meta:
        fields = ('id', 'email', 'username',)


class RegistrationSchema(Schema):
    email = fields.Email(required=True,
                         validate=lambda value:
                             unique(accounts, 'email', value))
    username = fields.Str(required=True,
                          max_length=accounts.c.username.type.length,
                          validate=lambda value:
                              unique(accounts, 'username', value))
    password = fields.Str(required=True)

    @post_load
    def make_object(self, data):
        pw_hash = passlib_ext.crypt_ctx.hash(data['password']).encode('utf-8')
        del data['password']
        data['pw_hash'] = pw_hash
        return data


class LoginSchema(Schema):
    username_or_email = fields.Str(required=True, validate=not_blank)
    password = fields.Str(required=True, validate=not_blank)

    @post_load
    def make_object(self, data):
        query = select([accounts.c.id, accounts.c.pw_hash])\
            .where(or_(
                accounts.c.username == data['username_or_email'],
                accounts.c.email == data['username_or_email']
            ))
        acc = repo(query).fetchone()
        if acc:
            try:
                if passlib_ext.crypt_ctx.verify(data['password'], acc['pw_hash']):
                    return {'id': acc['id']}
                else:
                    raise ValidationError('Password is incorrect', 'password')
            except (TypeError, ValueError):
                raise ValidationError('Password is incorrect', 'password')
        else:
            raise ValidationError('Not found', 'username_or_email')


def verify_token(token, callback):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'])
        return check_payload(callback, payload)
    except jwt.ExpiredSignatureError:
        return False, 'Token was expired'
    except jwt.DecodeError:
        return False, 'Invalid token'


def check_payload(callback, payload):
    """
    for replacing when testing with faked data
    """
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


def verify_auth_token(token):
    def self_verify(payload):
        if payload.get('sub') == 'auth':
            query = select([accounts.c.id])\
                .where(accounts.c.id == payload['account_id'])
            if repo(query).fetchone():
                return True, '', payload
        return False, 'Invalid token', payload
    return verify_token(token, self_verify)


class ActivationTokenSchema(Schema):
    token = fields.Str(required=True)

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
