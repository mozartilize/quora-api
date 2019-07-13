from sqlalchemy import (
    Table, Column, String, DateTime, Boolean
)
from db import meta
from db.mixins import timestamps, int_id


tokens = Table(
    "tokens",
    meta,
    int_id(),
    Column("jti", String(36), nullable=False),
    Column("token_type", String(10), nullable=False),
    Column("user_identity", String(50), nullable=False),
    Column("revoked", Boolean, nullable=False),
    Column("expired_at", DateTime, nullable=False),
    *timestamps(),
)
