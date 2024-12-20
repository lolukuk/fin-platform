from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserUpdatePassword(BaseModel):
    old_password: str
    new_password: str