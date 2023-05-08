import os
from typing import Optional

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


class Connection:
    def __init__(self, connection_url):
        self.url_connection = connection_url
        self.engine = None
        self.async_session = None
        self.sql_meta = MetaData()

    async def connect(self):
        self.engine = create_async_engine(f"{self.url_connection}")
        async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.async_session = async_session()

    async def close(self):
        await self.async_session.close()
        await self.engine.dispose()

    async def __aenter__(self):
        await self.connect()
        return self.async_session

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
