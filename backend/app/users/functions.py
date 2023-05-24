from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from app.users.models import User
from sqlalchemy.future import select
from fastapi import HTTPException


async def get_user_by_email(*, session, email: str):
    query = await session.execute(select(User).where(User.email == email))
    return handle_db_exceptions(query)


async def get_user_by_id(*, session, id: int):
    query = await session.execute(select(User).where(User.id == id))
    return handle_db_exceptions(query)


def handle_db_exceptions(query):
    try:
        return query.scalar_one()
    except NoResultFound as exc:
        raise HTTPException(
            status_code=404, detail=f"auth error user not found. {exc}."
        )
    except MultipleResultsFound as exc:
        HTTPException(
            status_code=404, detail=f"auth error multiple users found. {exc}."
        )


def get_user_claims(user) -> dict:
    return {"user_id": user["id"], "user_email": user["email"]}
