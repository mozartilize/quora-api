from marshmallow import validate, ValidationError
from sqlalchemy import text

not_blank = validate.Length(min=1, error='Field cannot be blank')


def unique(model_cls, field, value):
    '''
    unique(Account, 'username', 'john')
    '''
    obj = model_cls.query.filter(
        text('{0}=:{0}'.format(field))
        ).params({field: value}).first()
    if obj:
        raise ValidationError(
            '{} already exists'.format(field.capitalize()),
            field)
