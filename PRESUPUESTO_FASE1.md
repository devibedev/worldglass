# Presupuesto Fase 1 - Control de Gastos Mínimo

## 🎯 Objetivo: Mantener Costos Cercanos a $0

**Regla de oro**: Si no es esencial para el MVP, no gastar. Todo lo que tenga alternativa gratis, usar gratis.

---

## 💰 Desglose de Costos Fase 1 (1-2 semanas)

### ✅ COMPLETAMENTE GRATIS ($0)

#### 1. Desarrollo Local ($0)

- **Python 3.11**: Gratis (ya instalado en Mac)
- **VS Code**: Gratis (ya instalado)
- **Git**: Gratis (ya instalado en Mac)
- **Librerías Python**: FastAPI, Uvicorn, Pydantic = Gratis
- **Testing local**: $0

#### 2. Hosting Backend - Railway.app ($0)

- **Free tier**:
  - 512MB RAM
  - 0.5 CPU
  - 500 horas de ejecución/mes (suficiente para MVP)
  - 1GB de almacenamiento
- **Costo real**: $0 si no excedes límites
- **Límite**: Se "duerme" después de 30 min de inactividad (se despierta en ~30s al recibir request)
- **Cuando empieza a costar**: Solo cuando necesitas más recursos (no en Fase 1)

#### 3. Base de Datos - Railway PostgreSQL ($0)

- **Free tier**:
  - 1GB de almacenamiento
  - Conexiones ilimitadas
  - Backup automático
- **Costo real**: $0 si no excedes límites
- **Cuando empieza a costar**: Solo cuando necesitas más de 1GB (no en Fase 1)

#### 4. Dominio - Opción GRATIS ($0)

- **Opción gratis**: Usar subdominio Railway gratis
  - `tu-proyecto.railway.app`
  - Funciona perfectamente para MVP
  - Puedes mostrarlo a clientes piloto
- **Costo real**: $0
- **Cuándo comprar dominio**: Solo cuando tengas 5+ clientes pagando

#### 5. Email - SendGrid Free Tier ($0)

- **Free tier**:
  - 100 emails/día
  - Suficiente para MVP (registro, welcome emails)
- **Costo real**: $0
- **Cuando empieza a costar**: Cuando envíes >100 emails/día (no en Fase 1)

#### 6. Analytics - Google Analytics ($0)

- **Costo real**: $0 (siempre gratis)
- **Limitación**: No granularidad para SaaS específica, pero suficiente para MVP

#### 7. Version Control - GitHub ($0)

- **Repositorio público**: $0
- **Repositorio privado**: $0 (Gratis para desarrollo personal)
- **Costo real**: $0

#### 8. AI - OpenAI GPT-4o-mini (PAGO POR USO)

- **Costo**: ~$0.15 por 1M tokens (muy barato)
- **Uso estimado**: 100 cotizaciones/mes = ~$0.50-1.00
- **Costo real**: $0-1/mes en Fase 1
- **Alternativa gratis**: Puedes usar reglas simples al inicio (sin AI) para ahorrar

---

### ⚠️ COSTOS QUE PUEDEN EVITARSE

#### 1. Dominio Personalizado ($12-15/año)

- **Costo**: $12-15 USD/año
- **¿Es esencial para Fase 1?**: NO
- **Alternativa gratis**: `tu-proyecto.railway.app`
- **Cuándo comprar**: Fase 3, cuando tengas clientes reales

#### 2. SSL Certificado ($0)

- **Costo**: $0 (Railway incluye SSL gratis)
- **Alternativa**: Ya viene incluido en Railway

#### 3. Replicate SDXL - Renders IA ($0.01 por imagen)

- **Costo**: ~$1 por 100 renders
- **¿Es esencial para Fase 1?**: NO
- **Alternativa gratis**:
  - No usar renders en MVP inicial
  - O usar DALL-E 3 de OpenAI (más caro pero más simple)
  - O simplemente mostrar placeholder
- **Cuándo implementar**: Fase 2 o 3, cuando clientes lo pidan

#### 4. Herramientas de diseño - Figma ($0)

- **Free tier**: $0 (suficiente para MVP)
- **Costo real**: $0

---

