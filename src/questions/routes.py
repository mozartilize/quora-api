from questions.resources import QuestionListAPI, QuestionAPI, \
    AnswerListAPI, AnswerAPI

routes = [
    (AnswerAPI, '/questions/<question_id>/answers/<id>'),
    (AnswerListAPI, '/questions/<question_id>/answers'),
    (QuestionAPI, '/questions/<id>'),
    (QuestionListAPI, '/questions'),
]
