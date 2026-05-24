# WorldGlass SaaS - Contexto del Proyecto

## Misión
WorldGlass es un SaaS que permite a talleres de cancelería de aluminio/vidrio cotizar en 10 segundos desde WhatsApp, con render IA del trabajo terminado. 

Objetivo: Que el técnico capture medidas + foto en sitio, y el cliente reciba PDF con render + precio exacto antes de que el técnico se suba a la camioneta.

## Usuario Final No-Técnico
El founder NO es programador. No tiene experiencia en APIs. Aprende sobre la marcha.
Regla: Explicar todo como si fuera primera vez. Cero jerga sin traducción. Siempre dar el comando/código listo para copiar.

## Estado Actual: Fase 1 MVP - 6 semanas
Estamos construyendo el demo funcional más simple posible para validar con 3 talleres piloto.
NO estamos en fase de escalar, multi-tenant, ni Kubernetes.

## Stack Técnico APROBADO para Fase 1
| Componente | Tecnología | Razón |
| --- | --- | --- |
| Backend | FastAPI + Python 3.11 | Simple, rápido, async nativo |
| Base de Datos | PostgreSQL en Railway.app | Gratis, SQL completo, panel visual |
| Frontend | HTML + Jinja2 templates | Cero build tools. Deploy inmediato |
| IA Renders | Replicate API SDXL | $0.01 por imagen. Sin GPU propia |
| IA Chat | OpenAI GPT-4o-mini | Barato para extraer medidas de texto |
| Deploy | Railway.app | git push = deploy. Sin Docker aún |
| Pagos | Stripe Payment Links | Sin código de checkout complejo |

## Stack PROHIBIDO en Fase 1
No sugerir ni implementar hasta tener 10 clientes pagando:
- Kubernetes, EKS, Docker Compose
- Next.js, React, TypeScript, Tailwind
- Auth0, Cognito, RBAC complejo
- Redis, Celery, RabbitMQ, SQS
- Grafana, Prometheus, ELK
- Microservicios, API Gateway

Razón: Complejidad prematura mata proyectos. Primero ingresos, luego arquitectura.

## Reglas de Oro
1. **First make it work**: Si funciona en Flask monolítico, no refactorizar a microservicios
2. **Costo $0**: No sugerir servicios de pago hasta que haya MRR
3. **1 archivo cuando sea posible**: Preferir `app.py` gigante que 20 micro-archivos
4. **Copiar/pegar first**: Todo código debe ser ejecutable sin modificar paths
5. **Validar con usuario**: Antes de agregar features, preguntar "¿esto te consigue 1 cliente más?"