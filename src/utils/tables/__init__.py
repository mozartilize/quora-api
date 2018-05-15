from flask import current_app, _app_ctx_stack as stack

def get_db():
    ctx = stack.top
    if ctx is not None:
        return current_app.extensions['sqlalchemy'].db
