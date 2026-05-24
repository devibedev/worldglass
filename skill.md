Markdown
# WorldGlass Skill: Sistema de Registro Multi-Tenant v1.0

## 0. Principio Heredable
**Regla**: Todo lo que se construye debe permitir que mañana un taller se registre solo, sin que el founder toque la BD. Si requiere SQL manual, no es escalable.

## 1. Objetivo de esta Skill
Implementar registro de usuarios + organizaciones + límites de plan, usando solo FastAPI + PostgreSQL. Sin Auth0, sin Redis, sin microservicios.

**Resultado**: Un taller entra a `worldglass.app/registro`, pone su email, nombre del taller, y en 60s puede cotizar. Plan Free: 10 cotizaciones/mes.

## 2. Esquema de Base de Datos - Heredable
Copiar/pegar en Railway PostgreSQL Query:

```sql
-- Extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de planes. Heredable: agregar planes aquí, no en código
CREATE TABLE plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL, -- 'free', 'pro'
    max_quotes_month INTEGER NOT NULL,
    max_users INTEGER NOT NULL,
    price_mxn_cents INTEGER NOT NULL, -- 0 para free, 49000 para pro
    features JSONB DEFAULT '{}'::jsonb
);

INSERT INTO plans (name, max_quotes_month, max_users, price_mxn_cents) VALUES
('free', 10, 1, 0),
('pro', 999999, 5, 49000);

-- Organizaciones = Talleres. Un taller puede tener N usuarios
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL, -- para URLs: worldglass.app/c/mitaller
    plan_id INTEGER REFERENCES plans(id) DEFAULT 1, -- free por defecto
    stripe_customer_id VARCHAR(255), -- null hasta que pague
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usuarios. Un usuario pertenece a 1 organización en Fase 1
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(20) DEFAULT 'owner', -- 'owner', 'member'. Fase 1 solo owner
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Cotizaciones con límite por org
CREATE TABLE quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    customer_name VARCHAR(255),
    total_mxn_cents INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    details JSONB, -- guarda ancho, alto, materiales
    created_at TIMESTAMP DEFAULT NOW()
);

-- Índice para contar cotizaciones rápido
CREATE INDEX idx_quotes_org_month ON quotes (organization_id, created_at);

-- Función para validar límite. Heredable: cambiar plan sin tocar código
CREATE OR REPLACE FUNCTION check_quote_limit(org_id UUID)
RETURNS BOOLEAN AS $$
DECLARE
    current_count INTEGER;
    max_allowed INTEGER;
BEGIN
    SELECT COUNT(*) INTO current_count 
    FROM quotes 
    WHERE organization_id = org_id 
    AND created_at >= date_trunc('month', NOW());
    
    SELECT p.max_quotes_month INTO max_allowed
    FROM organizations o JOIN plans p ON o.plan_id = p.id
    WHERE o.id = org_id;
    
    RETURN current_count < max_allowed;
END;
$$ LANGUAGE plpgsql;

82 líneas ocultas
3. Backend FastAPI - Endpoints Heredables
3.1 auth.py - Registro + Login
Python
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import re

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str  # min 8 chars, validado abajo
    full_name: str
    organization_name: str

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

@router.post("/auth/register")
async def register(data: RegisterRequest, db = Depends(get_db)):
    # 1. Validar password
    if len(data.password) < 8:
        raise HTTPException(400, "Password mínimo 8 caracteres")
    
    # 2. Validar email único
    if await db.fetchrow("SELECT id FROM users WHERE email = $1", data.email):
        raise HTTPException(400, "Email ya registrado")
    
    # 3. Crear organización
    slug = slugify(data.organization_name)
    # Si slug existe, agregar -2, -3
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
    user_id = await db.fetchval(
        "INSERT INTO users (organization_id, email, password_hash, full_name) VALUES ($1, $2, $3, $4) RETURNING id",
        org_id, data.email, password_hash, data.full_name
    )
    
    return {"message": "Registrado", "organization_slug": slug}

46 líneas ocultas
3.2 Middleware de Límites
Python
# dependencies.py
async def check_quota(user: User = Depends(get_current_user), db = Depends(get_db)):
    can_create = await db.fetchval("SELECT check_quote_limit($1)", user.organization_id)
    if not can_create:
        raise HTTPException(402, "Límite de cotizaciones alcanzado. Actualiza a Pro")
    return True

# En routes/quotes.py
@router.post("/quotes")
async def create_quote(data: QuoteCreate, _: bool = Depends(check_quota)):
    # Solo llega aquí si tiene cuota
    pass

7 líneas ocultas
4. Frontend - Página de Registro Heredable
templates/registro.html:


5. Checklist de Heredabilidad
Antes de dar por terminado, verifica:

 Puedo crear 2 talleres diferentes sin tocar código
 Cada taller solo ve sus cotizaciones
 Al llegar a 10 cotizaciones, el 11 da error 402
 Si cambio plans.max_quotes_month en SQL, el límite cambia sin deploy
 Passwords están hasheadas con bcrypt, no en texto plano
 Slug es único: "Vidrios GDL" y "Vidrios GDL" crean vidrios-gdl y vidrios-gdl-2
6. Documentación para Futuro Dev
Agregar a README.md:

Code
## Registro de Nuevos Talleres
POST /auth/register con {email, password, full_name, organization_name}
Retorna {organization_slug}. El dashboard queda en /c/{slug}/dashboard

## Límites de Plan
Tabla `plans`. Para crear plan "Enterprise", INSERT nuevo row. 
No tocar código. El middleware lee de BD.

2 líneas ocultas
7. Qué NO hacer - Anti-patrones
No hardcodear límites: if count > 10: está prohibido. Usar check_quote_limit()
No asumir 1 user = 1 org: Aunque hoy es 1:1, el schema soporta N users por org
No guardar plan en users: El plan vive en organizations. Si upgradeas, upgradeas el taller
Code

---

### 2. `README.md` → Documentación Heredable del Proyecto

```markdown
# WorldGlass SaaS

