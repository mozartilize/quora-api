from importlib import import_module
from flask import Blueprint
from flask_restful import Api


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

modules = ['accounts', 'questions']

for module in modules:
    routes = import_module(module + '.routes').routes
    for r in routes:
        api.add_resource(*r)
