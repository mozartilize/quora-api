from flask import current_app, _app_ctx_stack as stack
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

meta = MetaData()

db = SQLAlchemy(metadata=meta)


def get_db():
    ctx = stack.top
    if ctx is not None:
        return current_app.extensions['sqlalchemy'].db


__all__ = [meta, db, get_db]
