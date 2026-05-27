from fastapi import APIRouter, HTTPException
from database import get_db
import json

router = APIRouter()

@router.get("/quotes/list")
async def list_quotes():
    """Lista las últimas 10 cotizaciones guardadas para verificar que la DB funciona"""
    try:
        async with get_db() as db:
            rows = await db.fetch("SELECT id, customer_name, details, created_at FROM quotes ORDER BY created_at DESC LIMIT 10")
            # Nota: r["details"] ya viene como dict/list gracias a asyncpg + JSONB
            return [
                {"id": str(r["id"]), "customer": r["customer_name"], "date": r["created_at"], "details": r["details"]} 
                for r in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer cotizaciones: {str(e)}")