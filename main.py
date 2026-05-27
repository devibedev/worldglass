from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging
from contextlib import asynccontextmanager
from database import get_db, close_db_pool
from routes import chat, quotes, auth

# Configurar logs para ver errores detallados en la consola de Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Silenciar logs innecesarios de librerías para ver mejor lo importante
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Ciclo de vida: Se ejecuta al arrancar y al apagar"""
    logger.info(f"🚀 Iniciando WorldGlass API en puerto {os.environ.get('PORT', 8000)}...")
    try:
        async with get_db() as conn:
            val = await conn.fetchval("SELECT 1")
            logger.info(f"✅ Conexión a DB exitosa: Test {val}")
    except Exception as e:
        logger.error(f"❌ ERROR DE BASE DE DATOS: {e}")
        logger.warning("La app seguirá funcionando pero las funciones de DB fallarán.")
    
    yield
    # Al cerrar la app, cerramos el pool de conexiones
    await close_db_pool()
    logger.info("Aplicación cerrada.")

app = FastAPI(title="WorldGlass API", version="1.0.0", lifespan=lifespan)

os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(quotes.router, prefix="/api", tags=["quotes"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal. Si falta chat.html, muestra un mensaje amigable."""
    if not os.path.exists("templates/chat.html"):
        return "<h1>WorldGlass Online</h1><p>API lista, pero falta el archivo <b>templates/chat.html</b> para mostrar el chat.</p>"
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/health")
async def health():
    """Health check para Railway"""
    return {"status": "healthy", "service": "worldglass-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
