from flask_jwt_extended import JWTManager
from .services import is_token_revoked


jwt = JWTManager()

jwt.token_in_blacklist_loader(is_token_revoked)
