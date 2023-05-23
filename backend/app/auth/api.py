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
        # TODO: correct error messages
        print(exc)
        raise HTTPException(status_code=422)
    await session.refresh(user)
    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
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
    query = await session.execute(select(User).where(User.email == user.email))

    users = query.scalars().all()

    u = [User(id=user.id, email=user.email, password=user.password) for user in users]

    if len(u) > 1:
        raise HTTPException(
            status_code=500, detail="Server error. More then one user found"
        )

    if not u:
        raise HTTPException(status_code=401, detail="Bad email or password")

    if not check_password(
        password=user.password, hashed_password=u[0].password.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Bad password")

    access_token = Authorize.create_access_token(subject=user.email)
    refresh_token = Authorize.create_refresh_token(subject=user.email)
    return {"user": u[0], "access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", dependencies=[Depends(FastapiJwtAuthRefreshBearer())])
def refresh_access_token(Authorize: AuthJWT = Depends()) -> AccessToken:
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}
