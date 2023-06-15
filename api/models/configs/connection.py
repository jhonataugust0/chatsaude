import asyncio
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from asyncio.queues import Queue

class Connection:
    def __init__(self, connection_url, pool_size=5):
        self.url_connection = connection_url
        self.pool_size = pool_size
        self.engine = None
        self.async_session = None
        self.sql_meta = MetaData()
        self.pool = Queue(maxsize=pool_size)
        self.lock = asyncio.Lock()

    async def create_new_connection(self):
        self.engine = create_async_engine(f"{self.url_connection}")
        async_session = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
        self.async_session = async_session()
        return self.async_session

    async def connect(self):
        for i in range(self.pool_size):
            session = await self.create_new_connection()
            await self.pool.put(session)

    async def close(self):
        while not self.pool.empty():
            session = await self.pool.get()
            await session.close()
        await self.engine.dispose()

    async def __aenter__(self):
        async with self.lock:
            if self.pool.empty():
                await self.connect()
            return await self.pool.get()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        async with self.lock:
            await self.async_session.close()
            await self.pool.put(self.async_session)
