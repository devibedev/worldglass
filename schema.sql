-- Extensión para UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de planes
CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    max_quotes_month INTEGER NOT NULL,
    max_users INTEGER NOT NULL,
    price_mxn_cents INTEGER NOT NULL,
    features JSONB DEFAULT '{}'::jsonb
);

INSERT INTO plans (name, max_quotes_month, max_users, price_mxn_cents) 
VALUES ('free', 10, 1, 0), ('pro', 999999, 5, 49000)
ON CONFLICT (name) DO NOTHING;

-- Organizaciones (Talleres)
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan_id INTEGER REFERENCES plans(id) DEFAULT 1,
    stripe_customer_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Usuarios
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    role VARCHAR(20) DEFAULT 'owner',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Cotizaciones
CREATE TABLE IF NOT EXISTS quotes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id),
    customer_name VARCHAR(255),
    total_mxn_cents INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'draft',
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_quotes_org_month ON quotes (organization_id, created_at);