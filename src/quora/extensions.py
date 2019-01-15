from flask import current_app as app, _app_ctx_stack as stack
from hashids import Hashids


class HashId(object):
    def __init__(self, app=None, resource_ids=None):
        self.app = app
        if app is not None and resource_ids is not None:
            self.init_app(app, resource_ids)

    def init_app(self, app, resource_ids):
        self.app = app
        self.resource_ids = resource_ids
        app.extensions['hashids'] = self

    @property
    def hasher(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(self, '_hasher'):
                self._hasher = Hashids(salt=app.config['SECRET_KEY'],
                                       min_length=10)
            return self._hasher

    def encode(self, val, resource_name):
        return self.hasher.encode(val, self.resource_ids[resource_name].value)

    def decode(self, val):
        return self.hasher.decode(val)[0]
