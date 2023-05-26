from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi_jwt_auth import AuthJWT

from app.db import get_session
from app.users.models import User
from app.users.schemas import UserCreate
from app.auth.schemas import UserLoginResponse, ReturnUser, AccessToken
from app.auth.hash_password import hash_password, check_password
from app.auth.auth_fastapi_jwt_auth_bearer import FastapiJwtAuthRefreshBearer
from app.users.functions import get_user_by_email, get_user_claims


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
) -> UserLoginResponse:
    hashed_password = hash_password(user.password)
    user = User(email=user.email, password=hashed_password)
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as exc:
        raise HTTPException(status_code=422, detail=f"{exc=}")
    await session.refresh(user)
    access_token = Authorize.create_access_token(
        subject=user.email, user_claims=get_user_claims(user.dict())
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user.email, user_claims=get_user_claims(user.dict())
    )
    return {
        "user": ReturnUser(id=user.id, email=user.email),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/login")
async def login(
    user: UserCreate,
    session: AsyncSession = Depends(get_session),
    Authorize: AuthJWT = Depends(),
) -> UserLoginResponse:
    user_from_db = await get_user_by_email(session=session, email=user.email)

    if not check_password(
        password=user.password, hashed_password=user_from_db.password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Bad password")
    access_token = Authorize.create_access_token(
        subject=user.email,
        user_claims=get_user_claims(
            {"id": user_from_db.id, "email": user_from_db.email}
        ),
    )
    refresh_token = Authorize.create_refresh_token(
        subject=user.email,
        user_claims=get_user_claims(
            {"id": user_from_db.id, "email": user_from_db.email}
        ),
    )
    return {
        "user": user_from_db,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@router.post("/refresh", dependencies=[Depends(FastapiJwtAuthRefreshBearer())])
async def refresh_access_token(
    Authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)
) -> AccessToken:
    current_user = Authorize.get_jwt_subject()
    user_from_db = await get_user_by_email(session=session, email=current_user)
    new_access_token = Authorize.create_access_token(
        subject=current_user, user_claims=get_user_claims(user_from_db.dict())
    )
    return {"access_token": new_access_token}
