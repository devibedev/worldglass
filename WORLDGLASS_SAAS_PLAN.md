# WorldGlass SaaS - Plan Estratégico de Desarrollo

## 📊 Análisis del Estado Actual

### Código Existente
- **Framework**: Flask monolítico
- **Frontend**: HTML/CSS/JS inline sin separación de concerns
- **Lógica**: Hardcoded, sin base de datos
- **Autenticación**: Inexistente
- **Escalabilidad**: No escalable
- **Monetización**: No implementada

### Problemas Críticos
1. Sin persistencia de datos
2. Sin multi-tenancy
3. Sin sistema de usuarios/roles
4. Lógica de negocio frágil
5. Sin infraestructura de producción
6. Sin monitoreo ni logging

---

## 🏗️ Arquitectura Técnica Escalable

### Arquitectura General
```
┌─────────────────────────────────────────────────────────┐
│                    CDN (CloudFront)                     │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────┴───────────────────────────────┐
│              Load Balancer (Application LB)             │
└─────────────────────────┬───────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
┌───────┴───────┐ ┌───────┴───────┐ ┌──────┴───────┐
│  API Gateway   │ │   Auth Svc    │ │  AI/ML Svc   │
│  (FastAPI)     │ │  (Auth0/Cognito)│ │  (OpenAI)    │
└───────┬───────┘ └───────┬───────┘ └──────┬───────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │    Application Layer (Kubernetes) │
        │  ┌──────────┐  ┌──────────┐      │
        │  │ Quote Svc│  │ User Svc │ ...  │
        │  └──────────┘  └──────────┘      │
        └─────────────────┬─────────────────┘
                          │
        ┌─────────────────┴─────────────────┐
        │         Data Layer                 │
        │  ┌──────────┐  ┌──────────┐      │
        │  │PostgreSQL│  │   Redis  │      │
        │  │(Primary) │  │  (Cache) │      │
        │  └──────────┘  └──────────┘      │
        └───────────────────────────────────┘
```

### Stack Tecnológico Recomendado

#### Backend
- **API Framework**: FastAPI (Python) - Alta performance, async, OpenAPI auto
- **Autenticación**: Auth0 o AWS Cognito (OAuth 2.0/OIDC)
- **Base de Datos**: PostgreSQL (RDS) + Redis (ElastiCache)
- **ORM**: SQLAlchemy 2.0 (async)
- **Cola de Tareas**: Celery + RabbitMQ/SQS
- **Storage**: S3 para archivos/static

#### Frontend
- **Framework**: Next.js 14 (React) + TypeScript
- **UI Components**: shadcn/ui + Tailwind CSS
- **State Management**: Zustand o Redux Toolkit
- **Forms**: React Hook Form + Zod validation
- **Chat Interface**: Custom component con streaming

#### Infraestructura
- **Cloud**: AWS (o Google Cloud)
- **Container Orchestration**: Kubernetes (EKS) o Docker Compose para MVP
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana + Sentry
- **Logging**: CloudWatch o ELK Stack

#### AI/ML
- **LLM**: OpenAI GPT-4o o Anthropic Claude
- **Vector DB**: Pinecone o pgvector (PostgreSQL)
- **Embeddings**: OpenAI text-embedding-3

---

## 🗂️ Modelo de Datos

### Schema Principal

