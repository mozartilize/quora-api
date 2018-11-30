import pytest
from flask import Flask

from accounts import passlib_ext


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_object({'TESTING': True})

    passlib_ext.init_app(app)

    yield app
