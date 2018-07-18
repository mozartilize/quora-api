from questions.resources import QuestionListAPI, QuestionAPI, \
    AnswerListAPI, AnswerAPI

routes = [
    (QuestionListAPI, '/questions'),
    (QuestionAPI, '/questions/<id>'),
    (AnswerListAPI, '/questions/<question_id>/answers'),
    (AnswerAPI, '/questions/<question_id>/answers/<id>', '/answers/<id>'),
]