Cotizador con IA para talleres de cancelería de aluminio y vidrio en México.

## Stack Fase 1 - MVP
- **Backend**: FastAPI Python 3.11
- **DB**: PostgreSQL 15 en Railway
- **Frontend**: HTML + Jinja2 + Vanilla JS
- **IA**: OpenAI GPT-4o-mini + Replicate SDXL
- **Deploy**: Railway.app

## Setup Local Mac M1
```bash
git clone <repo>
cd worldglass
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Crear .env con:
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
REPLICATE_API_TOKEN=r8_...

# Correr migraciones
psql $DATABASE_URL -f schema.sql

# Iniciar
uvicorn app:app --reload

30 líneas ocultas
Arquitectura de Datos
Ver docs/skill.md sección 2. Principio: Multi-tenant desde día 1.

organizations = talleres
users = empleados del taller
plans = límites y precios
quotes = cotizaciones
Agregar Nuevo Plan
No tocar código. Solo SQL:

SQL
INSERT INTO plans (name, max_quotes_month, max_users, price_mxn_cents) 
VALUES ('enterprise', 999999, 20, 199000);
Flujo de Registro
Usuario entra a /registro
Llena form → POST /auth/register
Se crea organizations + users con plan free
Redirect a /c/{slug}/dashboard
Variables de Entorno
Variable

Descripción

Ejemplo

DATABASE_URL

Conexión Postgres

postgresql://user:pass@host/db

OPENAI_API_KEY

Para extraer medidas

sk-...

REPLICATE_API_TOKEN

Para renders

r8_...

SECRET_KEY

Para JWT

openssl rand -hex 32

Comandos Útiles
Bash
# Ver logs prod
railway logs

# Backup BD
pg_dump $DATABASE_URL > backup.sql

# Contar usuarios activos
psql $DATABASE_URL -c "SELECT COUNT(*) FROM users WHERE is_active = true;"

3 líneas ocultas
Roadmap
Ver docs/skill.md. Fase actual: 1. No implementar features de Fase 3.

Contacto
Founder: <tu_email>
Para dudas técnicas, leer agent.md primero.

Code

---

### Cómo usar esto para que no se desvíe

1. **En Windsurf/Cursor**: Pon `context.md` y `agent.md` en raíz. El agente los lee automático
2. **Antes de pedir código**: Di "Basado en skill.md sección 3.1, genera el endpoint de login"
3. **Si se alucina**: Pégale esto: "Eso viola context.md línea 25. Estamos en Fase 1. Usa SQLite, no Kubernetes"

**¿Te genero ahora el `schema.sql` completo + `app.py` con registro funcionando para que copies, pegues y tengas usuarios reales hoy?**

5 líneas ocultas