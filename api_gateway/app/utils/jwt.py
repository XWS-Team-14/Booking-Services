import jwt

from app.constants import JWT_ACCESS_SECRET


def decode_access_token(access_token: str):
    return jwt.decode(access_token, JWT_ACCESS_SECRET, algorithms=["HS256"])


def get_id_from_access_token(access_token: str):
    return decode_access_token(access_token).get("id")
