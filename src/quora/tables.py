from flask_sqlalchemy import SQLAlchemy
from utils.tables.mixins import meta

db = SQLAlchemy(metadata=meta)
