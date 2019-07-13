from datetime import datetime
from sqlalchemy import Column, Integer, text, TIMESTAMP

int_id = lambda: Column('id', Integer, primary_key=True)

timestamps = lambda: (
    Column('created_at', TIMESTAMP,
           nullable=False,
           default=datetime.utcnow(),
           server_default=text('statement_timestamp()')),
    Column('updated_at', TIMESTAMP,
           onupdate=datetime.utcnow()),
)
