from fastapi import Depends, FastAPI, HTTPException, Body, Depends
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.db import get_session
from app.models import User, UserCreate
from app.auth.auth_handler import generate_JWT
from app.auth.auth_bearer import JWTBearer


app = FastAPI()


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
    return {
        "user": user,
        "jwt": generate_JWT(user.email)
    }


@app.post("/users/get_jwt_token", tags=["user"])
async def get_jwt_token(user: UserCreate = Body(...)):
    return generate_JWT(user.email)
