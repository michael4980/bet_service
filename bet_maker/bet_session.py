import os

from db_bet.bet_models import Base
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()
name = os.getenv('DB_BET_NAME')
user = os.getenv('DB_BET_USER')
password = os.getenv('DB_BET_PASS')
port = os.getenv('DB_BET_PORT')
host = os.getenv('DB_BET_HOST')


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
