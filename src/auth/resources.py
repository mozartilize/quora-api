from flask import jsonify, current_app
from sqlalchemy import select
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from db.repository import repo
from accounts.tables import accounts
from utils.typing import ResponseType
from utils.schemas import validate_input
from .schemas import LoginSchema
from .custom_jwt_extended import jwt_required, decode_jwt_from_request
from .repository import store_refresh_token, revoke_refresh_token


@validate_input(LoginSchema(), locations=("json", "form"))
def auth(data: dict) -> ResponseType:
    refresh_token = create_refresh_token(identity=data["id"])
    store_refresh_token(refresh_token, current_app.config["JWT_IDENTITY_CLAIM"])
    return (
        jsonify(
            {
                "access_token": create_access_token(identity=data["id"]),
                "refresh_token": refresh_token,
            }
        ),
        201,
    )


@jwt_required
def me() -> ResponseType:
    current_user = get_jwt_identity()
    fields = ["id", "username", "email"]
    q = select([accounts.c[field] for field in fields]).where(
        accounts.c.id == current_user
    )
    acc = repo(q).fetchone()
    return jsonify(dict(acc))


@jwt_required
def verify() -> ResponseType:
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})


@jwt_required(allow_expired=True)
def refresh() -> ResponseType:
    refresh_token_data = decode_jwt_from_request(
        request_type="refresh", locations=["json"]
    )
    current_user = refresh_token_data.get(current_app.config["JWT_IDENTITY_CLAIM"])
    if current_user == get_jwt_identity():
        ret = {"access_token": create_access_token(identity=current_user)}
        return jsonify(ret), 200
    else:
        return jsonify({"message": "Access token and refresh token do not match"}), 400


@jwt_required(allow_expired=True)
def revoke() -> ResponseType:
    refresh_token_data = decode_jwt_from_request(
        request_type="refresh", locations=["json"]
    )
    current_user = refresh_token_data.get(
        current_app.config["JWT_IDENTITY_CLAIM"], None
    )
    if current_user == get_jwt_identity():
        token = revoke_refresh_token(refresh_token_data["jti"], current_user)
        if not token:
            return jsonify({"message": "The specified token was not found"}), 404
        return jsonify({"message": "Token revoked"}), 200
    else:
        return jsonify({"message": "Access token and refresh token do not match"}), 400
