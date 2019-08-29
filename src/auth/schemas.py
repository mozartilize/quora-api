from marshmallow import fields, post_load, ValidationError, Schema, \
    EXCLUDE
from utils.schemas.validations import not_blank
from .services import retrieve_account, verify_password


class LoginSchema(Schema):
    username_or_email = fields.Str(required=True, validate=not_blank)
    password = fields.Str(required=True, validate=not_blank)

    class Meta:
        unknown = EXCLUDE

    @staticmethod
    def retrieve_account(*args, **kwargs):
        raise NotImplementedError("Callback is not set.")

    @staticmethod
    def verify_password(*args, **kwargs):
        raise NotImplementedError("Callback is not set.")

    @classmethod
    def set_retrieve_account(cls, callback):
        cls.retrieve_account = callback

    @classmethod
    def set_verify_password(cls, callback):
        cls.verify_password = callback

    @post_load
    def make_object(self, data, **kwargs):
        acc = self.__class__.retrieve_account(
            username_or_email=data['username_or_email']
        )
        if acc:
            if self.__class__.verify_password(pw=data["password"], acc=acc):
                return {'id': acc.id}
            else:
                raise ValidationError('Password is incorrect', 'password')
        else:
            raise ValidationError('Not found', 'username_or_email')

    def handle_error(self, exc, data, **kwargs):
        raise ValidationError(
            {'_schema': 'Authentication failed'}, data, **kwargs)


LoginSchema.set_retrieve_account(retrieve_account)
LoginSchema.set_verify_password(verify_password)
