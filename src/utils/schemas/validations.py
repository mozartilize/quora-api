from marshmallow import validate, ValidationError
from sqlalchemy import text, select

from utils.tables.repository import repo

not_blank = validate.Length(min=1, error='Field cannot be blank')


def unique(table, field, value):
    '''
    unique(Account, 'username', 'john')
    '''
    q = select([table.c.id])\
        .where(text('{0}=:{0}'.format(field))).params({field: value})
    if repo(q).fetchone():
        raise ValidationError(
            '{} already exists'.format(field.capitalize()), field)
