import os
import asyncpg
from contextlib import asynccontextmanager

DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def get_db():
    """
    Context manager para conexión a PostgreSQL.

    Uso:
    async with get_db() as conn:
        result = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
    """
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está configurada en variables de entorno")

    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


async def test_connection():
    """Prueba la conexión a la base de datos"""
    async with get_db() as conn:
        version = await conn.fetchval("SELECT version()")
        return version
