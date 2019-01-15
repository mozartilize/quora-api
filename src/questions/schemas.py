from marshmallow import Schema, fields, EXCLUDE, post_load


class AddQuestionSchema(Schema):
    account_id = fields.Int()
    title = fields.Str(required=True)
    content = fields.Str()

    class Meta:
        unknown = EXCLUDE


class AddAnswerSchema(Schema):
    account_id = fields.Int()
    content = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def post_load(self, data):
        data['question_id'] = self.context['question_id']
        return data
