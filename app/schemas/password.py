from pydantic import BaseModel


class Password(BaseModel):
    old_password: str
    new_password: str


class PasswordEmail(BaseModel):
    email: str


class NewPassword(PasswordEmail):
    new_password: str