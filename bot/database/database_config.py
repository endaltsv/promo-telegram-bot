from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
# todo: weak, postgres improve.
DATABASE_URL = "sqlite+aiosqlite:///bot/database/database.db"
engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def initialize_database():
    """
    Creates all tables defined in the declarative base.

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
