from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    email: str


class UserPerf(BaseModel):
    username: str
    email: str


class UserForm(BaseModel):
    email: str
    password: str
