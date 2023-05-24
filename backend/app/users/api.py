from typing import List

from fastapi import Depends, Depends, APIRouter, UploadFile, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT
import aiofiles

from app.db import get_session
from app.users.models import User
from app.users.schemas import ReturnUser
from app.auth.auth_fastapi_jwt_auth_bearer import FastapiJwtAuthBearer
from app.users.functions import get_user_by_email, get_user_by_id

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/users",
    dependencies=[Depends(FastapiJwtAuthBearer())],
)
async def get_users(
    session: AsyncSession = Depends(get_session),
) -> List[ReturnUser]:
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        ReturnUser(id=user.id, email=user.email, profile_img=user.profile_img)
        for user in users
    ]


@router.get(
    "/user",
    dependencies=[Depends(FastapiJwtAuthBearer())],
)
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

    # TODO: fix file name and file path
    file_name = f"/usr/src/data_base/user_profile_img/{current_user}.{file.filename}"

    async with aiofiles.open(file_name, "wb+") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    img_url = f"{current_user}.{file.filename}"

    try:
        user.profile_img = img_url
        await session.commit()
    except IntegrityError as exc:
        raise HTTPException(status_code=422, detail=f"{exc=}")

    return {"url": img_url}


@router.get("/profile-img/", dependencies=[Depends(FastapiJwtAuthBearer())])
async def get_profile_img(url: str, Authorize: AuthJWT = Depends()):
    Authorize.get_jwt_subject()
    file_path = f"/usr/src/data_base/user_profile_img/{url}"
    return FileResponse(file_path)
