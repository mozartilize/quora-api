from marshmallow import fields, post_load, ValidationError
from sqlalchemy import or_

from quora import ma
from quora.models import Account

from .validations import not_blank, unique


class AccountSchema(ma.ModelSchema):
    class Meta:
        model = Account
        fields = ('id', 'email', 'username',)


class RegistrationSchema(ma.Schema):
    email = fields.Email(required=True,
                         validate=lambda value:
                             unique(Account, 'email', value))
    username = fields.Str(required=True,
                          max_length=Account.USERNAME_MAX_LENGTH,
                          validate=lambda value:
                              unique(Account, 'username', value))
    password = fields.Str(required=True)


class LoginSchema(ma.Schema):
    username_or_email = fields.Str(required=True, validate=not_blank)
    password = fields.Str(required=True, validate=not_blank)

    @post_load
    def make_object(self, data):
        acc = Account.query.filter(
            or_(Account.username == data['username_or_email'],
                Account.email == data['username_or_email'])).first()
        if acc and acc.password == data['password']:
            return acc
        elif acc:
            raise ValidationError('Password is incorrect', 'password')
        else:
            raise ValidationError('Not found', 'username_or_email')
