from flask import request, url_for, current_app
from flask_restful import Resource, abort
from marshmallow import ValidationError
from sqlalchemy import insert
from utils.tables.repository import repo
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

    # def post(self):
    #     s = AddQuestionSchema()
    #     try:
    #         data = s.load(request.form or request.json)
    #         question_id = repo(
    #             insert(questions).values(**data).returning(questions.c.id)
    #         ).fetchone().id
    #         return None, 201, \
    #             {"Location": url_for('.questionapi',
    #                                  id=current_app.extensions['hashids']
    #                                                .encode(question_id))}
    #     except ValidationError as e:
    #         return {"errors": e.messages}, 400


class QuestionAPI(SingleResourceDetailMixin, Resource):
    get_hashid_pks = ('id',)


class AnswerListAPI(Resource):
    @hashids_decode('question_id')
    def get(self, question_id):
        pass

    @hashids_decode('question_id')
    def post(self, question_id):
        s = AddAnswerSchema()
        try:
            data = s.load(request.form or request.json)
            answer_id = repo(
                insert(answers).values(**data).returning(answers.c.id)
            ).fetchone().id
            return None, 201, \
                {"Location": url_for('.answerapi',
                                     id=current_app.extensions['hashids']
                                                   .encode(answer_id))}
        except ValidationError as e:
            return {"errors": e.messages}, 400


class AnswerAPI(Resource):
    @hashids_decode('question_id', 'id')
    def get(self, id, question_id=None):
        return {'question_id': question_id, 'id': id}
