from sqlalchemy import (
    Table, Column,
    Integer, String, TIMESTAMP,
    text,
)
from sqlalchemy.dialects.postgresql import UUID, BYTEA
from utils.tables.mixins import timestamps, meta


accounts = Table('accounts', meta,
    Column('id', UUID, primary_key=True,
           server_default=text('uuid_generate_v4()')),
    Column('username', String(80), nullable=False, unique=True),
    Column('email', String, nullable=False, unique=True),
    Column('pw_hash', BYTEA, nullable=False),
    Column('activated_at', TIMESTAMP),
    *timestamps
)
