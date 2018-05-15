from flask import Blueprint
from flask_restful import Api

from accounts.resources import AccountListAPI, AccountAPI, \
    AccountActivationAPI, AuthAPI


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

api.add_resource(AccountListAPI, '/accounts')
api.add_resource(AccountActivationAPI, '/accounts', 'accounts/<uuid:id>')
api.add_resource(AccountAPI, '/accounts/<uuid:id>')

api.add_resource(AuthAPI, '/auth')
