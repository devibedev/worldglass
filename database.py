import os
import asyncpg
from contextlib import asynccontextmanager

# Railway inyecta automáticamente esta variable
DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def get_db():
    """Manejador de conexión para usar con 'async with'"""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está configurada en las variables de entorno")
    
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()