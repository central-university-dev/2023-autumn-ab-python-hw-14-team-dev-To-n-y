from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserPerf(BaseModel):
    username: str
    email: str
