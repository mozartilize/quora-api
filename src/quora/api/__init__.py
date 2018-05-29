from flask import Blueprint
from flask_restful import Api

from accounts.resources import AccountListAPI, AccountAPI, \
    AccountActivationAPI, AuthAPI
from questions.resources import QuestionAPI, QuestionListAPI, \
    AnswerAPI, AnswerListAPI


api_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(api_bp)

api.add_resource(AccountListAPI, '/accounts')
api.add_resource(AccountActivationAPI, '/accounts', 'accounts/<uuid:id>')
api.add_resource(AccountAPI, '/accounts/<uuid:id>')

api.add_resource(AuthAPI, '/auth')

api.add_resource(QuestionListAPI, '/questions')
api.add_resource(QuestionAPI, '/questions/<int:id>')
api.add_resource(AnswerListAPI, '/questions/<int:id>/answers')
api.add_resource(AnswerAPI, '/questions/<int:question_id>/answers/<int:id>')
