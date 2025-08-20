from contextlib import asynccontextmanager
import asyncpg  # type: ignore
from typing import Any, AsyncContextManager
from contextlib import AbstractAsyncContextManager


class AsyncPGDatabase:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self.pool: asyncpg.Pool | None = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def close(self):
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args: Any) -> str:
        assert self.pool is not None, "Database pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> list[Any]:
        assert self.pool is not None, "Database pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> Any:
        assert self.pool is not None, "Database pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query: str, *args: Any) -> Any:
        assert self.pool is not None, "Database pool not initialized"
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def execute_script(self, script: str) -> None:
        """
        Executa um script SQL completo com múltiplas instruções, incluindo PL/pgSQL.
        """
        assert self.pool is not None, "Database pool not initialized"
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(script)

    @asynccontextmanager
    async def transaction(self):
        """
        Context manager para transações.
        Uso:
        async with db.transaction():
            await db.execute(...)
            await db.execute(...)
        """
        assert self.pool is not None, "Database pool not initialized"
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                yield conn
