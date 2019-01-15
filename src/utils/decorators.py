from flask import current_app
from functools import wraps
from flask_restful import abort


def hashids_decode(*pks):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not pks:
                cls = dict(zip(f.__code__.co_varnames, args)).get('self')
                if cls:
                    try:
                        _pks = getattr(cls, '{}_hashid_pks'.format(f.__name__))
                    except AttributeError:
                        _pks = ()
            for varname in _pks:
                try:
                    if kwargs[varname] is None:
                        continue
                    kwargs[varname] = current_app.extensions['hashids']\
                                                 .decode(kwargs[varname])
                except IndexError:
                    return abort(404)
                except KeyError:
                    pass
            return f(*args, **kwargs)
        return wrapper
    return decorator
