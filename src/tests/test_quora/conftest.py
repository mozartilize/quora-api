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

    yield app

    with app.app_context():
        db.engine.dispose()
        db.metadata.drop_all(db.engine)


@pytest.fixture
def client(app):
    return app.test_client()