### 💵 COSTOS MÍNIMOS NECESARIOS (PODEMOS EVITAR)

#### 1. OpenAI API - GPT-4o-mini ($0-5/mes)

- **Costo estimado**: $0.50-2.00/mes en Fase 1
- **Alternativa para ahorrar**:
  - Usar GPT-3.5-turbo (más barato)
  - O usar regex simple para extraer dimensiones (completamente gratis)
- **Recomendación**: Comenzar con regex gratis, agregar AI después

#### 2. Railway Upgrade (si excedes free tier)

- **Costo**: $5/mes (starter plan)
- **Cuándo necesitar**: Solo si app duerme demasiado o excedes límites
- **Probabilidad en Fase 1**: Baja (muy improbable con 3 clientes piloto)

---

## 📊 PRESUPUESTO REALISTA FASE 1

### Escenario Ultra-Conservador (Casi $0)
| Servicio | Costo/Mes | Notas |
|----------|-----------|-------|
| Railway (Backend + DB) | $0 | Free tier suficiente |
| OpenAI API | $0 | Usar regex simple (gratis) |
| SendGrid (Emails) | $0 | Free tier (100 emails/día) |
| Dominio | $0 | Usar railway.app subdomain |
| Replicate (Renders) | $0 | No usar en MVP inicial |
| **TOTAL** | **$0** | **Completamente gratis** |

### Escenario Moderado (OpenAI Básico)
| Servicio | Costo/Mes | Notas |
|----------|-----------|-------|
| Railway (Backend + DB) | $0 | Free tier suficiente |
| OpenAI API | $1-2 | GPT-4o-mini para 100-200 cotizaciones |
| SendGrid (Emails) | $0 | Free tier |
| Dominio | $0 | Railway subdomain |
| Replicate (Renders) | $0 | No usar aún |
| **TOTAL** | **$1-2/mes** | **Casi gratis** |

### Escenario Completo (Con Todos Features)
| Servicio | Costo/Mes | Notas |
|----------|-----------|-------|
| Railway (Backend + DB) | $0 | Free tier |
| OpenAI API | $2-3 | GPT-4o-mini + DALL-E ocasional |
| SendGrid (Emails) | $0 | Free tier |
| Dominio | $0 | Railway subdomain |
| Replicate (Renders) | $1-2 | Renders para 20-50 cotizaciones |
| **TOTAL** | **$3-5/mes** | **Muy bajo** |

---

## 🎯 ESTRATEGIA PARA MANTENER $0

### Fase 1A: Primera Semana ($0 Absoluto)
```python
# Sin OpenAI - Usar regex para extraer dimensiones
import re

def extract_dimensions(text):
    # Extrae "150x190" de cualquier texto
    match = re.search(r'(\d+)\s*[xX]\s*(\d+)', text)
    if match:
        return int(match.group(1)), int(match.group(2))  # ancho, alto
    return None, None

# Sin renders - Mostrar placeholder
def generate_render_quote(quote_data):
    return {
        "render_url": "/static/placeholder-image.jpg",
        "price": calculate_price(quote_data)
    }
```

### Fase 1B: Segunda Semana (Si necesitas AI)

- Agregar OpenAI solo si regex no es suficiente
- Comenzar con $1-2/mes máximo
- Monitorear uso con dashboard de OpenAI

---

## 📊 COMPARATIVA: GASTOS vs INGRESOS

### Escenario Realista Fase 1
| Periodo | Gastos | Ingresos | Neto |
|---------|--------|----------|------|
| Semana 1-2 | $0 | $0 | $0 |
| Semana 3-4 | $1-2 | $0 | -$1-2 |
| Semana 5-6 | $2-3 | $0-50 (primer cliente) | -$3 a +$47 |
| Semana 7-8 | $3-5 | $50-150 (3 clientes) | +$45 a +$145 |

### Punto de Equilibrio

- **1 cliente pagando**: $490 MXN ≈ $25 USD
- **Costos mensuales**: $3-5 USD
- **Resultado**: Positivo desde el primer cliente

---

## 🚨 ALERTAS DE COSTOS

### Señales que estás gastando demasiado

