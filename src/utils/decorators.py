from flask import current_app
from functools import wraps
from flask_restful import abort


def hashids_decode(*pks):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            for varname in pks:
                try:
                    if kwargs[varname] is None:
                        continue
                    kwargs[varname] = current_app.extensions['hashids']\
                                                 .decode(kwargs[varname])[0]
                except IndexError:
                    return abort(404)
                except KeyError:
                    pass
            return f(*args, **kwargs)
        return wrapper
    return decorator
