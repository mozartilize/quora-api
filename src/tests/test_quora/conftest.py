import pytest

from quora import create_app
from quora.tables import db


@pytest.fixture
def app():
    app = create_app('test_quora.settings')
    with app.app_context():
        with db.engine.connect() as conn:
            conn.execute('create EXTENSION if not EXISTS "uuid-ossp"')
        db.metadata.create_all(db.engine)

    def drop_db_tables(response_or_exc):
        db.engine.dispose()
        db.metadata.drop_all(db.engine)
        return response_or_exc

    app.teardown_appcontext(drop_db_tables)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
