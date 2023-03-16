from fastapi import Depends, FastAPI
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.models import User, UserCreate

app = FastAPI()


@app.get("/users", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(name=user.name, id=user.id) for user in users]


@app.post("/users")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(name=user.name)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

