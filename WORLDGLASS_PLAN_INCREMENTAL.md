# WorldGlass - Plan Incremental Escalonado

## 🎯 Filosofía: Escalado Inteligente y Progresivo

**Regla de oro**: No construir infraestructura antes de tener clientes que la necesiten.

---

## 📊 Fase 0: Estado Actual (Dónde Estamos)

### Código Existente
- ✅ Flask app funcionando
- ✅ Chat UI estilo WhatsApp
- ✅ Lógica básica de cotización
- ❌ Sin persistencia de datos
- ❌ Sin usuarios reales
- ❌ Fórmulas de precio hardcoded

### Qué Funciona
- Chat interactivo
- Interfaz atractiva
- Demo de cotización (150x190 negro = $8,450)

---

## 🚀 Fase 1: Mejoras Inmediatas (1-2 semanas)
**Objetivo**: Migrar Flask → FastAPI + PostgreSQL + Sistema de Registro
**Inversión**: $0 - $5 USD (Railway free tier)
**Tiempo**: 10-15 horas de desarrollo

### Tareas Concretas

#### 1. Migrar Flask a FastAPI (3 horas)
```python
# Estructura nueva (FastAPI)
worldglass/
├── main.py              # Entry point FastAPI
├── database.py          # Conexión PostgreSQL
├── models.py            # Pydantic models
├── routes/
│   ├── auth.py          # Registro/Login (usar skill.md)
│   ├── quotes.py        # Cotizaciones
│   └── chat.py          # Chatbot
├── templates/
│   ├── registro.html    # Página registro
│   ├── login.html       # Login
│   ├── dashboard.html   # Dashboard
│   └── chat.html        # Chat UI
└── utils/
    └── calculator.py    # Lógica de precios
```

#### 2. Configurar PostgreSQL en Railway (2 horas)
```bash
# 1. Crear proyecto Railway
# 2. Agregar servicio PostgreSQL
# 3. Obtener DATABASE_URL
# 4. Correr schema.sql de skill.md

# database.py
import asyncpg
from fastapi import Depends

async def get_db():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    try:
        yield conn
    finally:
        await conn.close()
```

#### 3. Implementar sistema de registro (4 horas)
```python
# Usar exactamente el código de skill.md:
# - Tabla plans, organizations, users, quotes
# - POST /auth/register
# - Middleware check_quote_limit
# - Slug único para cada taller
```

#### 4. Motor de precios real (3 horas)
```python
# utils/calculator.py
def calculate_shower_door(width_cm, height_cm, color, glass_type='9mm'):
    """
    Calcula precio de cancel de baño basado en:
    - Precio por m2 de aluminio
    - Precio por m2 de cristal
    - Herrajes
    - Instalación
    - Margen de ganancia
    """
    # Precios base (configurables)
    aluminum_price_per_m2 = {
        'natural': 450,
        'blanco': 520,
        'negro': 580,
        'champagne': 550
    }
    
    glass_price_per_m2 = {
        '6mm': 350,
        '8mm': 420,
        '9mm': 480
    }
    
    # Cálculos
    area_m2 = (width_cm * height_cm) / 10000
    aluminum_cost = area_m2 * aluminum_price_per_m2.get(color, 450)
    glass_cost = area_m2 * glass_price_per_m2.get(glass_type, 480)
    hardware_cost = 850  # Promedio herrajes
    installation_cost = 1200  # Instalación fija
    
    total = aluminum_cost + glass_cost + hardware_cost + installation_cost
    
    # Margen de ganancia (30%)
    final_price = total * 1.3
    
    return round(final_price, 2)
```

#### 5. Deploy en Railway (1 hora)
```bash
# 1. Crear archivo requirements.txt
fastapi==0.104.1
uvicorn==0.24.0
asyncpg==0.29.0
pydantic==2.5.0
passlib==1.7.4
python-jose[cryptography]==3.3.0

# 2. Railway detecta automáticamente Python
# 3. Configurar variables de entorno
# 4. git push railway main
```

### Resultado Esperado
- FastAPI funcionando con PostgreSQL
- Sistema de registro multi-tenant funcional
- Talleres pueden registrarse automáticamente
- Límites de cotizaciones por plan (free: 10/mes)
- **Cero costo mensual** (Railway free tier)

---

## 📈 Fase 2: MVP Funcional Simple (3-4 semanas)
**Objetivo**: Primeros usuarios reales y feedback
**Inversión**: $5 - $15 USD/mes (Railway + dominio)
**Tiempo**: 30-40 horas de desarrollo

