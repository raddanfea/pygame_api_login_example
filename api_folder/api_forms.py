from pydantic import BaseModel


class UserForm(BaseModel):
    name: str
    password: str
