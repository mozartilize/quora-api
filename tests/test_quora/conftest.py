import os.path
import pytest

from quora import create_app
from db import db


@pytest.fixture
def app():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    app = create_app('test_quora.settings', root_path=root_path)
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
