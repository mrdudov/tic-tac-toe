from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True)


class User(UserBase, table=True):
    name: str = Field(unique=True)
    id: int = Field(default=None, primary_key=True)


class UserCreate(UserBase):
    password: str = Field()


class UserLogin(UserBase):
    name: str = Field(unique=True)
