from datetime import datetime
from sqlalchemy import insert
from flask_jwt_extended import decode_token

from db.repository import repo

from .tables import tokens


def store_refresh_token(token, identity_claim):
    decoded_token = decode_token(token)
    q = insert(tokens).values(
        jti=decoded_token["jti"],
        token_type=decoded_token["type"],
        user_identity=decoded_token[identity_claim],
        revoked=False,
        expired_at=datetime.fromtimestamp(decoded_token['exp'])
    )
    repo(q)


def revoke_refresh_token(jti, uuid):
    stmt = tokens.update().values(revoked=True).where(
        (tokens.c.jti == jti)
        & (tokens.c.user_identity == uuid)
        & (tokens.c.revoked.is_(False))
    ).returning(tokens.c.id)
    return repo(stmt).fetchone()
