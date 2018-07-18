from questions.resources import QuestionListAPI, QuestionAPI, \
    AnswerListAPI, AnswerAPI

routes = [
    (QuestionListAPI, '/questions'),
    (QuestionAPI, '/questions/<string:id>'),
    (AnswerListAPI, '/questions/<string:question_id>/answers'),
    (AnswerAPI, '/questions/<string:question_id>/answers/<string:id>', '/answers/<string:id>'),
]
