from importlib import import_module
from flask import Blueprint
from flask_restful import Api
from auth.resources import auth, refresh, me, verify, revoke

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

modules = ['accounts', 'questions']

for module in modules:
    routes = import_module(module + '.routes').routes
    for r in routes:
        api.add_resource(*r)


api_bp.add_url_rule(
    "/auth", view_func=auth, methods=["POST"]
)
api_bp.add_url_rule(
    "/auth/refresh", view_func=refresh, methods=["POST"],
)
api_bp.add_url_rule(
    "/auth/me", view_func=me
)

api_bp.add_url_rule(
    "/auth/verify", view_func=verify
)

api_bp.add_url_rule(
    "/auth/revoke", view_func=revoke, methods=["PUT"]
)
