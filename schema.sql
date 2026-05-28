-- Extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de planes
CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    max_quotes_month INTEGER NOT NULL,
    max_users INTEGER NOT NULL,
    price_mxn_cents INTEGER NOT NULL
);

-- Insertar plan básico si no existe
INSERT INTO plans (name, max_quotes_month, max_users, price_mxn_cents) 
VALUES ('free', 10, 1, 0) ON CONFLICT DO NOTHING;

-- Organizaciones (Talleres)
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan_id INTEGER REFERENCES plans(id) DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insertar organización demo para que el chat no falle
INSERT INTO organizations (name, slug) 
VALUES ('Taller Demo', 'taller-demo') ON CONFLICT DO NOTHING;

-- Cotizaciones
CREATE TABLE IF NOT EXISTS quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    customer_name VARCHAR(255),
    total_mxn_cents INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quotes_org_month ON quotes (organization_id, created_at);