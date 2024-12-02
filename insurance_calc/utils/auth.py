from datetime import datetime, timedelta

from jose import jwt

from insurance_calc.db.models.user import User
from insurance_calc.settings import settings


def obtain_token(user: User) -> str:
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now() + access_token_expires
    to_encode = {
        "exp": expire,
        "sub": str(user.id),
        "username": str(user.username),
        "role": user.role.name,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt
