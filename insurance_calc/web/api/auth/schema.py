from pydantic import BaseModel


class LoginPayload(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
