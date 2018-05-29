from sqlalchemy import Table, Column, Integer, Text, \
    ForeignKey, text
from sqlalchemy.dialects import postgresql
from utils.tables.mixins import int_id, timestamps, meta


# allow null - as anonymous
account_fk = lambda: Column('account_id', postgresql.UUID(),
                            ForeignKey("accounts.id"))


questions = Table('questions', meta,
    int_id(),
    account_fk(),
    Column('title', Text, nullable=False),
    Column('content', Text),
    *timestamps()
)


answers = Table('answers', meta,
    int_id(),
    account_fk(),
    Column('question_id', Integer, ForeignKey("questions.id"), nullable=False),
    Column('content', Text, nullable=False),
    *timestamps()
)
