from flask_sqlalchemy import SQLAlchemy
from utils.tables.mixins import meta

db = SQLAlchemy(metadata=meta)

from accounts.tables import accounts
from questions.tables import questions, answers
