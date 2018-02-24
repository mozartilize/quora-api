from flask import g
from marshmallow import fields, post_load, ValidationError, Schema
from sqlalchemy import or_, select
from quora.tables import db, accounts
from quora.services.password import passlib_ext
from .validations import not_blank, unique


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
        with db.engine.connect() as conn:
            acc = conn.execute(query).fetchone()
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