### Tareas Concretas

#### 1. Sistema de login (usar skill.md) (4 horas)
```python
# Ya definido en skill.md:
# - POST /auth/login con email/password
# - JWT tokens para sesión
# - Middleware get_current_user
# - Protección de rutas con Depends(get_current_user)
```

#### 2. Dashboard multi-tenant (4 horas)
```python
# routes/dashboard.py
@router.get("/c/{org_slug}/dashboard")
async def dashboard(org_slug: str, user = Depends(get_current_user), db = Depends(get_db)):
    # Verificar que user pertenezca a esta org
    org = await db.fetchrow(
        "SELECT * FROM organizations WHERE slug = $1 AND id = $2",
        org_slug, user.organization_id
    )
    
    # Estadísticas del mes
    stats = await db.fetchrow("""
        SELECT 
            COUNT(*) as quote_count,
            SUM(total_mxn_cents)/100.0 as total_amount
        FROM quotes 
        WHERE organization_id = $1 
        AND created_at >= date_trunc('month', NOW())
    """, user.organization_id)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "org": org,
        "stats": stats
    })
```

#### 3. Generación de PDF simple (4 horas)
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_pdf(quote_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 750, "Cotización WorldGlass")
    
    p.setFont("Helvetica", 12)
    p.drawString(100, 700, f"Cliente: {quote_data['customer']}")
    p.drawString(100, 680, f"Total: ${quote_data['price']}")
    
    p.save()
    return buffer.getvalue()
```

#### 4. Chatbot con OpenAI GPT-4o-mini (6 horas)
```python
# routes/chat.py
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/chat")
async def chat(message: str, org_id: str, db = Depends(get_db)):
    # Verificar límite de cotizaciones
    can_create = await db.fetchval("SELECT check_quote_limit($1)", org_id)
    if not can_create:
        return {"error": "Límite alcanzado. Actualiza a Pro"}
    
    # Extraer medidas con IA
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Extrae dimensiones en cm. Formato JSON: {ancho, alto, color, producto}"},
            {"role": "user", "content": message}
        ]
    )
    
    dimensions = json.loads(response.choices[0].message.content)
    price = calculate_quote(dimensions)
    
    # Guardar cotización
    await db.execute("""
        INSERT INTO quotes (organization_id, total_mxn_cents, details, status)
        VALUES ($1, $2, $3, 'draft')
    """, org_id, int(price * 100), json.dumps(dimensions))
    
    return {"price": price, "dimensions": dimensions}
```

#### 5. Configuración de precios en BD (3 horas)
```python
# Crear tabla de precios configurables
CREATE TABLE material_prices (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR(50), -- 'aluminum', 'glass'
    variant VARCHAR(50), -- 'natural', 'negro', '9mm'
    price_per_m2_cents INTEGER
);

# Leer desde BD en calculator.py
async def get_material_prices(db):
    prices = await db.fetch("SELECT * FROM material_prices")
    return {p['variant']: p['price_per_m2_cents']/100 for p in prices}
```

#### 6. Dominio y branding (2 horas)
- Comprar dominio (worldglass.app o similar) - $12/año
- Configurar DNS en Railway
- Agregar logo simple

### Resultado Esperado
- Sistema de usuarios funcional
- Dashboard con métricas básicas
- PDFs descargables
- Chatbot más inteligente
- Precios configurables
- **Costo: ~$20-30/mes**

### Cómo conseguir los primeros usuarios
1. **Instagram/TikTok**: Mostrar el chatbot en acción
2. **Grupos de Facebook**: "Fabricantes de aluminio México"
3. **WhatsApp personal**: Usar el demo con conocidos del rubro
4. **Ferias de construcción**: Tener una tablet con el demo

---

## 💰 Fase 3: Primeros Pagos y Validación (4-6 semanas)
**Objetivo**: Primeros $500-$1,000 USD en revenue
**Inversión**: $50 - $100 USD/mes
**Tiempo**: 40-50 horas de desarrollo

### Tareas Concretas

#### 1. Integración Stripe Payment Links (2 horas)
```python
# NO código complejo de checkout
# Usar Stripe Payment Links pre-configurados

# Crear links en Stripe Dashboard:
# - Free: $0 MXN (gratis)
# - Pro Mensual: $490 MXN
# - Pro Anual: $4,900 MXN

# En dashboard, mostrar botón:
<a href="https://buy.stripe.com/..." class="upgrade-btn">
    Actualizar a Pro - $490 MXN/mes
