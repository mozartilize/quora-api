from sqlalchemy import select, insert, update
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
    ins = insert(accounts).values(**data)
    with db.engine.connect() as conn:
        return conn.execute(ins)


def activate_account(data):
    stmt = update(accounts)\
        .returning(accounts.c.id)\
        .where(accounts.c.id == data['uuid'])\
        .values(activated_at=data['activated_at'])
    with db.engine.connect() as conn:
        return conn.execute(stmt).fetchall()[0]
