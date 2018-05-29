from quora import create_app


def test_config():
    assert create_app('tests.test_quora.settings').testing