</a>

# Webhook para actualizar plan en BD:
@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db = Depends(get_db)):
    payload = await request.body()
    event = stripe.Webhook.construct_event(
        payload, headers["stripe-signature"], webhook_secret
    )
    
    if event["type"] == "checkout.session.completed":
        customer_email = event["data"]["object"]["customer_details"]["email"]
        # Actualizar organization a plan pro
        await db.execute("""
            UPDATE organizations o
            SET plan_id = 2, stripe_customer_id = $1
            FROM users u
            WHERE u.email = $2 AND u.organization_id = o.id
        """, event["data"]["object"]["customer"], customer_email)
    
    return {"status": "success"}
```

#### 2. Plan simple de pago (4 horas)
- **Mensual**: $490 MXN (~$25 USD)
- **Anual**: $4,900 MXN (~$250 USD) - 2 meses gratis
- Incluye: Cotizaciones ilimitadas, PDF personalizado, soporte prioritario

#### 3. Límites y cuotas (6 horas)
```python
# Límite de 10 cotizaciones/mes para usuarios gratis
def check_quote_limit(user_id):
    quotes_this_month = db.query(
        'SELECT COUNT(*) FROM quotes WHERE user_id = ? AND date > ?',
        (user_id, first_of_month())
    )
    if quotes_this_month >= 10 and not user.is_pro:
        return False
    return True
```

#### 4. Email marketing básico (4 horas)
```python
# SendGrid gratuito (100 emails/día)
import sendgrid
from sendgrid.helpers.mail import Mail

def send_welcome_email(user_email):
    message = Mail(
        from_email='hola@worldglass.app',
        to_emails=user_email,
        subject='Bienvenido a WorldGlass',
        html_content='<strong>Gracias por unirte</strong>'
    )
    sg = sendgrid.SendGridAPIClient(api_key='SG...')
    sg.send(message)
```

#### 5. Analytics simple (4 horas)
```python
# Google Analytics básico
# Mixpanel gratuito (1,000 eventos/mes)
def track_event(user_id, event_name, properties):
    mixpanel.track(event_name, {
        'distinct_id': user_id,
        ...properties
    })
```

#### 6. Landing page mejorada (4 horas)
```html
<!-- pages/landing.html -->
<section class="hero">
    <h1>Cotiza canceles y ventanas en segundos con IA</h1>
    <p>Olvida las calculadoras complejas. Nuestro chatbot entiende lo que necesitas.</p>
    <a href="/demo" class="cta">Prueba gratis</a>
</section>

<section class="features">
    <div class="feature">
        <h3>⚡ Cotiza en 30 segundos</h3>
        <p>Solo escribe "cancel 150x190 negro" y obtén el precio al instante</p>
    </div>
    <div class="feature">
        <h3>🤖 Entiende lenguaje natural</h3>
        <p>No necesitas ser técnico, escribe como le hablarías a un humano</p>
    </div>
