from sqlalchemy import Table, Column, String, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from db import meta
from db.mixins import timestamps


accounts = Table(
    'accounts',
    meta,
    Column('id', UUID, primary_key=True,
           server_default=text('uuid_generate_v4()')),
    Column('username', String(80), nullable=False, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('pw_hash', BYTEA),
    Column('activated_at', TIMESTAMP),
    *timestamps()
)
