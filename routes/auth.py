from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import re
from database import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    organization_name: str

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

@router.post("/auth/register")
async def register(data: RegisterRequest):
    # Nota: get_db se usa dentro del bloque 'async with' para mayor seguridad en Railway
    async with get_db() as db:
        # 1. Validar password
        if len(data.password) < 8:
            raise HTTPException(400, "Password mínimo 8 caracteres")
        
        # 2. Validar email único
        user_exists = await db.fetchrow("SELECT id FROM users WHERE email = $1", data.email)
        if user_exists:
            raise HTTPException(400, "Email ya registrado")
        
        # 3. Crear organización
        slug = slugify(data.organization_name)
        base_slug = slug
        counter = 1
        while await db.fetchrow("SELECT id FROM organizations WHERE slug = $1", slug):
            counter += 1
            slug = f"{base_slug}-{counter}"
        
        org_id = await db.fetchval(
            "INSERT INTO organizations (name, slug) VALUES ($1, $2) RETURNING id",
            data.organization_name, slug
        )
        
        # 4. Crear usuario owner
        password_hash = pwd_context.hash(data.password)
        await db.execute(
            "INSERT INTO users (organization_id, email, password_hash, full_name) VALUES ($1, $2, $3, $4)",
            org_id, data.email, password_hash, data.full_name
        )
        
        return {"message": "Registrado exitosamente", "organization_slug": slug}