import pytest

from quora import create_app
from quora.tables import db


@pytest.fixture
def app():
    app = create_app('tests.test_quora.settings')
    with app.app_context():
        db.metadata.create_all(db.engine)

    def drop_db_tables():
        db.engine.dispose()
        db.metadata.drop_all(db.engine)

    app.teardown_appcontext(drop_db_tables)

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