```sql
-- Usuarios y Autenticación
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    auth_provider VARCHAR(50), -- 'email', 'google', 'auth0'
    auth_provider_id VARCHAR(255),
    role VARCHAR(20) DEFAULT 'user', -- 'admin', 'user', 'sales'
    subscription_tier VARCHAR(20) DEFAULT 'free', -- 'free', 'pro', 'enterprise'
    subscription_status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Organizaciones (Multi-tenancy)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan_tier VARCHAR(20) DEFAULT 'free',
    max_users INTEGER DEFAULT 1,
    max_quotes_per_month INTEGER DEFAULT 10,
    custom_pricing JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE organization_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(20) DEFAULT 'member', -- 'owner', 'admin', 'member'
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(organization_id, user_id)
);

-- Productos y Materiales
CREATE TABLE product_categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    base_price_formula JSONB, -- Fórmula de cálculo
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    category_id UUID REFERENCES product_categories(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50), -- 'aluminum', 'glass', 'hardware'
    price_per_unit DECIMAL(10,2),
    unit VARCHAR(20), -- 'm', 'm2', 'piece'
    supplier VARCHAR(255),
    stock_quantity INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE material_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    material_id UUID REFERENCES materials(id),
    name VARCHAR(100), -- 'Natural', 'Negro', 'Blanco'
    price_modifier DECIMAL(5,2), -- Multiplicador de precio
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Cotizaciones
CREATE TABLE quotes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    customer_name VARCHAR(255),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    status VARCHAR(20) DEFAULT 'draft', -- 'draft', 'sent', 'accepted', 'rejected', 'expired'
    total_amount DECIMAL(12,2),
    currency VARCHAR(3) DEFAULT 'MXN',
    valid_until TIMESTAMP,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE quote_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_id UUID REFERENCES quotes(id) ON DELETE CASCADE,
    product_category_id UUID REFERENCES product_categories(id),
    width_cm DECIMAL(8,2),
    height_cm DECIMAL(8,2),
    quantity INTEGER DEFAULT 1,
    material_variant_id UUID REFERENCES material_variants(id),
    glass_type VARCHAR(50), -- 'templado_6mm', 'templado_9mm'
    hardware_type VARCHAR(50),
    calculated_price DECIMAL(12,2),
    specifications JSONB, -- Detalles adicionales
    created_at TIMESTAMP DEFAULT NOW()
);

-- Conversiones de Chat
CREATE TABLE chat_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    quote_id UUID REFERENCES quotes(id),
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    messages_count INTEGER DEFAULT 0,
    conversion_status VARCHAR(20), -- 'in_progress', 'converted', 'abandoned'
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES chat_conversations(id),
    role VARCHAR(20), -- 'user', 'assistant', 'system'
    content TEXT,
    metadata JSONB, -- Intent, entities, confidence
    timestamp TIMESTAMP DEFAULT NOW()
);

-- Pagos y Suscripciones
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID REFERENCES organizations(id),
    stripe_subscription_id VARCHAR(255),
    plan_tier VARCHAR(20),
    status VARCHAR(20), -- 'active', 'canceled', 'past_due'
    current_period_start TIMESTAMP,
    current_period_end TIMESTAMP,
    cancel_at_period_end BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscription_id UUID REFERENCES subscriptions(id),
    stripe_payment_intent_id VARCHAR(255),
    amount DECIMAL(12,2),
    currency VARCHAR(3) DEFAULT 'MXN',
    status VARCHAR(20), -- 'pending', 'completed', 'failed'
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analytics
CREATE TABLE analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    event_type VARCHAR(50), -- 'quote_created', 'chat_started', 'signup'
    properties JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 Roadmap de Desarrollo

### Fase 1: MVP (8-10 semanas)
**Objetivo**: Producto funcional mínimo viable para validar mercado

#### Semana 1-2: Fundamentos
- [ ] Configuración de proyecto monorepo (Nx o turborepo)
- [ ] Setup de FastAPI con PostgreSQL + Redis
- [ ] Sistema de autenticación básico (JWT local)
- [ ] Setup de Next.js con TypeScript + shadcn/ui
- [ ] CI/CD básico (GitHub Actions)

#### Semana 3-4: Core de Cotizaciones
- [ ] API REST para CRUD de usuarios
- [ ] API REST para CRUD de organizaciones
- [ ] Motor de cálculo de precios (fórmulas parametrizables)
- [ ] CRUD de productos y materiales
- [ ] Sistema de cotizaciones básico

#### Semana 5-6: Chatbot Inteligente
- [ ] Integración con OpenAI API
- [ ] Sistema de prompts para extracción de dimensiones
- [ ] Lógica de interpretación de lenguaje natural
- [ ] Chat UI con streaming de respuestas
- [ ] Manejo de errores y fallback

#### Semana 7-8: Frontend Completo
- [ ] Dashboard principal
- [ ] Historial de cotizaciones
- [ ] Vista detallada de cotización
- [ ] Generación de PDF (usando jsPDF o React-PDF)
- [ ] Formulario de edición manual

#### Semana 9-10: Testing y Deploy
- [ ] Tests unitarios (pytest + jest)
- [ ] Tests E2E (Playwright)
- [ ] Deploy a staging (Railway, Render, o AWS ECS)
- [ ] Monitoreo básico (Sentry)
- [ ] Documentación de API

---

### Fase 2: SaaS Enterprise (6-8 semanas)
**Objetivo**: Escalar a producto SaaS multi-tenant con pagos

#### Semana 1-2: Multi-tenancy
- [ ] Implementación completa de multi-tenancy
- [ ] Roles y permisos (RBAC)
- [ ] Cuotas y límites por plan
- [ ] Integración con Auth0 o Cognito

#### Semana 3-4: Sistema de Pagos
- [ ] Integración con Stripe
- [ ] Planes de suscripción (Free, Pro, Enterprise)
- [ ] Checkout flow
- [ ] Gestión de suscripciones
- [ ] Webhooks de Stripe

#### Semana 5-6: Features Pro
- [ ] Branding personalizable (logos, colores)
- [ ] Dominios personalizados
- [ ] API para integraciones
- [ ] Webhooks para terceros
- [ ] Exportación de datos (CSV, Excel)

#### Semana 7-8: Analytics y Optimización
- [ ] Dashboard de analytics interno
- [ ] Tracking de eventos (Mixpanel o Segment)
- [ ] Optimización de performance
- [ ] Caching agresivo con Redis
- [ ] CDN para assets

---

### Fase 3: Escalado y Automatización (8-10 semanas)
**Objetivo**: Infraestructura de producción y automatización

#### Semana 1-3: Infraestructura Cloud
- [ ] Migración a AWS/GCP
- [ ] Kubernetes (EKS/GKE) o ECS+Fargate
- [ ] Base de datos HA (Multi-AZ)
- [ ] CDN + CloudFront
- [ ] Auto-scaling
- [ ] Backup y disaster recovery

#### Semana 4-5: AI/ML Avanzado
- [ ] Fine-tuning de modelo para dominio específico
- [ ] Vector database para búsqueda semántica
- [ ] Sistema de recomendaciones
- [ ] Detección de anomalías en cotizaciones
- [ ] Análisis de sentimiento de clientes

#### Semana 6-7: Automatización de Marketing
- [ ] Email automation (SendGrid/Mailgun)
- [ ] SMS notifications (Twilio)
- [ ] In-app messaging
- [ ] Onboarding flow optimizado
- [ ] Sistema de referrals

#### Semana 8-10: Enterprise Features
- [ ] SSO (SAML, LDAP)
- [ ] Advanced security (2FA, audit logs)
- [ ] SLAs y soporte prioritario
- [ ] Contratos enterprise
- [ ] API rate limiting avanzado

---

## 💰 Modelo de Monetización

### Planes de Suscripción

#### Free
- **Precio**: $0
- **Límites**: 10 cotizaciones/mes, 1 usuario
- **Features**: Chatbot básico, PDF básico
- **Target**: Validación, freelancers pequeños

#### Pro ($49 USD/mes)
- **Límites**: 100 cotizaciones/mes, 5 usuarios
- **Features**: 
  - Branding personalizado
  - Analytics avanzado
  - API access
  - Exportación de datos
  - Soporte por email
- **Target**: Pequeñas empresas, instaladores

#### Enterprise ($199 USD/mes)
- **Límites**: Ilimitado, usuarios ilimitados
- **Features**:
  - Todo de Pro
  - SSO
  - Dominio personalizado
  - Webhooks personalizados
  - SLA 99.9%
  - Soporte prioritario 24/7
  - Entrenamiento personalizado
- **Target**: Grandes fabricantes, distribuidores

### Revenue Streams Adicionales
- **Transaction fee**: 1% sobre cotizaciones convertidas (opcional)
- **Marketplace de instalación**: Conectar clientes con instaladores (comisión 10-15%)
- **White-label**: Licencia para revendedores

---

## 🔒 Seguridad y Cumplimiento

### Seguridad
- **Autenticación**: OAuth 2.0/OIDC con Auth0/Cognito
- **Autorización**: RBAC con permisos granulares
- **Encriptación**: TLS 1.3 en transit, AES-256 at rest
- **API Security**: Rate limiting, input validation, SQL injection prevention
- **Secrets Management**: AWS Secrets Manager o HashiCorp Vault
- **2FA**: TOTP y SMS

### Cumplimiento
- **GDPR**: Derechos de usuarios, consentimiento, data portability
- **CCPA**: Opt-out, data deletion
- **SOC 2**: Control de accesos, logging, monitoreo
- **Data Residency**: Opción de región específica

---

## 📈 Métricas Clave (KPIs)

### Product Metrics
- **DAU/MAU**: Engagment de usuarios
- **Conversion Rate**: Visitas → Signup → Paid
- **Churn Rate**: Retención de suscriptores
- **ARPU**: Average Revenue Per User
- **LTV**: Lifetime Value
- **CAC**: Customer Acquisition Cost

### Business Metrics
- **MRR/ARR**: Monthly/Annual Recurring Revenue
- **Quotes per User**: Productividad
- **Conversion Rate**: Quotes → Sales
- **NPS**: Satisfacción del cliente
- **Support Ticket Volume**: Salud del producto

---

## 🎯 Próximos Pasos Inmediatos

1. **Validación de mercado**: Encuestas a 50+ fabricantes de aluminio
2. **Competitor analysis**: Estudiar cotizadores existentes
3. **Technical spike**: Prototipo de motor de cálculo de precios
4. **Design system**: Definir branding y UI/UX
5. **Legal**: Términos de servicio, privacy policy

---

## 🛠️ Stack de Herramientas de Desarrollo

### Development
- **IDE**: VS Code + Cursor/Windsurf
- **Version Control**: Git + GitHub
- **Project Management**: Linear o GitHub Projects
- **Documentation**: Notion o Confluence
- **Design**: Figma

### Communication
- **Async**: Slack o Discord
- **Video**: Zoom o Google Meet
- **Code Review**: GitHub PRs

### Quality Assurance
- **Testing**: pytest, jest, Playwright
- **CI/CD**: GitHub Actions
- **Code Quality**: SonarQube, ESLint, Black
- **Performance**: Lighthouse, WebPageTest

---

## 📚 Recursos y Documentación

### Technical Documentation
- OpenAPI/Swagger para documentación de API
- Arquitectura decision records (ADRs)
- Runbooks de operaciones
- Playbooks de incidentes

### User Documentation
- Guías de inicio rápido
- Video tutoriales
- FAQ y troubleshooting
- API documentation

---

*Última actualización: 2026-05-24*
*Versión: 1.0*
