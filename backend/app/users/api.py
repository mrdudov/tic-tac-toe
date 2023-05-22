from typing import List

from fastapi import Depends, Depends, APIRouter, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_jwt_auth import AuthJWT
import aiofiles

from app.db import get_session
from app.models import User, ReturnUser
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
    return [ReturnUser(id=user.id, email=user.email) for user in users]


@router.post("/profile-img/", dependencies=[Depends(FastapiJwtAuthBearer())])
async def create_upload_file(file: UploadFile, Authorize: AuthJWT = Depends()):

    # TODO: fix file name and file path
    current_user = Authorize.get_jwt_subject()
    file_name = f"/usr/src/data_base/user_profile_img/{current_user}.{file.filename}"
        
    async with aiofiles.open(file_name, 'wb+') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)
    print(current_user)
    return {"filename": file.filename}
