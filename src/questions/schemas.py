from marshmallow import Schema, fields


class AddQuestionSchema(Schema):
    account_id = fields.Int()
    title = fields.Str(required=True)
    content = fields.Str()


class AddAnswerSchema(Schema):
    account_id = fields.Int()
    content = fields.Str(required=True)
