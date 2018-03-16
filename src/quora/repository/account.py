from sqlalchemy import select
from quora.tables import db, accounts


def all(columns=[]):
    if not columns:
        selection = [accounts]
    else:
        selection = [accounts.c[col] for col in columns]
    with db.engine.connect() as conn:
        query = select(selection)
        return conn.execute(query).fetchall()


def regist_account(data):
    ins = accounts.insert().values(**data)
    with db.engine.connect() as conn:
        return conn.execute(ins)
