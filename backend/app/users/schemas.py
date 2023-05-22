from pydantic import EmailStr, BaseModel


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class ReturnUser(BaseModel):
    id: int
    email: EmailStr
    profile_img: str
