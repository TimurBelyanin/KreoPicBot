from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import sys
from config import settings


async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True)


class Base(DeclarativeBase):
    pass
