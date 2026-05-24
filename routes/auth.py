from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import re
from database import get_db

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars, validado abajo
    full_name: str
    organization_name: str


def slugify(text: str) -> str:
    """Convierte nombre de organización a slug URL-friendly"""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')


@router.post("/auth/register")
async def register(data: RegisterRequest):
    """
    Registro de nuevo usuario y organización (multi-tenant).

    Proceso:
    1. Validar password (mínimo 8 caracteres)
    2. Validar email único
    3. Crear organización con slug único
    4. Crear usuario owner con password hasheado
    5. Retornar slug de la organización

    Esto permite que múltiples talleres se registren sin intervención manual.
    """
    # 1. Validar password
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="Password mínimo 8 caracteres")

    # 2. Validar email único y crear organización
    async with get_db() as conn:
        # Verificar si email ya existe
        existing_user = await conn.fetchrow(
            "SELECT id FROM users WHERE email = $1",
            data.email
        )
        if existing_user:
            raise HTTPException(status_code=400, detail="Email ya registrado")

        # 3. Crear organización con slug único
        slug = slugify(data.organization_name)

        # Si slug existe, agregar -2, -3, etc.
        base_slug = slug
        counter = 1
        while await conn.fetchrow(
            "SELECT id FROM organizations WHERE slug = $1",
            slug
        ):
            counter += 1
            slug = f"{base_slug}-{counter}"

        org_id = await conn.fetchval(
            "INSERT INTO organizations (name, slug) VALUES ($1, $2) RETURNING id",
            data.organization_name, slug
        )

        # 4. Crear usuario owner con password hasheado
        password_hash = pwd_context.hash(data.password)
        user_id = await conn.fetchval(
            """INSERT INTO users (organization_id, email, password_hash, full_name)
            VALUES ($1, $2, $3, $4) RETURNING id""",
            org_id, data.email, password_hash, data.full_name
        )

    return {
        "message": "Registrado exitosamente",
        "organization_slug": slug,
        "organization_id": str(org_id),
        "user_id": str(user_id)
    }


@router.get("/auth/health")
async def auth_health():
    """Health check para rutas de auth"""
    return {"status": "auth_system_ready"}
