from datetime import datetime
from sqlalchemy import Table, Column, DateTime, text, TIMESTAMP
from quora import db

meta = db.metadata

timestamps = (
    Column('created_at', TIMESTAMP(True),
           nullable=False,
           default=datetime.utcnow(),
           server_default=text('statement_timestamp()')),
    Column('updated_at', TIMESTAMP(True),
           onupdate=datetime.utcnow(),
           server_onupdate=text('statement_timestamp()')),
)
