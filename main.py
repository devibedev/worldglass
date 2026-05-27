from dotenv import load_dotenv
# 1. CARGAR VARIABLES ANTES QUE TODO
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging
from database import get_db

# Configurar logs para ver errores detallados en la consola de Railway
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="WorldGlass API", version="1.0.0")

# Asegurar que existan las carpetas para evitar errores de montaje
os.makedirs("static", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_db_test():
    """Prueba la conexión a la base de datos al arrancar"""
    try:
        async with get_db() as conn:
            val = await conn.fetchval("SELECT 1")
            logger.info(f"✅ Conexión a DB exitosa: Test {val}")
    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO: No se pudo conectar a la DB: {e}")
        # No detenemos el app para que Railway no entre en bucle de reinicio, 
        # pero el log nos dirá qué pasó.

try:
    # Importar rutas de forma segura
    from routes import chat, quotes, auth
    # Registrar routers con prefijo consistente /api
    app.include_router(chat.router, prefix="/api", tags=["chat"])
    app.include_router(quotes.router, prefix="/api", tags=["quotes"])
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    logger.info("Rutas cargadas exitosamente")
except Exception as e:
    logger.error(f"Error cargando rutas: {e}")

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
