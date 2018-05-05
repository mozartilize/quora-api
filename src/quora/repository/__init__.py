from quora.tables import db


def repo(query):
    with db.engine.connect() as conn:
        return conn.execute(query)
