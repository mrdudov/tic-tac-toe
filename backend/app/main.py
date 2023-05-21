from typing import List

from fastapi import Depends, FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth.exceptions import AuthJWTException


from app.db import get_session
from app.models import User, ReturnUser
from app.auth.auth_fastapi_jwt_auth_bearer import FastapiJwtAuthBearer


from app.auth.api import router as auth_router

app = FastAPI()

app.include_router(auth_router)


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
