import jwt  # type: ignore
from passlib.context import CryptContext

from config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_ALGO = "HS256"


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_token(payload: dict) -> str:
    encoded_data = jwt.encode(
        payload=payload, key=settings.JWT_SECRET, algorithm=JWT_ALGO
    )

    return encoded_data


def decode_token(token: str) -> dict:
    decoded_data = jwt.decode(
        jwt=token, key=settings.JWT_SECRET, algorithms=[JWT_ALGO]
    )
    return decoded_data
