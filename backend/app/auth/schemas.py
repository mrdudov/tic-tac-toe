from pydantic import EmailStr, BaseModel


class ReturnUser(BaseModel):
    id: int
    email: EmailStr


class UserLoginResponse(BaseModel):
    user: ReturnUser
    refresh_token: str
    access_token: str


class AccessToken(BaseModel):
    access_token: str
