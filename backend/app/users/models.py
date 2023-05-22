from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    profile_img: str = Field(default="")
    password: str = Field()
