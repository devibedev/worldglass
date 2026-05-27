import os
import asyncpg
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

# Railway inyecta automáticamente esta variable
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    # asyncpg requiere 'postgresql://' en lugar de 'postgres://'
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Variable global para el pool
_pool = None

async def get_db_pool():
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            raise ValueError("DATABASE_URL no está configurada")
        
        # Railway requiere SSL, pero en local a veces no. 
        # Si la URL contiene 'railway.app', forzamos SSL.
        ssl_option = 'require' if 'railway.app' in DATABASE_URL else None
        
        _pool = await asyncpg.create_pool(DATABASE_URL, ssl=ssl_option, min_size=1, max_size=10)
    return _pool

@asynccontextmanager
async def get_db():
    """Manejador que obtiene una conexión del pool"""
    pool = await get_db_pool()
    async with pool.acquire() as conn:
        yield conn

async def close_db_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None