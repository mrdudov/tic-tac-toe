from typing import List

from fastapi import Depends, FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from app.db import get_session
from app.models import User, UserCreate, ReturnUser
from app.auth.hash_password import hash_password, check_password
from app.auth.auth_fastapi_jwt_auth_bearer import (
    FastapiJwtAuthBearer,
    FastapiJwtAuthRefreshBearer,
)


app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get(
    "/users",
    dependencies=[Depends(FastapiJwtAuthBearer())],
    response_model=list[ReturnUser],
    tags=["user"],
)
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> List[ReturnUser]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [ReturnUser(id=user.id, email=user.email) for user in users]


@app.post("/register", tags=["auth"])
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
) -> ReturnUser:
    hashed_password = hash_password(user.password)
    user = User(email=user.email, password=hashed_password)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        print(exc)
        raise HTTPException(status_code=422)
    await session.refresh(user)
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {
        "user": ReturnUser(id=user.id, email=user.email),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@app.post("/login", tags=["auth"])
async def login(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
):
    query = await session.execute(select(User).where(User.email == user.email))

    users = query.scalars().all()

    u = [User(id=user.id, email=user.email, password=user.password) for user in users]

    if len(u) > 1:
        raise HTTPException(
            status_code=500, detail="Server error. More then one user found"
        )

    if not u:
        raise HTTPException(status_code=401, detail="Bad email or password")

    if not check_password(
        password=user.password, hashed_password=u[0].password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Bad password")

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"user": u[0], "access_token": access_token, "refresh_token": refresh_token}


@app.post(
    "/refresh", dependencies=[Depends(FastapiJwtAuthRefreshBearer())], tags=["auth"]
)
def refresh_access_token(Authorize: AuthJWT = Depends()):
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