1. **Railway > $5/mes**: Tu código es ineficiente o necesitas optimizar
2. **OpenAI > $10/mes**: Estás usando modelo equivocado o hay bug
3. **SendGrid > $0**: Estás enviando demasiados emails innecesarios
4. **Replicate > $5/mes**: Generando renders sin necesidad

### Cómo reducir costos inmediatamente

1. **Railway**: Revisar logs, optimizar queries, cachear respuestas
2. **OpenAI**: Bajar a modelo más barato, cachear respuestas, usar regex
3. **SendGrid**: Reducir frecuencia de emails, usar solo esenciales
4. **Replicate**: Deshabilitar renders temporalmente

---

## 💡 CONSEJOS PARA MANTENER $0

### 1. Desarrollo

- **Usa librerías opensource**: FastAPI, SQLAlchemy, etc. son gratis
- **No pagues por IDEs**: VS Code es gratis y excelente
- **No pagues por herramientas de project management**: Trello, GitHub Projects gratis

### 2. Hosting

- **Free tiers primero**: Railway, Render, Vercel tienen generosos free tiers
- **Optimiza antes de escalar**: Comprime imágenes, cachea respuestas
- **Monitorea uso**: Revisa dashboards de uso semanalmente

### 3. Terceros

- **Email**: SendGrid free tier es suficiente para MVP
- **Analytics**: Google Analytics es gratis y suficiente
- **Monitoring**: Railway tiene logs gratis, no necesitas herramientas pagas

### 4. Dominio

- **Espera para comprar**: No es esencial hasta que tengas clientes
- **Subdominios gratis**: Railway.app funciona perfectamente para MVP
- **Cuando comprar**: Solo cuando tengas 5+ clientes pagando

---

## 🎯 CHECKLIST ANTES DE GASTAR $1

Antes de pagar cualquier servicio, pregúntate:

1. ❓ **¿Es esencial para el MVP?**

   - Sí → Considerar
   - No → Esperar

2. ❓ **¿Hay alternativa gratis?**

   - Sí → Usar gratis
   - No → Considerar pago

3. ❓ **¿Esto me acerca a tener 1 cliente pagando?**

   - Sí → Considerar
   - No → Esperar

4. ❓ **¿Puedo construir esto yo mismo?**

   - Sí → Construir
   - No → Considerar pago (si es esencial)

---

## 📋 PLAN DE GASTOS RECOMENDADO

### Semana 1-2: Desarrollo Local ($0)
- Todo gratis: Python, VS Code, Git
- No pagar nada aún

### Semana 3-4: Deploy y Testing ($0)
- Railway free tier
- SendGrid free tier
- Regex simple (sin OpenAI)
- Total: $0

### Semana 5-6: Con Clientes Piloto ($0-2)
- Si AI es necesaria: OpenAI $1-2
- Si no: Seguir con regex
- Total: $0-2

### Semana 7-8: Primer Pagos ($0-5)
- OpenAI $2-3
- Replicate $1-2 (si clientes lo piden)
- Railway sigue gratis
- Total: $3-5

### Fase 2: Con 3+ Clientes ($5-15)
- Railway upgrade $5 (si necesario)
- OpenAI $3-5
- Dominio $1-2 (comprar anual)
- Total: $9-12

---

## 🎯 CONCLUSIÓN

### Presupuesto Recomendado Fase 1
- **Mínimo absoluto**: $0/mes (regex + Railway free tier)
- **Realista**: $1-2/mes (OpenAI básico)
- **Completo**: $3-5/mes (todos los features)

### Regla Final
**No gastar más de $5/mes hasta tener 1 cliente pagando.**

Si llegas a $10/mes sin clientes, algo está mal. Revisa optimización.

---

## 📞 MONITOREO DE COSTOS

### Herramientas Gratuitas
- **Railway Dashboard**: Monitorea uso de CPU/RAM/DB
- **OpenAI Dashboard**: Monitorea tokens y costo
- **SendGrid Dashboard**: Monitorea emails enviados

### Frecuencia de Revisión
- **Diaria**: OpenAI usage (si usas AI)
- **Semanal**: Railway usage
- **Mensual**: Todos los servicios

---

*Última actualización: 2026-05-24*
*Objetivo: Mantener costos cercanos a $0 en Fase 1*