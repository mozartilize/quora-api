from flask import url_for, current_app
from flask_restful import Resource
from sqlalchemy import insert
from db.repository import repo
from utils.decorators import hashids_decode
from utils.views.mixins import ResourceCreationMixin, SingleResourceDetailMixin
from questions.schemas import AddQuestionSchema, AddAnswerSchema
from questions.tables import questions, answers


class QuestionListAPI(ResourceCreationMixin, Resource):
    post_schema_class = AddQuestionSchema

    def get(self):
        pass

    def persist_record(self, data):
        return repo(
            insert(questions).values(**data).returning(questions.c.id)
        ).fetchone()

    def get_created_resource_url(self, instance, data, *args, **kwargs):
        hasher = current_app.extensions['hashids']
        return url_for(
            '.questionapi',
            id=hasher.encode(instance.id, 'questions')
        )


class QuestionAPI(SingleResourceDetailMixin, Resource):
    get_hashid_pks = ('id',)


class AnswerListAPI(ResourceCreationMixin, Resource):
    post_hashid_pks = ('question_id',)

    post_schema_class = AddAnswerSchema

    def post_schema_args(self, *args, **kwargs):
        return {"context": {"question_id": kwargs['question_id']}}

    def get_created_resource_url(self, instance, data, *args, **kwargs):
        hasher = current_app.extensions['hashids']
        return url_for(
            '.answerapi',
            id=hasher.encode(instance.id, 'answers'),
            question_id=hasher.encode(data['question_id'], 'questions')
        )

    def persist_record(self, data):
        return repo(
            insert(answers).values(**data).returning(answers.c.id)
        ).fetchone()

    @hashids_decode('question_id')
    def get(self, question_id):
        pass


class AnswerAPI(Resource):
    @hashids_decode('question_id', 'id')
    def get(self, id, question_id=None):
        return {'question_id': question_id, 'id': id}
