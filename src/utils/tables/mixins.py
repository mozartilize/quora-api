from datetime import datetime
from sqlalchemy import Table, Column, DateTime, text, TIMESTAMP, MetaData


meta = MetaData()


timestamps = (
    Column('created_at', TIMESTAMP(True),
           nullable=False,
           default=datetime.utcnow(),
           server_default=text('statement_timestamp()')),
    Column('updated_at', TIMESTAMP(True),
           onupdate=datetime.utcnow(),
           server_onupdate=text('statement_timestamp()')),
)
