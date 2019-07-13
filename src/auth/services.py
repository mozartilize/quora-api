from sqlalchemy import select, or_
from db.repository import repo
from marshmallow.exceptions import ValidationError
from accounts import passlib_ext
from accounts.tables import accounts
from .tables import tokens


def is_token_revoked(decoded_token):
    jti = decoded_token['jti']
    stmt = select([tokens.c.id, tokens.c.revoked]).where(
        (tokens.c.jti == jti)
    )
    token = repo(stmt).fetchone()
    if not token:
        return True
    return token.revoked


def retrieve_account(username_or_email):
    stmt = select([
        accounts
    ]).where(
        or_(
            accounts.c.email == username_or_email,
            accounts.c.username == username_or_email
        )
    )
    return repo(stmt).fetchone()


def verify_password(pw, acc):
    try:
        if passlib_ext.crypt_ctx\
                .verify(pw, acc['pw_hash']):
            return {'id': acc['id']}
        raise ValidationError('Password is incorrect', 'password')
    except (TypeError, ValueError):
        raise ValidationError('Password is incorrect', 'password')
