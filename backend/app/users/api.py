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

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/users",
    dependencies=[Depends(FastapiJwtAuthBearer())],
    response_model=list[ReturnUser],
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
    response_model=ReturnUser,
)
async def get_users(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> ReturnUser:
    query = await session.execute(select(User).where(User.id == user_id))
    users = query.scalars().all()
    u = [
        User(
            id=user.id,
            email=user.email,
            password=user.password,
            profile_img=user.profile_img,
        )
        for user in users
    ]
    if len(u) > 1:
        raise HTTPException(
            status_code=500, detail="Server error. More then one user found"
        )

    return ReturnUser(id=u[0].id, email=u[0].email, profile_img=u[0].profile_img)


@router.post("/profile-img/", dependencies=[Depends(FastapiJwtAuthBearer())])
async def create_upload_file(
    file: UploadFile,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
):
    # TODO: fix file name and file path
    current_user = Authorize.get_jwt_subject()
    file_name = f"/usr/src/data_base/user_profile_img/{current_user}.{file.filename}"

    async with aiofiles.open(file_name, "wb+") as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    img_url = f"{current_user}.{file.filename}"
    query = await session.execute(select(User).where(User.email == current_user))

    query.scalar_one().profile_img = img_url

    try:
        await session.commit()
    except IntegrityError as exc:
        # TODO: correct error messages
        print(exc)
        raise HTTPException(status_code=422)
    except Exception as exc:
        print(exc)
        raise HTTPException(status_code=422, detail=exc)

    return {"url": img_url}


@router.get("/profile-img/", dependencies=[Depends(FastapiJwtAuthBearer())])
async def get_profile_img(url: str, Authorize: AuthJWT = Depends()):
    Authorize.get_jwt_subject()
    file_path = f"/usr/src/data_base/user_profile_img/{url}"
    return FileResponse(file_path)
