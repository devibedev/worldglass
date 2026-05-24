from fastapi import APIRouter

router = APIRouter()

@router.get("/api/quotes")
async def get_quotes():
    """Endpoint para obtener cotizaciones (Fase 2: con PostgreSQL)"""
    return {"message": "Endpoint quotes - implementar en Fase 2 con PostgreSQL"}

@router.post("/api/quotes")
async def create_quote():
    """Endpoint para crear cotización (Fase 2: con PostgreSQL)"""
    return {"message": "Endpoint create_quote - implementar en Fase 2 con PostgreSQL"}
