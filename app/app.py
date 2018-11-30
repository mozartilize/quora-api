import os.path
from quora import create_app

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
app = create_app('settings', root_path=root_path)
