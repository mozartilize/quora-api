from sqlalchemy import Table, Column, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from quora import db, pw_context

from .mixins import timestamps

meta = db.metadata


def cal_pw_hash_max_length(ctx):
    """https://github.com/kvesteri/sqlalchemy-utils/blob/master/sqlalchemy_utils/types/password.py#L172-L189
    """
    # Calculate the largest possible encoded password.
    # name + rounds + salt + hash + ($ * 4) of largest hash
    max_lengths = [1024]
    for name in ctx.schemes():
        scheme = getattr(__import__('passlib.hash').hash, name)
        length = 4 + len(scheme.name)
        length += len(str(getattr(scheme, 'max_rounds', '')))
        length += (getattr(scheme, 'max_salt_size', 0) or 0)
        length += getattr(
            scheme,
            'encoded_checksum_size',
            scheme.checksum_size
        )
        max_lengths.append(length)

    # Return the maximum calculated max length.
    return max(max_lengths)

pw_hash_max_lenght = cal_pw_hash_max_length(pw_context)

accounts = Table('accounts', meta,
    Column('id', UUID, primary_key=True,
           server_default=text('uuid_generate_v4()')),
    Column('username', String(80), nullable=False, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('pw_hash', BYTEA(pw_hash_max_lenght), nullable=False),
    *timestamps
)
