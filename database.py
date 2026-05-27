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

@asynccontextmanager
async def get_db():
    """Manejador de conexión para usar con 'async with'"""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no está configurada en las variables de entorno")

    # ssl='require' es fundamental para Railway
    conn = await asyncpg.connect(DATABASE_URL, ssl='require')
    try:
        yield conn
    finally:
        await conn.close()