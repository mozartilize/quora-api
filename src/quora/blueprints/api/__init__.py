from flask import Blueprint
from flask_restful import Api

from .resources import (
    accounts,
    auth,
)


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

api.add_resource(accounts.AccountListAPI, '/accounts')
api.add_resource(accounts.AccountAPI, '/accounts/<int:id>')

api.add_resource(auth.AuthApi, '/auth')
