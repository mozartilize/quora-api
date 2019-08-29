from typing import Tuple
from functools import wraps
from werkzeug.datastructures import ImmutableMultiDict
from flask import request, current_app
from marshmallow import Schema, ValidationError


def wrap_errors(errors: dict) -> dict:
    if errors.get("_schema"):
        return {"message": errors["_schema"]}
    else:
        return {"message": "Validation error", "errors": errors}


funcs = {
    "json": lambda: request.json,
    "form": lambda: request.form,
    "files": lambda: request.files,
    "querystring": lambda: request.args,
    "headers": lambda: request.headers,
    "cookies": lambda: request.cookies,
}


def get_request_data_from(locations: Tuple[str], mode: str) -> ImmutableMultiDict:
    """Get data from request.
    Return ImmutableMultiDict in case data from form could be array
    and schema can handle it via getlist.
    """
    data = {}
    for location in locations:
        if funcs[location]():
            if isinstance(funcs[location](), dict):
                data.update(funcs[location]())
            else:
                try:
                    data.update(dict(funcs[location]()))
                except TypeError:
                    raise TypeError("Unknown request data struct")
            if mode == "or":
                break
    return ImmutableMultiDict(data)


def validate_input(
    input_schema: Schema,
    locations: Tuple[str] = ("json",),
    mode: str = "or",
    args_name: str = "data",
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            request_data = get_request_data_from(locations, mode)
            try:
                data = input_schema.load(request_data)
            except ValidationError as e:
                return wrap_errors(e.messages), 400

            kwargs[args_name] = data

            try:
                return f(*args, **kwargs)
            except Exception as e:
                current_app.logger.exception(e)
                return dict(message=str(e)), 500

        return decorated_function

    return decorator
