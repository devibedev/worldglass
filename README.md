# WorldGlass SaaS - Cotizador con IA para Cancelería

## 🚀 Stack Fase 1 - MVP
- **Backend**: FastAPI + Python 3.14
- **Base de Datos**: PostgreSQL (Railway.app free tier)
- **Frontend**: HTML + Jinja2 Templates
- **Motor de Precios**: Cálculo matemático real (sin IA por ahora)
- **Deploy**: Railway.app

## 💰 Costos Fase 1
- **Total**: $0/mes (Railway free tier)
- **Base de datos**: 1GB PostgreSQL gratis
- **Límite**: Suficiente para MVP con 3 clientes piloto

## 🛠️ Setup Local

### 1. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
cp .env.example .env
# Editar .env con tus variables (DATABASE_URL de Railway)
```

### 4. Correr localmente
```bash
python main.py
# Acceder a http://localhost:8000
```

## 🌐 Deploy en Railway

### Paso 1: Crear cuenta Railway
1. Ir a https://railway.app
2. Crear cuenta con GitHub (gratis)
3. Railway tiene $5 gratis al inicio, suficiente para este proyecto

### Paso 2: Crear proyecto Railway
1. Click "New Project"
2. Seleccionar "Deploy from GitHub repo"
3. Autorizar Railway a acceder a tu GitHub
4. Seleccionar este repositorio
5. Railway detectará automáticamente que es Python

### Paso 3: Agregar PostgreSQL
1. En el proyecto Railway, click "New Service"
2. Seleccionar "Database"
3. Elegir "PostgreSQL"
4. Click "Add PostgreSQL"

### Paso 4: Obtener DATABASE_URL
1. En el servicio PostgreSQL, click "Variables"
2. Copiar el valor de `DATABASE_URL`
3. En el servicio web (app), click "Variables"
4. Agregar variable: `DATABASE_URL` = (pegar valor copiado)

### Paso 5: Ejecutar schema.sql
1. En el servicio PostgreSQL, click "Query"
2. Copiar todo el contenido de `schema.sql`
3. Pegar en el editor de Railway
4. Click "Execute"

### Paso 6: Deploy
1. Railway hará deploy automático
2. Esperar a que esté "Healthy"
3. Click en el dominio generado (ej: tu-app.railway.app)

### Paso 7: Verificar
1. Abrir el dominio en navegador
2. Deberías ver el chat de WorldGlass
3. Probar: `/health` debe retornar `{"status":"healthy"}`
4. Probar chat: "cancel 150x190 negro" debe cotizar

## 🧪 Testing Local

### Health check
```bash
curl http://localhost:8000/health
```

### Probar chat
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"msg": "cancel 150x190 negro"}'
```

### Documentación API automática
- Abrir http://localhost:8000/docs
- FastAPI genera Swagger UI automáticamente

## 📊 Estructura del Proyecto

```
worldglass/
├── main.py              # Entry point FastAPI
├── database.py          # Conexión PostgreSQL
├── schema.sql           # Esquema de base de datos
├── requirements.txt     # Dependencias Python
├── railway.toml         # Configuración Railway
├── routes/              # Endpoints API
│   ├── chat.py         # Chatbot cotizador
│   └── quotes.py       # Cotizaciones (Fase 2)
├── utils/               # Lógica de negocio
│   └── calculator.py   # Motor de precios
├── templates/           # HTML Jinja2
│   └── chat.html       # Interfaz chat
└── static/              # CSS, JS, imágenes
```

## 🎯 Próximos Pasos (Fase 1)

### ✅ Completado
- [x] Migrar Flask → FastAPI
- [x] Implementar motor de precios real
- [x] Crear esquema de base de datos multi-tenant
- [x] Configurar estructura de proyecto

### 🔄 En Progreso
- [ ] Deploy en Railway
- [ ] Configurar PostgreSQL en Railway
- [ ] Ejecutar schema.sql

### 📋 Pendiente
- [ ] Implementar sistema de registro (skill.md)
- [ ] Agregar autenticación JWT
- [ ] Implementar endpoints multi-tenant

## 🔐 Seguridad

- Los passwords se hashean con bcrypt (Fase 2)
- Las variables de entorno están en Railway (no en código)
- Conexión a BD con asyncpg (seguro y async)

## 📈 Monitoreo

- Railway tiene logs gratis
- Health check en `/health`
- Métricas en dashboard de Railway

## 💡 Notas Importantes

1. **Costos**: Railway free tier = $0. Si excedes límites, te avisará antes de cobrar.
2. **Multi-tenant**: El esquema soporta múltiples talleres desde día 1.
3. **Escalabilidad**: Cuando necesites más, Railway hace upgrade transparente.
4. **No Docker**: Usamos Nixpacks de Railway (más simple para MVP)

## 🆘 Problemas Comunes

### Error: "DATABASE_URL not configured"
- Solución: Agregar variable DATABASE_URL en Railway (ver Paso 4)

### Error: "relation does not exist"
- Solución: Ejecutar schema.sql en Railway Query (ver Paso 5)

### Error: "Module not found"
- Solución: `pip install -r requirements.txt`

### App se "duerme"
- Normal en Railway free tier. Se despierta en ~30s al recibir request.

---

*Última actualización: 2026-05-24*
*Fase 1 MVP - Costo: $0/mes*
