import jwt

from app.constants import JWT_ACCESS_SECRET, JWT_REFRESH_SECRET


def decode_token(token: str, token_type: str = "access"):
    secret = JWT_REFRESH_SECRET if token_type == "refresh" else JWT_ACCESS_SECRET
    return jwt.decode(token, secret, algorithms=["HS256"])


def get_id_from_token(token: str, token_type: str = "access"):
    return decode_token(token, token_type).get("id")


def get_role_from_token(token: str, token_type: str = "access"):
    return decode_token(token, token_type).get("role")
