from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.settings import SETTINGS


DATABASE_URL = (
    f"postgresql+asyncpg://{SETTINGS.POSTGRES_PASSWORD}:"
    f"{SETTINGS.POSTGRES_USER}@{SETTINGS.POSTGRES_HOST}/{SETTINGS.POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
