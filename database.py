import os
import asyncpg
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

# Variable global para el pool
_pool = None

async def get_db_pool():
    global _pool
    if _pool is None:
        url = os.getenv("DATABASE_URL")
        
        if not url or url.strip() == "":
            raise ValueError("DATABASE_URL no está configurada. Verifica las variables de entorno en Railway.")

        # asyncpg requiere 'postgresql://' en lugar de 'postgres://'
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        
        # Railway requiere SSL en producción. 
        # Detectamos si estamos en Railway o si la URL no es localhost.
        is_railway = os.getenv("RAILWAY_ENVIRONMENT") or "railway" in str(url)
        ssl_option = 'require' if is_railway else None
        
        _pool = await asyncpg.create_pool(url, ssl=ssl_option, min_size=1, max_size=10)
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