from flask import current_app, _app_ctx_stack as stack

from passlib.context import LazyCryptContext


class PassLib(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.config.setdefault('PASSLIB_CONTEXT', {
            'schemes': ['pbkdf2_sha512'],
        })

        app.extensions['passlib'] = self

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'passlib'):
            # TODO: do something?
            pass

    @property
    def crypt_ctx(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'passlib'):
                ctx.passlib = self
            return LazyCryptContext(**current_app.config['PASSLIB_CONTEXT'])
