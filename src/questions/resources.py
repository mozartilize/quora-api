from flask import request, url_for
from flask_restful import Resource, abort
from marshmallow import ValidationError
from sqlalchemy import insert
from utils.tables.repository import repo
from questions.schemas import AddQuestionSchema, AddAnswerSchema
from questions.tables import questions, answers


class QuestionListAPI(Resource):
    def get(self):
        pass

    def post(self):
        s = AddQuestionSchema()
        try:
            data = s.load(request.form or request.json)
            question_id = repo(
                insert(questions)\
                .values(**data)\
                .returning(questions.c.id))\
            .fetchone().id
            return {}, 201, \
                {"Location": url_for('.questionapi', id=question_id)}
        except ValidationError as e:
            return {"errors": e.messages}, 400


class QuestionAPI(Resource):
    def get(self, id):
        pass


class AnswerListAPI(Resource):
    def get(self, question_id):
        pass

    def post(self, question_id):
        s = AddAnswerSchema()
        try:
            data = s.load(request.form or request.json)
            answer_id = repo(
                insert(answers)\
                    .values(**data)\
                    .returning(answers.c.id)
                ).fetchone().id
            return {}, 201, \
                {"Location": url_for('.answerapi', id=answer_id)}
        except ValidationError as e:
            return {"errors": e.messages}, 400


class AnswerAPI(Resource):
    def get(self, id):
        pass