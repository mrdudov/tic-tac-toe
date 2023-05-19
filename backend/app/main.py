from fastapi import Depends, FastAPI, HTTPException, Body, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from app.db import get_session
from app.models import User, UserCreate
from app.auth.auth_handler import generate_JWT
from app.auth.auth_bearer import JWTBearer


app = FastAPI()


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.get(
    "/users",
    dependencies=[Depends(JWTBearer())],
    response_model=list[User],
    tags=["user"],
)
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(name=user.name, id=user.id, email=user.email) for user in users]


@app.post("/users", tags=["user"])
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(name=user.name, email=user.email, password=user.password)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=422)
    await session.refresh(user)
    return {"user": user, "jwt": generate_JWT(user.email)}


@app.post("/users/get_jwt_token", tags=["user"])
async def get_jwt_token(user: UserCreate = Body(...)):
    return generate_JWT(user.email)


@app.post("/login")
async def login(
    user: User,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
):
    result = await session.execute(select(User).where(User.email == user.email))
    if not list(result):
        raise HTTPException(status_code=401,detail="Bad username or password")
    
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/refresh")
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
