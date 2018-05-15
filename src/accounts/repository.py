from sqlalchemy import select, insert, update
from utils.tables.repository import repo
from accounts.tables import accounts


def all(columns=[]):
    if not columns:
        selection = [accounts]
    else:
        selection = [accounts.c[col] for col in columns]
    query = select(selection)
    return repo(query).fetchall()


def regist_account(data):
    ins = insert(accounts).values(**data)
    return repo(ins)


def activate_account(data):
    stmt = update(accounts)\
        .returning(accounts.c.id)\
        .where(accounts.c.id == data['uuid'])\
        .values(activated_at=data['activated_at'])
    return repo(stmt).fetchall()[0]
