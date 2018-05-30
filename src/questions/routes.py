from questions.resources import QuestionListAPI, QuestionAPI, \
    AnswerListAPI, AnswerAPI

routes = [
    (QuestionListAPI, '/questions'),
    (QuestionAPI, '/questions/<int:id>'),
    (AnswerListAPI, '/questions/<int:id>/answers'),
    (AnswerAPI, '/questions/<int:question_id>/answers/<int:id>'),
]
