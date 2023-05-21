from sqlmodel import SQLModel, Field
from pydantic import EmailStr, BaseModel


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password: str = Field()


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class ReturnUser(BaseModel):
    id: int
    email: EmailStr
