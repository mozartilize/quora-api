from marshmallow import validate, ValidationError
from sqlalchemy import text, select

from quora.tables import db

not_blank = validate.Length(min=1, error='Field cannot be blank')


def unique(table, field, value):
    '''
    unique(Account, 'username', 'john')
    '''
    q = select([table.c.id])\
        .where(text('{0}=:{0}'.format(field))).params({field: value})
    with db.engine.connect() as conn:
        if conn.execute(q).fetchone():
            raise ValidationError(
                '{} already exists'.format(field.capitalize()), field)
