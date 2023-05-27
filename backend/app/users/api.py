from typing import List

from fastapi import Depends, APIRouter, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT

from app.db import get_session
from app.users.models import User
from app.users.schemas import ReturnUser
from app.auth.auth_fastapi_jwt_auth_bearer import FastapiJwtAuthBearer
from app.users.functions import get_user_by_email, get_user_by_id, save_profile_img
from app.settings import SETTINGS


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/users", dependencies=[Depends(FastapiJwtAuthBearer())])
async def get_users(session: AsyncSession = Depends(get_session)) -> List[ReturnUser]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        ReturnUser(id=user.id, email=user.email, profile_img=user.profile_img)
        for user in users
    ]


@router.get("/user", dependencies=[Depends(FastapiJwtAuthBearer())])
async def get_users(
    user_id: int, session: AsyncSession = Depends(get_session)
) -> ReturnUser:
    user = await get_user_by_id(session=session, id=user_id)

    return ReturnUser(id=user.id, email=user.email, profile_img=user.profile_img)


@router.post("/profile-img/", dependencies=[Depends(FastapiJwtAuthBearer())])
async def set_user_profile_image(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
):
    current_user = Authorize.get_jwt_subject()
    user = await get_user_by_email(session=session, email=current_user)
    file_name = await save_profile_img(file)

    user.profile_img = file_name
    await session.commit()

    return {"url": file_name}


@router.get("/profile-img/", dependencies=[Depends(FastapiJwtAuthBearer())])
async def get_profile_img(url: str, Authorize: AuthJWT = Depends()):
    Authorize.get_jwt_subject()
    file_path = f"{SETTINGS.user_profile_img}/{url}"
    return FileResponse(file_path)
