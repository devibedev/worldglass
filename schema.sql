-- Extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de planes. Heredable: agregar planes aquí, no en código
CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL, -- 'free', 'pro'
    max_quotes_month INTEGER NOT NULL,
    max_users INTEGER NOT NULL,
    price_mxn_cents INTEGER NOT NULL, -- 0 para free, 49000 para pro
    features JSONB DEFAULT '{}'::jsonb
);

INSERT INTO plans (name, max_quotes_month, max_users, price_mxn_cents) VALUES
('free', 10, 1, 0),
('pro', 999999, 5, 49000)
ON CONFLICT (name) DO NOTHING;

-- Organizaciones = Talleres. Un taller puede tener N usuarios
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL, -- para URLs: worldglass.app/c/mitaller
    plan_id INTEGER REFERENCES plans(id) DEFAULT 1, -- free por defecto
    stripe_customer_id VARCHAR(255), -- null hasta que pague
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usuarios. Un usuario pertenece a 1 organización en Fase 1
CREATE TABLE IF NOT EXISTS users (
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
CREATE TABLE IF NOT EXISTS quotes (
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
CREATE INDEX IF NOT EXISTS idx_quotes_org_month ON quotes (organization_id, created_at);

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
