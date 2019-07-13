from functools import wraps
from jwt import ExpiredSignatureError
from flask import request
try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack

from flask_jwt_extended.config import config
from flask_jwt_extended.view_decorators import (
    _load_user, _decode_jwt_from_cookies, _decode_jwt_from_headers,
    _decode_jwt_from_json, _decode_jwt_from_query_string,
)
from flask_jwt_extended.utils import (
    verify_token_not_blacklisted, verify_token_type, verify_token_claims,
    decode_token,
)
from flask_jwt_extended.exceptions import NoAuthorizationError


def decode_jwt_from_request(request_type, **options):
    locations = options.get("locations", [])
    # All the places we can get a JWT from in this request
    get_encoded_token_functions = []
    if locations:
        if "cookies" in locations:
            get_encoded_token_functions.append(
                lambda: _decode_jwt_from_cookies(request_type)
            )
        if "query_string" in locations:
            get_encoded_token_functions.append(_decode_jwt_from_query_string)
        if "headers" in locations:
            get_encoded_token_functions.append(_decode_jwt_from_headers)
        if "json" in locations:
            get_encoded_token_functions.append(
                lambda: _decode_jwt_from_json(request_type)
            )
    else:
        if config.jwt_in_cookies:
            get_encoded_token_functions.append(
                lambda: _decode_jwt_from_cookies(request_type)
            )
        if config.jwt_in_query_string:
            get_encoded_token_functions.append(_decode_jwt_from_query_string)
        if config.jwt_in_headers:
            get_encoded_token_functions.append(_decode_jwt_from_headers)
        if config.jwt_in_json:
            get_encoded_token_functions.append(
                lambda: _decode_jwt_from_json(request_type)
            )

    # Try to find the token from one of these locations. It only needs to exist
    # in one place to be valid (not every location).
    errors = []
    decoded_token = None
    for get_encoded_token_function in get_encoded_token_functions:
        try:
            encoded_token, csrf_token = get_encoded_token_function()
            decoded_token = decode_token(encoded_token, csrf_token)
            break
        except ExpiredSignatureError:
            expired_data = decode_token(
                encoded_token, csrf_token, allow_expired=True
            )
            if options.get("allow_expired", False):
                decoded_token = expired_data
            else:
                # Save the expired token so
                # we can access it in a callback later
                ctx_stack.top.expired_jwt = expired_data
                raise
        except NoAuthorizationError as e:
            errors.append(str(e))

    # Do some work to make a helpful and human readable error message if no
    # token was found in any of the expected locations.
    if not decoded_token:
        token_locations = config.token_location
        multiple_jwt_locations = len(token_locations) != 1

        if multiple_jwt_locations:
            err_msg = "Missing JWT in {start_locs} or {end_locs} ({details})"\
                .format(
                    start_locs=", ".join(token_locations[:-1]),
                    end_locs=token_locations[-1],
                    details="; ".join(errors)
                )
            raise NoAuthorizationError(err_msg)
        else:
            raise NoAuthorizationError(errors[0])

    verify_token_type(decoded_token, expected_type=request_type)
    verify_token_not_blacklisted(decoded_token, request_type)
    return decoded_token


def custom_verify_jwt_in_request(**options):
    """
    Ensure that the requester has a valid access token. This does not check the
    freshness of the access token. Raises an appropiate exception there is
    no token or if the token is invalid.
    """
    if request.method not in config.exempt_methods:
        jwt_data = decode_jwt_from_request(
            request_type='access',
            allow_expired=options.get("allow_expired", False),
            locations=options.get("locations", [])
        )
        ctx_stack.top.jwt = jwt_data
        verify_token_claims(jwt_data)
        _load_user(jwt_data[config.identity_claim_key])


def jwt_required(fn_=None, *, allow_expired=False):
    def decorate_jwt_required(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            custom_verify_jwt_in_request(allow_expired=allow_expired)
            return fn(*args, **kwargs)
        return wrapper
    if fn_ is None:
        return decorate_jwt_required
    else:
        return decorate_jwt_required(fn_)