</section>
```

### Estrategia de Precios y Validación

#### Modelo de Validación
1. **Beta gratuita** - Primeros 20 usuarios gratis por 3 meses
2. **Feedback obligatorio** - Reunión mensual de 30 min
3. **Descuento fundadores** - $250 MXN/mes de por vida para primeros 50 usuarios

#### Meta de Revenue
- **Meta conservadora**: 5 usuarios pagando $490 MXN = $2,450 MXN/mes
- **Meta agresiva**: 20 usuarios pagando = $9,800 MXN/mes
- **Meta soñada**: 50 usuarios = $24,500 MXN/mes

### Resultado Esperado
- Sistema de pagos funcional
- Primeros clientes pagando
- Analytics implementados
- Landing page profesional
- **Revenue: $500-$1,000 USD/mes**
- **Costo: $50-100/mes**

---

## 🎯 Criterios para Escalar a SaaS Full

NO escalar a la arquitectura compleja hasta que tengas:

1. ✅ **20+ usuarios activos mensuales**
2. ✅ **$1,000+ USD revenue mensual**
3. ✅ **10+ clientes pidiendo features enterprise**
4. ✅ **Problemas de performance reales**
5. ✅ **Algún cliente pagando por integración/API**

### Señales de que ESTÁS listo para escalar:
- "Necesito que mis 5 empleados usen esto"
- "Quiero mi propio dominio: cotizaciones.miempresa.com"
- "Necesito integrar esto con mi CRM"
- "El sistema se lenta cuando tengo 100+ cotizaciones"

---

## 📅 Timeline Resumido

| Fase | Duración | Inversión | Revenue Esperado | Skills Necesarias |
|------|----------|-----------|------------------|-------------------|
| Fase 1 | 1-2 semanas | $0 | $0 | Python básico |
| Fase 2 | 3-4 semanas | $20-50/mes | $0 | Flask, HTML/CSS, SQLite |
| Fase 3 | 4-6 semanas | $50-100/mes | $500-1,000 | Stripe, Email marketing |

**Total**: 8-12 semanas para tener un producto generando revenue

---

## 🛠️ Stack Tecnológico Simplificado (Aprobado)

### Fase 1-2
```
Backend: FastAPI + Python 3.11
Base de Datos: PostgreSQL en Railway.app
Frontend: HTML + Jinja2 templates
Deploy: Railway.app (git push = deploy)
IA Chat: OpenAI GPT-4o-mini
IA Renders: Replicate SDXL
Email: SendGrid (free tier)
Analytics: Google Analytics (gratis)
```

### Fase 3
```
Todo lo anterior +
Pagos: Stripe Payment Links
Email automation: SendGrid (upgrade)
Analytics: Mixpanel (free tier)
```

### NO usar hasta Fase 4+
❌ Kubernetes, EKS, Docker Compose
❌ Next.js, React, TypeScript, Tailwind
❌ Auth0, Cognito, RBAC complejo
❌ Redis, Celery, RabbitMQ, SQS
❌ Grafana, Prometheus, ELK
❌ Microservicios, API Gateway
❌ SQLite (usar PostgreSQL como especifica context.md)
❌ Flask (migrar a FastAPI)

---

## 🎓 Qué Aprenderás en el Proceso

### Fase 1
- Organización de código Python
- SQLite básico
- Deploy en la nube

### Fase 2
- Flask-Login (autenticación)
- Generación de PDFs
- OpenAI API
- Git y version control

### Fase 3
- Stripe payments
- Email marketing
- Analytics basics
- Landing pages

---

## 🚨 Riesgos y Cómo Mitigarlos

### Riesgo 1: Nadie quiere pagar
**Mitigación**: 
- Validar con 20+ personas antes de cobrar
- Ofrecer gratis por 1 mes
- Bajar precio si necesario ($290 MXN)

### Riesgo 2: Competidores grandes
**Mitigación**:
- Enfocarte en nicho específico (México, canceles de baño)
- Ser más ágil y personal
- Usar IA como diferenciador

### Riesgo 3: No tienes tiempo
**Mitigación**:
- Dedica solo 10-15 horas/semana
- Automatiza lo posible
- Contrata freelancer para UI si necesario

### Riesgo 4: El código se vuelve un lío
**Mitigación**:
- Refactor constantemente
- No tengas miedo de reescribir
- Git commits frecuentes

---

## 💡 Tips para Éxito

1. **Habla con clientes reales** - No construyas en vacío
2. **Lanza rápido** - Perfecto es enemigo de bueno
3. **Cobra desde el inicio** - Si no pagan, no hay negocio
4. **Mide todo** - Analytics desde día 1
5. **No scales prematuramente** - Espera a tener problemas reales
6. **Automatiza soporte** - Chatbot, FAQs, emails automáticos
7. **Personaliza** - Trata a cada cliente como especial

---

## 📞 Recursos de Ayuda

### Aprendizaje
- **Flask**: Flask documentation (gratis)
- **Stripe**: Stripe docs (excelentes)
- **OpenAI**: OpenAI cookbook
- **Deploy**: Railway docs

### Comunidad
- **Reddit**: r/flask, r/SaaS, r/startups
- **Discord**: Indie Hackers, Python Discord
- **Twitter**: Siga a @levelsio, @arvidkahl

### Herramientas Gratis
- **VS Code**: Editor
- **GitHub**: Version control
- **Figma**: Design (free tier)
- **Notion**: Documentación

---

## 🎯 Próximos Pasos (Esta Semana)

1. ✅ **Migrar Flask → FastAPI** (3 horas)
2. ✅ **Configurar PostgreSQL** en Railway (2 horas)
3. ✅ **Implementar sistema de registro** (usar skill.md) (4 horas)
4. ✅ **Implementar motor de precios** real (3 horas)
5. ✅ **Deploy a Railway** + testing (1 hour)
5. ✅ **Mostrar a 5 personas** del rubro y obtener feedback

---

*Última actualización: 2026-05-24*
*Versión: 2.0 (Incremental)*
*Enfoque: Escalado inteligente y progresivo*
