import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db.db_models import Base
load_dotenv()

name = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
port = os.getenv('DB_PORT')
host = os.getenv('DB_HOST')


async def create_sessionmaker(sync=True):
    '''return async_session object'''
    engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}",
                                 echo=False
                                 )
    if sync:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async_sessionmaker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession, future=True
    )
    return async_sessionmaker
