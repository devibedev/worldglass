from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

app = FastAPI(title="WorldGlass API", version="1.0.0")

<<<<<<< Updated upstream
<<<<<<< Updated upstream
# Montar archivos estáticos (solo si el directorio existe)
if os.path.isdir("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
=======
# Montar archivos estáticos (Fase 1: desactivado hasta que necesitemos CSS/JS)
# app.mount("/static", StaticFiles(directory="static"), name="static")
>>>>>>> Stashed changes
=======
# Montar archivos estáticos (Fase 1: desactivado hasta que necesitemos CSS/JS)
# app.mount("/static", StaticFiles(directory="static"), name="static")
>>>>>>> Stashed changes

# Configurar templates
templates = Jinja2Templates(directory="templates")

# Importar rutas
from routes import chat, quotes, auth

app.include_router(chat.router, prefix="", tags=["chat"])
app.include_router(quotes.router, prefix="/api", tags=["quotes"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página principal con el chat"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/health")
async def health():
    """Health check para Railway"""
    return {"status": "healthy", "service": "worldglass-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
