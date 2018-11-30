from . import get_db


def repo(query):
    with get_db().engine.connect() as conn:
        return conn.execute(query)
