from typing import List, Annotated

from fastapi import Depends, Depends, APIRouter, File, UploadFile
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


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


@router.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
