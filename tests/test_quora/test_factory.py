import os.path
from quora import create_app


def test_config():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    assert create_app('test_quora.settings', root_path=root_path).testing
